"""ADD DOCSTRING

"""

from pydantic import BaseModel, Field, ConfigDict


class PredictRequest(BaseModel):
    """
    Input schema for the coronary heart disease prediction model.
    Validation limits are based on realistic clinical values.
    """

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
        description="Subject's age. Must be at least 18.",
    )
    education_level: int = Field(
        ...,
        ge=1,
        le=4,
        title="Education Level",
        description=(
            "Subject's level of formal education. "
            "It can range from 1 up to 4."
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
        le=100,
        title="Cigarettes per Day",
        description="Average number of cigarettes smoked per day (0 if non-smoker).",
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
        ge=100, 
        le=800,
        title="Total Cholesterol Level",
        description=(
            "Subject's total cholesterol level in mg/dL. "
            "Normal range is typically between 100 and 600."
        ),
    )
    systolic_bp: float = Field(
        ...,
        ge=80,   
        le=250,
        title="Systolic Blood Pressure",
        description=(
            "Subject's systolic blood pressure. "
            "Values typically range from 80 to 220."
        ),
    )
    diastolic_bp: float = Field(
        ...,
        ge=40,   
        le=160,
        title="Diastolic Blood Pressure",
        description=(
            "Subject's diastolic blood pressure. "
            "Values typically range from 50 to 140."
        ),
    )
    bmi: float = Field(
        ...,
        ge=10,   
        le=100,
        title="Body Mass Index (BMI)",
        description=(
            "Subject's body mass index. "
            "Values typically range from 15 to 50."
        ),
    )
    heart_rate: int = Field(
        ...,
        ge=30,   
        le=220,
        title="Heart Rate",
        description=(
            "Subject's heart rate in beats per minute. "
            "Values typically range from 40 to 180."
        ),
    )
    glucose: float = Field(
        ...,
        ge=40,   
        le=600,
        title="Blood Glucose Level",
        description=(
            "Subject's blood glucose level in mg/dL. "
            "Values typically range from 50 to 400."
        ),
    )

    model_config = ConfigDict(extra="forbid")


class PredictResponse(BaseModel):
    """
    Output schema containing the prediction and probability.
    """
    prediction: int
    probability: float
    threshold: float
    model_version: str
    roc_auc: float