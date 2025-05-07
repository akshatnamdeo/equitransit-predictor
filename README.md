# Public Transit Reliability and Equity Predictor

This project was created for the **CSC 4780** class at Georgia State University by:

**Akshat Namdeo, Hoang Tran, Joshith Reddy Aleti, Kartikeya Duvvuri, Mubashar Mian, and Muhammad Abdullah Nasir**

---

## 📂 Dataset Access & Setup

The datasets used in this project can be accessed here:  
🔗 [Google Drive - Datasets](https://drive.google.com/drive/u/1/folders/1K0cB00BBtButtvitraSU5AFmZep47nmA)

> ⚠️ **IMPORTANT:** Download the entire `datasets` folder from the Drive link and place it in the root directory (i.e., the same folder where both `preprocessing.ipynb` and `training.ipynb` are located). This is required for the notebooks to run successfully.

---

## 🚆 Project Overview

This project analyzes **transit reliability and equity** in New York City's subway system by integrating operational data with demographic insights to identify service disparities. It combines data engineering, geospatial analysis, and machine learning to:

- Predict significant transit delays
- Quantify equity-related impacts
- Prioritize stations for targeted interventions

---

## 📊 Data Sources

We utilized a wide range of open datasets:

- **MTA Hourly Ridership** (~53 million records): Hourly entries/exits per station
- **MTA Subway Train Delay Logs** (~40,503 records): Incident-level delay reports (2020–2025)
- **MTA MDBF (Mean Distance Between Failures)** (1,583 records): Subway car reliability stats
- **NYC Demographics (ACS 2023)**: Income, race, and dependency ratios by tract
- **NYC Geographic Data (OpenStreetMap)**: 497 subway stations, 16,347 bus stops

---

## 🗂 Repository Structure

### `preprocessing.ipynb`

Handles all initial data processing and engineering:

- Temporal feature extraction (month, season, weekday flags)
- Station name normalization and line mappings
- Integration of OSM + ACS data (geolocation, demographics)
- Construction of delay prediction targets
- Imputation and data cleaning logic

### `training.ipynb`

Implements the complete machine learning pipeline:

- Baseline models (majority class, logistic regression)
- Optimized Random Forest classifier (98.7% accuracy)
- Feature importance analysis
- Equity scoring framework
- Identification of high-priority stations
- Simulation of intervention impacts

### `figures/`

Contains key visual outputs:

- Delay distributions across boroughs and lines
- Heatmaps of equity metrics
- Accessibility scores and economic impact estimates
- Resource allocation and improvement simulations

### `analyze_osm.py`

Processes OpenStreetMap transit data to:

- Geolocate subway stations
- Build 500-meter catchment areas
- Calculate accessibility metrics
- Align street networks with station-level data

### `fetch_mta_hourly_dataset.py`

Automates downloading and preparing MTA hourly ridership data:

- API integration and batching
- Cleaning, parsing, and formatting
- Optimization for ~53 million rows

---

## 🔍 Key Findings

- **81 subway stations** (~23.3%) were identified as **high-priority** for equity-focused interventions.
- Targeted improvements could yield a **13.3% increase** in overall transit equity.
- The intervention strategy could generate up to **$2.31 billion** in annual economic benefits.
- Borough-specific plans ensure fairness by balancing **ridership**, **reliability**, and **demographics**.
