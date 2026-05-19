import requests

class ColetorESPN:
    def __init__(self):
        # Base da API oculta da ESPN
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports"

    def obter_historico(self, esporte: str, liga: str, team_id: str):
        """
        Busca o calendário/histórico de jogos de um time específico.
        Exemplo: esporte='soccer', liga='bra.1' (Brasileirão) ou liga='usa.1' (MLS)
        """
        url = f"{self.base_url}/{esporte}/{liga}/teams/{team_id}/schedule"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json().get('events', [])
            return []
        except Exception:
            return []

    def analisar_dados(self, events: list, team_id: str):
        """
        Processa o histórico cruzando os dados das últimas 20 partidas
        e calcula a reincidência dos mercados de gols e BTTS.
        """
        jogos_processados = 0
        gols_marcados = 0
        gols_sofridos = 0
        ambas_marcam_count = 0
        over_1_5_count = 0
        over_2_5_count = 0

        # Filtra apenas jogos que já foram concluídos e limita aos últimos 20
        jogos_finalizados = [
            e for e in events 
            if e.get('status', {}).get('type', {}).get('completed', False)
        ][:20]

        for event in jogos_finalizados:
            competitions = event.get('competitions', [])
            if not competitions:
                continue
            
            competitors = competitions[0].get('competitors', [])
            if len(competitors) < 2:
                continue

            gols_pro = None
            gols_contra = None

            # Varre os dois competidores da partida para isolar Pro vs Contra
            for c in competitors:
                score_value = c.get('score', {}).get('value')
                if score_value is None:
                    continue
                
                try:
                    score = int(score_value)
                except (ValueError, TypeError):
                    continue

                # Se o ID do competidor for o do time analisado, são gols a favor
                if str(c.get('team', {}).get('id')) == str(team_id):
                    gols_pro = score
                else:
                    gols_contra = score

            # Validação: Só processa a partida se coletou os gols de ambos os times
            if gols_pro is not None and gols_contra is not None:
                jogos_processados += 1
                gols_marcados += gols_pro
                gols_sofridos += gols_contra

                # Cálculo do mercado: Ambas Marcam (BTTS)
                if gols_pro > 0 and gols_contra > 0:
                    ambas_marcam_count += 1

                # Cálculo dos mercados de Over Gols
                total_gols = gols_pro + gols_contra
                if total_gols > 1.5:
                    over_1_5_count += 1
                if total_gols > 2.5:
                    over_2_5_count += 1

        # Prevenção contra divisão por zero caso não haja jogos no histórico
        if jogos_processados == 0:
            return {
                "jogos_analisados": 0,
                "media_gols_marcados": 0.0,
                "media_gols_sofridos": 0.0,
                "Ambas Marcam (BTTS)": 0.0,
                "Over 1.5 Gols": 0.0,
                "Over 2.5 Gols": 0.0
            }

        # Retorna o dicionário mastigado com as porcentagens prontas para o Frontend
        return {
            "jogos_analisados": jogos_processados,
            "media_gols_marcados": round(gols_marcados / jogos_processados, 2),
            "media_gols_sofridos": round(gols_sofridos / jogos_processados, 2),
            "Ambas Marcam (BTTS)": round((ambas_marcam_count / jogos_processados) * 100, 2),
            "Over 1.5 Gols": round((over_1_5_count / jogos_processados) * 100, 2),
            "Over 2.5 Gols": round((over_2_5_count / jogos_processados) * 100, 2)
        }
