# pylint disable: invalid-name

"""
home.py
"""

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

uploaded_file = st.session_state.get("uploaded_file", None)

if uploaded_file is not None:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    dropdown_options = all_sheets
    sheet_selector = st.selectbox("Select sheet", dropdown_options)

tab1, tab2, tab3 = st.tabs(["table_1","table_2","table_3"])

with tab1:
    st.dataframe(pd.read_excel("../files/dummy_excel_1.xlsx"))

with tab2:
    st.dataframe(pd.read_excel("../files/dummy_excel_1.xlsx"))

with tab3:
    st.dataframe(pd.read_excel("../files/dummy_excel_1.xlsx"))
