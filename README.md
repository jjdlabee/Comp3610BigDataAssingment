# NYC Yellow Taxi Data Analysis - COMP 3610 Big Data Assignment

Analysis of NYC Yellow Taxi trip patterns for January 2024 using Polars, DuckDB, and Streamlit.

## Overview

This project implements a **complete data pipeline** for analyzing millions of taxi trips, from raw data ingestion through interactive visualization. The assignment demonstrates:

- **Data Ingestion & Validation**: Download and validate multi-gigabyte parquet datasets
- **Data Cleaning & Transformation**: Remove anomalies, engineer features, aggregate to hourly grain
- **Exploratory Analysis**: SQL-based queries revealing temporal patterns, geographic hotspots, payment trends
- **Interactive Dashboard**: Real-time filtering and visualization of 5 key metrics and insights

## Submission Requirements

**GitHub Repository**: [jjdlabee/Comp3610BigDataAssingment](https://github.com/jjdlabee/Comp3610BigDataAssingment)

**Deployed Dashboard**: [Streamlit Cloud URL](https://jjdlabee-comp3610bigdataassingment-app-helj5m.streamlit.app/)

## Prerequisites

- **Python 3.13+**
- Virtual environment (venv/conda)
- ~500MB disk space for processed data

## Setup Instructions

### 1. Extract the Project

```bash
cd Comp3610BigDataAssingment
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Project

### Run the Analytical Notebook

```bash
jupyter notebook notebook.ipynb
```

The notebook executes a complete ETL pipeline:

- **Part 1**: Data ingestion from HTTP + schema validation
- **Part 2**: Data cleaning + feature engineering (remove nulls, invalid fares, temporal anomalies)
- **Part 3**: Exploratory analysis with 6 SQL queries + 5 Plotly visualizations
- **Part 4**: Interactive dashboard overview

Execution time: ~2-3 minutes

### Run the Interactive Dashboard

```bash
streamlit run app.py
```

Open browser to `http://localhost:8501`

## Data Source

**NYC Yellow Taxi Trip Records** (January 2024)

- Source: NYC Taxi & Limousine Commission (TLC)
- Format: Parquet (trip-level records)
- Volume: ~1.9 million trips
- Key fields: timestamps, locations, fare, distance, payment type, tips

**Zone Reference**: `data/raw/taxi_zone_lookup.csv`

## Key Findings

1. **Geographic Hotspot**: Manhattan dominates with 75%+ of pickups, particularly Midtown Center
2. **Rush Hour Patterns**: Weekday peaks at 8-9 AM (commute) and 5-6 PM (evening rush)
3. **Payment Methods**: Credit cards account for >70% of transactions
4. **Tipping**: Higher during business hours (8 AM-6 PM); lower late-night
5. **Trip Distance**: Right-skewed distribution with median ~2 miles; most trips within Manhattan

## AI Usage

Github copilot was used for quick completion of repetative lines.

ChatGPT was used to simple format and concepts learning (ie. setting up vs code with python and a notbook)

VS Code Copilot with Claude was used for fast creation of readme file, formating of text in the notebook and it heavily assisted with the visuallization using streamlit (Some stuff just was not clicking in the short timespan)
