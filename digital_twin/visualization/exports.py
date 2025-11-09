"""Excel/CSV export utilities."""

import pandas as pd


def export_to_excel(data: dict, filename: str) -> None:
    """Export data to Excel."""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)


def export_to_csv(data: dict, filename: str) -> None:
    """Export data to CSV."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


__all__ = ["export_to_excel", "export_to_csv"]
