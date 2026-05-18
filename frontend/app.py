import streamlit as st
import requests

# 1. Configuração da Página
st.set_page_config(
    page_title="Ultra Analytics Engine", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Definição do link real do seu Render (Sem barra no final)
URL_BACKEND = "https://ultra-analytics-engine.onrender.com"

# Inicializa a variável de sessão para o monitor de tarefas
if "ultimo_task_id" not in st.session_state:
    st.session_state["ultimo_task_id"] = ""

# 3. Cabeçalho da Interface
st.title("📊 Painel de Performance Esportiva")
st.caption("Sistema de Alta Performance para Cruzamento de Estatísticas Esportivas")

st.success("⚡ Conexão activa com o núcleo de análise.")

# 4. Criação das Abas Visuais
aba_disparar, aba_analise = st.tabs(["🚀 Disparar Coletas", "📈 Análise Operacional"])

with aba_disparar:
    st.header("Iniciar Nova Raspagem de Dados")
    st.write("Escolha a liga e o ID do time da ESPN para alimentar o banco de dados.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Dicionário que traduz o nome visual para a rota real que a API/Site da ESPN usa
        ligas_disponiveis = {
            "LaLiga (Espanha)": "/soccer/league/_/name/esp.1",
            "Premier League (Inglaterra)": "/soccer/league/_/name/eng.1",
            "Serie A (Itália)": "/soccer/league/_/name/ita.1",
            "Champions League": "/soccer/league/_/name/uefa.champions"
        }
        
        liga_visual = st.selectbox("Selecione a Liga", list(ligas_disponiveis.keys()))
        # Obtém o caminho correto (/soccer/...) em vez do texto bruto
        liga_selecionada = ligas_disponiveis[liga_visual]
        
    with col2:
        id_time = st.text_input(
            "ID do Time na ESPN (Ex: 360 para Real Madrid, 359 para Barcelona)", 
            value="360"
        )

    # Botão de Acção Principal
    if st.button("Executar Engenharia de Coleta"):
        with st.spinner("Acionando motores e enviando ordem para os Workers..."):
            try:
                # Envia o caminho de URL mapeado que o backend espera
                payload = {
                    "liga": str(liga_selecionada),
                    "id_time": str(id_time)
                }
                
                # Disparo POST apontando diretamente para a rota /disparar-coleta
                resposta = requests.post(
                    f"{URL_BACKEND}/disparar-coleta", 
                    json=payload, 
                    timeout=60
                )
                
                if resposta.status_code == 200:
                    dados = resposta.json()
                    st.success(f"🤖 {dados.get('status', 'Sucesso!')}")
                    st.session_state["ultimo_task_id"] = dados.get("task_id")
                    st.info(f"ID do Processo em segundo plano: **{dados.get('task_id')}**")
                else:
                    st.error(f"Erro {resposta.status_code}: O servidor recusou o formato da requisição.")
                    
            except Exception as e:
                st.error(f"Não foi possível estabelecer contato com o servidor backend: {e}")

    # 5. Painel de Monitoramento de Status
    st.divider()
    st.subheader("🕵️‍♂️ Monitor de Tarefas em Segundo Plano")
    st.write("Verifique se o Worker já terminou de processar a última requisição.")
    
    id_para_checar = st.text_input(
        "Insira o ID da Tarefa (Task ID):", 
        value=st.session_state["ultimo_task_id"]
    )
    
    if st.button("Verificar Progresso"):
        if not id_para_checar:
            st.warning("Insira um ID de tarefa válido para consultar.")
        else:
            with st.spinner("Consultando status no Redis..."):
                try:
                    resposta_status = requests.get(f"{URL_BACKEND}/status-coleta/{id_para_checar}", timeout=10)
                    
                    if resposta_status.status_code == 200:
                        dados_status = resposta_status.json()
                        status_atual = dados_status.get("status")
                        if status_atual == "PENDING":
                            st.warning("⏳ Aguardando na fila / Processando...")
                        elif status_atual == "SUCCESS":
                            st.success("✅ Concluído com sucesso pelo Worker!")
                            st.json(dados_status.get("resultado"))
                        else:
                            st.error(f"❌ Status retornado: {status_atual}")
                    else:
                        st.error(f"Erro {resposta_status.status_code} ao buscar status.")
                except Exception as e:
                    st.error(f"Erro de comunicação: {e}")