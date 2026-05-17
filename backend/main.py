from fastapi import FastAPI, BackgroundTasks
import os
import redis
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Ultra Analytics Engine - Core")

REDIS_URL = os.getenv("REDIS_URL")
redis_client = None

if REDIS_URL:
    try:
        redis_client = redis.Redis.from_url(REDIS_URL, socket_timeout=3.0, decode_responses=True)
    except Exception:
        redis_client = None

def processar_metricas_esportivas(dados: dict):
    print(f"[BACKGROUND TASK] Processando lote de dados: {dados}")

@app.get("/")
def home():
    redis_status = False
    if redis_client:
        try:
            redis_status = redis_client.ping()
        except Exception:
            redis_status = False

    return {
        "status": "online",
        "engine": "FastAPI Native BackgroundTasks",
        "cache_redis_connected": redis_status,
        "database_configured": "DATABASE_URL" in os.environ
    }

@app.post("/analytics/processar")
def disparar_processamento(dados: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(processar_metricas_esportivas, dados)
    return {"status": "enfileirado", "mensagem": "Processamento iniciado em segundo plano."}
