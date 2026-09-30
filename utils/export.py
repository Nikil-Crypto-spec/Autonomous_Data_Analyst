import io
import pandas as pd


def export_csv(df):
    return df.to_csv(index=False)


def export_excel(df):
    buffer = io.BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(writer, index=False)

    return buffer.getvalue()


def export_json(df):
    return df.to_json(
        orient="records",
        indent=4
    )


def export_tsv(df):
    return df.to_csv(
        sep="\t",
        index=False
    )