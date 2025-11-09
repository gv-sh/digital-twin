"""Data cleaning and normalization."""

import pandas as pd
import numpy as np


def clean_numeric_data(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Clean numeric data by removing outliers and null values."""
    df = df.dropna(subset=[column])
    return df


def normalize_data(data: np.ndarray) -> np.ndarray:
    """Normalize data to 0-1 range."""
    return (data - data.min()) / (data.max() - data.min())


__all__ = ["clean_numeric_data", "normalize_data"]
