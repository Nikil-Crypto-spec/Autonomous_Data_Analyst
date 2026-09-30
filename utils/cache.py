import streamlit as st


@st.cache_data
def cache_dataframe(df):

    return df.copy()


@st.cache_data
def cached_describe(df):

    return df.describe()