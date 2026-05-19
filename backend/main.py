import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from coletor_espn import ColetorESPN
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Ultra Analytics Engine API")
coletor = ColetorESPN()

# Modelo de entrada inteligente: aceita qualquer tipo comum e trata internamente
class RequisicaoAnalise(BaseModel):
    liga: str = Field(..., description="Slug da liga na ESPN")
    id_time: str = Field(..., description="ID do clube")

@app.get("/")
def home():
    return {"status": "Backend online e operando"}

@app.post("/analisar")
def analisar_time(dados: RequisicaoAnalise):
    try:
        # Extração forçando conversão segura para string limpa
        liga_limpa = str(dados.liga).strip()
        id_limpo = str(dados.id_time).strip()
        
        print(f"[API] Processando parâmetros -> Liga: '{liga_limpa}' | ID: '{id_limpo}'")
        
        ids_jogos = coletor.obter_ultimos_jogos_id(liga_limpa, id_limpo)
        
        if not ids_jogos:
            raise HTTPException(status_code=404, detail="Nenhum registro retornado.")
            
        return {
            "sucesso": True,
            "quantidade_jogos_localizados": len(ids_jogos),
            "lista_ids": ids_jogos
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"[API] Falha inesperada: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")