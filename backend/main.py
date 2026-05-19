import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from coletor_espn import ColetorESPN
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Scalt Bet Pro API")
coletor = ColetorESPN()

# Validador para puxar a rodada do dia
class RequisicaoGrade(BaseModel):
    liga: str
    data: Optional[str] = None # Formato YYYYMMDD opcional

# Validador para o cruzamento avançado (Mandante vs Visitante)
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
        raise HTTPException(status_code=404, detail="Nenhuma partida localizada para esta data ou liga.")
        
    return {"sucesso": True, "jogos": jogos}

@app.post("/analisar")
def analisar_confronto(dados: RequisicaoCruzamento):
    # Rota stub - Próximo passo: integrar as funções de médias históricas (Últimos 20 jogos de cada)
    print(f"[API] Cruzando dados: Mandante {dados.id_mandante} vs Visitante {dados.id_visitante}")
    return {
        "sucesso": True,
        "mensagem": "Motor pronto para cruzar históricos",
        "id_mandante": dados.id_mandante,
        "id_visitante": dados.id_visitante
    }