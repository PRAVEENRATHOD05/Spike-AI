import pandas as pd

SHEET_ID = "1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VEE"
GID = "1438203274"

CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/export?format=csv&gid={GID}"
)


def load_seo_dataframe():
    df = pd.read_csv(CSV_URL)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df
