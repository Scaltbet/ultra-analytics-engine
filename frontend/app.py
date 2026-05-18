elif "SEU-BACKEND-AQUI" in URL_BACKEND:
            st.error("Configure a URL do Backend no código para usar esta função.")
        else:
            with st.spinner("Consultando status no Redis..."):
                try:
                    # Consulta a rota GET do backend para ver o status da tarefa do Celery
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