"""Training script for the coronary heart disease prediction model.

This module trains and serializes a scikit-learn pipeline that predicts
10-year coronary heart disease (CHD) risk from demographic, behavioral, and
clinical measurements. It is intended to be run as a standalone program and
produces two artifacts consumed by the FastAPI service:

    - `app/model/model_pipeline.pkl`: a Joblib-serialized sklearn Pipeline
    - `app/model/metadata.json`: JSON metadata describing the model contract,
      feature set, evaluation metrics, and decision threshold

High-level workflow:
    1. Load the raw dataset from `data/coronary_disease.csv`
    2. Normalize column names and encodings (snake_case, binary mappings) and
       drop rows with missing values
    3. Split data into train/test sets prior to fitting scalers to avoid data
       leakage
    4. Build a Pipeline consisting of:
         - feature engineering (`FeatureEngineer`)
         - column-wise scaling / passthrough (`ColumnTransformer`)
         - logistic regression classifier
    5. Evaluate on the held-out test set and persist artifacts

Notes:
    - The API contract is defined by `RAW_FEATS`; only these raw features are
      required at inference time. Engineered features are computed inside the
      Pipeline
    - This script mutates `sys.path` so it can import the application
      preprocessing module when executed from the repository root
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import List, Dict

import joblib
import pandas as pd
import sys

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    roc_auc_score,
    precision_score,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Set paths
ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

from app.preprocessing import FeatureEngineer

MODEL_DIR = ROOT / "app" / "model"
MODEL_METADATA = MODEL_DIR / "metadata.json"
MODEL_PIPELINE = MODEL_DIR / "model_pipeline.pkl"

DATA_PATH = ROOT / "data" / "coronary_disease.csv"

# Create output dir
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Raw feature contract
TARGET = "ten_year_chd"
RAW_FEATS = [
    "sex",
    "age",
    "education_level",
    "current_smoker",
    "cigs_per_day",
    "bp_meds",
    "prevalent_stroke",
    "prevalent_hypertension",
    "diabetes",
    "total_cholesterol",
    "systolic_bp",
    "diastolic_bp",
    "bmi",
    "heart_rate",
    "glucose",
]


# AUXILIARY CLASSES
@dataclass(frozen=True)
class Metadata:
    """Serializable training and model contract metadata.

    This structure is written to `metadata.json` and is intended to be consumed
    by the serving layer for:
        - input feature ordering (raw feature contract)
        - transparency about engineered and modeled features
        - thresholding behavior
        - reporting of offline evaluation metrics

    Attributes:
        version: Version identifier for the model/artifacts (training date)
        target: Name of the target column used during training
        raw_features: Ordered list of raw input features expected by the API
        engineered_features: Names of features created in-pipeline
        model_features_scaled: Feature names scaled via `StandardScaler`.
        model_features_passthrough: Feature names passed through unscaled
        threshold: Decision threshold used for binary classification
        metrics: Evaluation metrics computed on a held-out test set
        notes: Free-text notes describing pipeline behavior
    """
    version: str
    target: str
    raw_features: List[str]
    engineered_features: List[str]
    model_features_scaled: List[str]
    model_features_passthrough: List[str]
    threshold: float
    metrics: Dict[str, float]
    notes: str


# AUXILIARY FUNCTION
def clean_df(in_path: Path) -> pd.DataFrame:
    """Load and normalize the raw coronary disease dataset.

    Performs a minimal set of deterministic transformations to align the dataset
    to the model's input contract:
        - renames columns to match the service schema (snake_case)
        - maps categorical encodings to numeric binaries where needed
        - drops rows containing missing values.

    Args:
        in_path: Path to the CSV dataset.

    Returns:
        A cleaned pandas DataFrame suitable for model training and evaluation
    """
    data = pd.read_csv(in_path)

    # Turn column names to snake_case and lowercase
    rename_map = {
        "sex": "sex",
        "age": "age",
        "education": "education_level",
        "currentSmoker": "current_smoker",
        "cigsPerDay": "cigs_per_day",
        "BPMeds": "bp_meds",
        "prevalentStroke": "prevalent_stroke",
        "prevalentHyp": "prevalent_hypertension",
        "diabetes": "diabetes",
        "totChol": "total_cholesterol",
        "sysBP": "systolic_bp",
        "diaBP": "diastolic_bp",
        "BMI": "bmi",
        "heartRate": "heart_rate",
        "glucose": "glucose",
        "TenYearCHD": "ten_year_chd",
    }
    data = data.rename(columns=rename_map)

    # Turn yes/no male/female variables to binary
    data["sex"] = data["sex"].replace({"F": 0, "M": 1}).astype("Int64")
    data["current_smoker"] = (
        data["current_smoker"].replace({"Yes": 1, "No": 0}).astype("Int64")
    )

    # Set correct data types
    data["bp_meds"] = data["bp_meds"].astype("Int64")

    # Remove NAs
    data = data.dropna().reset_index(drop=True)

    return data


def main():
    """Train, evaluate, and persist the model pipeline and metadata.

    Loads and cleans the dataset, performs a stratified train/test split, fits
    a preprocessing and logistic regression pipeline, evaluates on the test set,
    and writes the resulting artifacts to the ``app/model`` directory.
    """
    data = clean_df(in_path=DATA_PATH)

    X = data[RAW_FEATS].copy()
    y = data[TARGET].copy()

    # Split BEFORE fitting the scaler to avoid data leakage
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # What the model actually consumes:
    # Engineered variables
    engineered = ["smoker_intensity", "pulse_pressure"]
    # Scale continuous numeric variables
    scaled_num = [
        "age",
        "bmi",
        "systolic_bp",
        "diastolic_bp",
        "total_cholesterol",
        "glucose",
        "heart_rate",
        "pulse_pressure",
        "smoker_intensity",
    ]
    # Pass-through (not scaled): binaries + ordinal
    passthrough = [
        "sex",
        "education_level",
        "current_smoker",
        "bp_meds",
        "prevalent_stroke",
        "prevalent_hypertension",
        "diabetes",
    ]

    # Build preprocessing and model pipeline
    preprocess = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), scaled_num),
            ("cat", "passthrough", passthrough),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    model = LogisticRegression(class_weight={0: 1, 1: 10}, max_iter=2000)

    pipeline = Pipeline(
        steps=[
            ("feat", FeatureEngineer()),
            ("prep", preprocess),
            ("model", model),
        ]
    )

    # Scaler is fit only in the X_train through the pipeline
    pipeline.fit(X_train, y_train)

    # Evaluate
    probability = pipeline.predict_proba(X_test)[:, 1]
    predictions = (probability >= 0.5).astype(int)

    metrics = {
        "accuracy": f"{accuracy_score(y_test, predictions):.2f}",
        "recall": f"{recall_score(y_test, predictions):.2f}",
        "precision": f"{precision_score(
                y_test, predictions, zero_division=0
            ):.2f}",
        "F1-score": f"{f1_score(y_test, predictions):.2f}",
        "ROC-AUC": f"{roc_auc_score(y_test, probability):.2f}",
    }

    # Save artifacts
    joblib.dump(pipeline, MODEL_PIPELINE)

    meta_out = Metadata(
        version=str(date.today()),
        target=TARGET,
        raw_features=RAW_FEATS,
        engineered_features=engineered,
        model_features_scaled=scaled_num,
        model_features_passthrough=passthrough,
        threshold=0.5,
        metrics=metrics,
        notes=(
            "API accepts raw_features only. "
            "Pipeline perfroms feat engineering, scaling, and classification."
        ),
    )

    MODEL_METADATA.write_text(
        json.dumps(asdict(meta_out), indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
