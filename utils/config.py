import os

PROJECT_NAME = "Autonomous Data Analyst"

REPORT_DIR = "reports"
CHART_DIR = os.path.join(REPORT_DIR, "charts")
HTML_DIR = os.path.join(REPORT_DIR, "html")

SUPPORTED_FORMATS = [
    ".csv",
    ".xlsx",
    ".xls",
    ".tsv",
    ".json"
]