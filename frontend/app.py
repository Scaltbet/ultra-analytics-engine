python
import streamlit as st
import requests

# Configuração de Página Estilo Dashboard Moderno
st.set_page_config(page_title="Ultra Analytics Engine", layout="wide", page_icon="📊")

st.title("📊 Ultra Analytics Engine")
st.write("Layout operacional com inteligência preditiva baseada nas últimas 20 partidas.")

# --- BARRA LATERAL ---
st.sidebar.header("⚙️ Configurações do Motor")
esporte_selecionado = st.sidebar.selectbox("Escolha a Modalidade", ["Futebol", "NBA"])
intervalo_atualizacao = st.sidebar.slider("Frequência de Atualização (Minutos)", 1, 60, 5)
st.sidebar.info(f"Filtro de Segurança: Atualizando a cada {intervalo_atualizacao} min (Cool-down ativo).")

# --- CONTEÚDO PRINCIPAL: GRADE DE JOGOS DO DIA (Estilo Casa de Apostas) ---
st.subheader("📆 Grade de Partidas do Dia")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("⚽ Premier League - 16:00")
    partida_1 = st.button("Arsenal 🆚 Chelsea", use_container_width=True)

with col2:
    st.info("⚽ LaLiga - 17:00")
    partida_2 = st.button("Real Madrid 🆚 Barcelona", use_container_width=True)

with col3:
    st.info("🏀 NBA - 21:30")
    partida_3 = st.button("LA Lakers 🆚 Boston Celtics", use_container_width=True)

# Lógica de clique nas partidas da grade
partida_ativa = None
times = {}

if partida_1:
    partida_ativa = "ARSxCHE"
    times = {"casa": "Arsenal", "fora": "Chelsea", "id_casa": "1", "id_fora": "2"}
elif partida_2:
    partida_ativa = "RMAxBAR"
    times = {"casa": "Real Madrid", "fora": "Barcelona", "id_casa": "3", "id_fora": "4"}
elif partida_3:
    partida_ativa = "LALxCEL"
    times = {"casa": "LA Lakers", "fora": "Boston Celtics", "id_casa": "5", "id_fora": "6"}

# --- TELA DETALHADA DA PARTIDA (Abra ao clicar em um jogo) ---
if partida_ativa:
    st.divider()
    st.header(f"🔎 Análise Estratégica: {times['casa']} x {times['fora']}")
    st.caption("Cruzando o histórico de 40 jogos simultâneos (20 de cada equipe)...")
    
    # Chamada fictícia simulando a rota POST do nosso backend rodando no Render
    # Em produção, use: requests.post("https://ultra-backend.onrender.com/api/analisar", json=...)
    payload_simulado = {
        "reincidencias": [
            {"mercado": "Over 9.5 Escanteios no Confronto", "probabilidade": 84.2, "tipo": "Ataque x Defesa Cruzado"},
            {"mercado": "Ambas Marcam (BTTS)", "probabilidade": 76.5, "tipo": "Média Frequentista"},
            {"mercado": f"Mais de 1.5 Gols a favor do {times['casa']}", "probabilidade": 71.0, "tipo": "Filtro de Consistência (Desvio Padrão Baixo)"}
        ]
    }
    
    st.subheader("💡 Top 3 Reincidências Simultâneas Detectadas")
    
    # Renderiza os 3 potes de ouro destacados na cor verde
    for i, item in enumerate(payload_simulado["reincidencias"], 1):
        st.success(f"**Padrão #{i}: {item['mercado']}**")
        st.markdown(f"* **Probabilidade Teórica:** {item['probabilidade']}% | **Métrica Aplicada:** {item['tipo']}")