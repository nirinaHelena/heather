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
| **Variables** | Mean, maximum and minimum temperature at 2 m (°C), precipitation (mm/day), relative humidity (%) |
| **Source** | NASA POWER (satellite- and model-based estimates) |

**Out of scope:** this project measures climate *hazards*, not their impacts. Crop yields, food insecurity and health outcomes would require additional data and are planned as a follow-up project (starting with malaria).

### Stakeholders
| Stakeholder | How the results could help |
|---|---|
| Farmers and agricultural extension services | Adapt sowing dates and choose crop varieties suited to a less reliable rainy season |
| Environmental and food-security organisations | Target drought preparedness and resilience programmes where the risk grows fastest |
| Public-health authorities and municipalities | Prepare heat-wave alerts and protect the most vulnerable people in cities |
| Citizens and local communities | Understand, with clear figures, how their region's climate has changed in their lifetime |

## 2. Prepare

### Data source
Daily climate data from the [NASA POWER](https://power.larc.nasa.gov/) project (Prediction Of Worldwide Energy Resources), retrieved through its Daily Point API with the Agroclimatology community (`community=AG`). The values come from the MERRA-2 reanalysis, a model that combines satellite and ground observations.

Data were downloaded on 9 November 2026 with [`src/fetch_data.py`](src/fetch_data.py).

### Data collected
| City | Climate zone | Latitude | Longitude |
|---|---|---|---|
| Antananarivo | Central Highlands | -18.91 | 47.52 |
| Fianarantsoa | Southern Highlands | -21.45 | 47.09 |
| Toamasina | East coast | -18.15 | 49.40 |
| Mahajanga | West coast | -15.72 | 46.32 |
| Antsiranana | Far north | -12.28 | 49.29 |
| Toliara | Semi-arid south | -23.35 | 43.67 |

| Variable | Description | Unit |
|---|---|---|
| `T2M` | Mean air temperature at 2 m | °C |
| `T2M_MAX` | Daily maximum temperature at 2 m | °C |
| `T2M_MIN` | Daily minimum temperature at 2 m | °C |
| `PRECTOTCORR` | Precipitation (bias-corrected) | mm/day |
| `RH2M` | Relative humidity at 2 m | % |

- **Period:** 1 January 1981 – 31 December 2025, one value per day in local solar time (LST)
- **Volume:** 16,436 days × 6 cities = 98,616 rows, stored as one CSV per city in `data/raw/`

### Data quality (ROCCC)
| Criterion | Assessment |
|---|---|
| **Reliable** | Produced by NASA and widely used in agroclimatology research, but modelled data, not weather-station records |
| **Original** | Downloaded directly from the official API, with no intermediary |
| **Comprehensive** | 45 years of daily data for 6 cities covering the main climate zones; no missing values (`-999`) and no duplicate dates |
| **Current** | Covers the period up to 31 December 2025 |
| **Cited** | See *Sources & acknowledgements* |

### Known limitations of the data
- **Grid cells, not stations:** each value is an average over a cell of about 0.5° × 0.625° (roughly 55 × 65 km). For Antananarivo, the cell's mean elevation is 1,425 m, higher than the city itself (about 1,280 m), so local effects are smoothed out.
- **"Drizzle" bias:** the model produces small amounts of rain on almost every day. A dry day is therefore defined as a day with less than 1 mm of rain, not 0 mm.
- **Rainfall is less certain than temperature:** reanalysis models estimate precipitation less accurately than temperature, so rainfall results should be read as trends rather than exact amounts.

## 3. Process

## 4. Analyze

## 5. Share

## 6. Act

## Repository structure

## How to reproduce

## Limitations

## Sources & acknowledgements
- These data were obtained from the NASA Langley Research Center (LaRC) POWER Project funded through the NASA Earth Science/Applied Science Program.

## Author