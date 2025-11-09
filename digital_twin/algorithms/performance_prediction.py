"""Real-time performance prediction."""

from digital_twin.physics import calculate_wheel_energy


def predict_performance(vehicle_specs, operational_profile) -> dict:
    """Predict vehicle performance in real-time."""
    energy = calculate_wheel_energy(
        mass=vehicle_specs.mass_kg,
        grade=operational_profile.average_grade_radians,
        distance=operational_profile.daily_km * 1000,
        velocity=operational_profile.average_velocity_kmh / 3.6,
    )
    return {"predicted_energy_joules": energy}


__all__ = ["predict_performance"]
