# -*- coding: utf-8 -*-
"""Server-side nearby-food lookup.

The phone browser only obtains GPS coordinates. Overpass requests are made by
the Streamlit/Python server, avoiding mobile-browser CORS/network differences.
"""

from __future__ import annotations

import json
import threading
import time
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import streamlit as st


_ALLOWED_CATEGORIES = {
    "all", "sichuan", "hotpot", "snacks", "noodles", "coffee", "dessert"
}
_ALLOWED_RADII = {0.5, 1.0, 2.0, 5.0}

_ENDPOINTS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
)

# Best-effort stale fallback shared within the current Streamlit process.
_STALE: dict[tuple[float, float, float, str], dict[str, Any]] = {}
_STALE_LOCK = threading.Lock()


def _normalise_request(
    lat: float, lon: float, radius_km: float, category: str
) -> tuple[float, float, float, str]:
    lat = max(-90.0, min(90.0, float(lat)))
    lon = max(-180.0, min(180.0, float(lon)))
    radius = float(radius_km)
    if radius not in _ALLOWED_RADII:
        radius = 2.0
    category = str(category or "all").lower()
    if category not in _ALLOWED_CATEGORIES:
        category = "all"

    # ~11 m coordinate grid: accurate enough for walking distance while also
    # improving cache reuse for a family standing in roughly the same place.
    return round(lat, 4), round(lon, 4), radius, category


def _query_text(lat: float, lon: float, radius_km: float, category: str) -> str:
    around = f"(around:{round(radius_km * 1000)},{lat},{lon})"

    if category == "coffee":
        body = f'nwr["amenity"="cafe"]{around};'
    elif category == "dessert":
        body = (
            f'nwr["amenity"~"ice_cream|cafe"]'
            f'["cuisine"~"dessert|ice_cream|cake|bakery",i]{around};'
        )
    elif category == "hotpot":
        body = (
            f'nwr["amenity"="restaurant"]'
            f'["cuisine"~"hot_pot|hotpot",i]{around};'
        )
    elif category == "noodles":
        body = (
            f'nwr["amenity"~"restaurant|fast_food"]'
            f'["cuisine"~"noodle|ramen|noodles",i]{around};'
        )
    elif category == "sichuan":
        body = (
            f'nwr["amenity"="restaurant"]'
            f'["cuisine"~"sichuan|chinese",i]{around};'
        )
    elif category == "snacks":
        body = f'nwr["amenity"~"fast_food|food_court"]{around};'
    else:
        body = (
            f'nwr["amenity"~"restaurant|fast_food|cafe|food_court|ice_cream"]'
            f'{around};'
        )

    return f"[out:json][timeout:25];({body});out center tags;"


def _live_query(
    lat: float, lon: float, radius_km: float, category: str
) -> dict[str, Any]:
    query = _query_text(lat, lon, radius_km, category)
    body = urlencode({"data": query}).encode("utf-8")
    errors: list[str] = []

    for endpoint in _ENDPOINTS:
        try:
            req = Request(
                endpoint,
                data=body,
                method="POST",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "User-Agent": "OurChengduStory/1.0 (private family travel app)",
                    "Accept": "application/json",
                },
            )
            with urlopen(req, timeout=25) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}")
                payload = json.loads(response.read().decode("utf-8"))
                elements = payload.get("elements") or []
                return {
                    "ok": True,
                    "elements": elements,
                    "source": "live",
                    "endpoint": endpoint,
                    "fetched_at": int(time.time()),
                }
        except Exception as exc:  # try the next public endpoint
            errors.append(f"{endpoint}: {type(exc).__name__}")

    raise RuntimeError("; ".join(errors) or "All Overpass endpoints failed")


@st.cache_data(ttl=1800, show_spinner=False)
def _cached_live_query(
    lat: float, lon: float, radius_km: float, category: str
) -> dict[str, Any]:
    return _live_query(lat, lon, radius_km, category)


def get_nearby_food(
    lat: float,
    lon: float,
    radius_km: float,
    category: str,
    *,
    force: bool = False,
) -> dict[str, Any]:
    """Return nearby OSM elements with fresh + stale fallback.

    Successful results are cached server-side for 30 minutes. If all live
    endpoints fail, the most recent successful in-process result for the same
    area/filter is returned as stale data when available.
    """

    lat, lon, radius, category = _normalise_request(
        lat, lon, radius_km, category
    )
    key = (lat, lon, radius, category)

    try:
        result = (
            _live_query(lat, lon, radius, category)
            if force
            else _cached_live_query(lat, lon, radius, category)
        )
        with _STALE_LOCK:
            _STALE[key] = dict(result)
        result = dict(result)
        result.update(
            {
                "lat": lat,
                "lon": lon,
                "radius": radius,
                "category": category,
                "status": "live",
            }
        )
        return result
    except Exception as exc:
        with _STALE_LOCK:
            stale = _STALE.get(key)

        if stale:
            result = dict(stale)
            result.update(
                {
                    "lat": lat,
                    "lon": lon,
                    "radius": radius,
                    "category": category,
                    "status": "stale",
                    "source": "stale",
                }
            )
            return result

        return {
            "ok": False,
            "elements": [],
            "lat": lat,
            "lon": lon,
            "radius": radius,
            "category": category,
            "status": "failed",
            "source": "none",
            "error": type(exc).__name__,
            "fetched_at": int(time.time()),
        }
