"""CSV/Excel/database loading utilities."""

import pandas as pd
from typing import Optional


def load_csv(file_path: str) -> pd.DataFrame:
    """Load data from CSV file."""
    return pd.read_csv(file_path)


def load_excel(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """Load data from Excel file."""
    return pd.read_excel(file_path, sheet_name=sheet_name)


__all__ = ["load_csv", "load_excel"]
