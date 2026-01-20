"""Model bundle loader.

This module provides a small, single-responsibility API for loading a
serialized model pipeline and its accompanying metadata from a local `model/`
directory that lives alongside this source file.

Artifacts:
    - `model/model_pipeline.pkl`: a Joblib-serialized pipeline object
    - `model/metadata.json`: UTF-8 JSON metadata describing the pipeline
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import joblib

ROOT = Path(__file__).resolve().parents[0]
MODEL_DIR = ROOT / "model"

MODEL_PATH = MODEL_DIR / "model_pipeline.pkl"
META_PATH = MODEL_DIR / "metadata.json"


@dataclass(frozen=True)
class Bundle:
    pipeline: Any
    metadata: Dict[str, Any]


def load_bundle() -> Bundle:
    pipeline = joblib.load(MODEL_PATH)
    metadata = json.loads(META_PATH.read_text(encoding="utf-8"))

    return Bundle(pipeline=pipeline, metadata=metadata)
