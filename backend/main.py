import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from coletor_espn import ColetorESPN
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Scalt Bet Pro API")
coletor = ColetorESPN()

class RequisicaoGrade(BaseModel):
    liga: str
    data: Optional[str] = None

class RequisicaoCruzamento(BaseModel):
    liga: str
    id_mandante: str
    id_visitante: str

@app.get("/")
def home():
    return {"status": "Scalt Bet Pro Backend ativo e operando"}

@app.post("/grade")
def obter_grade_jogos(dados: RequisicaoGrade):
    print(f"[API] Solicitando grade para a liga: {dados.liga}")
    jogos = coletor.obter_jogos_do_dia(dados.liga, dados.data)
    if not jogos:
        raise HTTPException(status_code=404, detail="Nenhuma partida localizada.")
    return {"sucesso": True, "jogos": jogos}

@app.post("/analisar")
def analisar_confronto(dados: RequisicaoCruzamento):
    print(f"[API] Cruzando dados avançados: Mandante {dados.id_mandante} vs Visitante {dados.id_visitante}")
    
    stats_mandante = coletor.obter_estatisticas_equipe(dados.liga, dados.id_mandante)
    stats_visitante = coletor.obter_estatisticas_equipe(dados.liga, dados.id_visitante)
    
    if not stats_mandante or not stats_visitante:
        raise HTTPException(status_code=404, detail="Dados históricos insuficientes na ESPN para uma das equipes.")
        
    expectativa_gols = round(stats_mandante["media_gols_marcados"] + stats_visitante["media_gols_sofridos"], 2)
    prob_ambas_marcam = round((stats_mandante["porcentagem_ambas_marcam"] + stats_visitante["porcentagem_ambas_marcam"]) / 2, 1)
    
    return {
        "sucesso": True,
        "mandante": stats_mandante,
        "visitante": stats_visitante,
        "insights_preditivos": {
            "expectativa_gols_confronto": expectativa_gols,
            "probabilidade_ambas_marcam": prob_ambas_marcam
        }
    }