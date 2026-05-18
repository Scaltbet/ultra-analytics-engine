import os
from fastapi import FastAPI
from celery import Celery

app = FastAPI(title="Ultra Analytics Engine API")

# Define a URL de conexão de forma direta e segura
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Inicialização limpa do cliente do Celery
celery_client = Celery()
celery_client.conf.update(
    broker_url=REDIS_URL,
    result_backend=REDIS_URL
)

@app.get("/")
def home():
    return {"status": "Backend online", "engine": "FastAPI + Celery"}

@app.post("/coletar/soccer/liga/{liga}/{id_time}")
def disparar_coleta(liga: str, id_time: str):
    """ Envia a tarefa de raspagem para o Worker processar em segundo plano """
    try:
        celery_client.send_task("tarefa_coleta_espn", args=[liga, id_time])
        return {"status": "Sucesso", "mensagem": f"Coleta agendada na fila Redis para {liga} e time {id_time}"}
    except Exception as e:
        return {"status": "Erro", "detalhes": str(e)}