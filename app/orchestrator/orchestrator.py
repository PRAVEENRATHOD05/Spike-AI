from app.agents.ga4_executor import run_ga4
from app.agents.seo_executor import run_seo, is_seo_query


def run_tier3_query(query: str, property_id: str | None):
    results = {}

    # SEO agent
    if is_seo_query(query):
        results["seo"] = run_seo(query)

    # GA4 agent
    if property_id:
        results["ga4"] = run_ga4(
            query=query,
            property_id=property_id
        )

    return results
