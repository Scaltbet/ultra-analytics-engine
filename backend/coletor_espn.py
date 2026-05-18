import requests
import time
import random
# Alinhado: Importa a instância do Celery configurada com SSL na pasta workers
from workers.celery_app import celery_app

class ColetorESPN:
    def __init__(self):
        # Este disfarce faz o servidor da ESPN pensar que o seu código é um navegador comum
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
    def obter_ultimos_jogos_id(self, liga: str, id_time: str, limite: int = 20):
        """ Busca o calendário e os IDs das últimas partidas """
        url = f"https://espn.com{liga}/teams/{id_time}/schedule"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            dados = response.json()
            eventos = dados.get('events', [])
            jogos_finalizados = [e for e in eventos if e.get('status', {}).get('type', {}).get('completed') == True]
            
            # Pega os IDs dos últimos jogos dentro do limite solicitado
            ids = [jogo['id'] for jogo in jogos_finalizados[-limite:]]
            return ids
        except Exception as e:
            print(f"Erro ao buscar calendário: {e}")
            return []

    def obter_scout_partida(self, liga: str, game_id: str):
        """ Abre os dados brutos de gols, cantos e cartões de um jogo específico """
        url = f"https://espn.com{liga}/summary?event={game_id}"
        
        # Pausa aleatória importante para o servidor não bloquear o robô
        time.sleep(random.uniform(3.0, 6.0))
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Erro ao coletar jogo {game_id}: {e}")
            return None

# ==============================================================================
# ALINHAMENTO COM O MOTOR CELERY
# ==============================================================================

@celery_app.task(name="backend.coletor_espn.tarefa_coleta_espn")
def tarefa_coleta_espn(liga: str, id_time: str):
    """
    Função gerenciadora executada em segundo plano pelo Worker.
    Ela utiliza a classe ColetorESPN para minerar os dados com segurança.
    """
    # 1. Instancia o robô coletor
    coletor = ColetorESPN()
    
    print(f"Instanciando motor de busca para a liga: {liga} | Time ID: {id_time}")
    
    # 2. Busca a lista de IDs dos jogos finalizados (Limite padrão de 20)
    lista_de_ids = coletor.obter_ultimos_jogos_id(liga, id_time)
    
    if not lista_de_ids:
        return {
            "status": "Aviso", 
            "mensagem": f"Nenhum jogo finalizado encontrado para o time {id_time}."
        }
        
    resultados_finais = []
    
    # 3. Varre os IDs encontrados coletando o scout individual de cada partida
    for game_id in lista_de_ids:
        print(f"Minerando dados detalhados da partida ID: {game_id}")
        scout_jogo = coletor.obter_scout_partida(liga, game_id)
        
        if scout_jogo:
            resultados_finais.append({
                "game_id": game_id,
                "dados_brutos": scout_jogo
            })
            
    # 4. Retorna o relatório final para salvar o estado no Redis com SSL
    return {
        "status": "Sucesso",
        "liga": liga,
        "id_time": id_time,
        "total_jogos_processados": len(resultados_finais),
        "payload_coletado": resultados_finais
    }