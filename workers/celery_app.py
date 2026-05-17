import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# Puxa a URL do Redis das configurações de ambiente do servidor
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery.task
def testar_worker_task():
    return "Worker respondendo perfeitamente!"