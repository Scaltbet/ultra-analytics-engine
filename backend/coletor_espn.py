score = c.get('score', {}).get('value')
if score is None:
    continue

dados_validos = True
if str(c.get('team', {}).get('id')) == str(team_id):
    gols_pro = int(score)
else:
    gols_contra = int(score)

if dados_validos:
    jogos_processados += 1
    gols_marcados += gols_pro
    gols_sofridos += gols_contra

    # Cálculos de mercados de apostas
    if gols_pro > 0 and gols_contra > 0:
        ambas_marcam_count += 1
        
    total_gols = gols_pro + gols_contra
    if total_gols > 1.5:
        over_1_5_count += 1
    if total_gols > 2.5:
        over_2_5_count += 1

if jogos_processados == 0:
    return None

return {
    "jogos_analisados": jogos_processados,
    "media_gols_marcados": round(gols_marcados / jogos_processados, 2),
    "media_gols_sofridos": round(gols_sofridos / jogos_processados, 2),
    "porcentagem_ambas_marcam": round((ambas_marcam_count / jogos_processados) * 100, 2),
    "porcentagem_over_1_5": round((over_1_5_count / jogos_processados) * 100, 2),
    "porcentagem_over_2_5": round((over_2_5_count / jogos_processados) * 100, 2)
}