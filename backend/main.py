import os
from fastapi import FastAPI
from celery import Celery

app = FastAPI(title="Ultra Analytics Engine API")

# Conecta ao Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_client = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

# Aceita tanto GET quanto HEAD na rota raiz para testes do servidor
@app.get("/")
@app.head("/")
def home():
    return {"status": "Backend online", "engine": "FastAPI + Celery"}

# ROTA UNIVERSAL COM QUERY PARAMETERS (Para receber o clique do Streamlit)
@app.post("/coletar")
def disparar_coleta(liga: str, id_time: str):
    """ Rota que recebe os parâmetros limpos e joga na fila do Celery """
    celery_client.send_task("tarefa_coleta_espn", args=[liga, id_time])
    return {"status": "Sucesso", "mensagem": f"Coleta agendada para a liga {liga} e time {id_time}"}