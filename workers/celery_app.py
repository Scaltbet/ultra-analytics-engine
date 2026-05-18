import os
from celery import Celery

# Puxa a URL com 'rediss://' configurada no Render
REDIS_URL = os.getenv("REDIS_URL")

# Inicializa o Celery apontando para o Redis como Broker e Backend
celery_app = Celery(
    "ultra_analytics_engine",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["backend.coletor_espn"]  # Garante que o Celery encontre suas tarefas da ESPN
)

# Configurações de segurança para aceitar o 'rediss://' do Render sem quebrar
celery_app.conf.update(
    broker_use_ssl={"ssl_cert_reqs": "none"},
    redis_backend_use_ssl={"ssl_cert_reqs": "none"},
    timezone="America/Sao_Paulo",
    enable_utc=True
)

# Apenas para testes rápidos se necessário
@celery_app.task
def check_worker_status():
    return "Worker está online e operando com SSL!"