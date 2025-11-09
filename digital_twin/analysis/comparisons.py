"""Technology comparison matrices."""


def compare_technologies(technologies: list, metrics: list) -> dict:
    """Compare multiple technologies across metrics."""
    return {
        "technologies": [t.get("name", f"Tech{i}") for i, t in enumerate(technologies)],
        "metrics": metrics,
    }


__all__ = ["compare_technologies"]
