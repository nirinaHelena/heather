"""Download daily ERA5 temperatures for the six cities from the Open-Meteo archive API."""
from pathlib import Path
import time

import pandas as pd
import requests

from fetch_data import CITIES

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
START, END = START, END = "1981-01-01", "2025-12-31"
DAILY_VARS = {
    "temperature_2m_mean": "tmean_era5",
    "temperature_2m_max": "tmax_era5",
    "temperature_2m_min": "tmin_era5",
}
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "era5"


def fetch_city(name: str, lat: float, lon: float) -> pd.DataFrame:
    """Daily ERA5 temperatures for one city, dates as YYYYMMDD."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START,
        "end_date": END,
        "daily": ",".join(DAILY_VARS),
        "timezone": "Indian/Antananarivo",
        "models": "era5",
    }
    for attempt in range(5):
        response = requests.get(BASE_URL, params=params, timeout=120)
        if response.status_code != 429:
            break
        wait = 60 * (attempt + 1)
        print(f"Rate limit reached for {name}, waiting {wait} s...")
        time.sleep(wait)
    response.raise_for_status()

    daily = response.json()["daily"]
    df = pd.DataFrame(daily).rename(columns={"time": "date", **DAILY_VARS})
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y%m%d")
    df.insert(1, "city", name)
    return df


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, (lat, lon) in CITIES.items():
        out_path = RAW_DIR / f"{name}.csv"
        if out_path.exists():
            print(f"{out_path.name} already exists. Skipping {name}.")
            continue
        df = fetch_city(name, lat, lon)
        df.to_csv(out_path, index=False)
        print(f"Fetched {len(df)} rows for {name} → {out_path.name}")
        time.sleep(2)


if __name__ == "__main__":
    main()