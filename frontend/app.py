import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

st.set_page_config(
    page_title="Ultra Analytics Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Ultra Analytics Engine — Painel de Performance Esportiva")
st.markdown("---")

# CONFIGURAÇÃO DE VARIÁVEIS DE AMBIENTE
BACKEND_URL = os.getenv("BACKEND_URL", "https://onrender.com")

# Sidebar para Autenticação e Configurações
st.sidebar.markdown("### 🔑 Controle de Acesso")

# Inicializa o estado de login se não existir
if "conectado" not in st.session_state:
    st.session_state.conectado = False

usuario = st.sidebar.text_input("Usuário", value="admin@ultra.com")
senha = st.sidebar.text_input("Senha", type="password", value="12345678")

if st.sidebar.button("Conectar ao Engine"):
    if usuario == "admin@ultra.com" and senha == "12345678":
        st.session_state.conectado = True
        st.sidebar.success("Conectado com sucesso!")
    else:
        st.sidebar.error("Usuário ou senha incorretos.")

if not st.session_state.conectado:
    st.warning("Por favor, insira suas credenciais na barra lateral para liberar o controle do Engine.")
else:
    st.success("⚡ Conexão ativa com o núcleo de análise.")
    
    # Abas de navegação interna
    aba_coleta, aba_graficos = st.tabs(["🚀 Disparar Coletas", "📈 Análise Operacional"])
    
    with aba_coleta:
        st.subheader("Iniciar Nova Raspagem de Dados")
        st.write("Escolha a liga e o ID do time da ESPN para alimentar o banco de dados.")
        
        col1, col2 = st.columns(2)
        with col1:
            liga_selecionada = st.selectbox(
                "Selecione a Liga", 
                ["/soccer/liga/eng.1", "/soccer/liga/esp.1", "/soccer/liga/bra.1"],
                format_func=lambda x: "Premier League (Inglaterra)" if "eng.1" in x else "LaLiga (Espanha)" if "esp.1" in x else "Brasileirão (Brasil)"
            )
        with col2:
            id_time = st.text_input("ID do Time na ESPN (Ex: 360 para Real Madrid, 359 para Barcelona)", value="360")
            
        if st.button("Executar Engenharia de Coleta"):
            with st.spinner("Enviando requisição para a fila de execução rápida..."):
                try:
                    url_final = f"{BACKEND_URL}/coletar{liga_selecionada}/{id_time}"
                    resposta = requests.post(url_final, timeout=10)
                    
                    if resposta.status_code == 200:
                        st.balloons()
                        st.success(f"Sucesso! O Worker começou a processar os dados do time {id_time}.")
                    else:
                        st.error(f"O servidor backend retornou um erro: {resposta.status_code}")
                except Exception as e:
                    st.error(f"Não foi possível conectar ao Backend: {e}")

    with aba_graficos:
        # Exibição simulada dos gráficos que aparecem na sua tela
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.subheader("📈 Curva Evolutiva de ROI / Lucro Operacional")
            dados_roi = pd.DataFrame({"Jogos": range(1, 11), "ROI": [2, 5, 4, 7, 6, 9, 8, 12, 11, 15]})
            fig_roi = px.line(dados_roi, x="Jogos", y="ROI", markers=True)
            st.plotly_chart(fig_roi, use_container_width=True)
            
        with col_g2:
            st.subheader("📊 Distribuição Macroeconômica por Mercado")
            dados_mercado = pd.DataFrame({
                "Mercado": ["Gols", "Handicap", "Cantos", "Ambos Marcam"],
                "Volume": [400, 300, 200, 150]
            })
            fig_mercado = px.bar(dados_mercado, x="Mercado", y="Volume", color="Mercado")
            st.plotly_chart(fig_mercado, use_container_width=True)