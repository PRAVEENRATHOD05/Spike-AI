def non_https_urls(df, url_col):
    return df[~df[url_col].str.startswith("https", na=False)][[url_col]]


def group_by_status_code(df, status_col):
    return (
        df.groupby(status_col)
        .size()
        .reset_index(name="count")
        .to_dict(orient="records")
    )


def psi_error_pages(df, psi_col):
    return df[df[psi_col].notna()][["address", psi_col]]


def accessibility_violations_summary(df):
    violation_cols = [c for c in df.columns if "violations" in c]

    summary = {}

    for col in violation_cols:
        try:
            values = (
                df[col]
                .replace("", 0)
                .fillna(0)
                .astype(float)
            )
            summary[col] = int(values.sum())
        except Exception:
            summary[col] = 0

    return summary
