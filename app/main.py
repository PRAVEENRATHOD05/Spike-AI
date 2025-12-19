from fastapi import FastAPI, HTTPException
from app.orchestrator.orchestrator import run_tier3_query

app = FastAPI()


@app.post("/query")
def query(payload: dict):
    query_text = payload.get("query")
    property_id = payload.get("propertyId")

    if not query_text:
        raise HTTPException(status_code=400, detail="query is required")

    results = run_tier3_query(
        query=query_text,
        property_id=property_id
    )

    return {
        "agents_used": list(results.keys()),
        "raw_results": results
    }
