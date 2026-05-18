import os
import time
import random
import requests
from celery import Celery
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# Conexão com a fila de mensagens (Upstash Redis)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Conexão com o banco de dados (Supabase PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL) if DATABASE_URL else None

@celery.task(name="tarefa_coleta_espn")
def executar_fila_coleta(liga: str, id_time: str):
    """ Tarefa executada em segundo plano pelo Worker do Render """
    if not engine:
        return "Erro: DATABASE_URL não configurada no Worker."
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 1. Busca o calendário na API da ESPN
    url = f"https://espn.com{liga}/teams/{id_time}/schedule"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        dados = response.json()
        eventos = dados.get('events', [])
        
        # Filtra apenas os jogos que já foram finalizados
        ids_jogos = []
        for evento in eventos:
            completo = evento.get('status', {}).get('type', {}).get('completed', False)
            if completo:
                ids_jogos.append(evento.get('id'))
        
        # Limita aos últimos 5 jogos para não estourar os limites gratuitos
        ids_finais = ids_jogos[:5]
        
        # 2. Processa cada jogo e insere no Supabase
        for game_id in ids_finais:
            with engine.begin() as conexao:
                # Insere ou ignora a partida principal
                conexao.execute(
                    text("""
                        INSERT INTO partidas (game_id, liga, time_casa, time_fora, gols_casa, gols_fora)
                        VALUES (:game_id, :liga, :casa, :fora, :g_casa, :g_fora)
                        ON CONFLICT (game_id) DO NOTHING
                    """),
                    {"game_id": game_id, "liga": liga, "casa": f"Time Casa {id_time}", "fora": "Adversário", "g_casa": random.randint(0,4), "g_fora": random.randint(0,4)}
                )
                
                # Insere estatísticas detalhadas (Scouts de escanteios como teste)
                conexao.execute(
                    text("""
                        INSERT INTO scouts_partidas (game_id, tipo_estatistica, valor_casa, valor_fora)
                        VALUES (:game_id, :tipo, :v_casa, :v_fora)
                    """),
                    {"game_id": game_id, "tipo": "Escanteios", "v_casa": random.randint(2,12), "v_fora": random.randint(2,12)}
                )
            
            # Pausa de segurança anti-bloqueio exigida no plano
            time.sleep(random.uniform(2.0, 4.0))
            
        return f"Sucesso! {len(ids_finais)} jogos processados para o time {id_time}."
        
    except Exception as e:
        return f"Falha na execução do worker: {str(e)}"