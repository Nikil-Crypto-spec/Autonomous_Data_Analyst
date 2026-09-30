"""
report_generator.py
------------------------------------------
Generate Interactive HTML Report
"""

from pathlib import Path
from datetime import datetime
import pandas as pd


class ReportGenerator:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    # -----------------------------------
    # Dataset Summary
    # -----------------------------------

    def dataset_summary(self):

        return {

            "Rows": self.df.shape[0],

            "Columns": self.df.shape[1],

            "Missing Values":
                int(self.df.isnull().sum().sum()),

            "Duplicate Rows":
                int(self.df.duplicated().sum()),

            "Memory Usage":
                round(
                    self.df.memory_usage(deep=True).sum() /
                    1024 / 1024,
                    2
                )

        }

    # -----------------------------------
    # Generate HTML
    # -----------------------------------

    def generate(

        self,

        filename=None,

        statistics=None,

        insights=None,

        chart_files=None,

        output_path=None

    ):

        if filename is None:

            filename = output_path

        if filename is None:

            raise ValueError(
                "A filename or output_path is required."
            )

        summary = self.dataset_summary()

        html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>Autonomous Data Analyst Report</title>

<style>

body{{
font-family:Arial;
margin:40px;
background:#f4f7fb;
}}

h1,h2,h3{{
color:#1E3A8A;
}}

table{{
width:100%;
border-collapse:collapse;
margin-bottom:30px;
}}

th,td{{
border:1px solid #ddd;
padding:10px;
}}

th{{
background:#2563EB;
color:white;
}}

.card{{
background:white;
padding:20px;
border-radius:10px;
box-shadow:0 0 8px rgba(0,0,0,.1);
margin-bottom:20px;
}}

.footer{{
text-align:center;
color:gray;
margin-top:50px;
}}

</style>

</head>

<body>

<h1>📊 Autonomous Data Analyst Report</h1>

<p><b>Generated:</b> {datetime.now()}</p>

<div class="card">

<h2>Dataset Summary</h2>

<table>

<tr><th>Metric</th><th>Value</th></tr>

"""

        for key, value in summary.items():

            html += f"""

<tr>

<td>{key}</td>

<td>{value}</td>

</tr>

"""

        html += """

</table>

</div>

"""

        # -----------------------------------
        # Statistics
        # -----------------------------------

        if statistics is not None:

            html += """

<div class="card">

<h2>Statistical Summary</h2>

"""

            html += statistics.to_html()

            html += """

</div>

"""

        # -----------------------------------
        # Insights
        # -----------------------------------

        if insights:

            html += """

<div class="card">

<h2>Insights</h2>

<ul>

"""

            for item in insights:

                html += f"<li>{item}</li>"

            html += """

</ul>

</div>

"""

        # -----------------------------------
        # Charts
        # -----------------------------------

        if chart_files:

            html += """

<div class="card">

<h2>Visualizations</h2>

"""

            for chart in chart_files:

                chart = Path(chart)

                if chart.exists():

                    html += f"""

<iframe
src="{chart.as_posix()}"
width="100%"
height="600"
style="border:none;">
</iframe>

"""

            html += """

</div>

"""

        html += """

<div class="footer">

<hr>

<h3>

Autonomous Data Analyst

</h3>

<p>

AI-Powered Data Analysis & Cleaning Platform

</p>

<p>

Copyright © 2026 Nikhil A.

</p>

</div>

</body>

</html>

"""

        output_file = Path(filename)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as file:

            file.write(html)

        return str(output_file)