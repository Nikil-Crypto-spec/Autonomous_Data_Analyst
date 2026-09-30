"""
insight_engine.py
---------------------------------------
Rule-Based Dataset Insight Engine
"""

import pandas as pd
import numpy as np


class InsightEngine:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    # =====================================================
    # Dataset Health Score
    # =====================================================

    def health_score(self):

        score = 100

        # Missing values
        missing_percent = (
            self.df.isna().sum().sum()
            / (self.df.shape[0] * self.df.shape[1])
        ) * 100

        score -= min(missing_percent, 30)

        # Duplicate rows
        duplicate_percent = (
            self.df.duplicated().sum()
            / max(len(self.df), 1)
        ) * 100

        score -= min(duplicate_percent, 20)

        return max(0, round(score))

    # =====================================================
    # Recommendations
    # =====================================================

    def recommendations(self):

        rec = []

        if self.df.isna().sum().sum() > 0:
            rec.append("Dataset contains missing values. Consider cleaning them.")

        if self.df.duplicated().sum() > 0:
            rec.append("Duplicate rows detected. Remove duplicates.")

        if len(self.df.columns) > 20:
            rec.append("Dataset has many features. Feature selection may improve analysis.")

        numeric = self.df.select_dtypes(include=np.number)

        if not numeric.empty:
            corr = numeric.corr().abs()

            upper = corr.where(
                np.triu(np.ones(corr.shape), k=1).astype(bool)
            )

            if (upper > 0.90).any().any():
                rec.append("Highly correlated features detected.")

        return rec

    # =====================================================
    # Missing Value Insights
    # =====================================================

    def missing_value_insights(self):

        missing = self.df.isnull().sum()

        result = []

        for col, count in missing.items():

            if count > 0:

                result.append(
                    f"{col}: {count} missing values"
                )

        return result

    # =====================================================
    # Duplicate Insights
    # =====================================================

    def duplicate_insights(self):

        dup = self.df.duplicated().sum()

        if dup > 0:
            return [f"{dup} duplicate rows found."]

        return []

    # =====================================================
    # High Correlation
    # =====================================================

    def high_correlation(self):

        numeric = self.df.select_dtypes(include=np.number)

        if numeric.empty:
            return pd.DataFrame()

        corr = numeric.corr().abs()

        upper = corr.where(
            np.triu(np.ones(corr.shape), k=1).astype(bool)
        )

        rows = []

        for col in upper.columns:

            for idx in upper.index:

                value = upper.loc[idx, col]

                if pd.notna(value) and value >= 0.80:

                    rows.append(
                        {
                            "Feature 1": idx,
                            "Feature 2": col,
                            "Correlation": round(value, 3),
                        }
                    )

        return pd.DataFrame(rows)

    # =====================================================
    # Outlier Summary
    # =====================================================

    def outlier_summary(self):

        numeric = self.df.select_dtypes(include=np.number)

        rows = []

        for col in numeric.columns:

            q1 = numeric[col].quantile(0.25)
            q3 = numeric[col].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            outliers = (
                (numeric[col] < lower)
                | (numeric[col] > upper)
            ).sum()

            rows.append(
                {
                    "Column": col,
                    "Outliers": int(outliers),
                }
            )

        return pd.DataFrame(rows)

    # =====================================================
    # Summary
    # =====================================================

    def summary(self):

        return {

            "Rows": len(self.df),

            "Columns": len(self.df.columns),

            "Missing Values": int(
                self.df.isna().sum().sum()
            ),

            "Duplicate Rows": int(
                self.df.duplicated().sum()
            ),

            "Numeric Columns": len(
                self.df.select_dtypes(include=np.number).columns
            ),

            "Categorical Columns": len(
                self.df.select_dtypes(
                    exclude=np.number
                ).columns
            ),
        }