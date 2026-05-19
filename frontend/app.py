import streamlit as st
import requests

st.set_page_config(page_title="Ultra Analytics Engine", layout="wide")
st.title("📊 Ultra Analytics Engine")

BACKEND_URL = "https://ultra-analytics-engine.onrender.com"

# Teste de conexão básico
try:
    checar = requests.get(BACKEND_URL, timeout=5)
    if checar.status_code == 200:
        st.success("⚡ Conexão activa com o núcleo de análise.")
    else:
        st.error("❌ Conexão instável com o servidor.")
except Exception:
    st.error("❌ Núcleo de análise offline no Render.")

st.subheader("Iniciar Nova Raspagem de Dados")

OPCOES_LIGAS = {
    "LaLiga (Espanha)": "soccer/esp.1",
    "Brasileirão Série A": "soccer/bra.1",
    "Premier League (Inglaterra)": "soccer/eng.1",
    "Serie A (Itália)": "soccer/ita.1",
    "Champions League": "soccer/uefa.champions"
}

# Criando duas colunas idênticas ao seu novo layout da imagem
col1, col2 = st.columns([2, 1])

with col1:
    liga_selecionada = st.selectbox("Selecione a Liga", list(OPCOES_LIGAS.keys()))

with col2:
    id_time = st.text_input("ID do Time na ESPN", value="360")

if st.button("Executar Engenharia de Coleta"):
    liga_slug = OPCOES_LIGAS[liga_selecionada]
    
    # Payload explícito e limpo combinando com o FastAPI
    payload = {
        "liga": str(liga_slug),
        "id_time": str(id_time).strip()
    }
    
    with st.spinner("Motor ESPN ativado..."):
        try:
            response = requests.post(f"{BACKEND_URL}/analisar", json=payload, timeout=20)
            
            if response.status_code == 200:
                resultado = response.json()
                st.success(f"🔥 Sucesso! Localizados {resultado['quantidade_jogos_localizados']} jogos recentes para o banco de dados.")
                st.json(resultado["lista_ids"])
            elif response.status_code == 404:
                st.error("Erro 404: Nenhum jogo recente ou time localizado com os parâmetros informados.")
            else:
                st.error(f"Erro {response.status_code}: O servidor recusou o formato da requisição.")
        except Exception as e:
            st.error(f"Erro crítico de rede: {e}")