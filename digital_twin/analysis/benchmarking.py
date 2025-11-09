"""Industry standards and best-in-class comparisons."""


def get_industry_benchmark(category: str) -> dict:
    """Get industry benchmark values."""
    benchmarks = {
        "diesel_efficiency": 0.35,
        "bev_efficiency": 0.85,
        "utilization": 0.75,
    }
    return benchmarks.get(category, {})


__all__ = ["get_industry_benchmark"]
