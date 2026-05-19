import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from coletor_espn import ColetorESPN
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Ultra Analytics Engine API")
coletor = ColetorESPN()

# Mantém o Celery configurado corretamente (Sem backend de resultados para não travar o Redis)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=None 
)

# Validador flexível: força tudo a virar string para não dar conflito de formato
class RequisicaoAnalise(BaseModel):
    liga: str
    id_time: str 

@app.get("/")
def home():
    return {"status": "Backend online e operando"}

@app.post("/analisar")
def analisar_time(dados: RequisicaoAnalise):
    try:
        print(f"[API] Analisando -> Liga: {dados.liga} | Time ID: {dados.id_time}")
        ids_jogos = coletor.obter_ultimos_jogos_id(dados.liga, dados.id_time)
        
        if not ids_jogos:
            # Retorna um erro catalogado para o Streamlit entender, em vez de um Erro 500 fatal
            raise HTTPException(status_code=404, detail="Nenhum jogo finalizado encontrado na ESPN para esses dados.")
            
        return {
            "sucesso": True,
            "quantidade_jogos_localizados": len(ids_jogos),
            "lista_ids": ids_jogos
        }
    except HTTPException:
        raise # Permite que o 404 passe ileso
    except Exception as e:
        print(f"[API] Falha no motor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no motor: {str(e)}")