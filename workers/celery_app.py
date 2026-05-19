import os
import ssl
from celery import Celery

# Puxa a URL com 'rediss://' configurada no Render através do grupo Config
REDIS_URL = os.getenv("REDIS_URL")

# Inicializa o Celery apontando para o Redis APENAS como Broker (Fila)
celery_app = Celery(
    "ultra_analytics_engine",
    broker=REDIS_URL,
    include=["backend.coletor_espn"]  # Garante que o Celery encontre suas tarefas da ESPN
)

# Configurações de segurança para o canal de mensagens funcionar na nuvem
celery_app.conf.update(
    # BLOQUEIO CRÍTICO: Força o Celery a NUNCA usar um backend de resultados,
    # matando o comportamento oculto que gerava o erro de reconexão.
    result_backend=None,
    task_ignore_result=True,
    task_store_errors_even_if_ignored=False,
    
    # Ativa o SSL para o envio de mensagens (Fila) desativando validação estrita
    broker_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    
    # Configurações padrão de fuso horário
    timezone="America/Sao_Paulo",
    enable_utc=True
)

@celery_app.task
def check_worker_status():
    return "Worker de fila operando perfeitamente no Render!"