import os
import ssl
from celery import Celery

# Puxa a URL com 'rediss://' configurada no Render através do grupo Config
REDIS_URL = os.getenv("REDIS_URL")

# Inicializa o Celery apontando para o Redis APENAS como Broker (Fila)
# O parâmetro backend=None remove totalmente o circuito de conexões problemáticas
celery_app = Celery(
    "ultra_analytics_engine",
    broker=REDIS_URL,
    backend=None,
    include=["backend.coletor_espn"]  # Garante que o Celery encontre suas tarefas da ESPN
)

# Configurações de segurança para o canal de mensagens funcionar na nuvem
celery_app.conf.update(
    # Ativa o SSL para o envio de mensagens (Fila) desativando validação estrita
    broker_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    
    # Ignora os resultados das tarefas para evitar que o Celery tente gravar dados no Redis
    task_ignore_result=True,
    task_store_errors_even_if_ignored=False,
    
    # Configurações padrão de fuso horário
    timezone="America/Sao_Paulo",
    enable_utc=True
)

@celery_app.task
def check_worker_status():
    return "Worker de fila operando perfeitamente no Render!"