# -*- coding: utf-8 -*-
"""Our Chengdu Story — Streamlit entry point."""

from __future__ import annotations

import streamlit as st

from food_service import get_nearby_food
from shared import build_html, build_payload


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


def _one_query_param(name: str, default: str = "") -> str:
    value = st.query_params.get(name, default)
    if isinstance(value, list):
        return str(value[-1] if value else default)
    return str(value or default)


server_food = st.session_state.get("server_food")
initial_page = "home"

lat_raw = _one_query_param("food_lat")
lon_raw = _one_query_param("food_lon")

if lat_raw and lon_raw:
    try:
        lat = float(lat_raw)
        lon = float(lon_raw)
        radius = float(_one_query_param("food_r", "2"))
        category = _one_query_param("food_cat", "all")
        force = bool(_one_query_param("food_refresh"))

        server_food = get_nearby_food(
            lat, lon, radius, category, force=force
        )
        st.session_state["server_food"] = server_food
        initial_page = "food"
    except (TypeError, ValueError):
        # Keep the previous successful server result, if any.
        initial_page = "food"

payload = build_payload(server_food=server_food, initial_page=initial_page)
HTML = build_html(payload)
FRAME_HEIGHT = 860

import streamlit.components.v1 as components

# HTML is a complete document, not a URL. Always render it with components.html.
components.html(HTML, height=FRAME_HEIGHT, scrolling=False)
