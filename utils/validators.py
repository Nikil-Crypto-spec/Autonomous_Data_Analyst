import pandas as pd


def dataframe_exists(df):

    return isinstance(df, pd.DataFrame)


def has_numeric(df):

    return len(
        df.select_dtypes(include="number").columns
    ) > 0


def has_missing(df):

    return df.isnull().sum().sum() > 0


def has_duplicates(df):

    return df.duplicated().sum() > 0