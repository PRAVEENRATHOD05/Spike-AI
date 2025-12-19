from app.agents.ga4_validator import validate_plan, GA4ValidationError
from app.llm.lite_llm import infer_ga4_plan
from app.analytics.ga4_agent import run_ga4_report


def normalize_dates(start_date: str, end_date: str):
    text = f"{start_date} {end_date}".lower()
    if "14" in text:
        return "14daysAgo", "today"
    if "30" in text:
        return "30daysAgo", "today"
    if "7" in text:
        return "7daysAgo", "today"
    return "7daysAgo", "today"


def run_ga4(query: str, property_id: str):
    # 1. Infer plan
    plan = infer_ga4_plan(query)

    # 2. Validate against allowlist
    try:
        validated = validate_plan(plan)
    except GA4ValidationError as e:
        return {
            "agent": "ga4",
            "response": {
                "type": "error",
                "message": str(e)
            }
        }

    metrics = validated["metrics"]
    dimensions = validated["dimensions"]

    # 3. Normalize dates
    start_date, end_date = normalize_dates(
        plan.get("start_date", ""),
        plan.get("end_date", "")
    )

    # 4. Execute GA4
    rows = run_ga4_report(
        property_id=property_id,
        metrics=metrics,
        dimensions=dimensions,
        start_date=start_date,
        end_date=end_date
    )

    # 5. Empty / low traffic handling
    if not rows:
        return {
            "agent": "ga4",
            "response": {
                "type": "empty",
                "message": "No data available for the selected period."
            }
        }

    # 6. Success
    return {
        "agent": "ga4",
        "response": {
            "type": "table",
            "row_count": len(rows),
            "data": rows
        }
    }
