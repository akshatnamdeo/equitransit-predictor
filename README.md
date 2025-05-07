# Public Transit Reliability and Equity Predictor

This project was created for the CSC 4780 class at Georgia State University by Akshat Namdeo, Hoang Tran, Joshith Reddy Aleti, Kartikeya Duvvuri, Mubashar Mian, and Muhammad Abdullah Nasir.

## Dataset Access

The complete datasets used in this project are available at:
https://drive.google.com/drive/u/1/folders/1K0cB00BBtButtvitraSU5AFmZep47nmA

## Project Overview

This project analyzes transit reliability and equity in New York City's subway system, integrating transportation operational data with demographic information to identify and quantify service disparities. We developed a machine learning pipeline to predict significant transit delays and created a comprehensive equity impact framework to prioritize stations for intervention.

### Data Sources

Our analysis combines multiple datasets:
- **MTA Ridership Data**: ~53 million records of hourly ridership across NYC subway stations
- **MTA Subway Trains Delayed Data**: ~40,503 records of delay incidents from 2020-2025
- **MTA Mean Distance Between Failures (MDBF) Data**: 1,583 records on subway car reliability
- **NYC Demographic Data**: American Community Survey (ACS) 2023 demographic information
- **NYC Geographic Data**: OpenStreetMap data including 497 subway stations and 16,347 bus stops

## Repository Structure

### `preprocessing.ipynb`
This notebook contains all data preprocessing steps, including:
- Temporal feature extraction (year, month, day, weekday flags, seasonal categorization)
- Station name standardization and line mapping
- Geographic integration of station locations with census tracts
- Demographic feature development (income categories, transit dependency ratio, racial composition)
- Target variable construction for delay prediction

The preprocessing addresses several challenges including temporal alignment of datasets with different coverage periods, station name inconsistencies, line-to-station mapping, and handling of missing data.

### `training.ipynb`
This notebook implements the machine learning pipeline and analysis:
- Baseline model evaluation using majority class and logistic regression approaches
- Random Forest model development with hyperparameter optimization
- Feature importance analysis and selection
- Model performance evaluation (achieving 98.7% accuracy, 98.5% precision)
- Equity impact scoring calculation
- Priority station identification
- Resource allocation optimization
- Intervention strategy development
- Simulation of equity improvements

### `figures/`
This directory contains all visualizations generated from the analysis, including:
- Delay distribution by borough, line, and demographic factors
- Demographic comparison visualizations
- Transit reliability metrics
- Economic impact analysis
- Accessibility and mobility impact visualizations
- Equity priority maps
- Intervention strategy visualizations

### `analyze_osm.py`
This script processes OpenStreetMap (OSM) data for New York City to extract and analyze geographic information about the transit network. It handles:
- Extraction of subway station locations
- Association of stations with street networks
- Calculation of station accessibility metrics
- Generation of 500-meter catchment areas for demographic analysis

### `fetch_mta_hourly_dataset.py`
This script downloads and processes the MTA hourly ridership dataset, which forms the foundation of our analysis. It handles:
- API connection to MTA data sources
- Downloading of hourly ridership records
- Initial data cleaning and formatting
- Storage optimization for the ~53 million records

## Key Findings

Our analysis identified 81 high-priority stations (23.3% of total) where targeted interventions could yield a 13.3% system-wide equity improvement and $2.31 billion in annual economic benefits. The optimized resource allocation model provides borough-specific intervention strategies, balancing reliability, ridership impact, and equity considerations.
