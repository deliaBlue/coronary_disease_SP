"""Pydantic schemas for the coronary heart disease prediction API.

This module defines the request and response models used by the FastAPI
service.

The models provide:
    - input validation (types and numeric bounds) for inference requests
    - OpenAPI/Swagger documentation via field titles and descriptions
    - strict payload control (extra fields are forbidden) to keep the API
      contract stable and predictable

Models:
    - `PredictRequest`: validated feature payload for inference
    - `PredictResponse`: structured prediction output returned by the
      `/predict` endpoint
"""

from pydantic import BaseModel, Field, ConfigDict


class PredictRequest(BaseModel):
    """Input payload for coronary heart disease risk prediction.

    Contains the patient's demographic, behavioral, and clinical measurements
    required by the model pipeline. Each field enforces basic domain constraints
    (e.g., non-negative values and plausible physiological ranges). Additional,
    unspecified fields are rejected (`extra='forbid'`) to prevent silent schema
    drift and to ensure the model receives only expected inputs.
    """
    sex: int = Field(
        ...,
        ge=0,
        le=1,
        title="Gender",
        description="Patient's gender. Set 0 for female, and 1 for male.",
    )
    age: int = Field(
        ...,
        ge=0,
        le=120,
        title="Age",
        description="Patient's age. Age can range from 0 to up 120 years.",
    )
    education_level: int = Field(
        ...,
        ge=0,
        le=4,
        title="Education Level",
        description=(
            "Patient's level of formal education. "
            "It can range from 0 up to 4 (both inclusive)."
        ),
    )
    current_smoker: int = Field(
        ...,
        ge=0,
        le=1,
        title="Current Smoker",
        description="Whether the subject is a current smoker (1) or not (0).",
    )
    cigs_per_day: int = Field(
        ...,
        ge=0,
        title="Cigarrets per Day",
        description="Amount of cigarrets the subject smokes a day.",
    )
    bp_meds: int = Field(
        ...,
        ge=0,
        le=1,
        title="Blood Pressure Medication",
        description=(
            "Whether the subject takes blood pressure medication (1) "
            "or not (0)."
        ),
    )
    prevalent_stroke: int = Field(
        ...,
        ge=0,
        le=1,
        title="Stroke History",
        description=(
            "Whether the subject has had a previous stroke (1) " "or not (0)."
        ),
    )
    prevalent_hypertension: int = Field(
        ...,
        ge=0,
        le=1,
        title="Hypertension",
        description="Whether the subject has hypertension (1) or not (0).",
    )
    diabetes: int = Field(
        ...,
        ge=0,
        le=1,
        title="Diabetes",
        description="Whether the subject has diabetes (1) or not (0).",
    )
    total_cholesterol: float = Field(
        ...,
        gt=0,
        le=1000,
        title="Total Cholesterol Level",
        description=(
            "Patient's total cholesterol level in mg/dL. "
            "Its values range from 0 up to 1000 (both exclusive)."
        ),
    )
    systolic_bp: float = Field(
        ...,
        ge=50,
        le=300,
        title="Systolic Blood Pressure",
        description=(
            "Patient's systolic blood pressure. "
            "Its values range from 50 (inclusive) up to 300 (exclusive)."
        ),
    )
    diastolic_bp: float = Field(
        ...,
        ge=30,
        le=200,
        title="Diastolic Blood Pressure",
        description=(
            "Patient's diastolic blood pressure. "
            "Its values range from 30 (inclusive) up to 200 (exclusive)."
        ),
    )
    bmi: float = Field(
        ...,
        ge=5,
        le=200,
        title="Body Mass Index (BMI)",
        description=(
            "Patient's body mass index. "
            "It can range from 5 up to 200 (inclusive)."
        ),
    )
    heart_rate: int = Field(
        ...,
        ge=30,
        le=250,
        title="Heart Rate",
        description=(
            "Patient's heart rate in beats per minute. "
            "It can range from 30 up to 240 (inclusive)."
        ),
    )
    glucose: float = Field(
        ...,
        ge=20,
        le=700,
        title="Blood Glucose Level",
        description=(
            "Patient's blood glucose level in mg/dL. "
            "It can range from 20 (inclusive) up to 700 (exclusive)."
        ),
    )

    model_config = ConfigDict(extra="forbid")


class PredictResponse(BaseModel):
    """Output payload returned by the prediction endpoint.

    Attributes:
        prediction: Binary class label produced by applying `threshold` to
            `probability`
        probability: Model-estimated probability of the positive class
        threshold: Decision threshold used to convert probability to the
            discrete `prediction`
        model_version: Version identifier propagated from model metadata
        roc_auc: ROC-AUC score reported in model metadata.
    """
    prediction: int
    probability: float
    threshold: float
    model_version: str
    roc_auc: float
