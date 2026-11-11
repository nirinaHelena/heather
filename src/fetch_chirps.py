"""Download daily CHIRPS rainfall for the six cities through the ClimateSERV API."""
from pathlib import Path
import time

import climateserv
import pandas as pd

from fetch_data import CITIES

DATASET_CHIRPS = 0      # ClimateSERV dataset ID for UCSB CHIRPS rainfall
HALF_CELL = 0.025       # half the size of one CHIRPS cell (0.05°)
PERIODS = [             # test first with [("01/01/2024", "01/31/2024")]
    ("01/01/1981", "12/31/1990"),
    ("01/01/1991", "12/31/2000"),
    ("01/01/2001", "12/31/2010"),
    ("01/01/2011", "12/31/2020"),
    ("01/01/2021", "12/31/2025"),
]
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "chirps"


def square(lat: float, lon: float, d: float = HALF_CELL) -> list[list[float]]:
    """Closed square polygon of [lon, lat] corners around a point."""
    return [[lon - d, lat + d], [lon + d, lat + d], [lon + d, lat - d], [lon - d, lat - d], [lon - d, lat + d]]


def fetch_period(lat: float, lon: float, start: str, end: str) -> pd.DataFrame:
    """Daily CHIRPS rainfall for one point and one period."""
    result = climateserv.request_data(
        DATASET_CHIRPS, "Average", start, end, square(lat, lon), "", "", "memory_object"
    )
    rows = [{"date": day["date"], "rain_chirps": day["value"]["avg"]} for day in result["data"]]
    return pd.DataFrame(rows)


def fetch_city(name: str, lat: float, lon: float) -> pd.DataFrame:
    """Daily CHIRPS rainfall for one city over all periods, dates as YYYYMMDD."""
    frames = []
    for start, end in PERIODS:
        frames.append(fetch_period(lat, lon, start, end))
        time.sleep(2)
    df = pd.concat(frames, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y").dt.strftime("%Y%m%d")
    df.insert(1, "city", name)
    return df


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, (lat, lon) in CITIES.items():
        out_path= RAW_DIR / f"{name}.csv"
        if out_path.exists():
            print(f"{out_path.name} already exists. Skipping {name}")
            continue
        df= fetch_city(name, lat, lon)
        df.to_csv(out_path, index=False)
        print(f"Fetched {len(df)} rows for {name}. Saved to {out_path.name}.")
        time.sleep(2)


if __name__ == "__main__":
    main()