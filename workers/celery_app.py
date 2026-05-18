import os
import requests
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

class ColetorESPN:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
    def executar_fluxo(self, liga: str, id_time: str):
        # Aqui entra a lógica de mapeamento para a URL da ESPN
        # Exemplo: se o usuário escolheu "LaLiga (Espanha)", convertemos para a rota correta da URL (/soccer)
        slug_liga = "/soccer" 
        
        url_agenda = f"https://site.api.espn.com/apis/site/v2/sports{slug_liga}/leagues/esp.1/teams/{id_time}/schedule"
        
        try:
            # Teste de requisição para puxar a agenda do time informado
            resposta = requests.get(url_agenda, headers=self.headers, timeout=10)
            if resposta.status_code == 200:
                return f"Sucesso! Conectado à ESPN. Dados da liga mapeados para o time {id_time}."
            return f"ESPN respondeu com status {resposta.status_code}"
        except Exception as e:
            return f"Erro de conexão com a API ESPN: {e}"

@celery.task(name="tarefa_coleta_espn")
def tarefa_coleta_espn(liga: str, id_time: str):
    coletor = ColetorESPN()
    resultado = coletor.executar_fluxo(liga, id_time)
    return resultado