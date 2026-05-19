import requests

class ColetorESPN:
    def __init__(self):
        # Disfarce e cabeçalhos reforçados
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
    def obter_ultimos_jogos_id(self, esporte_liga: str, id_time: str, limite: int = 20):
        """Busca os últimos IDs de partidas já finalizadas na ESPN"""
        id_time_str = str(id_time).strip()
        url = f"https://site.api.espn.com/apis/site/v2/sports/{esporte_liga}/teams/{id_time_str}/schedule"
        
        try:
            print(f"[COLETOR] Disparando requisição para API: {url}")
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code != 200:
                print(f"[COLETOR] ESPN recusou conexão. Status: {response.status_code}")
                return []
                
            dados = response.json()
            eventos = dados.get('events', [])
            
            # Fallback caso a ESPN mude o formato da árvore JSON para ligas menores
            if not eventos:
                eventos = dados.get('requestedTeam', {}).get('schedule', [])
            
            ids_coletados = []
            for jogo in eventos:
                # Filtra estritamente: Só queremos o ID se o jogo já tiver acabado (completed = True)
                status = jogo.get('status', {}).get('type', {}).get('completed', False)
                id_jogo = jogo.get('id')
                
                if id_jogo and status:
                    ids_coletados.append(str(id_jogo))
            
            resultados_finais = ids_coletados[-limite:] if ids_coletados else []
            print(f"[COLETOR] Coleta limpa. {len(resultados_finais)} jogos válidos encontrados.")
            return resultados_finais
            
        except Exception as e:
            print(f"[COLETOR] Erro interno crítico: {str(e)}")
            return []