import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from coletor_espn import ColetorESPN
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Ultra Analytics Engine API")
coletor = ColetorESPN()

class RequisicaoAnalise(BaseModel):
    liga: str
    id_time: str # Aceita como string no payload

@app.get("/")
def home():
    return {"status": "Backend online e operando"}

@app.post("/analisar")
def analisar_time(dados: RequisicaoAnalise):
    try:
        # Passa os dados tratados para o coletor
        ids_jogos = coletor.obter_ultimos_jogos_id(dados.liga, dados.id_time)
        
        # Se retornar vazio, enviamos uma mensagem clara em vez de quebrar tudo
        return {
            "sucesso": True,
            "quantidade_jogos_localizados": len(ids_jogos),
            "lista_ids": ids_jogos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no motor: {str(e)}")