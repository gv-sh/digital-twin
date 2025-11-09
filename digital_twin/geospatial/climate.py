"""Regional climate data."""


def get_regional_climate(region: str) -> dict:
    """Get climate data for a region."""
    return {"avg_temp": 25.0, "avg_humidity": 60, "rainfall_mm": 1000}


__all__ = ["get_regional_climate"]
