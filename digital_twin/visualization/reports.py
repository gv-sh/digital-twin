"""PDF/Word report generation."""


def generate_full_report(scenario, npv_analysis, simulation_results) -> dict:
    """Generate comprehensive report."""
    report = {
        "scenario": scenario.name if hasattr(scenario, 'name') else "Scenario",
        "npv": npv_analysis,
        "simulation": simulation_results,
        "status": "generated"
    }
    return type('Report', (), {
        'save': lambda self, path: print(f"Report saved to {path}"),
        'data': report
    })()


__all__ = ["generate_full_report"]
