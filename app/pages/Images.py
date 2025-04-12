# pylint disable: invalid-name

"""
Images
"""
import streamlit as st

st.set_page_config(layout="wide")

uploaded_file = st.session_state.get("current_file", None)

if uploaded_file:

    dropdown_options = uploaded_file.raw.keys()
    sheet_selector = st.selectbox("Select sheet", list(dropdown_options))

    for i, img in enumerate(uploaded_file.sheets[sheet_selector].images):
        resized_img = img.resize((256, 256))
        st.image(resized_img, caption=f"Image {i+1}", use_container_width=False)

else:
    st.warning("Please upload an Excel file.")
