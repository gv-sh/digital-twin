"""External API providers for weather and fuel prices."""


def get_weather_data(location: str) -> dict:
    """Get weather data from external API (stub)."""
    return {"temp": 25.0, "humidity": 60}


def get_fuel_prices(region: str) -> dict:
    """Get current fuel prices (stub)."""
    return {"diesel": 1.50, "electricity": 0.25, "hydrogen": 8.00}


__all__ = ["get_weather_data", "get_fuel_prices"]
