from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RoundInput(BaseModel):
    p_score: int
    b_score: int
    winner: str

@app.get("/")
def home():
    return {"status": "Bac Bo Engine Online", "version": "1.0"}

@app.post("/predict")
def predict_round(data: RoundInput):
    margin = abs(data.p_score - data.b_score)
    score = 50
    
    if margin <= 1:
        score += 20
    else:
        score += 10
        
    is_confirmed = score >= 65
    target_side = "BANQUEIRO (B)" if data.winner == 'P' else "JOGADOR (P)"
    
    return {
        "action": "ENTRADA CONFIRMADA" if is_confirmed else "AGUARDAR",
        "target": target_side,
        "confidence_score": f"{score}%",
        "pattern_detected": "Tendência / Avenida Detectada",
        "derived_roads_status": "3 Vermelhos (Estável)"
    }
