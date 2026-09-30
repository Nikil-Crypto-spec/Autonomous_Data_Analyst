# Autonomous Data Analyst

A Streamlit-powered tool that makes data exploration, cleaning, analysis, and visualization effortless. Upload your dataset, dive into its structure and quality, apply cleaning operations, and generate insights—all in one interactive app.

## What You Can Do

**Load your data:**
- Import CSV, TSV, Excel (`.xlsx` and `.xls`), and JSON files

**Explore what you have:**
- Preview your data records and examine column names and types
- Check for missing values, duplicates, and unique values
- Understand dataset size, memory usage, and get descriptive statistics
- Explore numeric correlations between columns

**Clean it up:**
- Remove duplicate rows and empty rows or columns
- Fill missing values intelligently
- Standardize column names and trim strings
- Filter out numeric outliers using the IQR method
- Use automatic cleaning for quick preprocessing (but always review the results!)

**Visualize and analyze:**
- Generate interactive Plotly charts: histograms, bar and line charts, scatter plots, box and violin plots, pie and area charts, heatmaps, bubble charts, density heatmaps, sunbursts, and treemaps
- Explore descriptive statistics and rule-based insights
- Export your findings as downloadable HTML reports
- Save cleaned data in your preferred format: CSV, Excel, TSV, or JSON

## Getting Started

**Prerequisites:**
- Python (available as `python` on your system, or `py` on Windows)
- Dependencies listed in [`requirements.txt`](requirements.txt)

**Setup:**

1. Create and activate a virtual environment:

   **On Windows:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **On macOS or Linux:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Launch the app:
   ```bash
   streamlit run app.py
   ```

Streamlit will print a local URL in your terminal. Open it in your browser to start using the app.

## How to Use

1. **Upload your dataset** using the sidebar—the app supports CSV, TSV, Excel, and JSON files
2. **Explore** your data with the **Data Preview** and **Data Profile** sections
3. **Clean** your data in **Data Cleaning**—any operations you apply affect your working dataset
4. **Analyze and visualize** using **Statistics**, **Visualizations**, and **Insights**
5. **Export** by creating an HTML report, or download your cleaned data and saved reports from **Download**

**Note:** The automatic cleaning feature is convenient but always review the results before relying on them—automatic filling and outlier removal may not suit every dataset.

## Project Structure

```
app.py                      Streamlit interface and page navigation
style.css                   Application styles
modules/                    Data loading, profiling, cleaning, analysis,
                            visualization, insights, and report generation
utils/                      Configuration, validation, caching, and export helpers
data/raw/                   Local workspace for raw datasets
data/cleaned/               Local workspace for cleaned datasets
reports/charts/             Saved interactive chart HTML files
reports/html/               Generated analysis reports
tests/                      Automated tests
requirements.txt            Python dependencies
```

## Generated Files

- **HTML reports:** stored in `reports/html/`
- **Chart files:** saved to `reports/charts/`
- **Data folders:** Use `data/raw/` and `data/cleaned/` for local file organization; files uploaded through the app are processed in the session and aren't automatically stored here

## Running Tests

To run the automated test suite:

```bash
python -m pytest
```
