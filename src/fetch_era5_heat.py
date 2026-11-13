"""Download hourly ERA5 temperature and humidity, then compute the daily maximum heat index (NOAA)."""
from pathlib import Path
import time

import numpy as np
import pandas as pd
import requests

from fetch_data import CITIES

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
PERIODS = [
    ("1981-01-01", "1990-12-31"),
    ("1991-01-01", "2000-12-31"),
    ("2001-01-01", "2010-12-31"),
    ("2011-01-01", "2020-12-31"),
    ("2021-01-01", "2025-12-31"),
]

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "era5_heat"


def heat_index_c(temp_c: np.ndarray, rh: np.ndarray) -> np.ndarray:
    """NOAA heat index (Rothfusz regression with NWS adjustments), in °C."""
    t = temp_c * 9 / 5 + 32
    simple = 0.5 * (t + 61.0 + (t - 68.0) * 1.2 + rh * 0.094)
    full = (-42.379 + 2.04901523 * t + 10.14333127 * rh - 0.22475541 * t * rh
            - 0.00683783 * t**2 - 0.05481717 * rh**2 + 0.00122874 * t**2 * rh
            + 0.00085282 * t * rh**2 - 0.00000199 * t**2 * rh**2)
    low_rh = (rh < 13) & (t >= 80) & (t <= 112)
    full = np.where(low_rh, full - ((13 - rh) / 4) * np.sqrt(np.clip((17 - np.abs(t - 95)) / 17, 0, None)), full)
    high_rh = (rh > 85) & (t >= 80) & (t <= 87)
    full = np.where(high_rh, full + ((rh - 85) / 10) * ((87 - t) / 5), full)
    hi = np.where((simple + t) / 2 >= 80, full, simple)
    return (hi - 32) * 5 / 9


def get_json(params: dict, label: str) -> dict:
    """GET with retries when the API rate limit is reached."""
    for attempt in range(8):
        response = requests.get(BASE_URL, params=params, timeout=300)
        if response.status_code != 429:
            response.raise_for_status()
            return response.json()
        wait = min(60 * 2**attempt, 900)
        print(f"Rate limit reached ({label}), waiting {wait} s...")
        time.sleep(wait)
    response.raise_for_status()


def fetch_city(name: str, lat: float, lon: float) -> pd.DataFrame:
    """Daily mean humidity and daily maximum heat index for one city, dates as YYYYMMDD."""
    frames = []
    for start, end in PERIODS:
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start,
            "end_date": end,
            "hourly": "temperature_2m,relative_humidity_2m",
            "timezone": "Indian/Antananarivo",
            "models": "era5",
        }
        frames.append(pd.DataFrame(get_json(params, f"{name} {start[:4]}")["hourly"]))
        time.sleep(10)

    hourly = pd.concat(frames, ignore_index=True)
    hourly["time"] = pd.to_datetime(hourly["time"])
    hourly["hi"] = heat_index_c(hourly["temperature_2m"].to_numpy(), hourly["relative_humidity_2m"].to_numpy())

    daily = hourly.groupby(hourly["time"].dt.strftime("%Y%m%d")).agg(
        rh_mean_era5=("relative_humidity_2m", "mean"),
        hi_max_era5=("hi", "max"),
        hours=("hi", "count"),
    )
    incomplete = (daily["hours"] != 24).sum()
    if incomplete:
        print(f"Warning: {incomplete} days without 24 hourly values for {name}")

    daily = daily.drop(columns="hours").round(2).reset_index(names="date")
    daily.insert(1, "city", name)
    return daily


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, (lat, lon) in CITIES.items():
        out_path = RAW_DIR / f"{name}.csv"
        if out_path.exists():
            print(f"{out_path.name} already exists. Skipping {name}.")
            continue
        print(f"Fetching {name}...")
        df = fetch_city(name, lat, lon)
        df.to_csv(out_path, index=False)
        print(f"Saved {len(df)} days for {name} → {out_path.name}")


if __name__ == "__main__":
    main()