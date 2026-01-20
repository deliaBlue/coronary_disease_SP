from fastapi.testclient import TestClient
from app.main import app

def test_predict():
    payload = {
        "sex": 1,
        "age": 55,
        "education_level": 2,
        "current_smoker": 1,
        "cigs_per_day": 10,
        "bp_meds": 0,
        "prevalent_stroke": 0,
        "prevalent_hypertension": 1,
        "diabetes": 0,
        "total_cholesterol": 220,
        "systolic_bp": 135,
        "diastolic_bp": 85,
        "bmi": 26.5,
        "heart_rate": 72,
        "glucose": 90
    }

    with TestClient(app) as client:
        r = client.post("/predict", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert 0.0 <= data["probability"] <= 1.0
        assert data["prediction"] in (0, 1)
