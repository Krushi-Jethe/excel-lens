# pylint disable: invalid-name

"""
home.py
"""

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.header("Welcome to Excel-Lens!")

uploaded_file = st.file_uploader("Upload an excel file", type="xlsx")

data_selector = st.container()
sheet, table, images, charts, urls = data_selector.columns([2,2,2,2,2])

if uploaded_file is not None:

    st.session_state.uploaded_file = uploaded_file
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    dropdown_options = all_sheets

    with sheet:
        sheet_selector = st.selectbox("Select sheet", dropdown_options)



input_prompt = st.text_input("Ask anything")

if input_prompt:
    st.text( "received!")