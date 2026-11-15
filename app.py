from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AstroVibe", page_icon="🛰️", layout="wide", initial_sidebar_state="collapsed")

# Remove Streamlit's own padding, header and footer so the tool fills the page.
st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden; height: 0;}
      .block-container {padding: 0 !important; max-width: 100% !important;}
      iframe {border: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")
components.html(html, height=1400, scrolling=True)
