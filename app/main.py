from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
from fastapi.middleware.cors import CORSMiddleware
from rag.chatbot import ask_rag
from typing import Optional



# ==========================================
# LOAD TRAINED MODEL
# ==========================================

model = joblib.load("transformer_model.pkl")

# ==========================================
# CREATE FASTAPI INSTANCE
# ==========================================

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ==========================================
# INPUT DATA SCHEMA
# ==========================================

class TransformerInput(BaseModel):
    BDV: float
    Tan_Delta: float
    Insulation_Resistance: float
    Capacitance_Variation: float
    Polarization_Index: float
    DDF: float

class ChatRequest(BaseModel):
    question: str
    status: Optional[str] = None
    inputs: Optional[dict] = None

# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Transformer AI Backend Running"
    }

# ==========================================
# PREDICTION ENDPOINT
# ==========================================

@app.post("/predict")
def predict(data: TransformerInput):

    # Convert frontend data into ML array
    input_data = np.array([[
        data.BDV,
        data.Tan_Delta,
        data.Insulation_Resistance,
        data.Capacitance_Variation,
        data.Polarization_Index,
        data.DDF
    ]])

    # AI prediction
    prediction = model.predict(input_data)[0]

    # Status mapping
    status_map = {
        0: "EXCELLENT",
        1: "GOOD",
        2: "MARGINAL",
        3: "POOR",
        4: "CRITICAL"
    }

    return {
        "prediction": int(prediction),
        "status": status_map[prediction],
        "inputs": {
            "BDV": data.BDV,
            "Tan_Delta": data.Tan_Delta,
            "Insulation_Resistance": data.Insulation_Resistance,
            "Capacitance_Variation": data.Capacitance_Variation,
            "Polarization_Index": data.Polarization_Index,
            "DDF": data.DDF
        }
    }

@app.post("/chat")
def chat(data: ChatRequest):

    answer = ask_rag(
        question=data.question,
        status=data.status,
        inputs=data.inputs
    )

    return {
        "answer": answer
    }