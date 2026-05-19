import requests
import time
import random

class ColetorESPN:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json'
        }
        
    def obter_ultimos_jogos_id(self, esporte_liga: str, id_time: str, limite: int = 20):
        # Força o ID a ser string limpa
        id_time_str = str(id_time).strip()
        url = f"https://site.api.espn.com/apis/site/v2/sports/{esporte_liga}/teams/{id_time_str}/schedule"
        
        try:
            print(f"Disparando chamada para a URL: {url}")
            response = requests.get(url, headers=self.headers, timeout=12)
            
            if response.status_code != 200:
                print(f"ESPN recusou com status: {response.status_code}")
                return []
                
            dados = response.json()
            eventos = dados.get('events', [])
            
            if not eventos:
                # Estrutura alternativa da API para algumas ligas
                eventos = dados.get('requestedTeam', {}).get('schedule', [])
            
            ids = []
            for jogo in eventos:
                # Captura IDs de jogos finalizados ou agendados para ter dados
                id_jogo = jogo.get('id')
                if id_jogo:
                    ids.append(str(id_jogo))
            
            # Retorna os últimos dentro do limite estipulado
            return ids[-limite:] if ids else []
            
        except Exception as e:
            print(f"Erro interno de processamento no Coletor: {str(e)}")
            return []