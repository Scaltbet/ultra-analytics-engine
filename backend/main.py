from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
import redis
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

app = FastAPI(title="Ultra Analytics Engine - Secure Core")

# ==========================================
# SEGURANÇA E CRIPTOGRAFIA (ETAPA 16)
# ==========================================
# Configurações de Token (Usa chave padrão caso não exista no Environment)
SECRET_KEY = os.getenv("SECRET_KEY", "7963d3fb12a02b1f81d86d5e71c9fa0f4e3c84b126d40ad52f89f")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verificar_senha(senha_pura, senha_criptografada):
    return pwd_context.verify(senha_pura, senha_criptografada)

def obter_hash_senha(senha):
    return pwd_context.hash(senha)

def criar_token_acesso(dados: dict):
    dados_copia = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_copia.update({"exp": expiracao})
    return jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ==========================================
DATABASE_URL = os.getenv("DATABASE_URL")
engine = None
SessionLocal = None

if DATABASE_URL:
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception:
        pass

def get_db():
    db = SessionLocal() if SessionLocal else None
    if db is None: return
    try: yield db
    finally: db.close()

# ==========================================
# CONFIGURAÇÃO DO CACHE REDIS
# ==========================================
REDIS_URL = os.getenv("REDIS_URL")
redis_client = None

if REDIS_URL:
    try: redis_client = redis.Redis.from_url(REDIS_URL, socket_timeout=3.0, decode_responses=True)
    except Exception: pass

# ==========================================
# ROTAS DE AUTENTICAÇÃO AND SECURE ENDPOINTS
# ==========================================
@app.post("/token")
def login_gerar_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Rota de login simulação de validação. 
    Para homologação do MVP, aceita o usuário mestre de desenvolvimento.
    """
    usuario_mestre = "admin@ultra.com"
    senha_mestre_hash = obter_hash_senha("ultra123") # Senha encriptada via bcrypt
    
    if form_data.username != usuario_mestre or not verificar_senha(form_data.password, senha_mestre_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_acesso = criar_token_acesso(dados={"sub": form_data.username})
    return {"access_token": token_acesso, "token_type": "bearer"}

@app.get("/")
def home(db: Session = Depends(get_db)):
    db_status = False
    if db:
        try:
            db.execute(text("SELECT 1"))
            db_status = True
        except Exception: pass

    redis_status = False
    if redis_client:
        try: redis_status = redis_client.ping()
        except Exception: pass

    return {
        "status": "online",
        "autenticacao": "JWT Ativa (Bcrypt)",
        "cache_redis_connected": redis_status,
        "database_postgres_connected": db_status
    }

@app.post("/analytics/processar")
def disparar_processamento(dados: dict, background_tasks: BackgroundTasks, token: str = Depends(oauth2_scheme)):
    """
    Rota protegida de alta segurança. Exige o Bearer JWT Token válido no Header 
    HTTP enviado pelo Streamlit para liberar o enfileiramento das BackgroundTasks.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub")
        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    print(f"[SECURE TASK] Processamento disparado pelo operador autenticado: {usuario}")
    background_tasks.add_task(print, f"[BACKGROUND] Processando: {dados}")
    return {"status": "enfileirado", "operador": usuario}
