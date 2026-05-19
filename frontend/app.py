import streamlit as st
import requests
from datetime import datetime

# Configuração de Layout Profissional de Inteligência Esportiva
st.set_page_config(page_title="Scalt Bet Pro", layout="wide", initial_sidebar_state="collapsed")

# CSS para estilização e remoção de margens excessivas - Correção de Sintaxe Aplicada
st.markdown("""
    <style>
    .metric-box {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #334155;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #38bdf8;
    }
    </style>
""", unsafe_allow_html=True)

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
                for jogo in lista_jogos:
                    id_partida = jogo.get("id_partida")
                    status = jogo.get("status", "Agendado")
                    mandante = jogo.get("mandante", {})
                    visitante = jogo.get("visitante", {})
                    
                    col_status, col_jogo, col_acao = st.columns([1, 4, 2])
                    
                    with col_status:
                        st.markdown(f"**`{status}`**")
                        
                    with col_jogo:
                        st.markdown(f"🏟️ {mandante.get('nome')} vs **{visitante.get('nome')}**")
                        
                    with col_acao:
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

# Bloco 2: Painel Central de Cruzamento de Dados
if st.session_state.confronto_ativo:
    conf = st.session_state.confronto_ativo
    st.subheader(f"📊 Painel Estatístico Comparativo: {conf['mandante_nome']} vs {conf['visitante_nome']}")
    
    payload_analise = {
        "liga": str(liga_slug),
        "id_mandante": str(conf['id_mandante']),
        "id_visitante": str(conf['id_visitante'])
    }
    
    with st.spinner("Executando inteligência preditiva... Escaneando históricos..."):
        try:
            res_analise = requests.post(f"{BACKEND_URL}/analisar", json=payload_analise, timeout=20)
            if res_analise.status_code == 200:
                res = res_analise.json()
                
                m = res["mandante"]
                v = res["visitante"]
                insights = res["insights_preditivos"]
                
                # Cards de Insights de Tendência no Topo do Confronto
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    st.markdown(f"""
                        <div class="metric-box">
                            <div>⚽ Expectativa de Gols do Confronto</div>
                            <div class="metric-value">{insights['expectativa_gols_confronto']} Gols</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_i2:
                    st.markdown(f"""
                        <div class="metric-box">
                            <div>🔥 Probabilidade de Ambas Marcam</div>
                            <div class="metric-value">{insights['probabilidade_ambas_marcam']}%</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Tabela de Comparação Direta das Últimas 20 Partidas
                st.markdown("### 📈 Raio-X dos Últimos 20 Jogos")
                
                st.write(f"""
                | Métrica Estatística | {conf['mandante_nome']} (Mandante) | {conf['visitante_nome']} (Visitante) |
                | :--- | :---: | :---: |
                | Jogos Analisados | {m['jogos_analisados']} | {v['jogos_analisados']} |
                | Média de Gols Marcados | {m['media_gols_marcados']} | {v['media_gols_marcados']} |
                | Média de Gols Sofridos | {m['media_gols_sofridos']} | {v['media_gols_sofridos']} |
                | Ambas as Equipes Marcam | {m['porcentagem_ambas_marcam']}% | {v['porcentagem_ambas_marcam']}% |
                | Mercado: Mais de 1.5 Gols | {m['porcentagem_over_1_5']}% | {v['porcentagem_over_1_5']}% |
                | Mercado: Mais de 2.5 Gols | {m['porcentagem_over_2_5']}% | {v['porcentagem_over_2_5']}% |
                """)
                
            else:
                st.error("Dados históricos insuficientes na ESPN para gerar o cruzamento de dados desta partida.")
        except Exception as e:
            st.error(f"Erro ao conectar com a rota de análise: {e}")




            forcando atualizacao 