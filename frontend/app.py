import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração de Layout Científico da Página
st.set_page_config(
    page_title="Ultra Analytics Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Ultra Analytics Engine — Painel de Performance Esportiva")
st.markdown("---")

# ==========================================
# CONFIGURAÇÃO DE VARIÁVEIS DE AMBIENTE
# ==========================================
BACKEND_URL = os.getenv("BACKEND_URL", "https://onrender.com")

# Sidebar para Autenticação e Filtros (ETAPA 16 / 17)
st.sidebar.header("🔑 Controle de Acesso")
usuario = st.sidebar.text_input("Usuário", value="admin@ultra.com")
senha = st.sidebar.text_input("Senha", type="password", value="ultra123")
botao_login = st.sidebar.button("Conectar ao Engine")

# Estado de Sessão para Token JWT
if "token" not in st.session_state:
    st.session_state.token = None

if botao_login:
    try:
        response = requests.post(
            f"{BACKEND_URL}/token",
            data={"username": usuario, "password": senha},
            timeout=5.0
        )
        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.sidebar.success("Autenticado com sucesso via JWT!")
        else:
            st.sidebar.error("Falha na autenticação. Verifique as credenciais.")
    except Exception as e:
        st.sidebar.error(f"Erro ao conectar com a API Backend: {e}")

# ==========================================
# GERAÇÃO DE DADOS SINTÉTICOS PARA APRESENTAÇÃO VETORIAL
# ==========================================
# Simulação de dados de cruzamento estatístico que virão do PostgreSQL/ML
@st.cache_data
def carregar_dados_analiticos():
    dados = {
        "Data": pd.date_range(start="2026-05-01", periods=15, freq="D"),
        "Lucro_ROI": [12.5, 14.2, -5.1, 8.9, 22.4, 18.1, 31.0, -2.4, 15.6, 28.9, 34.2, 11.0, 42.1, 38.5, 51.2],
        "Lote_Eventos": [100, 120, 115, 130, 145, 140, 160, 155, 170, 185, 190, 180, 210, 205, 220],
        "Mercado": ["Gols", "Handicap", "Cantos", "Gols", "Ambos Marcam", "Handicap", "Gols", "Cantos", "Ambos Marcam", "Gols", "Handicap", "Cantos", "Gols", "Ambos Marcam", "Handicap"]
    }
    return pd.DataFrame(dados)

df = carregar_dados_analiticos()

# ==========================================
# ESTRUTURAÇÃO DOS GRÁFICOS PLOTLY (ETAPA 17)
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Curva Evolutiva de ROI / Lucro Operacional")
    # Gráfico de linha dinâmico com marcadores vetoriais
    fig_linha = px.line(
        df, 
        x="Data", 
        y="Lucro_ROI", 
        title="Retorno Percentual sobre Investimento por Período",
        labels={"Lucro_ROI": "Lucro / ROI (%)", "Data": "Data do Evento"},
        markers=True,
        template="plotly_dark"
    )
    # Customização técnica das linhas de grade e eixos
    fig_linha.update_traces(line_color="#00ffcc", width=3)
    st.plotly_chart(fig_linha, use_container_width=True)

with col2:
    st.subheader("📊 Distribuição Macroeconômica por Mercado")
    # Gráfico de barras agregando volumetria de dados processados
    fig_barra = px.bar(
        df,
        x="Mercado",
        y="Lote_Eventos",
        color="Mercado",
        title="Volumetria de Lotes Processados por Segmento Esportivo",
        labels={"Lote_Eventos": "Volume de Eventos", "Mercado": "Segmento"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_barra, use_container_width=True)

# ==========================================
# BOTÃO DE INTERAÇÃO ASSÍNCRONA COM O BACKEND
# ==========================================
st.markdown("---")
st.subheader("⚙️ Gatilho de Processamento em Lote")
st.write("Dispare tarefas analíticas pesadas diretamente para a Thread Pool do Backend.")

if st.button("Disparar Carga de Trabalho Assíncrona"):
    if st.session_state.token is None:
        st.warning("🔒 Operação bloqueada. Você precisa se autenticar na barra lateral primeiro.")
    else:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        payload = {"solicitante": usuario, "lote_tamanho": 150, "operacao": "cruzamento_metricas"}
        
        try:
            res = requests.post(f"{BACKEND_URL}/analytics/processar", json=payload, headers=headers, timeout=5.0)
            if res.status_code == 200:
                st.success(f"Sucesso! Resposta do Engine: {res.json()}")
            else:
                st.error(f"Erro no processamento da API: {res.status_code}")
        except Exception as e:
            st.error(f"Erro físico de conexão com o servidor Backend: {e}")
