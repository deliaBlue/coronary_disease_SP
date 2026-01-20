"""Custom scikit-learn transformer for domain-specific feature engineering.

This module defines `FeatureEngineer`, a lightweight transformer that derives
additional clinical risk features from an input pandas DataFrame for use in a
scikit-learn pipeline.

The transformer is stateless (`fit` returns `self` without learning any new
parameters) and returns a copy of the input pandas DataFrame with the new
feature columns appended.

Generated features:
    - `smoker_intensity`: `current_smoker * cigs_per_day`
    - `pulse_pressure`: `systolic_bp - diastolic_bp`

Requirements:
The input to `transform` must be a pandas DataFrame containing the columns
`current_smoker`, `cigs_per_day`, `systolic_bp`, and `diastolic_bp`.

Notes:
"""
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
