"""ADD DOCSTRING."""
from __future__ import annotations

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Adds:
        - smoker_intensity = current_smoker * cigs_per_day
        - pulse_pressure = systolic_bp - diastolic_bp

    Assumes input is a pandas DataFrame with the required columns present.
    """

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """ADD DOCSTRING."""
        x = X.copy()

        x["smoker_intensity"] = x["current_smoker"] * x["cigs_per_day"]
        x["pulse_pressure"] = x["systolic_bp"] - x["diastolic_bp"]

        return x
