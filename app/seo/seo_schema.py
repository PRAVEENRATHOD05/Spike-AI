COLUMN_ALIASES = {
    "address": ["address", "url"],
    "status_code": ["status_code", "status"],
    "psi_status": ["psi_status"],
}


def resolve_columns(df):
    resolved = {}

    for canonical, options in COLUMN_ALIASES.items():
        for opt in options:
            if opt in df.columns:
                resolved[canonical] = opt
                break

    return resolved
