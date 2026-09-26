# -*- coding: utf-8 -*-
"""Our Chengdu Story — Streamlit entry point."""

from __future__ import annotations

import streamlit as st


st.set_page_config(
    page_title="Our Chengdu Story",
    page_icon="🐼",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Keep Streamlit's own chrome out of the composition.
st.markdown(
    """
    <style>
      html, body, [data-testid="stAppViewContainer"], .stApp {
        margin: 0 !important;
        background: #e6e2d6 !important;
      }
      [data-testid="stHeader"], [data-testid="stToolbar"],
      [data-testid="stDecoration"], #MainMenu, footer { display:none !important; }
      .block-container { padding:0 !important; max-width:none !important; }
      [data-testid="stElementContainer"] { margin:0 !important; }
      iframe { display:block !important; width:100% !important; border:0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

from shared import build_html, build_payload


HTML = build_html(build_payload())
FRAME_HEIGHT = 860

if hasattr(st, "iframe"):
    st.iframe(HTML, width="stretch", height=FRAME_HEIGHT)
else:  # older Streamlit versions
    import streamlit.components.v1 as components

    components.html(HTML, height=FRAME_HEIGHT, scrolling=False)
