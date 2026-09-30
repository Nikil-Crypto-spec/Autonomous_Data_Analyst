"""
loader.py
---------------------------------------
Handles loading datasets into pandas.

Supported formats:
- CSV
- TSV
- Excel (.xlsx/.xls)
- JSON
"""

from pathlib import Path
import json
import pandas as pd


class DataLoader:
    """Loads datasets from uploaded files."""

    SUPPORTED_FORMATS = {
        ".csv",
        ".tsv",
        ".xlsx",
        ".xls",
        ".json",
    }

    def __init__(self):
        self.df = None

    def load(self, uploaded_file):
        """
        Load a dataset from a Streamlit UploadedFile.

        Parameters
        ----------
        uploaded_file : UploadedFile

        Returns
        -------
        pandas.DataFrame
        """

        if uploaded_file is None:
            raise ValueError("No file uploaded.")

        suffix = Path(uploaded_file.name).suffix.lower()

        if suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format: {suffix}"
            )

        if suffix == ".csv":
            self.df = pd.read_csv(uploaded_file)

        elif suffix == ".tsv":
            self.df = pd.read_csv(
                uploaded_file,
                sep="\t"
            )

        elif suffix in [".xlsx", ".xls"]:
            self.df = pd.read_excel(uploaded_file)

        elif suffix == ".json":

            try:
                self.df = pd.read_json(uploaded_file)

            except ValueError:

                uploaded_file.seek(0)

                data = json.load(uploaded_file)

                self.df = pd.json_normalize(data)

        return self.df

    def get_dataframe(self):
        """Return loaded dataframe."""
        return self.df

    def is_loaded(self):
        """Returns True if dataset is loaded."""
        return self.df is not None

    @staticmethod
    def supported_formats():
        """Returns supported file extensions."""
        return sorted(DataLoader.SUPPORTED_FORMATS)