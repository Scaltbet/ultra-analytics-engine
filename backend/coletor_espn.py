import requests
import time
import random

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