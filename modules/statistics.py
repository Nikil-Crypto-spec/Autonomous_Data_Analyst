"""
statistics.py
---------------------------------------
Statistical Analysis Module
"""

import pandas as pd
import numpy as np


class StatisticsEngine:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    # -----------------------------------
    # Basic Summary
    # -----------------------------------

    def describe(self):
        return self.df.describe(include="all").T

    # -----------------------------------
    # Mean
    # -----------------------------------

    def mean(self):
        return self.df.mean(numeric_only=True)

    # -----------------------------------
    # Median
    # -----------------------------------

    def median(self):
        return self.df.median(numeric_only=True)

    # -----------------------------------
    # Mode
    # -----------------------------------

    def mode(self):
        return self.df.mode()

    # -----------------------------------
    # Variance
    # -----------------------------------

    def variance(self):
        return self.df.var(numeric_only=True)

    # -----------------------------------
    # Standard Deviation
    # -----------------------------------

    def standard_deviation(self):
        return self.df.std(numeric_only=True)

    # -----------------------------------
    # Minimum
    # -----------------------------------

    def minimum(self):
        return self.df.min(numeric_only=True)

    # -----------------------------------
    # Maximum
    # -----------------------------------

    def maximum(self):
        return self.df.max(numeric_only=True)

    # -----------------------------------
    # Range
    # -----------------------------------

    def data_range(self):
        return (
            self.maximum() -
            self.minimum()
        )

    # -----------------------------------
    # Quantiles
    # -----------------------------------

    def quantiles(self):
        return self.df.quantile(
            [0.25, 0.50, 0.75],
            numeric_only=True
        )

    # -----------------------------------
    # Skewness
    # -----------------------------------

    def skewness(self):
        return self.df.skew(numeric_only=True)

    # -----------------------------------
    # Kurtosis
    # -----------------------------------

    def kurtosis(self):
        return self.df.kurt(numeric_only=True)

    # -----------------------------------
    # Correlation
    # -----------------------------------

    def correlation(self):
        return self.df.corr(
            numeric_only=True
        )

    # -----------------------------------
    # Covariance
    # -----------------------------------

    def covariance(self):
        return self.df.cov(
            numeric_only=True
        )

    # -----------------------------------
    # Missing Values
    # -----------------------------------

    def missing_values(self):

        return pd.DataFrame({

            "Missing Values":
                self.df.isnull().sum(),

            "Percentage":
                round(
                    self.df.isnull().mean() * 100,
                    2
                )

        })

    # -----------------------------------
    # Unique Values
    # -----------------------------------

    def unique_values(self):

        return self.df.nunique()

    # -----------------------------------
    # Frequency Table
    # -----------------------------------

    def frequency(self, column):

        return self.df[column].value_counts()

    # -----------------------------------
    # Numeric Columns
    # -----------------------------------

    def numeric_columns(self):

        return list(

            self.df.select_dtypes(

                include=np.number

            ).columns

        )

    # -----------------------------------
    # Categorical Columns
    # -----------------------------------

    def categorical_columns(self):

        return list(

            self.df.select_dtypes(

                exclude=np.number

            ).columns

        )

    # -----------------------------------
    # Outlier Summary
    # -----------------------------------

    def outlier_summary(self):

        result = {}

        numeric = self.numeric_columns()

        for col in numeric:

            q1 = self.df[col].quantile(.25)
            q3 = self.df[col].quantile(.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            count = self.df[
                (self.df[col] < lower) |
                (self.df[col] > upper)
            ].shape[0]

            result[col] = count

        return pd.DataFrame(
            result.items(),
            columns=["Column", "Outliers"]
        )

    # -----------------------------------
    # Complete Report
    # -----------------------------------

    def summary(self):

        return {

            "Rows": self.df.shape[0],

            "Columns": self.df.shape[1],

            "Numeric Columns":
                len(self.numeric_columns()),

            "Categorical Columns":
                len(self.categorical_columns()),

            "Missing Values":
                int(
                    self.df.isnull().sum().sum()
                ),

            "Duplicate Rows":
                int(
                    self.df.duplicated().sum()
                )

        }