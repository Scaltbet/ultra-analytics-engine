import os
from fastapi import FastAPI
from celery import Celery

app = FastAPI(title="Ultra Analytics Engine API")

# Conecta ao mesmo Redis do Worker
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_client = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

@app.get("/")
def home():
    return {"status": "Backend online e operando com Celery"}

@app.post("/coletar/soccer/liga/{liga}/{id_time}")
def disparar_coleta(liga: str, id_time: str):
    """ Rota que recebe o clique do Streamlit e cria a tarefa na fila """
    # Envia a tarefa de forma assíncrona usando o nome exato registrado no Worker
    celery_client.send_task("tarefa_coleta_espn", args=[liga, id_time])
    return {"status": "Sucesso", "mensagem": f"Coleta enviada para a fila Upstash para a liga {liga} e time {id_time}"}