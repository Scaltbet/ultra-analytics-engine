import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from celery import Celery

app = FastAPI(title="Ultra Analytics Engine API")

# Permite que o Streamlit acesse o Backend sem bloqueios de segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_client = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

class SolicitacaoColeta(BaseModel):
    liga: str
    id_time: str

@app.get("/")
def home():
    return {"status": "Backend online e operando"}

# Configurado sem a barra para alinhar com o Streamlit
@app.post("/disparar-coleta")
def disparar_coleta(dados: SolicitacaoColeta):
    tarefa = celery_client.send_task(
        "tarefa_coleta_espn", 
        args=[dados.liga, dados.id_time]
    )
    return {
        "status": "Engenharia de coleta iniciada com sucesso!",
        "task_id": tarefa.id
    }

@app.get("/status-coleta/{task_id}")
def obter_status(task_id: str):
    resultado = celery_client.AsyncResult(task_id)
    return {
        "id": task_id,
        "status": resultado.status,
        "resultado": resultado.result if resultado.ready() else None
    }