# app/agents/ga4_allowlist.py

ALLOWED_METRICS = {
    "users": "totalUsers",
    "sessions": "sessions",
    "page views": "screenPageViews",
    "pageviews": "screenPageViews",
    "engaged sessions": "engagedSessions",
}

ALLOWED_DIMENSIONS = {
    "date": "date",
    "page": "pagePath",
    "page path": "pagePath",
    "country": "country",
    "device": "deviceCategory",
    "source": "sessionSource",
}
