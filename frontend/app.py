import streamlit as st
import requests
from datetime import datetime

# Configuração de Layout Profissional de Inteligência Esportiva
st.set_page_config(page_title="Scalt Bet Pro", layout="wide", initial_sidebar_state="collapsed")

# Cabeçalho de Identidade Visual
st.title("🚀 Scalt Bet Pro")
st.caption("Plataforma Avançada de Análise Estatística Preditiva e Cruzamento de Dados")

BACKEND_URL = "https://ultra-analytics-engine.onrender.com"

# Painel de Controle Superior
st.subheader("🗓️ Seleção de Rodada e Coleta")
col_liga, col_data = st.columns([2, 1])

OPCOES_LIGAS = {
    "LaLiga (Espanha)": "soccer/esp.1",
    "Brasileirão Série A": "soccer/bra.1",
    "Premier League (Inglaterra)": "soccer/eng.1",
    "Serie A (Itália)": "soccer/ita.1",
    "Champions League": "soccer/uefa.champions"
}

with col_liga:
    liga_selecionada = st.selectbox("Selecione a Liga para Mapeamento", list(OPCOES_LIGAS.keys()))

with col_data:
    # Cria um seletor de data padrão
    data_escolhida = st.date_input("Data dos Confrontos", datetime.now())
    data_formatada = data_escolhida.strftime("%Y%m%d")

liga_slug = OPCOES_LIGAS[liga_selecionada]

st.markdown("---")

# Inicializa o estado para guardar os dados do confronto selecionado para análise
if "confronto_ativo" not in st.session_state:
    st.session_state.confronto_ativo = None

# Bloco 1: Carregamento Automático da Grade Estilo Casa de Apostas
st.subheader("🎮 Grade de Partidas Disponíveis")

payload_grade = {
    "liga": str(liga_slug),
    "data": str(data_formatada)
}

with st.spinner("Varrendo calendário da liga e montando grade de eventos..."):
    try:
        response = requests.post(f"{BACKEND_URL}/grade", json=payload_grade, timeout=15)
        
        if response.status_code == 200:
            dados_grade = response.json()
            lista_jogos = dados_grade.get("jogos", [])
            
            if not lista_jogos:
                st.info("Nenhum jogo agendado para esta liga na data selecionada.")
            else:
                # Cria a tabela de confrontos estilizada
                for jogo in lista_jogos:
                    id_partida = jogo.get("id_partida")
                    status = jogo.get("status", "Agendado")
                    mandante = jogo.get("mandante", {})
                    visitante = jogo.get("visitante", {})
                    
                    # Layout em Linha: Horário | Mandante vs Visitante | Ação
                    col_status, col_jogo, col_acao = st.columns([1, 4, 2])
                    
                    with col_status:
                        st.markdown(f"**`{status}`**")
                        
                    with col_jogo:
                        st.markdown(f"🏟️ {mandante.get('nome')} vs **{visitante.get('nome')}**")
                        
                    with col_acao:
                        # Botão único para cada confronto passando os IDs secretos no clique
                        if st.button("📊 Analisar Confronto", key=f"btn_{id_partida}"):
                            st.session_state.confronto_ativo = {
                                "mandante_nome": mandante.get('nome'),
                                "visitante_nome": visitante.get('nome'),
                                "id_mandante": mandante.get('id'),
                                "id_visitante": visitante.get('id')
                            }
                            
        elif response.status_code == 404:
            st.warning("⚠️ Nenhuma partida localizada na ESPN para esta combinação de liga e data.")
        else:
            st.error(f"Erro {response.status_code}: Falha ao obter grade com o servidor.")
            
    except Exception as e:
        st.error(f"Erro de conexão com o ecossistema: {e}")

st.markdown("---")

# Bloco 2: Painel Central de Cruzamento de Dados (Ativado ao clicar no botão acima)
if st.session_state.confronto_ativo:
    conf = st.session_state.confronto_ativo
    st.subheader(f"📊 Painel Estatístico Compartivo: {conf['mandante_nome']} vs {conf['visitante_nome']}")
    
    payload_analise = {
        "liga": str(liga_slug),
        "id_mandante": str(conf['id_mandante']),
        "id_visitante": str(conf['id_visitante'])
    }
    
    with st.spinner("Executando engenharia de cruzamento... Escaneando últimos 20 jogos..."):
        try:
            res_analise = requests.post(f"{BACKEND_URL}/analisar", json=payload_analise, timeout=20)
            if res_analise.status_code == 200:
                resultado = res_analise.json()
                
                st.success("🔥 Conexão estruturada! Próximo passo: renderizar as tabelas de médias reais.")
                st.json(resultado) # Exibe o stub de confirmação por enquanto
            else:
                st.error("Falha no processamento interno do motor de cruzamento.")
        except Exception as e:
            st.error(f"Erro ao conectar com a rota de análise: {e}")