"""
profiler.py
-------------------------------------
Dataset Profiling Module
"""

import pandas as pd


class DataProfiler:
    """Provides dataset profiling information."""

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    # ----------------------------------
    # Basic Information
    # ----------------------------------

    def shape(self):
        """Return number of rows and columns."""
        rows, cols = self.df.shape
        return rows, cols

    def columns(self):
        """Return column names."""
        return list(self.df.columns)

    def dtypes(self):
        """Return data types."""
        return self.df.dtypes

    def memory_usage(self):
        """Return memory usage in MB."""
        memory = self.df.memory_usage(deep=True).sum()
        return round(memory / (1024 ** 2), 2)

    # ----------------------------------
    # Missing Values
    # ----------------------------------

    def missing_values(self):
        """Missing values per column."""
        missing = self.df.isnull().sum()

        return pd.DataFrame({
            "Missing Values": missing,
            "Percentage": round(
                (missing / len(self.df)) * 100,
                2
            )
        })

    # ----------------------------------
    # Duplicate Rows
    # ----------------------------------

    def duplicate_rows(self):
        """Number of duplicate rows."""
        return int(self.df.duplicated().sum())

    # ----------------------------------
    # Numeric Columns
    # ----------------------------------

    def numeric_columns(self):
        return list(
            self.df.select_dtypes(
                include="number"
            ).columns
        )

    # ----------------------------------
    # Categorical Columns
    # ----------------------------------

    def categorical_columns(self):
        return list(
            self.df.select_dtypes(
                include=["object", "category"]
            ).columns
        )

    # ----------------------------------
    # Date Columns
    # ----------------------------------

    def datetime_columns(self):
        return list(
            self.df.select_dtypes(
                include=["datetime"]
            ).columns
        )

    # ----------------------------------
    # Unique Values
    # ----------------------------------

    def unique_values(self):
        return self.df.nunique().to_frame(
            "Unique Values"
        )

    # ----------------------------------
    # Statistical Summary
    # ----------------------------------

    def summary(self):
        return self.df.describe(include="all").T

    # ----------------------------------
    # Correlation Matrix
    # ----------------------------------

    def correlation(self):

        numeric = self.df.select_dtypes(
            include="number"
        )

        if numeric.shape[1] < 2:
            return None

        return numeric.corr()

    # ----------------------------------
    # Complete Profile
    # ----------------------------------

    def profile(self):
        """Return all profile information."""

        rows, cols = self.shape()

        return {

            "Rows": rows,

            "Columns": cols,

            "Memory (MB)": self.memory_usage(),

            "Duplicate Rows": self.duplicate_rows(),

            "Numeric Columns":
                len(self.numeric_columns()),

            "Categorical Columns":
                len(self.categorical_columns()),

            "Datetime Columns":
                len(self.datetime_columns())
        }