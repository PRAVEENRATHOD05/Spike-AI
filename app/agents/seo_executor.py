def is_seo_query(query: str) -> bool:
    seo_keywords = [
        "seo", "crawl", "audit", "screaming frog",
        "pagespeed", "psi", "wcag", "violation"
    ]
    return any(k in query.lower() for k in seo_keywords)


def run_seo(query):
    return {
        "agent": "seo",
        "response": {
            "message": "SEO intent detected but no matching rule implemented"
        }
    }
