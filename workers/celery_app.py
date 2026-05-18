import os
import ssl
from celery import Celery

# Puxa a URL com 'rediss://' configurada no Render através do grupo Config
REDIS_URL = os.getenv("REDIS_URL")

# Inicializa o Celery apontando para o Redis como Broker e Backend
celery_app = Celery(
    "ultra_analytics_engine",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["backend.coletor_espn"]  # Garante que o Celery encontre suas tarefas da ESPN
)

# Configurações auditadas de segurança para conexões criptografadas no Render
celery_app.conf.update(
    # Garante compatibilidade SSL na transmissão de mensagens do Broker
    broker_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    
    # Resolve o erro de 'auth_response' e 'connect_check_health' no Backend
    redis_backend_transport_options={
        "ssl_cert_reqs": ssl.CERT_NONE,
        "ssl_check_hostname": False
    },
    
    # Configurações padrão de fuso horário
    timezone="America/Sao_Paulo",
    enable_utc=True
)

# Tarefa de monitoramento interna
@celery_app.task
def check_worker_status():
    return "Worker está online e operando com SSL no Render!"