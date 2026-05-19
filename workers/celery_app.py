import os
import ssl
from celery import Celery

# Puxa a URL com 'rediss://' configurada no Render através do grupo Config
REDIS_URL = os.getenv("REDIS_URL")

# Inicializa o Celery apontando para o Redis APENAS como Broker (Fila)
# O parâmetro 'backend=None' remove a necessidade de checagem SSL complexa que quebrava o app
celery_app = Celery(
    "ultra_analytics_engine",
    broker=REDIS_URL,
    backend=None,
    include=["backend.coletor_espn"]  # Garante que o Celery encontre suas tarefas da ESPN
)

# Configurações estritas de segurança para o Broker funcionar na nuvem
celery_app.conf.update(
    # Ativa o SSL para o envio de mensagens (Fila) desativando validação de hostname
    broker_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    
    # Ignora os resultados das tarefas (evita que o Celery tente criar tabelas de status no Redis)
    task_ignore_result=True,
    task_store_errors_even_if_ignored=False,
    
    # Configurações padrão de fuso horário
    timezone="America/Sao_Paulo",
    enable_utc=True
)

@celery_app.task
def check_worker_status():
    return "Worker de fila operando perfeitamente no Render!"