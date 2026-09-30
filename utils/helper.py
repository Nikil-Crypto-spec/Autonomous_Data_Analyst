import pandas as pd

def memory_usage(df):
    """Return DataFrame memory usage in MB."""
    return round(df.memory_usage(deep=True).sum() / (1024 ** 2), 2)


def missing_values(df):
    """Return total missing values."""
    return int(df.isnull().sum().sum())


def duplicate_rows(df):
    """Return duplicate row count."""
    return int(df.duplicated().sum())


def numeric_columns(df):
    return df.select_dtypes(include="number").columns.tolist()


def categorical_columns(df):
    return df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()