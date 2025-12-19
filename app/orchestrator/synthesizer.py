def synthesize_response(results: dict):
    """
    Combines GA4 + SEO outputs into business insight
    """

    insights = []
    recommendations = []

    ga4 = results.get("ga4")
    seo = results.get("seo")

    # --- GA4 Insight ---
    if ga4:
        rows = ga4.get("row_count", 0)
        insights.append(f"GA4 returned {rows} rows of analytics data.")

        if rows == 0:
            recommendations.append(
                "Verify GA4 date range and tracking implementation."
            )

    # --- SEO Insight ---
    if seo:
        insights.append("SEO audit data detected potential site issues.")
        recommendations.append(
            "Fix critical SEO issues and re-run crawl."
        )

    # --- Fusion Insight ---
    if ga4 and seo:
        insights.append(
            "Traffic behavior and SEO health together indicate organic performance impact."
        )
        recommendations.append(
            "Monitor GA4 metrics after SEO fixes."
        )

    return {
        "summary": " ".join(insights),
        "recommendations": recommendations or ["No action required."]
    }
