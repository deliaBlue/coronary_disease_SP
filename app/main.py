"""FastAPI application for coronary heart disease risk inference.

This module defines a small web service that:
    - Loads a trained model pipeline and its metadata once at application
      startup
    - Serves a simple HTML landing page rendered via Jinja2 templates
    - Exposes health and prediction endpoints for operational monitoring and
      programmatic inference

Routes:
    - `GET /`: Renders `templates/index.html` (static assets served from
      `/static`)
    - `GET /healthz`: Returns a lightweight readiness payload indicating
      whether the model bundle is loaded and which model version is active
    - `POST /predict`: Accepts a `PredictRequest` class, constructs
      a 1-row pandas DataFrame in the raw feature order specified by model
      metadata, and returns a `PredictResponse` class containing:
        * probability for the positive class
        * binary prediction using the configured threshold (default 0.5)
        * model's ROC-AUC and version from metadata
"""
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
