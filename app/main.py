"""ADD DOCSTRING."""
from __future__ import annotations

from contextlib import asynccontextmanager
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .artifacts import load_bundle
from .schemas import PredictRequest, PredictResponse

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.bundle = load_bundle()

    yield


app = FastAPI(
    title="Coronary Heart Disease Predictor",
    version="1.0.0",
    lifespan=lifespan
)


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/healthz")
def healthz():
    b = getattr(app.state, "bundle", None)

    return {
        "status": "ok",
        "model_loaded": b is not None,
        "model_version": (b.metadata.get("version") if b else None),
    }


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    b = app.state.bundle
    meta = b.metadata

    # Build a 1-row DF in the exact raw feature order
    raw_features = meta["raw_features"]
    df = pd.DataFrame([req.model_dump()], columns=raw_features)

    proba = float(b.pipeline.predict_proba(df)[0][1])
    threshold = float(meta.get("threshold", 0.5))
    pred = int(proba >= threshold)

    return PredictResponse(
        prediction=pred,
        probability=proba,
        threshold=threshold,
        roc_auc=(meta.get("metrics", {}).get("ROC-AUC")),
        model_version=str(meta.get("version", "unknown")),
    )
