if redis_client:
        try:
            redis_status = redis_client.ping()
        except Exception:
            redis_status = False

    return {
        "status": "online",
        "engine": "FastAPI Core Engine",
        "security": "JWT Protected Endpoint Enabled",
        "cache_redis_connected": redis_status
    }

@app.post("/analytics/processar")
def disparar_processamento(dados: dict, background_tasks: BackgroundTasks, usuario_autenticado: dict = Depends(obter_usuario_atual)):
    """
    Endpoint protegido. Apenas requisições que enviem o Token JWT correto no Header
    podem disparar tarefas de processamento esportivo em segundo plano.
    """
    print(f"[BACKGROUND] Executando rotina iniciada por {usuario_autenticado['username']}")
    return {"status": "enfileirado", "solicitante": usuario_autenticado["username"]}
