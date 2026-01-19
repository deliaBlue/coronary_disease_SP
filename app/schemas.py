"""ADD DOCSTRING."""

from pydantic import BaseModel, Field, ConfigDict


class PredictRequest(BaseModel):
    """ADD DOCSTRING."""

    sex: int = Field(
        ...,
        ge=0,
        le=1,
        title="Gender",
        description="Subject's gender. Set 0 for female, and 1 for male.",
    )
    age: int = Field(
        ...,
        ge=0,
        le=120,
        title="Age",
        description="Subject's age. Age can range from 0 to up 120 years.",
    )
    education_level: int = Field(
        ...,
        ge=0,
        le=4,
        title="Education Level",
        description=(
            "Subject's level of formal education. "
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
            "Subject's total cholesterol level in mg/dL. "
            "Its values range from 0 up to 1000 (both exclusive)."
        ),
    )
    systolic_bp: float = Field(
        ...,
        ge=50,
        le=300,
        title="Systolic Blood Pressure",
        description=(
            "Subject's systolic blood pressure. "
            "Its values range from 50 (inclusive) up to 300 (exclusive)."
        ),
    )
    diastolic_bp: float = Field(
        ...,
        ge=30,
        le=200,
        title="Diastolic Blood Pressure",
        description=(
            "Subject's diastolic blood pressure. "
            "Its values range from 30 (inclusive) up to 200 (exclusive)."
        ),
    )
    bmi: float = Field(
        ...,
        ge=5,
        le=200,
        title="Body Mass Index (BMI)",
        description=(
            "Subject's body mass index. "
            "It can range from 5 up to 200 (inclusive)."
        ),
    )
    heart_rate: int = Field(
        ...,
        ge=30,
        le=250,
        title="Heart Rate",
        description=(
            "Subject's heart rate in beats per minute. "
            "It can range from 30 up to 240 (inclusive)."
        ),
    )
    glucose: float = Field(
        ...,
        ge=20,
        le=700,
        title="Blood Glucose Level",
        description=(
            "Subject's blood glucose level in mg/dL. "
            "It can range from 20 (inclusive) up to 700 (exclusive)."
        ),
    )

    model_config = ConfigDict(extra="forbid")


class PredictResponse(BaseModel):
    """ADD DOCSTRING."""
    prediction: int
    probability: float
    threshold: float
    model_version: str
    roc_auc: float
