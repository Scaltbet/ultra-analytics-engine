from fastapi import FastAPI, BackgroundTasks, Depends
import os
import redis
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

app = FastAPI(title="Ultra Analytics Engine - V2")

# ==========================================
# CONFIGURAÇÃO CIENTÍFICA DO BANCO DE DADOS (ETAPA 15)
# ==========================================
DATABASE_URL = os.getenv("DATABASE_URL")
engine = None
SessionLocal = None

if DATABASE_URL:
    try:
        # pool_pre_ping=True evita conexões caídas (stale connections) no Supabase
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as e:
        print(f"[DB ERROR] Erro ao inicializar SQLAlchemy: {e}")

# Injeção de Dependência para gerenciar o ciclo de vida das sessões do banco de dados
def get_db():
    db = SessionLocal() if SessionLocal else None
    if db is None:
        return
    try:
        yield db
    finally:
        db.close()

# ==========================================
# CONFIGURAÇÃO DO CACHE REDIS
# ==========================================
REDIS_URL = os.getenv("REDIS_URL")
redis_client = None

if REDIS_URL:
    try:
        redis_client = redis.Redis.from_url(REDIS_URL, socket_timeout=3.0, decode_responses=True)
    except Exception:
        redis_client = None

# ==========================================
# PROCESSAMENTO EM SEGUNDO PLANO (BACKGROUND TASKS)
# ==========================================
def processar_e_salvar_metricas(dados: dict):
    print(f"[BACKGROUND TASK] Executando processamento analítico: {dados}")
    # A lógica de persistência pesada será inserida aqui quando mapearmos as tabelas

# ==========================================
# ENDPOINTS (ROTAS DA API)
# ==========================================
@app.get("/")
def home(db: Session = Depends(get_db)):
    # Teste em tempo real de integridade do PostgreSQL do Supabase
    db_status = False
    if db:
        try:
            db.execute(text("SELECT 1"))
            db_status = True
        except Exception:
            db_status = False

    # Teste de integridade do Redis do Upstash
    redis_status = False
    if redis_client:
        try:
            redis_status = redis_client.ping()
        except Exception:
            redis_status = False

    return {
        "status": "online",
        "engine": "FastAPI + SQLAlchemy Core",
        "cache_redis_connected": redis_status,
        "database_postgres_connected": db_status
    }

@app.post("/analytics/processar")
def disparar_processamento(dados: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(processar_e_salvar_metricas, dados)
    return {"status": "enfileirado", "mensagem": "Processamento assíncrono iniciado."}
