import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from coletor_espn import ColetorESPN
from celery import Celery
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (.env)
load_dotenv()

app = FastAPI(title="Ultra Analytics Engine API")
coletor = ColetorESPN()

# Puxa a URL do Redis mapeada no Render
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Configuração estável do Celery recomendada para o seu plano
celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=None  # Desativado explicitamente para evitar bypass e overhead no Redis
)

# Validador de dados recebidos do Streamlit
class RequisicaoAnalise(BaseModel):
    liga: str       # Ex: "soccer/bra.1"
    id_time: str    # Ex: "2026"

@app.get("/")
def home():
    return {"status": "Backend online e operando"}

@app.post("/analisar")
def analisar_time(dados: RequisicaoAnalise):
    try:
        ids_jogos = coletor.obter_ultimos_jogos_id(dados.liga, dados.id_time)
        if not ids_jogos:
            raise HTTPException(status_code=404, detail="Nenhum histórico encontrado para os parâmetros informados.")
            
        return {
            "sucesso": True,
            "quantidade_jogos_localizados": len(ids_jogos),
            "lista_ids": ids_jogos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no motor: {str(e)}")