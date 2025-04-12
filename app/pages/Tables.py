# pylint disable: invalid-name

"""
Tables
"""

import streamlit as st

st.set_page_config(layout="wide")

uploaded_file = st.session_state.get("current_file", None)

if uploaded_file:
    dropdown_options = uploaded_file.raw.keys()
    sheet_selector = st.selectbox("Select sheet", list(dropdown_options))

    sheet_data = uploaded_file.sheets.get(sheet_selector)

    if sheet_data and sheet_data.tables:
        tabs = st.tabs(sheet_data.tables.keys())

        for tab, key in zip(tabs, sheet_data.tables.keys()):
            with tab:
                st.dataframe(sheet_data.tables[key])
    else:
        st.warning("No tables found in selected sheet.")
else:
    st.warning("Please upload an Excel file.")
