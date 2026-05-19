import requests
from datetime import datetime

class ColetorESPN:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json'
        }
        
    def obter_jogos_do_dia(self, esporte_liga: str, data_str: str = None):
        """Busca todas as partidas de uma liga para uma data específica (Formato: YYYYMMDD)"""
        if not data_str:
            data_str = datetime.now().strftime("%Y%m%d")
            
        # URL do Scoreboard da ESPN que traz a rodada completa da liga
        url = f"https://site.api.espn.com/apis/site/v2/sports/{esporte_liga}/scoreboard?dates={data_str}"
        
        try:
            print(f"[SCALT COLETOR] Buscando rodada do dia na URL: {url}")
            response = requests.get(url, headers=self.headers, timeout=12)
            
            if response.status_code != 200:
                print(f"[SCALT COLETOR] Erro de conexão com ESPN: Status {response.status_code}")
                return []
                
            dados = response.json()
            eventos = dados.get('events', [])
            
            grade_partidas = []
            
            for evento in eventos:
                id_jogo = evento.get('id')
                status_jogo = evento.get('status', {}).get('type', {}).get('detail', '')
                
                competidores = evento.get('competitions', [{}])[0].get('competitors', [])
                
                # Na ESPN, o índice 0 costuma ser o Home (Mandante) e o 1 o Away (Visitante)
                # Mas vamos validar a flag 'homeAway' para garantir precisão cirúrgica
                mandante = {}
                visitante = {}
                
                for time in competidores:
                    info_time = {
                        "id": str(time.get('id')),
                        "nome": time.get('team', {}).get('displayName'),
                        "logo": time.get('team', {}).get('logo'),
                        "sigla": time.get('team', {}).get('abbreviation')
                    }
                    if time.get('homeAway') == 'home':
                        mandante = info_time
                    else:
                        visitante = info_time
                
                if id_jogo and mandante and visitante:
                    grade_partidas.append({
                        "id_partida": str(id_jogo),
                        "status": status_jogo,
                        "mandante": mandante,
                        "visitante": visitante
                    })
                    
            print(f"[SCALT COLETOR] Sucesso. {len(grade_partidas)} confrontos mapeados para a grade.")
            return grade_partidas
            
        except Exception as e:
            print(f"[SCALT COLETOR] Falha crítica ao gerar grade: {str(e)}")
            return []