import requests
import time
import random

class ColetorESPN:
    def __init__(self):
        # Disfarce padrão para evitar bloqueios por IP
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
    def obter_ultimos_jogos_id(self, esporte_liga: str, id_time: str, limite: int = 20):
        """ 
        Busca o calendário oficial da API oculta.
        esporte_liga deve ser formatado como: 'soccer/bra.1' ou 'soccer/eng.1'
        """
        url = f"https://site.api.espn.com/apis/site/v2/sports/{esporte_liga}/teams/{id_time}/schedule"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                print(f"ESPN retornou status {response.status_code}")
                return []
                
            dados = response.json()
            eventos = dados.get('events', [])
            
            # Filtra apenas confrontos que já foram totalmente concluídos
            jogos_finalizados = [e for e in eventos if e.get('status', {}).get('type', {}).get('completed') == True]
            
            # Captura os IDs das partidas respeitando o limite estatístico
            ids = [jogo['id'] for jogo in jogos_finalizados[-limite:]]
            return ids
        except Exception as e:
            print(f"Erro crítico ao processar o JSON de calendário: {e}")
            return []

    def obter_scout_partida(self, esporte_liga: str, game_id: str):
        """ Abre os dados estatísticos puros (gols, cantos, cartões) de um jogo """
        url = f"https://site.api.espn.com/apis/site/v2/sports/{esporte_liga}/summary?event={game_id}"
        
        # Delay de segurança obrigatório do plano de contingência
        time.sleep(random.uniform(3.0, 6.0))
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return None
            return response.json()
        except Exception as e:
            print(f"Erro de comunicação com endpoint summary {game_id}: {e}")
            return None