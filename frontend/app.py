import streamlit as st
import pandas as pd

# Simulação da Grade de Jogos (Em produção, isso virá de uma chamada ao seu Supabase)
jogos_do_dia = [
    {"id": 1, "casa": "Flamengo", "fora": "Palmeiras", "liga": "Brasileirão"},
    {"id": 2, "casa": "Lakers", "fora": "Celtics", "liga": "NBA"}
]

st.set_page_config(page_title="Ultra Analytics", layout="wide")
st.title("📊 Ultra Analytics - Grade de Oportunidades")

# Renderização da Grade estilo Casa de Apostas
for jogo in jogos_do_dia:
    with st.container():
        cols = st.columns([4, 1])
        cols[0].write(f"**{jogo['casa']} vs {jogo['fora']}** - {jogo['liga']}")
        if cols[1].button("Analisar", key=jogo['id']):
            st.session_state['jogo_ativo'] = jogo

# Lógica de Cruzamento e Exibição (Após clicar em Analisar)
if 'jogo_ativo' in st.session_state:
    j = st.session_state['jogo_ativo']
    st.divider()
    st.subheader(f"Análise: {j['casa']} vs {j['fora']}")
    
    # Simulação dos dados que o seu 'coletor_espn.py' retorna
    # Aqui o sistema cruzará os dados do histórico de 20 partidas
    stats = {
        "Ambas Marcam (BTTS)": 75,
        "Over 2.5 Gols": 65,
        "Over 8.5 Escanteios": 88,
        "Gol no 1º Tempo": 55
    }
    
    df_stats = pd.DataFrame(list(stats.items()), columns=["Mercado", "Probabilidade"])
    # Ordena pelos 3 maiores e exibe
    top_3 = df_stats.sort_values(by="Probabilidade", ascending=False).head(3)
    
    st.write("### 🔥 Top 3 Mercados com Alta Reincidência")
    for i, row in top_3.iterrows():
        st.metric(label=row["Mercado"], value=f"{row['Probabilidade']}%")

    if st.button("Fechar Análise"):
        del st.session_state['jogo_ativo']
        st.rerun()
l