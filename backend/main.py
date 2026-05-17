from fastapi import FastAPI

app = FastAPI(title="Ultra Analytics Engine API")

@app.get("/")
def home():
    return {"status": "Backend online e operando"}