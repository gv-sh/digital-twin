"""Pydantic request/response models."""

from typing import Dict, List, Optional


class AnalysisRequest:
    """Analysis request schema (simplified)."""

    def __init__(self, scenario_name: str, parameters: Dict):
        self.scenario_name = scenario_name
        self.parameters = parameters


class AnalysisResponse:
    """Analysis response schema (simplified)."""

    def __init__(self, results: Dict, status: str = "success"):
        self.results = results
        self.status = status


__all__ = ["AnalysisRequest", "AnalysisResponse"]
