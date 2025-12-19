from app.analytics.ga4_client import get_ga4_client


def run_ga4_report(
    property_id: str,
    metrics: list[str],
    dimensions: list[str],
    start_date: str,
    end_date: str
):
    client = get_ga4_client()  # credentials.json ONLY

    request = {
        "property": f"properties/{property_id}",
        "date_ranges": [{"start_date": start_date, "end_date": end_date}],
        "metrics": [{"name": m} for m in metrics],
        "dimensions": [{"name": d} for d in dimensions],
    }

    response = client.run_report(request)

    rows = []
    for row in response.rows:
        record = {}
        for i, dim in enumerate(dimensions):
            record[dim] = row.dimension_values[i].value
        for i, met in enumerate(metrics):
            record[met] = row.metric_values[i].value
        rows.append(record)

    return rows
