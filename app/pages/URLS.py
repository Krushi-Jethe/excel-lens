# pylint disable: invalid-name


import streamlit as st

st.set_page_config(layout="wide")

uploaded_file = st.session_state.get("current_file", None)

if uploaded_file:

    dropdown_options = uploaded_file.raw.keys()
    sheet_selector = st.selectbox("Select sheet", list(dropdown_options))

    for url_dict in uploaded_file.sheets[sheet_selector].urls:
        for key, value in url_dict.items():
            st.markdown(f"[{key}]({value})", unsafe_allow_html=True)
else:
    st.warning("Please upload an Excel file.")
