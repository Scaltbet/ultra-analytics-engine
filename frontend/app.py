import streamlit as st
import requests

st.set_page_config(page_title="Ultra Analytics Engine", layout="wide")
st.title("📊 Ultra Analytics Engine")

# URL oficial do seu backend hospedado no Render
BACKEND_URL = "https://ultra-analytics-engine.onrender.com"

# Teste automático de conexão de segurança
try:
    checar_conexao = requests.get(BACKEND_URL, timeout=5)
    if checar_conexao.status_code == 200:
        st.success("⚡ Conexão activa com o núcleo de análise.")
    else:
        st.error("❌ Conexão instável com o servidor principal.")
except Exception:
    st.error("❌ Núcleo de análise offline no Render.")

st.subheader("Iniciar Nova Raspagem de Dados")
st.write("Escolha a liga e o ID do time da ESPN para alimentar o banco de dados.")

# DICIONÁRIO CRÍTICO: Mapeia o texto da tela para o código que a API da ESPN exige
OPCOES_LIGAS = {
    "LaLiga (Espanha)": "soccer/esp.1",
    "Brasileirão Série A": "soccer/bra.1",
    "Premier League (Inglaterra)": "soccer/eng.1",
    "Serie A (Itália)": "soccer/ita.1",
    "Champions League": "soccer/uefa.champions"
}

# Cria o campo de seleção usando as chaves amigáveis
liga_selecionada = st.selectbox("Selecione a Liga", list(OPCOES_LIGAS.keys()))
id_time = st.text_input("ID do Time na ESPN (Ex: 360 para Real Madrid)", value="360")

if st.button("Executar Engenharia de Coleta"):
    # Traduz o nome bonito para o slug técnico (ex: "soccer/esp.1")
    liga_slug = OPCOES_LIGAS[liga_selecionada]
    
    payload = {
        "liga": liga_slug,
        "id_time": str(id_time)
    }
    
    with st.spinner("Motor ESPN ativado... Coletando histórico de confrontos..."):
        try:
            # Dispara a requisição POST para a rota /analisar do seu FastAPI
            response = requests.post(f"{BACKEND_URL}/analisar", json=payload, timeout=20)
            
            if response.status_code == 200:
                resultado = response.json()
                st.success(f"🔥 Sucesso! Localizados {resultado['quantidade_jogos_localizados']} jogos recentes para o banco de dados.")
                st.json(resultado["lista_ids"]) # Exibe os IDs coletados temporariamente
            elif response.status_code == 404:
                st.error("Erro 404: ID do time ou Liga não encontrados na base de dados da ESPN. Verifique o código do clube.")
            else:
                st.error(f"Erro {response.status_code}: Falha na resposta do motor de análise.")
        except Exception as e:
            st.error(f"Erro crítico de rede: Não foi possível alcançar o servidor. ({e})")