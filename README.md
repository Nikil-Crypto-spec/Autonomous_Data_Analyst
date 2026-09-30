# Autonomous Data Analyst

Autonomous Data Analyst is a Streamlit application for exploring, cleaning, analyzing, and visualizing tabular datasets. Upload a file, inspect its structure and data quality, apply cleaning operations, and export the cleaned data or an HTML analysis report.

## Features

- Load CSV, TSV, Excel (`.xlsx` and `.xls`), and JSON files.
- Preview records, column names, data types, missing values, unique values, and duplicates.
- Profile dataset size, memory use, data types, descriptive statistics, and numeric correlations.
- Clean data by removing duplicates, empty rows or columns, filling missing values, standardizing column names, trimming strings, and filtering numeric outliers using the IQR rule.
- Calculate descriptive statistics and rule-based dataset insights.
- Build interactive Plotly charts, including histograms, bar and line charts, scatter plots, box and violin plots, pie and area charts, heatmaps, bubble charts, density heatmaps, sunbursts, and treemaps.
- Generate and download HTML reports, and export cleaned data as CSV, Excel, TSV, or JSON.

## Requirements

- Python installed and available as `python` (or use `py` on Windows).
- Packages listed in [`requirements.txt`](requirements.txt).

## Setup and Run

From the project directory, create and activate a virtual environment, install the dependencies, then launch Streamlit:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

Streamlit prints a local URL in the terminal when the app starts. Open that URL in a browser. Use **Upload Dataset** in the sidebar to select a supported file; the other analysis pages become available after upload.

## Using the App

1. Upload a CSV, TSV, Excel, or JSON dataset.
2. Review the dataset in **Data Preview** and **Data Profile**.
3. Use **Data Cleaning** to apply the operations you need. Cleaning actions affect the working dataset used by the analysis and exports.
4. Explore **Statistics**, **Visualizations**, and **Insights**.
5. Create an HTML report from **HTML Report**, or download cleaned data and saved reports from **Download**.

The cleaning page also offers an automatic cleaning operation. Review the resulting data before treating the output as authoritative: automatic filling and outlier removal may not be appropriate for every dataset or analysis.

## Generated Files

- HTML reports are written to `reports/html/`.
- Saved chart HTML files are written to `reports/charts/`.
- The `data/raw/` and `data/cleaned/` folders are available for local dataset organization; files uploaded through the app are processed in the running session and are not automatically stored there.

## Project Layout

```text
app.py                      Streamlit interface and page navigation
style.css                   Application styles
modules/                    Data loading, profiling, cleaning, analysis,
                            visualization, insights, and report generation
utils/                      Configuration, validation, caching, and export helpers
data/raw/                   Raw-data workspace
data/cleaned/               Cleaned-data workspace
reports/charts/             Saved interactive chart HTML
reports/html/               Generated analysis reports
tests/                      Automated tests
requirements.txt            Python dependencies
```

## Tests

Run the test suite from the project directory with:

```bash
python -m pytest
```