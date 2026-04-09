"""
FastAPI bridge for the React frontend.
Uses the same local model pipeline as Streamlit.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from model_loader import get_model_and_tokenizer, model_loader
from inference import create_inference_engine
from utils import format_explanation, format_risk_level, validate_clause


app = FastAPI(title="Legal Clause Simplifier API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimplifyRequest(BaseModel):
    clause: str = Field(..., min_length=10, max_length=5000)


class SimplifyResponse(BaseModel):
    risk: str
    explanation: str


_inference_engine = None


def get_inference_engine():
    global _inference_engine
    if _inference_engine is None:
        model, tokenizer = get_model_and_tokenizer("./model")
        _inference_engine = create_inference_engine(model, tokenizer, model_loader.device)
    return _inference_engine


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return JSONResponse(
        {
            "message": "Legal Clause Simplifier API is running",
            "health": "/health",
            "simplify": "/simplify",
        }
    )


@app.get("/favicon.ico")
def favicon():
    # Avoid noisy 404 logs from browser favicon probes.
    return Response(status_code=204)


@app.post("/simplify", response_model=SimplifyResponse)
def simplify(req: SimplifyRequest):
    is_valid, msg = validate_clause(req.clause)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg or "Invalid clause input")

    try:
        engine = get_inference_engine()
        result = engine.simplify_clause(req.clause)
        return SimplifyResponse(
            risk=format_risk_level(result["risk"]),
            explanation=format_explanation(result["explanation"]),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
