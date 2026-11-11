# Heather — Madagascar Climate Analysis (1981–2025)

> 🇫🇷 Résumé en français : à écrire à la phase 5.

## Summary
_To be written in phase 5._

## 1. Ask

### Business task
Use 45 years of daily climate data (1981–2025) to measure how the climate risks that most affect people's lives in Madagascar — unreliable rains, drought and dangerous heat — have evolved, and identify the regions and communities most exposed.

**Main question:** Is Madagascar's climate becoming harder to live with — less reliable for farmers, drier in the South and more dangerous in the heat — and where is the risk growing fastest?

### Key questions
1. **Rain reliability (food)** — Does the rainy season start later, vary more from year to year, or have more "false starts" (first rains followed by a long dry spell that ruins the sowing)?
2. **Drought (water)** — Are droughts becoming more frequent, longer or more severe, especially in the semi-arid South (Toliara)?
3. **Dangerous heat (health)** — How many days per year exceed heat-index danger thresholds, and is this number increasing?
4. **Inequality between regions** — Which regions face the fastest-growing risks, and are the most exposed regions the same for all three risks?

### Scope
| | |
|---|---|
| **Cities** | Antananarivo, Fianarantsoa, Toamasina, Mahajanga, Antsiranana, Toliara |
| **Period** | 1 January 1981 – 31 December 2025, daily values |
| **Variables** | Mean, maximum and minimum temperature at 2 m (°C), relative humidity (%), precipitation (mm/day) |
| **Sources** | NASA POWER for temperature and humidity; CHIRPS for rainfall (satellite- and station-based estimates) |

**Out of scope:** this project measures climate *hazards*, not their impacts. Crop yields, food insecurity and health outcomes would require additional data and are planned as a follow-up project (starting with malaria).

### Stakeholders
| Stakeholder | How the results could help |
|---|---|
| Farmers and agricultural extension services | Adapt sowing dates and choose crop varieties suited to a less reliable rainy season |
| Environmental and food-security organisations | Target drought preparedness and resilience programmes where the risk grows fastest |
| Public-health authorities and municipalities | Prepare heat-wave alerts and protect the most vulnerable people in cities |
| Citizens and local communities | Understand, with clear figures, how their region's climate has changed in their lifetime |

## 2. Prepare

### Data sources
| Source | Variables used | Resolution | Retrieved with |
|---|---|---|---|
| [NASA POWER](https://power.larc.nasa.gov/) (MERRA-2 reanalysis), Daily Point API, Agroclimatology community | Temperature (mean, max, min), relative humidity | 0.5° × 0.625° grid cell (about 55 × 65 km) | [`src/fetch_data.py`](src/fetch_data.py) |
| [CHIRPS v2](https://www.chc.ucsb.edu/data/chirps) (Climate Hazards Group, UC Santa Barbara), through the [ClimateSERV](https://climateserv.servirglobal.net/) API | Daily rainfall | 0.05° grid cell (about 5 km) | [`src/fetch_chirps.py`](src/fetch_chirps.py) |

Data were downloaded on 9 November 2026 (NASA POWER) and 11 November 2026 (CHIRPS).

**Why two sources?** NASA POWER was first used for every variable. A validation against published long-term normals (see below) showed that its rainfall amounts are badly misplaced over Madagascar: far too much rain on the Highlands, far too little on the east coast. Temperatures were consistent with the normals. Rainfall was therefore replaced by CHIRPS, a reference dataset for drought monitoring in Africa that blends satellite imagery with rain-gauge records.

### Data collected
| City | Climate zone | Latitude | Longitude |
|---|---|---|---|
| Antananarivo | Central Highlands | -18.91 | 47.52 |
| Fianarantsoa | Southern Highlands | -21.45 | 47.09 |
| Toamasina | East coast | -18.15 | 49.40 |
| Mahajanga | West coast | -15.72 | 46.32 |
| Antsiranana | Far north | -12.28 | 49.29 |
| Toliara | Semi-arid south | -23.35 | 43.67 |

| Variable | Description | Unit | Source |
|---|---|---|---|
| `T2M` | Mean air temperature at 2 m | °C | NASA POWER |
| `T2M_MAX` | Daily maximum temperature at 2 m | °C | NASA POWER |
| `T2M_MIN` | Daily minimum temperature at 2 m | °C | NASA POWER |
| `RH2M` | Relative humidity at 2 m | % | NASA POWER |
| `rain_chirps` | Daily rainfall (**used for the analysis**) | mm/day | CHIRPS |
| `PRECTOTCORR` | Daily rainfall, bias-corrected (kept for comparison only) | mm/day | NASA POWER |

- **Period:** 1 January 1981 – 31 December 2025, one value per day
- **Volume:** 16,436 days × 6 cities = 98,616 rows per source, stored as one CSV per city in `data/raw/` (NASA POWER) and `data/raw/chirps/` (CHIRPS)

### Rainfall validation
Mean annual rainfall over 1981–2025, compared with published long-term normals (mostly weather-station records, over different periods: use for order of magnitude only).

| City | NASA POWER | CHIRPS | Published normal | NASA POWER error | CHIRPS error |
|---|---|---|---|---|---|
| Toamasina | 1,926 mm | 3,271 mm | 3,368 mm | -43 % | **-3 %** |
| Antananarivo | 2,371 mm | 1,322 mm | 1,365 mm | +74 % | **-3 %** |
| Mahajanga | 1,417 mm | 1,470 mm | 1,476 mm | -4 % | **0 %** |
| Fianarantsoa | 2,038 mm | 1,151 mm | 1,085 mm | +88 % | **+6 %** |
| Toliara | 550 mm | 312 mm | about 360 mm (semi-arid south-west) | +53 % | **-13 %** |
| Antsiranana | 1,102 mm | 1,156 mm | 940 mm | +17 % | +23 % |

CHIRPS stays within about 15 % of the normals for five cities out of six, while NASA POWER is off by more than 40 % in four of them. Antsiranana remains uncertain: both sources exceed the station normal by about 20 %.

### Data quality (ROCCC)
| Criterion | Assessment |
|---|---|
| **Reliable** | Both sources are produced by recognised scientific institutions (NASA; UC Santa Barbara Climate Hazards Center) and widely used in research, but they are gridded estimates, not weather-station records. Rainfall was cross-checked against published normals |
| **Original** | Downloaded directly from the official APIs, with no intermediary dataset |
| **Comprehensive** | 45 years of daily data for 6 cities covering the main climate zones; no missing values and no duplicate dates in either source |
| **Current** | Covers the period up to 31 December 2025 |
| **Cited** | See *Sources & acknowledgements* |

### Known limitations of the data
- **Grid cells, not stations:** each value is an average over a grid cell. NASA POWER cells are large (about 55 × 65 km): for Antananarivo, the cell's mean elevation is 1,425 m, higher than the city itself (about 1,280 m), so its temperatures are slightly too cool. CHIRPS cells are much smaller (about 5 km).
- **CHIRPS daily values are approximations:** CHIRPS is built on 5-day totals that are then split into days. Daily figures (and day-by-day indicators such as dry spells or the start of the rainy season) should be read as indicative; monthly and seasonal totals are more robust.

## 3. Process

Cleaning is done in [`notebooks/01_cleaning.ipynb`](notebooks/01_cleaning.ipynb) with Python (pandas). The output is `data/processed/madagascar_climate_daily.csv`: 98,616 rows × 13 columns, one row per city per day.

### Cleaning log
| Step | Operation | Result |
|---|---|---|
| 1 | Combined the 6 NASA POWER city files and added each city's climate zone | 98,616 rows (16,436 per city); every city mapped to a zone |
| 1b | Merged daily CHIRPS rainfall on city and date (one-to-one) | 0 days without a CHIRPS value |
| 2 | Converted `date` from text (`YYYYMMDD`) to a date type | Dates valid; all 6 measurements stored as numbers |
| 3 | Replaced the missing-value codes (`-999` NASA POWER, `-9999` CHIRPS) with `NaN` | 0 missing values found |
| 4 | Consistency checks: duplicates, missing days, `T2M_MIN ≤ T2M ≤ T2M_MAX`, rainfall ≥ 0 (both sources), humidity 0–100 %, temperature between -5 and 50 °C | 0 rows failing; no rows removed or modified |
| 5 | Investigated extreme values | Hottest day: 39.8 °C (Toliara, 11 Jan 2025). Coldest night: 3.0 °C (Fianarantsoa, 30 Jun 2009). Wettest day in CHIRPS: 434 mm (Toamasina, 7 Apr 1992). The NASA POWER record (244 mm, Antananarivo, 12 Apr 2020) is not confirmed by CHIRPS (see *Limitations*) |
| 6 | Added `year`, `month`, `season` (rainy: Nov–Apr, dry: May–Oct) and `hydro_year` (1 July – 30 June) | Hydrological years 1980 and 2025 are incomplete and are excluded from rainy-season analyses |
| 7 | Validated mean annual rainfall of both sources against published normals | CHIRPS retained for all rainfall analyses (see *Rainfall validation*) |
| 8 | Reordered columns, sorted by city and date, saved the clean file | 98,616 rows × 13 columns |

## 4. Analyze

## 5. Share

## 6. Act

## Repository structure
```
heather/
├── data/
│   ├── raw/              # NASA POWER files, one per city (never modified)
│   │   └── chirps/       # CHIRPS rainfall files, one per city (never modified)
│   └── processed/        # clean dataset produced by 01_cleaning.ipynb
├── notebooks/
│   ├── 01_cleaning.ipynb
│   └── 02_analysis.ipynb
├── src/
│   ├── fetch_data.py     # downloads NASA POWER data
│   └── fetch_chirps.py   # downloads CHIRPS rainfall through ClimateSERV
├── figures/              # exported charts
├── requirements.txt
└── README.md
```

## How to reproduce
```bash
git clone https://github.com/nirinaHelena/heather.git
cd heather
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python src/fetch_data.py           # NASA POWER: a few seconds per city
python src/fetch_chirps.py         # CHIRPS: a few minutes per city
```
Then run `notebooks/01_cleaning.ipynb` and `notebooks/02_analysis.ipynb` in order.

## Limitations
- **The NASA POWER rainfall record is probably a model artefact.** NASA POWER shows a six-day wet episode in Antananarivo (about 680 mm from 11 to 16 April 2020, including 244 mm on 12 April), also visible in Toamasina and Mahajanga. CHIRPS, which blends satellite and rain-gauge data, records **no rain at all** in Antananarivo over the same days, and no matching report was found. This is consistent with the rainfall bias found in the validation and is one of the reasons NASA POWER rainfall is not used for the analysis.
- **Rainfall validation is approximate:** the published normals cover other periods (e.g. 1961–1990) and some come from secondary compilations, so the comparison only detects large biases.
- **Antsiranana rainfall is uncertain:** both sources exceed the station normal by about 20 %.

## Sources & acknowledgements
- These data were obtained from the NASA Langley Research Center (LaRC) POWER Project funded through the NASA Earth Science/Applied Science Program.
- Funk, C. et al. (2015). The climate hazards infrared precipitation with stations — a new environmental record for monitoring extremes. *Scientific Data*, 2, 150066. https://doi.org/10.1038/sdata.2015.66
- CHIRPS data were accessed through ClimateSERV (NASA / SERVIR).
- Published rainfall normals: NOAA climate normals 1961–1990 (Toamasina, Mahajanga) and public climate summaries for the other cities.

## Author