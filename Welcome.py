#Welcome 👋
import streamlit as st

st.set_page_config(page_title = "Welcome")

st.title("Paper Classifier for MNE")
st.write(
    "This is an initial prototype. Use the sidebar to choose the input type"
)

st.write(
    "This version currently supports only single input. Will support file upload and CSV generation soon."
)
