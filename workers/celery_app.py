python
import time
import requests
from celery import Celery

# Configuração do Celery usando o Redis gratuito do Upstash
app = Celery('tasks', broker='redis://localhost:6337/0') # Altere para sua URL do Upstash em Produção

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

@app.task(name="tasks.coletar_dados_espn")
def coletar_dados_espn(esporte: str, liga: str, id_time: str):
    """
    Worker que executa buscas inteligentes respeitando regras de anti-bloqueio.
    Esporte: 'soccer' ou 'basketball'
    Liga: 'eng.1', 'esp.1', 'nba'
    """
    # URL Base Oculta mapeada via Inspecionar Elemento (F12)
    url_base = f"https://site.api.espn.com/apis/site/v2/sports/{esporte}/{liga}/scoreboard"
    
    try:
        # Executa requisição na API interna da ESPN
        resposta = requests.get(url_base, headers=HEADERS, timeout=10)
        dados = resposta.json()
        
        # 🛑 REGLA DE COOL-DOWN (Evita disparar requisições em rajada)
        # Durante partidas ao vivo ou loops intensos, força uma folga automática de segurança
        time.sleep(3) 
        
        # Aqui os dados filtrados seriam processados e inseridos no Supabase
        return f"Coleta realizada com sucesso para o time {id_time}. {len(dados.get('events', []))} partidas mapeadas."