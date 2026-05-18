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

# Configurações auditadas de segurança para aceitar o 'rediss://' do Render
celery_app.conf.update(
    # Ativa o SSL para o envio de mensagens (Fila/Broker) desativando validação estrita
    broker_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    
    # CORREÇÃO CRÍTICA: Passa as opções de TLS para o Backend e resolve o connect_check_health
    redis_backend_transport_options={
        "ssl_cert_reqs": ssl.CERT_NONE,
        "ssl_check_hostname": False
    },
    
    # Configurações de fuso horário do projeto
    timezone="America/Sao_Paulo",
    enable_utc=True
)

# Apenas para testes rápidos se necessário
@celery_app.task
def check_worker_status():
    return "Worker está online e operando com SSL no Render!"