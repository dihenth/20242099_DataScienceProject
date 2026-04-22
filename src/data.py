import pandas as pd
import requests

INDICATOR_CODE = "EG.ELC.RNWX.ZS"
API_URL = f"https://api.worldbank.org/v2/country/all/indicator/{INDICATOR_CODE}"


def load_indicator_data():
    params = {
        "format": "json",
        "per_page": 500,
        "page": 1,
    }

    all_rows = []

    while True:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        metadata = payload[0]
        records = payload[1]

        for item in records:
            country = item["country"]["value"]
            year = item["date"]
            value = item["value"]

            if value is None:
                continue

            all_rows.append(
                {
                    "country": country,
                    "year": int(year),
                    "value": float(value),
                }
            )

        if params["page"] >= metadata["pages"]:
            break

        params["page"] += 1

    return pd.DataFrame(all_rows)
