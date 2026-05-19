from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from coletor_espn import ColetorESPN

app = FastAPI(title="Ultra Analytics Engine API")
coletor = ColetorESPN()

# Modelo de validação estrita para evitar erros de formato de payload
class RequisicaoAnalise(BaseModel):
    liga: str  # Ex: "soccer/bra.1"
    id_time: str # Ex: "2026" (ID do time na ESPN)

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
        raise HTTPException(status_code=500, detail=f"Erro interno no processamento do motor: {str(e)}")