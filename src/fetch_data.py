"""Download daily climate data for six Malagasy cities from the NASA POWER API."""
from pathlib import Path
import time

import pandas as pd
from prometheus_client import values
import requests

BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
PARAMETERS = ["T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR", "RH2M"]
START, END = "19810101", "20251231"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

CITIES = {
    "antananarivo": (-18.91, 47.52),
    "fianarantsoa": (-21.45, 47.09),
    "toamasina":    (-18.15, 49.40),
    "mahajanga":    (-15.72, 46.32),
    "antsiranana":  (-12.28, 49.29),
    "toliara":      (-23.35, 43.67),
}


def fetch_city(name: str, lat: float, lon: float) -> pd.DataFrame:
    """Return one row per day for one city."""
    params = {
        "parameters": ",".join(PARAMETERS),
        "community": "AG",
        "latitude": lat,
        "longitude": lon,
        "start": START,
        "end": END,
        "format": "JSON",
    }
    response = requests.get(BASE_URL, params=params, timeout=120)
    response.raise_for_status()

    values = response.json()["properties"]["parameter"]
    df = pd.DataFrame(values)

    df.index.name = "date"
    df = df.reset_index()
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
        print(f"Fetched {len(df)} rows for {name}. Saved to {out_path.name}.")
        time.sleep(2)


if __name__ == "__main__":
    main()