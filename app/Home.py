# pylint disable: invalid-name

"""
home.py
"""
import os
import sys
import openpyxl
import streamlit as st
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from excel_lens import ExcelDataExtractor

st.set_page_config(layout="wide")
st.header("Welcome to Excel-Lens!")

uploaded_file = st.file_uploader("Upload an excel file", type="xlsx")

data_selector = st.container()
sheet, table, images, charts, urls = data_selector.columns([2, 2, 2, 2, 2])

if uploaded_file is not None:
    pandas_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    openpyxl_sheets = openpyxl.load_workbook(uploaded_file)
    extractor = ExcelDataExtractor()
    ext_xl_files = extractor.extract(excel_file=(pandas_sheets, openpyxl_sheets))
    st.session_state.current_file = ext_xl_files
    dropdown_options = pandas_sheets

    with sheet:
        sheet_selector = st.selectbox("Select sheet", dropdown_options)

input_prompt = st.text_input("Ask anything")

if input_prompt:
    st.text("received!")
