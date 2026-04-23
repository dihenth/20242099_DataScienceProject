import time

import pandas as pd
import requests

INDICATOR_CODE = "EG.ELC.RNWX.ZS"
API_URL = f"https://api.worldbank.org/v2/country/all/indicator/{INDICATOR_CODE}"


def fetch_json(url, params, timeout=60, retries=3, delay=2):
    last_error = None

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(delay)

    raise last_error


def load_indicator_data():
    params = {
        "format": "json",
        "per_page": 250,
        "page": 1,
    }

    all_rows = []

    while True:
        payload = fetch_json(API_URL, params=params, timeout=60, retries=3, delay=2)

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
