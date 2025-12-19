# app/agents/ga4_validator.py

from app.agents.ga4_allowlist import ALLOWED_METRICS, ALLOWED_DIMENSIONS

class GA4ValidationError(Exception):
    pass

def validate_plan(plan: dict):
    metrics = plan.get("metrics", [])
    dimensions = plan.get("dimensions", [])

    validated_metrics = []
    validated_dimensions = []

    for m in metrics:
        key = m.lower()
        if key in ALLOWED_METRICS:
            validated_metrics.append(ALLOWED_METRICS[key])

    for d in dimensions:
        key = d.lower()
        if key in ALLOWED_DIMENSIONS:
            validated_dimensions.append(ALLOWED_DIMENSIONS[key])

    if not validated_metrics:
        raise GA4ValidationError("No valid GA4 metrics inferred")

    return {
        "metrics": validated_metrics,
        "dimensions": validated_dimensions
    }
