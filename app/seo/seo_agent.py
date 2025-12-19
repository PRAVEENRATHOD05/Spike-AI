from app.seo.seo_ingestion import load_seo_dataframe
from app.seo.seo_schema import resolve_columns
from app.seo.seo_utils import (
    non_https_urls,
    group_by_status_code,
    psi_error_pages,
    accessibility_violations_summary,
)


def handle_seo_query(query: str):
    try:
        df = load_seo_dataframe()
        cols = resolve_columns(df)
        q = query.lower()

        # HTTPS CHECK
        if "https" in q:
            if "address" not in cols:
                return {
                    "error": "address column missing",
                    "available_columns": list(df.columns)
                }

            rows = non_https_urls(df, cols["address"])
            return {
                "type": "filter",
                "count": len(rows),
                "rows": rows.to_dict(orient="records")
            }

        # STATUS CODE GROUPING
        if "status" in q and "group" in q:
            if "status_code" not in cols:
                return {
                    "error": "status_code column missing",
                    "available_columns": list(df.columns)
                }

            return {
                "type": "aggregation",
                "groups": group_by_status_code(df, cols["status_code"])
            }

        # PSI ERRORS
        if "psi" in q:
            if "psi_status" not in cols:
                return {
                    "error": "psi_status column missing",
                    "available_columns": list(df.columns)
                }

            rows = psi_error_pages(df, cols["psi_status"])
            return {
                "type": "filter",
                "count": len(rows),
                "rows": rows.to_dict(orient="records")
            }

        # ACCESSIBILITY / WCAG
        if "accessibility" in q or "wcag" in q or "violation" in q:
            return {
                "type": "summary",
                "data": accessibility_violations_summary(df)
            }

        return {
            "message": "SEO intent detected but no matching rule implemented",
            "available_columns": list(df.columns)
        }

    except Exception as e:
        # NEVER crash the API
        return {
            "error": "SEO processing failed",
            "details": str(e),
            "available_columns": list(df.columns) if "df" in locals() else []
        }
