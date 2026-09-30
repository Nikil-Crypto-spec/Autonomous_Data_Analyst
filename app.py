import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io
import os

from modules import (
    DataLoader,
    DataProfiler,
    DataCleaner,
    StatisticsEngine,
    Visualizer,
    InsightEngine,
    ReportGenerator,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Autonomous Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# LOAD CSS
# ==========================================================

def load_css():

    try:

        with open("style.css") as css:

            st.markdown(
                f"<style>{css.read()}</style>",
                unsafe_allow_html=True
            )

    except FileNotFoundError:

        pass


load_css()


# ==========================================================
# SESSION STATE
# ==========================================================

if "df" not in st.session_state:

    st.session_state.df = None

if "clean_df" not in st.session_state:

    st.session_state.clean_df = None

if "uploaded" not in st.session_state:

    st.session_state.uploaded = False


# ==========================================================
# PAGE FUNCTIONS
# ==========================================================

def home_page():

    st.title("📊 Autonomous Data Analyst")

    st.markdown("""
Welcome to **Autonomous Data Analyst**.

This application provides:

- 📂 Dataset Upload
- 👀 Dataset Preview
- 📋 Data Profiling
- 🧹 Automatic Cleaning
- 📊 Statistical Analysis
- 📈 Interactive Visualizations
- 💡 Rule-Based Insights
- 📄 HTML Report Generation

---
""")

    col1, col2, col3 = st.columns(3)

    col1.metric("Supported Formats", "CSV / Excel")

    col2.metric("Charts", "12+")

    col3.metric("Reports", "HTML")


# ---------------------------------------------------------

def upload_page():

    st.title("📂 Upload Dataset")

    uploaded_file = st.file_uploader(

        "Upload your dataset",

        type=[
            "csv",
            "xlsx",
            "xls",
            "tsv",
            "json"
        ]

    )

    if uploaded_file:

        loader = DataLoader()

        try:

            df = loader.load(uploaded_file)

            st.session_state.df = df

            st.session_state.clean_df = df.copy()

            st.session_state.uploaded = True

            st.success("Dataset Loaded Successfully.")

            c1, c2, c3 = st.columns(3)

            c1.metric("Rows", df.shape[0])

            c2.metric("Columns", df.shape[1])

            c3.metric(
                "Missing",
                int(df.isnull().sum().sum())
            )

        except Exception as e:

            st.error(e)


# ---------------------------------------------------------
def preview_page():

    st.title("👀 Dataset Preview")

    df = st.session_state.df

    st.success("Dataset Loaded Successfully")

    # ==========================================
    # Dataset Metrics
    # ==========================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", df.shape[0])

    c2.metric("Columns", df.shape[1])

    c3.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

    c4.metric(
        "Duplicate Rows",
        int(df.duplicated().sum())
    )

    st.divider()

    # ==========================================
    # Tabs
    # ==========================================

    tab1, tab2, tab3, tab4 = st.tabs(

        [

            "Dataset",

            "Columns",

            "Data Types",

            "Sample"

        ]

    )

    # ==========================================
    # Dataset
    # ==========================================

    with tab1:

        st.subheader("Dataset")

        rows = st.slider(

            "Rows to Display",

            min_value=5,

            max_value=min(
                len(df),
                100
            ),

            value=10

        )

        st.dataframe(

            df.head(rows),

            use_container_width=True,

            height=500

        )

    # ==========================================
    # Columns
    # ==========================================

    with tab2:

        st.subheader("Columns")

        column_df = pd.DataFrame({

            "Column Name": df.columns,

            "Data Type": df.dtypes.astype(str),

            "Missing":

                df.isnull().sum().values,

            "Unique":

                df.nunique().values

        })

        st.dataframe(

            column_df,

            use_container_width=True

        )

    # ==========================================
    # Data Types
    # ==========================================

    with tab3:

        dtype_df = pd.DataFrame({

            "Column": df.columns,

            "Type": df.dtypes.astype(str)

        })

        st.dataframe(

            dtype_df,

            use_container_width=True

        )

        st.write()

        st.subheader("Data Type Count")

        st.dataframe(

            dtype_df["Type"]

            .value_counts()

            .reset_index()

            .rename(

                columns={

                    "index": "Type",

                    "Type": "Count"

                }

            ),

            use_container_width=True

        )

    # ==========================================
    # Sample
    # ==========================================

    with tab4:

        c1, c2 = st.columns(2)

        with c1:

            st.subheader("First 5 Rows")

            st.dataframe(

                df.head(),

                use_container_width=True

            )

        with c2:

            st.subheader("Last 5 Rows")

            st.dataframe(

                df.tail(),

                use_container_width=True

            )

        st.subheader("Random Sample")

        sample_size = min(10, len(df))

        st.dataframe(

            df.sample(sample_size),

            use_container_width=True

        )

    
# ---------------------------------------------------------
def profile_page():

    st.title("📋 Data Profile")

    df = st.session_state.df

    profiler = DataProfiler(df)

    profile = profiler.profile()

    # ==================================================
    # KPI Cards
    # ==================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", profile["Rows"])

    c2.metric("Columns", profile["Columns"])

    c3.metric(
        "Memory",
        f"{profile['Memory (MB)']} MB"
    )

    c4.metric(
        "Duplicates",
        profile["Duplicate Rows"]
    )

    st.divider()

    # ==================================================
    # Tabs
    # ==================================================

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(

        [

            "Overview",

            "Missing Values",

            "Unique Values",

            "Statistics",

            "Correlation",

            "Data Types"

        ]

    )

    # ==================================================
    # Overview
    # ==================================================

    with tab1:

        st.subheader("Dataset Overview")

        overview = pd.DataFrame({

            "Metric": [

                "Rows",

                "Columns",

                "Memory Usage (MB)",

                "Duplicate Rows",

                "Numeric Columns",

                "Categorical Columns",

                "Datetime Columns"

            ],

            "Value": [

                profile["Rows"],

                profile["Columns"],

                profile["Memory (MB)"],

                profile["Duplicate Rows"],

                profile["Numeric Columns"],

                profile["Categorical Columns"],

                profile["Datetime Columns"]

            ]

        })

        st.dataframe(

            overview,

            use_container_width=True

        )

    # ==================================================
    # Missing Values
    # ==================================================

    with tab2:

        st.subheader("Missing Values")

        missing = profiler.missing_values()

        st.dataframe(

            missing,

            use_container_width=True

        )

        st.bar_chart(

            missing["Missing Values"]

        )

    # ==================================================
    # Unique Values
    # ==================================================

    with tab3:

        st.subheader("Unique Values")

        unique = profiler.unique_values()

        st.dataframe(

            unique,

            use_container_width=True

        )

    # ==================================================
    # Statistics
    # ==================================================

    with tab4:

        st.subheader("Descriptive Statistics")

        st.dataframe(

            profiler.summary(),

            use_container_width=True

        )

    # ==================================================
    # Correlation
    # ==================================================

    with tab5:

        st.subheader("Correlation Matrix")

        corr = profiler.correlation()

        if corr is None:

            st.info(

                "Correlation requires at least two numeric columns."

            )

        else:

            st.dataframe(

                corr,

                use_container_width=True

            )

    # ==================================================
    # Data Types
    # ==================================================

    with tab6:

        dtype_df = pd.DataFrame({

            "Column":

                profiler.columns(),

            "Data Type":

                profiler.dtypes().astype(str)

        })

        st.dataframe(

            dtype_df,

            use_container_width=True

        )

# ---------------------------------------------------------

def cleaning_page():

    st.title("🧹 Data Cleaning")

    df = st.session_state.clean_df.copy()

    cleaner = DataCleaner(df)

    st.info(
        "Choose a cleaning operation and click the corresponding button."
    )

    st.divider()

    # =====================================================
    # Cleaning Options
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        missing_strategy = st.selectbox(

            "Missing Value Strategy",

            [

                "mean",

                "median",

                "mode",

                "zero",

                "unknown"

            ]

        )

    with col2:

        remove_outliers = st.checkbox(

            "Remove Outliers (IQR)",

            value=False

        )

    st.divider()

    # =====================================================
    # Cleaning Buttons
    # =====================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button("Remove Duplicates"):

            removed = cleaner.remove_duplicates()

            st.session_state.clean_df = cleaner.get_dataframe()

            st.success(
                f"{removed} duplicate rows removed."
            )

    with c2:

        if st.button("Remove Empty Rows"):

            removed = cleaner.remove_empty_rows()

            st.session_state.clean_df = cleaner.get_dataframe()

            st.success(
                f"{removed} empty rows removed."
            )

    with c3:

        if st.button("Remove Empty Columns"):

            removed = cleaner.remove_empty_columns()

            st.session_state.clean_df = cleaner.get_dataframe()

            st.success(
                f"{removed} empty columns removed."
            )

    st.divider()

    c4, c5, c6 = st.columns(3)

    with c4:

        if st.button("Fill Missing Values"):

            cleaner.fill_missing(missing_strategy)

            st.session_state.clean_df = cleaner.get_dataframe()

            st.success(
                f"Missing values filled using '{missing_strategy}'."
            )

    with c5:

        if st.button("Clean Column Names"):

            cleaner.clean_column_names()

            st.session_state.clean_df = cleaner.get_dataframe()

            st.success("Column names cleaned.")

    with c6:

        if st.button("Trim Strings"):

            cleaner.trim_strings()

            st.session_state.clean_df = cleaner.get_dataframe()

            st.success("String values trimmed.")

    st.divider()

    c7, c8 = st.columns(2)

    with c7:

        if st.button("Automatic Cleaning"):

            report = cleaner.auto_clean()

            st.session_state.clean_df = cleaner.get_dataframe()

            st.success("Automatic cleaning completed.")

            st.write(report)

    with c8:

        if st.button("Reset Cleaned Dataset"):

            st.session_state.clean_df = st.session_state.df.copy()

            st.success("Dataset restored.")

    if remove_outliers:

        if st.button("Remove Outliers"):

            removed = cleaner.remove_outliers()

            cleaner.reset_index()

            st.session_state.clean_df = cleaner.get_dataframe()

            st.success(
                f"{removed} outliers removed."
            )

    st.divider()

    # =====================================================
    # Dataset Comparison
    # =====================================================

    st.subheader("Dataset Comparison")

    original = st.session_state.df

    cleaned = st.session_state.clean_df

    left, right = st.columns(2)

    with left:

        st.markdown("### Original Dataset")

        st.dataframe(

            original.head(),

            use_container_width=True,

            height=300

        )

    with right:

        st.markdown("### Cleaned Dataset")

        st.dataframe(

            cleaned.head(),

            use_container_width=True,

            height=300

        )

    st.divider()

    # =====================================================
    # Cleaning Summary
    # =====================================================

    col1, col2, col3 = st.columns(3)

    col1.metric(

        "Rows",

        cleaned.shape[0]

    )

    col2.metric(

        "Columns",

        cleaned.shape[1]

    )

    col3.metric(

        "Missing Values",

        int(cleaned.isnull().sum().sum())

    )


# ---------------------------------------------------------

def statistics_page():

    st.title("📊 Statistical Analysis")

    df = st.session_state.clean_df

    stats = StatisticsEngine(df)

    summary = stats.summary()

    # ====================================================
    # KPI Cards
    # ====================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Rows",
        summary["Rows"]
    )

    c2.metric(
        "Columns",
        summary["Columns"]
    )

    c3.metric(
        "Missing",
        summary["Missing Values"]
    )

    c4.metric(
        "Duplicates",
        summary["Duplicate Rows"]
    )

    st.divider()

    # ====================================================
    # Tabs
    # ====================================================

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(

        [

            "Summary",

            "Central Tendency",

            "Dispersion",

            "Distribution",

            "Correlation",

            "Frequency",

            "Outliers"

        ]

    )

    # ====================================================
    # Summary
    # ====================================================

    with tab1:

        st.subheader("Descriptive Statistics")

        st.dataframe(

            stats.describe(),

            use_container_width=True

        )

    # ====================================================
    # Mean / Median / Mode
    # ====================================================

    with tab2:

        st.subheader("Mean")

        st.dataframe(

            stats.mean(),

            use_container_width=True

        )

        st.subheader("Median")

        st.dataframe(

            stats.median(),

            use_container_width=True

        )

        st.subheader("Mode")

        st.dataframe(

            stats.mode(),

            use_container_width=True

        )

    # ====================================================
    # Dispersion
    # ====================================================

    with tab3:

        st.subheader("Variance")

        st.dataframe(

            stats.variance(),

            use_container_width=True

        )

        st.subheader("Standard Deviation")

        st.dataframe(

            stats.standard_deviation(),

            use_container_width=True

        )

        st.subheader("Range")

        st.dataframe(

            stats.data_range(),

            use_container_width=True

        )

        st.subheader("Quantiles")

        st.dataframe(

            stats.quantiles(),

            use_container_width=True

        )

    # ====================================================
    # Distribution
    # ====================================================

    with tab4:

        st.subheader("Skewness")

        st.dataframe(

            stats.skewness(),

            use_container_width=True

        )

        st.subheader("Kurtosis")

        st.dataframe(

            stats.kurtosis(),

            use_container_width=True

        )

    # ====================================================
    # Correlation
    # ====================================================

    with tab5:

        st.subheader("Correlation Matrix")

        st.dataframe(

            stats.correlation(),

            use_container_width=True

        )

        st.subheader("Covariance Matrix")

        st.dataframe(

            stats.covariance(),

            use_container_width=True

        )

    # ====================================================
    # Frequency
    # ====================================================

    with tab6:

        categorical = stats.categorical_columns()

        if categorical:

            column = st.selectbox(

                "Select Column",

                categorical

            )

            st.dataframe(

                stats.frequency(column),

                use_container_width=True

            )

        else:

            st.info(

                "No categorical columns available."

            )

    # ====================================================
    # Outliers
    # ====================================================

    with tab7:

        st.subheader("Outlier Summary")

        st.dataframe(

            stats.outlier_summary(),

            use_container_width=True

        )

# ---------------------------------------------------------

def visualization_page():

    st.title("📈 Data Visualizations")

    df = st.session_state.clean_df

    visualizer = Visualizer(df)

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    st.sidebar.subheader("Chart Configuration")

    chart_type = st.selectbox(

        "Chart Type",

        [

            "Histogram",

            "Bar Chart",

            "Line Chart",

            "Scatter Plot",

            "Box Plot",

            "Violin Plot",

            "Pie Chart",

            "Area Chart",

            "Heatmap",

            "Bubble Chart",

            "Density Heatmap",

            "Sunburst",

            "Treemap"

        ]

    )

    x = None
    y = None
    color = None
    size = None

    if chart_type != "Heatmap":

        x = st.selectbox(

            "X Axis",

            df.columns

        )

    if chart_type in [

        "Scatter Plot",

        "Line Chart",

        "Bar Chart",

        "Area Chart",

        "Bubble Chart"

    ]:

        y = st.selectbox(

            "Y Axis",

            numeric_columns

        )

    if chart_type in [

        "Scatter Plot",

        "Bubble Chart",

        "Bar Chart",

        "Histogram",

        "Box Plot",

        "Violin Plot"

    ]:

        color = st.selectbox(

            "Color",

            [None] + list(df.columns)

        )

    if chart_type == "Bubble Chart":

        size = st.selectbox(

            "Bubble Size",

            numeric_columns

        )

    st.divider()

    fig = None

    try:

        if chart_type == "Histogram":

            fig = visualizer.histogram(

                x,

                color=color

            )

        elif chart_type == "Bar Chart":

            fig = visualizer.bar_chart(

                x,

                y,

                color=color

            )

        elif chart_type == "Line Chart":

            fig = visualizer.line_chart(

                x,

                y

            )

        elif chart_type == "Scatter Plot":

            fig = visualizer.scatter_plot(

                x,

                y,

                color=color

            )

        elif chart_type == "Box Plot":

            fig = visualizer.box_plot(

                x,

                color=color

            )

        elif chart_type == "Violin Plot":

            fig = visualizer.violin_plot(

                x,

                color=color

            )

        elif chart_type == "Pie Chart":

            fig = visualizer.pie_chart(

                x

            )

        elif chart_type == "Area Chart":

            fig = visualizer.area_chart(

                x,

                y

            )

        elif chart_type == "Heatmap":

            fig = visualizer.heatmap()

        elif chart_type == "Bubble Chart":

            fig = visualizer.bubble_chart(

                x,

                y,

                size=size,

                color=color

            )

        elif chart_type == "Density Heatmap":

            fig = visualizer.density_heatmap(

                x,

                y

            )

        elif chart_type == "Sunburst":

            fig = visualizer.sunburst(

                x

            )

        elif chart_type == "Treemap":

            fig = visualizer.treemap(

                x

            )

        if fig:

            st.plotly_chart(

                fig,

                use_container_width=True

            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button("Save Chart as HTML"):

                    filename = f"reports/charts/{chart_type.lower().replace(' ','_')}.html"

                    visualizer.save_html(

                        fig,

                        filename

                    )

                    st.success(

                        f"Chart saved to {filename}"

                    )

            with col2:

                st.download_button(

                    "Download Chart HTML",

                    fig.to_html(),

                    file_name=f"{chart_type}.html",

                    mime="text/html"

                )

    except Exception as e:

        st.error(e)


# ---------------------------------------------------------

def insights_page():

    st.title("💡 Dataset Insights")

    df = st.session_state.clean_df

    engine = InsightEngine(df)

    st.info(
        "These insights are generated using rule-based data analysis."
    )

    st.divider()

    # ======================================================
    # Health Score
    # ======================================================

    score = engine.health_score()

    st.metric(
        "Dataset Health Score",
        f"{score}/100"
    )

    st.progress(score / 100)

    st.divider()

    # ======================================================
    # Tabs
    # ======================================================

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Recommendations",
            "Missing Values",
            "Duplicates",
            "Correlations",
            "Outliers",
            "Summary"
        ]
    )

    # ======================================================
    # Recommendations
    # ======================================================

    with tab1:

        recommendations = engine.recommendations()

        if recommendations:

            for item in recommendations:
                st.success(item)

        else:

            st.success(
                "No major issues detected."
            )

    # ======================================================
    # Missing Values
    # ======================================================

    with tab2:

        missing = engine.missing_value_insights()

        if missing:

            for item in missing:
                st.warning(item)

        else:

            st.success(
                "No missing values found."
            )

    # ======================================================
    # Duplicate Rows
    # ======================================================

    with tab3:

        duplicates = engine.duplicate_insights()

        if duplicates:

            for item in duplicates:
                st.warning(item)

        else:

            st.success(
                "No duplicate rows detected."
            )

    # ======================================================
    # High Correlations
    # ======================================================

    with tab4:

        correlations = engine.high_correlation()

        if not correlations.empty:

            st.dataframe(
                correlations,
                use_container_width=True
            )

        else:

            st.success(
                "No highly correlated features."
            )

    # ======================================================
    # Outliers
    # ======================================================

    with tab5:

        outliers = engine.outlier_summary()

        st.dataframe(
            outliers,
            use_container_width=True
        )

    # ======================================================
    # Summary
    # ======================================================

    with tab6:

        summary = engine.summary()

        if isinstance(summary, dict):

            summary_df = pd.DataFrame(
                list(summary.items()),
                columns=["Metric", "Value"]
            )

            st.dataframe(
                summary_df,
                use_container_width=True
            )

        else:

            st.write(summary)


# ---------------------------------------------------------

from pathlib import Path

def report_page():

    st.title("📄 HTML Report")

    df = st.session_state.clean_df

    if df is None:

        st.info("Upload a dataset first to generate a report.")

        return

    st.write(
        "Generate a comprehensive HTML report for the cleaned dataset."
    )

    st.divider()

    report_name = st.text_input(
        "Report Name",
        value="data_analysis_report"
    )

    include_statistics = st.checkbox(
        "Include Statistics",
        value=True
    )

    include_insights = st.checkbox(
        "Include Insights",
        value=True
    )

    output_dir = Path("reports/html")
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / f"{report_name}.html"

    if st.button("Generate HTML Report"):

        with st.spinner("Generating report..."):

            try:

                stats_engine = StatisticsEngine(df)
                insight_engine = InsightEngine(df)

                statistics = (
                    stats_engine.describe()
                    if include_statistics
                    else None
                )

                insights = (
                    insight_engine.recommendations()
                    if include_insights
                    else None
                )

                generator = ReportGenerator(df)

                generator.generate(
                    filename=str(report_path),
                    statistics=statistics,
                    insights=insights
                )

                st.success("Report generated successfully.")

                with open(report_path, "r", encoding="utf-8") as file:

                    html = file.read()

                st.subheader("Report Preview")

                st.components.v1.html(
                    html,
                    height=700,
                    scrolling=True
                )

                st.download_button(
                    label="Download HTML Report",
                    data=html,
                    file_name=report_path.name,
                    mime="text/html"
                )

            except Exception as e:

                st.error(f"Error generating report: {e}")

# ---------------------------------------------------------

import io

def download_page():

    st.title("⬇ Download Center")

    st.write(
        "Download your cleaned dataset and generated reports."
    )

    st.divider()

    df = st.session_state.clean_df

    # ===============================================
    # Dataset Downloads
    # ===============================================

    st.subheader("📊 Dataset Export")

    c1, c2 = st.columns(2)

    # CSV
    with c1:

        csv = df.to_csv(index=False)

        st.download_button(

            "⬇ Download CSV",

            data=csv,

            file_name="cleaned_dataset.csv",

            mime="text/csv"

        )

    # Excel
    with c2:

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False
            )

        st.download_button(

            "⬇ Download Excel",

            data=excel_buffer.getvalue(),

            file_name="cleaned_dataset.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )

    st.divider()

    # ===============================================
    # TSV
    # ===============================================

    c3, c4 = st.columns(2)

    with c3:

        tsv = df.to_csv(

            sep="\t",

            index=False

        )

        st.download_button(

            "⬇ Download TSV",

            data=tsv,

            file_name="cleaned_dataset.tsv",

            mime="text/tab-separated-values"

        )

    # JSON
    with c4:

        json_data = df.to_json(

            orient="records",

            indent=4

        )

        st.download_button(

            "⬇ Download JSON",

            data=json_data,

            file_name="cleaned_dataset.json",

            mime="application/json"

        )

    st.divider()

    # ===============================================
    # Report Download
    # ===============================================

    st.subheader("📄 HTML Reports")

    report_dir = "reports/html"

    if os.path.exists(report_dir):

        reports = [

            file

            for file in os.listdir(report_dir)

            if file.endswith(".html")

        ]

        if reports:

            selected = st.selectbox(

                "Available Reports",

                reports

            )

            path = os.path.join(

                report_dir,

                selected

            )

            with open(

                path,

                "r",

                encoding="utf-8"

            ) as f:

                report_html = f.read()

            st.download_button(

                "⬇ Download Report",

                data=report_html,

                file_name=selected,

                mime="text/html"

            )

        else:

            st.info(

                "No reports available."

            )

    else:

        st.info(

            "Report directory not found."

        )

    st.divider()

    # ===============================================
    # Dataset Summary
    # ===============================================

    st.subheader("Current Dataset")

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Rows",

        df.shape[0]

    )

    c2.metric(

        "Columns",

        df.shape[1]

    )

    c3.metric(

        "Missing Values",

        int(df.isnull().sum().sum())

    )

    st.success("Export completed successfully.")


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("📊 Autonomous Data Analyst")

st.sidebar.markdown("---")

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Home",

        "📂 Upload Dataset",

        "👀 Data Preview",

        "📋 Data Profile",

        "🧹 Data Cleaning",

        "📊 Statistics",

        "📈 Visualizations",

        "💡 Insights",

        "📄 HTML Report",

        "⬇ Download"

    ]

)

st.sidebar.markdown("---")

st.sidebar.success(

"""
Supported Formats

✔ CSV

✔ Excel

✔ TSV

✔ JSON
"""
)

st.sidebar.markdown("---")

st.sidebar.caption(

"© 2026 Nikhil Reddy."

)


# ==========================================================
# CHECK DATASET
# ==========================================================

def dataset_required():

    if st.session_state.df is None:

        st.warning(
            "Please upload a dataset first."
        )

        st.stop()


# ==========================================================
# NAVIGATION
# ==========================================================

if page == "🏠 Home":

    home_page()

elif page == "📂 Upload Dataset":

    upload_page()

elif page == "👀 Data Preview":

    dataset_required()

    preview_page()

elif page == "📋 Data Profile":

    dataset_required()

    profile_page()

elif page == "🧹 Data Cleaning":

    dataset_required()

    cleaning_page()

elif page == "📊 Statistics":

    dataset_required()

    statistics_page()

elif page == "📈 Visualizations":

    dataset_required()

    visualization_page()

elif page == "💡 Insights":

    dataset_required()

    insights_page()

elif page == "📄 HTML Report":

    dataset_required()

    report_page()

elif page == "⬇ Download":

    dataset_required()

    download_page()

st.markdown(
    """
    <div class="footer">
        <hr>
        <p><strong>Autonomous Data Analyst</strong></p>
        <p>AI-Powered Data Analysis & Cleaning Platform</p>
        <p>Copyright © 2026 Nikhil Reddy. All Rights Reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)