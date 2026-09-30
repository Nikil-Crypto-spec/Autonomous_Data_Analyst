"""
cleaner.py
----------------------------------------
Data Cleaning Module
"""

import pandas as pd
import numpy as np


class DataCleaner:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    # ---------------------------------
    # Remove Duplicate Rows
    # ---------------------------------

    def remove_duplicates(self):

        before = len(self.df)

        self.df.drop_duplicates(inplace=True)

        after = len(self.df)

        return before - after

    # ---------------------------------
    # Remove Empty Rows
    # ---------------------------------

    def remove_empty_rows(self):

        before = len(self.df)

        self.df.dropna(how="all", inplace=True)

        after = len(self.df)

        return before - after

    # ---------------------------------
    # Remove Empty Columns
    # ---------------------------------

    def remove_empty_columns(self):

        before = self.df.shape[1]

        self.df.dropna(axis=1, how="all", inplace=True)

        after = self.df.shape[1]

        return before - after

    # ---------------------------------
    # Fill Missing Values
    # ---------------------------------

    def fill_missing(self, strategy="mean"):

        numeric = self.df.select_dtypes(include=np.number).columns

        categorical = self.df.select_dtypes(
            exclude=np.number
        ).columns

        if strategy == "mean":

            for col in numeric:
                self.df[col].fillna(
                    self.df[col].mean(),
                    inplace=True
                )

        elif strategy == "median":

            for col in numeric:
                self.df[col].fillna(
                    self.df[col].median(),
                    inplace=True
                )

        elif strategy == "mode":

            for col in self.df.columns:
                mode = self.df[col].mode()

                if not mode.empty:
                    self.df[col].fillna(
                        mode.iloc[0],
                        inplace=True
                    )

        elif strategy == "zero":

            self.df.fillna(0, inplace=True)

        elif strategy == "unknown":

            for col in categorical:
                self.df[col].fillna(
                    "Unknown",
                    inplace=True
                )

    # ---------------------------------
    # Drop Missing Rows
    # ---------------------------------

    def drop_missing(self):

        before = len(self.df)

        self.df.dropna(inplace=True)

        after = len(self.df)

        return before - after

    # ---------------------------------
    # Rename Columns
    # ---------------------------------

    def clean_column_names(self):

        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )

    # ---------------------------------
    # Trim String Columns
    # ---------------------------------

    def trim_strings(self):

        object_cols = self.df.select_dtypes(
            include="object"
        ).columns

        for col in object_cols:

            self.df[col] = (
                self.df[col]
                .astype(str)
                .str.strip()
            )

    # ---------------------------------
    # Convert Numeric Columns
    # ---------------------------------

    def convert_numeric(self):

        for col in self.df.columns:

            self.df[col] = pd.to_numeric(
                self.df[col],
                errors="ignore"
            )

    # ---------------------------------
    # Remove Outliers (IQR)
    # ---------------------------------

    def remove_outliers(self):

        numeric = self.df.select_dtypes(
            include=np.number
        ).columns

        removed = 0

        for col in numeric:

            q1 = self.df[col].quantile(0.25)
            q3 = self.df[col].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            before = len(self.df)

            self.df = self.df[
                (self.df[col] >= lower)
                &
                (self.df[col] <= upper)
            ]

            removed += before - len(self.df)

        return removed

    # ---------------------------------
    # Reset Index
    # ---------------------------------

    def reset_index(self):

        self.df.reset_index(
            drop=True,
            inplace=True
        )

    # ---------------------------------
    # Automatic Cleaning
    # ---------------------------------

    def auto_clean(self):

        report = {}

        report["Duplicate Rows Removed"] = (
            self.remove_duplicates()
        )

        report["Empty Rows Removed"] = (
            self.remove_empty_rows()
        )

        report["Empty Columns Removed"] = (
            self.remove_empty_columns()
        )

        self.clean_column_names()

        self.trim_strings()

        self.fill_missing("mean")

        report["Outliers Removed"] = (
            self.remove_outliers()
        )

        self.reset_index()

        return report

    # ---------------------------------
    # Return Clean Dataset
    # ---------------------------------

    def get_dataframe(self):

        return self.df