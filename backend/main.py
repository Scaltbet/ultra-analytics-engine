import os
from fastapi import FastAPI
from pydantic import BaseModel
from celery import Celery

app = FastAPI(title="Ultra Analytics Engine API")

# Conexão Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_client = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

# Modelo para validar os dados que vêm do Streamlit
class SolicitacaoColeta(BaseModel):
    liga: str
    id_time: str

@app.get("/")
def home():
    return {"status": "Backend online e operando"}

# Mudamos para garantir que aceita POST e recebe o corpo correto
@app.post("/disparar-coleta")
def disparar_coleta(dados: SolicitacaoColeta):
    # Envia os parâmetros reais para o Worker rodar em segundo plano
    tarefa = celery_client.send_task(
        "tarefa_coleta_espn", 
        args=[dados.liga, dados.id_time]
    )
    return {
        "status": "Engenharia de coleta iniciada com sucesso!",
        "task_id": tarefa.id
    }