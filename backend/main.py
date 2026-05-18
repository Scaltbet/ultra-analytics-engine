import os  # Corrigido o 'import' com letra minúscula
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from celery import Celery

app = FastAPI(title="Ultra Analytics Engine API")

# Permite que o Streamlit acesse o Backend sem bloqueios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão Redis usando a variável de ambiente do Render
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Ajustado o nome para "ultra_analytics_engine" para bater com o Worker
celery_client = Celery("ultra_analytics_engine", broker=REDIS_URL, backend=REDIS_URL)

# Ajuste cirúrgico de SSL para evitar rejeições e timeouts com o Redis seguro
celery_client.conf.update(
    broker_use_ssl={"ssl_cert_reqs": "none"},
    redis_backend_use_ssl={"ssl_cert_reqs": "none"}
)

class SolicitacaoColeta(BaseModel):
    liga: str
    id_time: str

@app.get("/")
def home():
    return {"status": "Backend online e operando"}

# Rota principal de disparo ajustada com o caminho real da task
@app.post("/disparar-coleta")
def disparar_coleta(dados: SolicitacaoColeta):
    tarefa = celery_client.send_task(
        "backend.coletor_espn.tarefa_coleta_espn",  # Caminho mapeado pelo Celery
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