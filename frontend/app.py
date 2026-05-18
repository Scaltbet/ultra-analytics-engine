import streamlit as st
import requests

# 1. Configuração da Página
st.set_page_config(
    page_title="Ultra Analytics Engine", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Configuração do Endereço do Servidor
# Coloque a URL do seu 'ultra-backend' do Render dentro das aspas (Sem a barra '/' no final)
URL_BACKEND = "https://ultra-backend-w8f4.onrender.com"

# Inicializa a variável de sessão para o monitor de tarefas
if "ultimo_task_id" not in st.session_state:
    st.session_state["ultimo_task_id"] = ""

# 3. Cabeçalho da Interface
st.title("📊 Ultra Analytics Engine")
st.caption("Sistema de Alta Performance para Cruzamento de Estatísticas Esportivas")

st.success("⚡ Conexão ativa com o núcleo de análise.")

# 4. Criação das Abas Visuais
aba_disparar, aba_analise = st.tabs(["🚀 Disparar Coletas", "📈 Análise Operacional"])

with aba_disparar:
    st.header("Iniciar Nova Raspagem de Dados")
    st.write("Escolha a liga e o ID do time da ESPN para alimentar o banco de dados.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        liga_selecionada = st.selectbox(
            "Selecione a Liga", 
            [
                "LaLiga (Espanha)", 
                "Premier League (Inglaterra)", 
                "Serie A (Itália)", 
                "Champions League"
            ]
        )
        
    with col2:
        id_time = st.text_input(
            "ID do Time na ESPN (Ex: 360 para Real Madrid, 359 para Barcelona)", 
            value="360"
        )

    # Botão de Ação Principal
    if st.button("Executar Engenharia de Coleta"):
        with st.spinner("Acionando motores e enviando ordem para os Workers..."):
            try:
                payload = {
                    "liga": str(liga_selecionada),
                    "id_time": str(id_time)
                }
                
                resposta = requests.post(
                    f"{URL_BACKEND}/disparar-coleta", 
                    json=payload, 
                    timeout=15
                )
                
                if resposta.status_code == 200:
                    dados = resposta.json()
                    st.success(f"🤖 {dados.get('status', 'Sucesso!')}")
                    st.session_state["ultimo_task_id"] = dados.get("task_id")
                    st.info(f"ID do Processo em segundo plano: **{dados.get('task_id')}**")
                else:
                    st.error(f"Erro {resposta.status_code}: Rota inválida ou formato incorreto no servidor.")
                    
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
                            st.info(f"Status atual: {status_atual}")
                    else:
                        st.error(f"Não foi possível encontrar dados para este ID. Status: {resposta_status.status_code}")
                except Exception as e:
                    st.error(f"Erro ao conectar no monitor: {e}")

with aba_analise:
    st.header("Análise Operacional")
    st.info("Esta aba exibirá os gráficos probabilísticos de gols e escanteios assim que o banco de dados receber os primeiros registros da ESPN.")