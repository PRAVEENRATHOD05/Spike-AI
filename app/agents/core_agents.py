from app.llm.lite_llm import infer_ga4_plan
from app.analytics.ga4_agent import run_ga4_report
from app.analytics.ga4_schema import ALLOWED_METRICS, ALLOWED_DIMENSIONS
from app.seo.seo_agent import handle_seo_query


def normalize_dates(start_date: str, end_date: str):
    text = f"{start_date} {end_date}".lower()

    if "14" in text:
        return "14daysAgo", "today"
    if "30" in text:
        return "30daysAgo", "today"
    if "7" in text:
        return "7daysAgo", "today"

    return "7daysAgo", "today"


def is_seo_query(query: str) -> bool:
    seo_keywords = [
        "seo", "https", "http", "status", "crawl",
        "accessibility", "wcag", "violation", "violations",
        "psi", "performance", "pagespeed",
        "screaming frog", "audit"
    ]

    q = query.lower()
    return any(k in q for k in seo_keywords)




def handle_query(property_id: str | None, query: str, credentials_path: str):
    # ---------- Tier 2 : SEO ----------

    if not property_id:
        return {
        "error": "propertyId is required for GA4 queries",
        "hint": "SEO queries do not require propertyId"
    }



    plan = infer_ga4_plan(query)

    metrics = [
        ALLOWED_METRICS[m.lower()]
        for m in plan.get("metrics", [])
        if m.lower() in ALLOWED_METRICS
    ] or ["activeUsers"]

    dimensions = [
        ALLOWED_DIMENSIONS[d.lower()]
        for d in plan.get("dimensions", [])
        if d.lower() in ALLOWED_DIMENSIONS
    ]

    start_date, end_date = normalize_dates(
        plan.get("start_date", ""),
        plan.get("end_date", "")
    )

    rows = run_ga4_report(
        property_id=property_id,
        credentials_path=credentials_path,
        metrics=metrics,
        dimensions=dimensions,
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "agent": "ga4",
        "interpreted_plan": {
            "metrics": metrics,
            "dimensions": dimensions,
            "start_date": start_date,
            "end_date": end_date,
        },
        "row_count": len(rows),
        "data": rows,
    }
