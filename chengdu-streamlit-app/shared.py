# -*- coding: utf-8 -*-
"""Shared data, asset loading, and exact document assembly."""

from __future__ import annotations

import base64
import json
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

import streamlit as st


def _secret(name: str, default: str = "") -> str:
    """Read optional Streamlit secrets without making local/demo mode fail."""
    try:
        return str(st.secrets.get(name, default) or default)
    except Exception:
        return default


def _safe_supabase_client_key() -> str:
    """Only expose a browser-safe Supabase publishable/legacy anon key."""
    key = _secret("SUPABASE_PUBLISHABLE_KEY") or _secret("SUPABASE_ANON_KEY")
    lowered = key.lower()
    if not key or lowered.startswith("sb_secret_") or "service_role" in lowered:
        return ""
    # Legacy JWT keys expose their role in the payload. Reject service-role JWTs.
    if key.count(".") == 2:
        try:
            payload = key.split(".")[1]
            payload += "=" * (-len(payload) % 4)
            claims = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))
            if claims.get("role") == "service_role":
                return ""
        except Exception:
            pass
    return key


APP_CONFIG = {
    "supabase_url": _secret("SUPABASE_URL"),
    "supabase_key": _safe_supabase_client_key(),
    "trip_id": _secret("SUPABASE_TRIP_ID", "chengdu-family-2026"),
}


def commons(filename: str, width: int = 1400) -> str:
    """Stable Wikimedia redirect URL with an output width hint."""
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(filename)}?width={width}"


IMG = {
    # Home hero / shared images
    "panda_portrait": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=1600&q=92",
    "panda_bamboo": "https://images.unsplash.com/photo-1508264165352-258a6c1915d1?auto=format&fit=crop&w=1500&q=90",

    # Route imagery — intentionally curated so the accordion feels scenic,
    # editorial and varied rather than repeating the same few thumbnails.
    "taikoo_night": commons("Sino-Ocean Taikoo Li Chengdu.jpg", 1200),
    "taikoo_day": commons("Sino-Ocean Taikoo Li Chengdu 12.jpg", 1200),
    "taikoo_alt": commons("Sino-Ocean Taikoo Li Chengdu 10.jpg", 1200),
    "people_park": commons("Teahouse in Peoples Park - Chengdu, China - DSC05371.jpg", 1200),
    "people_park_alt": commons("Teahouse in Peoples Park - Chengdu, China - DSC05353.jpg", 1200),
    "panda_base_gate": commons("Chengdu Research Base of Giant Panda Breeding, 201907, 01.jpg", 1200),
    "panda_base": commons("Chengdu Research Base of Giant Panda Breeding, 201907, 05.jpg", 1200),
    "panda_base_alt": commons("Chengdu Research Base of Giant Panda Breeding, 201907, 09.jpg", 1200),
    "dujiangyan": commons("都江堰南桥 Dujiangyan Nanqiao Bridge.jpg", 1200),
    "dujiangyan_night": commons("Anshun Bridge at night.jpg", 1200),
    "guanxian": commons("Dujiangyan ancient city.jpg", 1200),
    "jiuzhai_long": commons("Long Lake (Jiuzhaigou) 20260511-1.jpg", 1200),
    "jiuzhai_five": commons("5 Flowers Lake (127556467).jpeg", 1200),
    "jiuzhai_waterfall": commons("九寨溝-珍珠灘瀑布 Jiuzhaigou Pearl Shoal Waterfall.jpg", 1200),
    "jiuzhai_nuorilang": commons("1 nuorilang jiuzhaigou 2023.jpg", 1200),
    "sanxingdui_museum": commons("New Sandingdui Museum 02.jpg", 1200),
    "sanxingdui_gallery": commons("Sanxingdui Museum 20260512-1.jpg", 1200),
    "anshun_2026": commons("Anshun Bridge Jin River Chengdu night 2026 dllu.jpg", 1200),
    "jinli_night": commons("Chengdu Jinli-Straße bei Nacht 02.jpg", 1200),
    "dongjiao": commons("东郊记忆 (123423479).jpeg", 1200),
    "yulin": commons("15196 (Route 153) at Yulin Donglu 20241007195012.jpg", 1200),

    # Home accordion route gallery — iconic, place-specific views.
    "ifs_panda": commons("IFS Chengdu Tower and I AM HERE Panda Statue.jpg", 1400),
    "kuanzhai": commons("Street scene - Kuanzhai Alleys - Chengdu, China - DSC05311.jpg", 1400),
    "wide_alley": commons("Wide Alley - 宽巷子 - January 2019, Chengdu, Sichuan.jpg", 1400),
    "yulin_street": commons("Yulin East Road 20241007194923.jpg", 1400),
    "sanxingdui_mask": commons("20250519 Bronze mask in the Sanxingdui Museum.jpg", 1400),
    "pudong_t2": commons("201801 Intl departure entrance at PVG T2.jpg", 1400),
    "penang_home": commons("George Town skyline at dusk Nov 2024-6-cropped.jpg", 1400),

    # Transport / food — used only where scenery would be misleading.
    "airport": commons("成都天府国际机场 Chengdu Tianfu International Airport 1.jpg", 1200),
    "airport_hall": commons("2025 Chengdu Tianfu Airport 03.jpg", 1200),
    "chongqing_train": commons("202308 Platform of Chongqingbei Railway Station, passengers leaving.jpg", 1200),
    "chongqing_city": commons("Chongqing Panorama1.jpg", 1200),
    "chongqing_night": commons("Chongqing-NanbinRd-Night.jpg", 1200),
    "shancheng_trail": commons("山城步道——山城巷.jpg", 1200),
    "shibati": commons("Shibati 十八梯 2022.1.1.jpg", 1200),
    "xiahaoli": commons("山城巷上区.jpg", 1200),
    "jiefangbei": commons("Chongqing Jiefangbei CBD.jpg", 1200),
    "chaotianmen": commons("Raffles City Chongqing 20260507-1.jpg", 1200),
    "hongya": commons("202308 Hongya Cave at night from Qiansimen Bridge.jpg", 1200),
    "ciqikou": commons("Street in the Old Town of Ciqikou.jpg", 1200),
    "liziba": commons("A train of Chongqing Rail Transit Line 2 coming through a residential building at Liziba 2255.jpg", 1200),
    "bayi": commons("Sichuan-style hotpot.jpg", 1200),
    "panda_huahua": commons("Chengdu Research Base of Giant Panda Breeding, 201907, 06.jpg", 1200),
    "dujiangyan_waterworks": commons("Dujiangyan Scenic Area 36606-Dujiangyan (49067671478).jpg", 1200),
    "zhongshuge": commons("DujiangyanZhongshuge.jpg", 1200),
    "nanqiao": commons("都江堰南桥 2024-05-01 06.jpg", 1200),
    "blue_tears": commons("都江堰南桥 5.jpg", 1200),
    "mapo": commons("Authentic Mapo Tofu.jpg", 1200),
    "hotpot": commons("Sichuan-style hotpot.jpg", 1200),
    "snack": commons("Chengdu Zhong Dumpling(Zhong Jiaozi).jpg", 1200),
    "coffee": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1100&q=88",
    "noodles": commons("担担面 Dandan noodles.jpg", 1200),
    "dessert": commons("Brown Sugar Bing Fen.jpg", 1200),
}


ASSET_ROOT = Path(__file__).resolve().parent / "assets"


@lru_cache(maxsize=None)
def asset_data_uri(relative_path: str, mime_type: str) -> str:
    """Return an extracted binary asset using the original inline URI format."""
    data = (ASSET_ROOT / relative_path).read_bytes()
    return f"data:{mime_type};base64,{base64.b64encode(data).decode('ascii')}"


def optional_asset_data_uri(relative_path: str, mime_type: str) -> str:
    """Return an optional asset as a data URI, or an empty string if it is absent."""
    path = ASSET_ROOT / relative_path
    if not path.exists():
        return ""
    return asset_data_uri(relative_path, mime_type)


def build_payload(server_food=None, initial_page: str = "home") -> str:
    """Build the browser payload with the same keys and ordering as the source."""
    from food import FOODS
    from home import DAYS

    card_art = {
        day: {
            "front": asset_data_uri(f"cards/day-{day}-front.webp", "image/webp"),
            "back": asset_data_uri(f"cards/day-{day}-back.webp", "image/webp"),
        }
        for day in range(1, 7)
    }
    payload = {
        "days": DAYS,
        "images": IMG,
        "foods": FOODS,
        "config": APP_CONFIG,
        "landing_image": "",
        "landing_video": asset_data_uri("landing/landing.mp4", "video/mp4"),
        "traveler_panda": asset_data_uri("panda/traveler.png", "image/png"),
        "route_traveler_panda": asset_data_uri("panda/route-traveler.webp", "image/webp"),
        "card_art": card_art,
        "covers": {},
        "avatar_options": [
            {"key": f"avatar_{i}", "src": (optional_asset_data_uri(f"avatars/avatar-{i:02d}.webp", "image/webp") or optional_asset_data_uri(f"avatar-{i:02d}.webp", "image/webp"))}
            for i in range(1, 11)
        ],
        "avatar_version": "v12-approved-panda-sanxingdui",
        "expense_hero": "data:image/webp;base64,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",
        "server_food": server_food,
        "initial_page": initial_page if initial_page in {"home", "food", "expenses"} else "home",
    }
    return json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")


HTML_PREFIX = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<meta name="theme-color" content="#faf8f1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Caveat:wght@500;600&family=Ma+Shan+Zheng&family=Noto+Sans+SC:wght@300;400;500;600&family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#faf8f1; --paper-2:#f3f1e7; --sheet:#fcfbf6;
  --ink:#1f2b25; --ink-soft:#56655c; --muted:#7d8a82;
  --forest:#2c6a4c; --forest-2:#4f8467; --slate:#6f86a0; --slate-ink:#57738f;
  --line:rgba(45,80,62,.14); --gold:#e3aa3f; --coral:#d96d5f;
  --serif:"Cormorant Garamond","Noto Serif SC",serif;
  --cn-serif:"Noto Serif SC",serif; --sans:"Noto Sans SC",sans-serif;
  --hand:"Ma Shan Zheng","Noto Serif SC",serif; --script:"Caveat","Cormorant Garamond",cursive;
  --nav-h:68px; --acc-h:clamp(390px,calc(100dvh - 340px),505px);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;min-height:100%;background:#e6e2d6;color:var(--ink);font-family:var(--sans);overscroll-behavior:none}
body{display:flex;justify-content:center}
button,input{font:inherit;color:inherit}
img{display:block}
.app-shell{width:min(100%,460px);min-height:100dvh;position:relative;overflow:hidden;background:linear-gradient(180deg,#fdfcf7 0%,#f8f6ee 100%);box-shadow:0 0 60px rgba(50,60,45,.14)}
.app-shell:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.16;z-index:99;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 160 160' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.08'/%3E%3C/svg%3E")}
main{min-height:100dvh}
.page{display:none;padding:14px 8px calc(var(--nav-h) + 14px);animation:pageIn .35s ease both}
.page.active{display:block}
@keyframes pageIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.icon{width:20px;height:20px;display:block;stroke:currentColor;fill:none;stroke-width:1.55;stroke-linecap:round;stroke-linejoin:round}
.icon.sm{width:14px;height:14px}.icon.lg{width:24px;height:24px}

'''
NAV_CSS = r'''/* ───── BOTTOM NAV ───── */
.bottom-nav{position:fixed;z-index:80;left:50%;bottom:0;transform:translateX(-50%);width:min(100vw,460px);height:calc(var(--nav-h) + env(safe-area-inset-bottom));padding:6px 10px env(safe-area-inset-bottom);display:grid;grid-template-columns:repeat(3,1fr);background:rgba(253,252,247,.95);backdrop-filter:blur(16px);border-top:1px solid rgba(60,75,65,.1)}
.nav-btn{border:0;background:transparent;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;font:400 10.5px var(--sans);color:var(--slate);cursor:pointer}
.nav-btn .icon{width:22px;height:22px}
.nav-btn.active{color:var(--forest);font-weight:600}
.nav-btn.active .icon{stroke-width:2}

'''
SHARED_PAGES_CSS = r'''/* ───── shared page bits (Food / Expenses) ───── */
.page-head{height:50px;display:grid;grid-template-columns:42px 1fr 42px;align-items:center;margin:1px 0 8px}
.page-head .center{text-align:center}.page-head h1{font:600 27px/.9 var(--serif);margin:0}.page-head .sub{font-size:9px;color:var(--muted);margin-top:5px}
.round-btn{width:38px;height:38px;border:1px solid var(--line);border-radius:50%;background:rgba(255,255,255,.82);display:grid;place-items:center;cursor:pointer}
.paper-card{background:rgba(255,255,255,.9);border:1px solid rgba(44,116,84,.1);box-shadow:0 8px 22px rgba(45,70,55,.06)}
.search-box{border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.6);display:flex;align-items:center;gap:9px;padding:11px 13px;font-size:10px;color:var(--muted)}
.filter-scroll{display:flex;gap:7px;overflow:auto;scrollbar-width:none;margin:11px 0 13px}.filter-scroll::-webkit-scrollbar{display:none}
.filter-chip{border:0;border-radius:99px;background:#eae7db;padding:7px 12px;white-space:nowrap;font-size:10px;color:#626960;cursor:pointer}.filter-chip.active{background:var(--forest);color:#fff}
.radius-select{display:flex;justify-content:flex-end;gap:5px;margin:-3px 0 10px}.radius-select button{border:0;background:transparent;color:#85877f;font-size:9px;padding:3px;cursor:pointer}.radius-select button.active{color:var(--forest);font-weight:600;border-bottom:1px solid var(--forest)}
.food-list{display:grid;gap:9px}.food-card{display:grid;grid-template-columns:104px 1fr;gap:12px;padding:8px;border-radius:19px}.food-card img{width:104px;height:101px;border-radius:15px;object-fit:cover}.food-card h3{font:600 13px/1.3 var(--cn-serif);margin:3px 0 5px}.food-meta{font-size:9px;line-height:1.65;color:var(--muted)}.food-rating{font:600 12px var(--serif);color:var(--gold)}.platforms{display:flex;gap:5px;margin-top:7px}.platform{width:22px;height:17px;border-radius:5px;background:#e4ece3;color:#3c674e;display:grid;place-items:center;font:600 6.5px var(--sans);font-style:normal}.open-t{color:#4c7256;font-weight:600}
.ending{margin:20px 0 6px;text-align:center;padding:16px 12px;color:#6d5b49}.ending .cn{font:400 15px var(--cn-serif)}.ending .en{font:italic 12px var(--serif);margin-top:5px;color:#878078}
.nearby-tools{margin:2px 0 13px}.nearby-tools-head{display:flex;justify-content:space-between;align-items:flex-end;margin:0 3px 8px}.nearby-tools-head h2{font:600 15px/1.2 var(--cn-serif);margin:0}.nearby-tools-head small{font-size:8px;color:var(--muted)}.nearby-tools-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}.nearby-tool{border:1px solid var(--line);border-radius:15px;background:rgba(255,255,255,.72);padding:9px 2px;text-align:center;font-size:9px;color:#5f675f;cursor:pointer}.nearby-tool .icon{margin:0 auto 5px;color:var(--forest)}.nearby-tool:active{transform:scale(.97);background:#edf3e9}
.exp-total{border-radius:22px;padding:18px;text-align:center;background:linear-gradient(140deg,#eef3e6,#fbf7e8)}.exp-total small{font:500 10px var(--sans);color:var(--muted)}.exp-total b{display:block;font:600 38px/1.1 var(--serif);color:#25382e;margin-top:6px}
.exp-form{border-radius:20px;padding:13px;margin-top:11px}.exp-row{display:flex;gap:7px;margin-top:9px}.exp-input{min-width:0;flex:1;border:1px solid var(--line);background:#fffefa;border-radius:13px;padding:10px 11px;font-size:12px;outline:none}.exp-input:focus{border-color:#77917c;box-shadow:0 0 0 3px rgba(83,119,91,.1)}.exp-input.amt{flex:0 0 96px}
.exp-add{border:0;border-radius:13px;background:var(--forest);color:#fff;padding:0 15px;font-size:12px;cursor:pointer}
.exp-list{margin-top:11px;display:grid;gap:7px}.exp-item{display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:10px;border-radius:15px;padding:10px 12px}.exp-item b{font:600 12px var(--cn-serif)}.exp-item small{display:block;font-size:9px;color:var(--muted);margin-top:3px}.exp-item .amt{font:600 16px var(--serif)}.exp-item button{border:0;background:transparent;color:#9a9a92;cursor:pointer;padding:4px}

'''
FUNCTIONAL_PAGES_CSS = r'''/* ───── FUNCTIONAL PAGES + LANGUAGE (Home geometry intentionally untouched) ───── */
.home-tools{display:flex;align-items:flex-start;gap:7px}.lang-toggle{margin-top:1px;border:1px solid rgba(54,86,67,.16);background:rgba(255,255,255,.72);border-radius:999px;padding:4px 7px;font:600 8px/1 var(--sans);letter-spacing:.25px;color:#587064;cursor:pointer;white-space:nowrap}.greeting-en:empty{display:none}
.app-page{padding:12px 10px calc(var(--nav-h) + 18px)}
.app-head{display:flex;align-items:flex-start;justify-content:space-between;margin:2px 4px 14px}.app-head h1{font:700 28px/1 var(--cn-serif);margin:0;color:#1d3428}.app-head p{font:400 11px/1.4 var(--sans);color:var(--muted);margin:6px 0 0}.head-actions{display:flex;gap:7px;align-items:center}.mini-btn,.icon-btn{border:1px solid var(--line);background:rgba(255,255,255,.78);color:var(--forest);border-radius:999px;padding:8px 11px;font-size:10px;cursor:pointer}.icon-btn{width:36px;height:36px;padding:0;display:grid;place-items:center}.status-pill{display:inline-flex;align-items:center;gap:6px;padding:6px 9px;border-radius:999px;background:#eef3e9;color:#55705f;font-size:9px}.status-pill.warn{background:#f5eee1;color:#8a6a42}.status-dot{width:6px;height:6px;border-radius:50%;background:#5c8a68}.status-pill.warn .status-dot{background:#c18b4e}
.tool-row{display:flex;gap:8px;align-items:center;margin:0 2px 10px}.tool-row .search-box{flex:1}.search-box input{width:100%;border:0;outline:0;background:transparent;font-size:11px}.primary-btn{border:0;border-radius:14px;background:var(--forest);color:#fff;padding:11px 15px;font-size:11px;font-weight:600;cursor:pointer;box-shadow:0 7px 16px rgba(44,106,76,.16)}.secondary-btn{border:1px solid var(--line);border-radius:14px;background:#fffef9;color:var(--forest);padding:10px 13px;font-size:10px;font-weight:600;cursor:pointer}.danger-soft{color:#a65d52;background:#fbefeb;border-color:#edd5ce}.full{width:100%}.hidden{display:none!important}
.state-card{border-radius:22px;padding:26px 20px;text-align:center;margin-top:12px}.state-card .state-icon{width:52px;height:52px;border-radius:50%;background:#edf2e9;color:var(--forest);display:grid;place-items:center;margin:0 auto 12px}.state-card h3{font:600 17px var(--cn-serif);margin:0}.state-card p{font-size:10px;line-height:1.6;color:var(--muted);margin:7px auto 14px;max-width:260px}.spinner{width:24px;height:24px;border:2px solid #dce6dc;border-top-color:var(--forest);border-radius:50%;animation:spin .8s linear infinite;margin:12px auto}@keyframes spin{to{transform:rotate(360deg)}}
.food-list{display:grid;gap:9px}.food-card.live{position:relative;grid-template-columns:90px 1fr;padding:8px;cursor:pointer;overflow:hidden}.food-photo,.food-placeholder{width:90px;height:92px;border-radius:15px;object-fit:cover}.food-placeholder{display:grid;place-items:center;background:linear-gradient(145deg,#e4eadf,#f5ecdc);color:#67806e}.food-card.live h3{font:600 13px/1.25 var(--cn-serif);margin:3px 0 6px;padding-right:38px}.food-card.live .score{position:absolute;right:11px;top:10px;width:34px;height:34px;border-radius:50%;background:#eef3e7;color:#315d46;display:grid;place-items:center;font:700 13px var(--serif)}.food-line{font-size:9.5px;line-height:1.55;color:var(--muted)}.food-bottom{display:flex;align-items:center;gap:7px;margin-top:6px}.smart{font-size:9px;font-weight:600;color:#3e7054}.open-label{font-size:8px;color:#5b7e63;background:#edf4e9;border-radius:99px;padding:3px 6px}.confidence{font-size:8px;color:#927a58}.radius-select{align-items:center}.radius-label{font-size:9px;color:#96978f;padding:3px;margin-right:auto}
.modal-backdrop{position:fixed;z-index:150;inset:0;margin:auto;width:min(100vw,460px);background:rgba(19,35,27,.34);display:flex;align-items:flex-end;backdrop-filter:blur(2px)}.sheet-modal{width:100%;max-height:88dvh;overflow:auto;border-radius:28px 28px 0 0;background:#fbf9f2;padding:13px 15px calc(18px + env(safe-area-inset-bottom));box-shadow:0 -18px 50px rgba(20,45,31,.2);animation:sheetUp .28s ease}.sheet-grab{width:38px;height:4px;border-radius:9px;background:#ccd3ca;margin:0 auto 12px}@keyframes sheetUp{from{transform:translateY(18px);opacity:.5}to{transform:none;opacity:1}}.sheet-title{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.sheet-title h2{font:700 21px/1.12 var(--cn-serif);margin:0}.sheet-title p{font-size:10px;color:var(--muted);margin:6px 0}.sheet-close{border:0;background:#eeeae0;width:30px;height:30px;border-radius:50%;cursor:pointer}.detail-photo,.detail-placeholder{width:100%;height:178px;border-radius:20px;margin:10px 0;object-fit:cover}.detail-placeholder{display:grid;place-items:center;background:linear-gradient(145deg,#dce9df,#f3eadb);color:#577565}.detail-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:10px 0}.detail-stat{border:1px solid var(--line);border-radius:15px;background:#fffef9;padding:10px}.detail-stat small{display:block;font-size:8px;color:var(--muted)}.detail-stat b{display:block;font:600 14px var(--cn-serif);margin-top:3px}.sheet-actions{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:12px}.sheet-actions a,.sheet-actions button{text-decoration:none;text-align:center;border:1px solid var(--line);border-radius:14px;background:#fffef9;color:var(--forest);padding:11px 6px;font-size:10px;font-weight:600;cursor:pointer}.sheet-actions .main{grid-column:1/-1;background:var(--forest);color:#fff;border-color:var(--forest)}
.segmented{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;padding:4px;border-radius:15px;background:#ebe9df;margin-bottom:11px}.segmented button{border:0;border-radius:11px;background:transparent;padding:8px 2px;font-size:9px;color:#737970;cursor:pointer}.segmented button.active{background:#fffef9;color:var(--forest);font-weight:600;box-shadow:0 3px 9px rgba(52,70,57,.08)}.sync-row{display:flex;justify-content:space-between;align-items:center;margin:0 2px 10px}.summary-hero{padding:18px;border-radius:24px;background:linear-gradient(145deg,#edf3e8,#faf4e6);position:relative;overflow:hidden}.summary-hero:after{content:"";position:absolute;width:130px;height:130px;border-radius:50%;background:rgba(116,148,115,.08);right:-45px;bottom:-65px}.summary-hero small{font-size:9px;color:var(--muted)}.summary-hero .big{font:700 38px/1.05 var(--serif);color:#213a2d;margin-top:5px}.summary-hero .fx{font-size:10px;color:#7c796d;margin-top:5px}.summary-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:9px}.summary-card{border-radius:17px;padding:12px}.summary-card small{font-size:8px;color:var(--muted)}.summary-card b{display:block;font:600 18px var(--serif);margin-top:4px}.section-label{display:flex;justify-content:space-between;align-items:center;margin:17px 3px 8px}.section-label h3{font:600 16px var(--cn-serif);margin:0}.section-label small{font-size:9px;color:var(--muted)}.transfer-list,.member-list,.bill-list{display:grid;gap:7px}.transfer,.member-row,.bill-row{border-radius:16px;padding:11px 12px;display:flex;align-items:center;gap:10px}.avatar{width:34px;height:34px;border-radius:50%;background:#e6eee3;color:#315f47;display:grid;place-items:center;font:700 12px var(--serif);flex:none}.member-main,.bill-main{min-width:0;flex:1}.member-main b,.bill-main b{font:600 12px var(--cn-serif)}.member-main small,.bill-main small{display:block;font-size:8.5px;color:var(--muted);margin-top:3px}.row-amount{font:600 15px var(--serif);white-space:nowrap}.row-actions{display:flex;gap:4px}.row-actions button{border:0;background:#f0eee6;border-radius:9px;padding:6px;color:#68766d;cursor:pointer}.me-badge{font-size:8px;color:#fff;background:var(--forest);border-radius:99px;padding:3px 6px}.inactive{opacity:.56}.form-grid{display:grid;gap:9px;margin-top:12px}.field label{display:block;font-size:9px;color:#6e7a72;margin:0 0 5px 3px}.field input,.field select{width:100%;border:1px solid var(--line);background:#fffef9;border-radius:13px;padding:11px 12px;font-size:12px;outline:0}.check-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:7px}.check-pill{display:flex;align-items:center;gap:7px;border:1px solid var(--line);border-radius:13px;background:#fffef9;padding:9px;font-size:10px}.split-lines{display:grid;gap:6px}.split-line{display:grid;grid-template-columns:1fr 108px;align-items:center;gap:8px}.split-line input{width:100%;border:1px solid var(--line);border-radius:11px;background:#fff;padding:9px;text-align:right}.validation{min-height:16px;font-size:9px;color:#ad5f55;margin-top:3px}.local-note{border-radius:15px;background:#f5eee0;color:#806b4d;padding:9px 11px;font-size:9px;line-height:1.45;margin-bottom:9px}.toast{position:fixed;z-index:220;left:50%;bottom:calc(var(--nav-h) + 18px);transform:translateX(-50%);width:max-content;max-width:calc(min(100vw,460px) - 32px);background:#203a2d;color:#fff;border-radius:999px;padding:10px 15px;font-size:10px;box-shadow:0 9px 25px rgba(20,45,31,.24);animation:toastIn .25s ease}@keyframes toastIn{from{opacity:0;transform:translate(-50%,8px)}to{opacity:1;transform:translate(-50%,0)}}


/* ───── Food v2: text-only focus carousel ───── */
.food-head{align-items:flex-start}.location-pill{display:flex;align-items:center;gap:5px;border:1px solid var(--line);background:rgba(255,254,249,.9);border-radius:999px;padding:8px 10px;color:#5f675f;font-size:9.5px;box-shadow:0 5px 14px rgba(48,54,45,.06);cursor:pointer}.location-pill .icon{width:15px;height:15px;color:var(--forest)}
.food-filter-tabs{margin:7px 0 12px;padding-bottom:2px}.food-filter-tabs .filter-chip{background:transparent;border-radius:0;padding:6px 8px 7px;color:#6e716a;font-size:10px;position:relative}.food-filter-tabs .filter-chip.active{background:transparent;color:var(--forest);font-weight:700}.food-filter-tabs .filter-chip.active:after{content:"";position:absolute;height:2px;border-radius:2px;left:8px;right:8px;bottom:0;background:var(--forest)}
.food-tools-row{display:flex;gap:8px;align-items:center;margin-bottom:12px}.food-tools-row .search-box{flex:1}.radius-mini{display:flex;gap:2px;border:1px solid var(--line);background:rgba(255,255,255,.62);padding:3px;border-radius:12px}.radius-mini button{border:0;background:transparent;color:#8a8b84;border-radius:9px;padding:5px 6px;font-size:7.5px;cursor:pointer}.radius-mini button.active{background:#e9efe5;color:var(--forest);font-weight:700}
.food-focus-section{margin:2px -10px 17px;overflow:hidden}.food-carousel{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding:0 21%;padding:4px 21% 12px;scrollbar-width:none;-webkit-overflow-scrolling:touch}.food-carousel::-webkit-scrollbar{display:none}
.food-focus-card{flex:0 0 58%;min-height:220px;scroll-snap-align:center;border:1px solid rgba(70,91,75,.15);border-radius:25px;background:linear-gradient(180deg,rgba(255,254,249,.98),rgba(249,246,237,.98));padding:15px 14px 14px;box-shadow:0 12px 24px rgba(50,58,49,.09);cursor:pointer;transition:transform .22s ease,box-shadow .22s ease;display:flex;flex-direction:column}.food-focus-card:active{transform:scale(.985)}.food-card-handle{width:28px;height:3px;border-radius:9px;background:#c5c6c0;margin:0 auto 13px}.food-focus-card h3{font:650 17px/1.15 var(--cn-serif);margin:0 0 7px;color:#27302b;min-height:39px}.lang-en .food-focus-card h3{font-family:var(--serif);font-size:16px}.food-focus-meta,.food-compact-meta{font-size:9.5px;color:var(--muted);line-height:1.5}.food-focus-rule{height:1px;background:rgba(73,84,74,.10);margin:12px 0}.food-focus-stats{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.smart-pill,.food-status{display:inline-flex;align-items:center;min-height:25px;border-radius:999px;padding:5px 9px;font-size:9px}.smart-pill{background:#e6f1e3;color:#2f724e;font-weight:700}.smart-pill.large{font-size:11px;padding:7px 12px}.food-status{background:#eef4e9;color:#5d7a62}.food-status.quiet{background:#f2eee5;color:#8b806d}.cuisine-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:auto;padding-top:13px}.cuisine-chip{display:inline-flex;align-items:center;border-radius:10px;padding:5px 8px;background:#f1ece3;color:#6d5b49;font-size:8.5px;white-space:nowrap}.cuisine-chip.muted{color:#979188}.food-carousel-dots{height:7px;display:flex;align-items:center;justify-content:center;gap:5px}.food-carousel-dots span{width:5px;height:5px;border-radius:50%;background:#babbb5;transition:all .2s}.food-carousel-dots span.active{width:17px;border-radius:5px;background:var(--forest)}
.food-more-section{margin:8px 0 13px}.food-section-head{display:flex;justify-content:space-between;align-items:flex-end;margin:0 2px 8px}.food-section-head h2{font:650 15px/1.2 var(--cn-serif);margin:0}.lang-en .food-section-head h2{font-family:var(--serif)}.food-section-head span{font-size:8px;color:var(--muted)}.food-more-list{display:grid;gap:8px}.food-compact-card{border:1px solid rgba(73,84,74,.10);border-radius:17px;background:rgba(255,254,249,.9);padding:11px 12px;box-shadow:0 6px 14px rgba(50,58,49,.045);cursor:pointer}.food-compact-card:active{transform:scale(.993)}.food-compact-main h3{font:600 12.5px/1.25 var(--cn-serif);margin:0 0 4px}.lang-en .food-compact-main h3{font-family:var(--serif)}.food-compact-bottom{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:8px}.smart-inline{font-size:8.5px;font-weight:700;color:#3e7054}.compact-cuisines{display:flex;gap:4px;margin-left:auto}.compact-cuisines .cuisine-chip{padding:4px 6px;font-size:7.5px}
.nearby-tools-collapsed{margin-top:13px}.nearby-tools-collapsed summary{list-style:none;display:flex;align-items:center;justify-content:space-between;border-top:1px solid rgba(74,84,75,.1);padding:12px 3px 8px;cursor:pointer}.nearby-tools-collapsed summary::-webkit-details-marker{display:none}.nearby-tools-collapsed summary span{font:600 12px var(--cn-serif)}.nearby-tools-collapsed summary small{font-size:8px;color:var(--muted)}
.food-sheet-title{padding:4px 1px 10px;border-bottom:1px solid rgba(73,84,74,.1)}.food-sheet-title h2{font-size:22px}.food-sheet-score-row{display:flex;gap:8px;align-items:center;margin:12px 0}.food-sheet-section{padding:3px 0 12px}.food-sheet-section h3{font:650 13px/1.2 var(--cn-serif);margin:0 0 9px}.lang-en .food-sheet-section h3{font-family:var(--serif)}.cuisine-row.detail{margin:0;padding:0}.cuisine-row.detail .cuisine-chip{font-size:9.5px;padding:6px 10px}.food-info-panel{border:1px solid rgba(73,84,74,.11);border-radius:18px;background:rgba(255,254,249,.7);overflow:hidden}.food-info-panel>div{display:grid;grid-template-columns:38% 1fr;gap:8px;padding:11px 12px;border-bottom:1px solid rgba(73,84,74,.08);align-items:center}.food-info-panel>div:last-child{border-bottom:0}.food-info-panel span{font-size:9px;color:#777d76}.food-info-panel b{font-size:9.5px;font-weight:600;color:#5c625d;text-align:right}.food-source-note{margin-top:11px;border-radius:16px;background:#eef2e9;padding:11px 12px;font-size:8.5px;line-height:1.55;color:#71776f}.food-only-nav{grid-template-columns:1fr;margin-top:12px}.food-only-nav .main{font-size:11px;padding:12px}
@media(max-width:360px){.food-focus-card{flex-basis:64%}.food-carousel{scroll-padding:0 18%;padding-left:18%;padding-right:18%}.radius-mini button{padding:5px 4px}.food-focus-card h3{font-size:15px}}


/* ───── v6 fixed bottom nav + internal scrolling ───── */
html,body{height:100%;min-height:100%;overflow:hidden;overscroll-behavior:none}
body{align-items:stretch}
.app-shell{height:100dvh;min-height:100dvh;max-height:100dvh;overflow:hidden}
main{
  height:100dvh;
  min-height:0;
  overflow-y:auto;
  overflow-x:hidden;
  -webkit-overflow-scrolling:touch;
  overscroll-behavior-y:contain;
  scrollbar-width:none;
}
main::-webkit-scrollbar{display:none}
.page{min-height:100%;padding-bottom:calc(var(--nav-h) + env(safe-area-inset-bottom) + 18px)}
.bottom-nav{
  position:absolute;
  left:0;
  right:0;
  bottom:0;
  transform:none;
  width:100%;
  z-index:180;
}
.modal-backdrop{z-index:260}

/* ───── v6 curved Food carousel ───── */
.food-carousel{
  perspective:900px;
  overflow-y:visible;
  padding-top:8px;
  padding-bottom:26px;
}
.food-focus-card{
  transform-origin:50% 145%;
  will-change:transform,opacity;
  transition:transform .12s linear,opacity .12s linear,box-shadow .18s ease;
  backface-visibility:hidden;
}
.food-carousel:not(:active) .food-focus-card{
  transition:transform .22s cubic-bezier(.22,.75,.25,1),opacity .18s ease,box-shadow .18s ease;
}
.food-focus-card:active{box-shadow:0 8px 18px rgba(50,58,49,.11)}

/* ───── v6 Card → Modal ───── */
.card-modal-backdrop{
  position:fixed;
  inset:0;
  width:100%;
  height:100%;
  margin:0;
  display:grid;
  place-items:center;
  padding:18px 14px calc(var(--nav-h) + env(safe-area-inset-bottom) + 14px);
  background:rgba(24,36,29,.38);
  opacity:0;
  transition:opacity .26s ease;
  backdrop-filter:blur(2px);
}
.card-modal-panel{
  width:min(100%,420px);
  max-height:min(74dvh,680px);
  overflow-y:auto;
  border-radius:26px;
  padding:14px 15px 18px;
  background:#fbf9f2;
  box-shadow:0 24px 70px rgba(20,36,27,.28);
  transform-origin:center center;
  will-change:transform,opacity,border-radius;
  transition:transform .30s cubic-bezier(.22,.8,.24,1),opacity .22s ease,border-radius .30s ease;
}
.card-modal-panel .sheet-grab{display:none}
.card-modal-panel .food-sheet-title{padding-top:2px}
.card-modal-panel .sheet-close{position:relative;z-index:2}
@media (max-width:460px){
  .app-shell,main{height:100dvh;min-height:100dvh;max-height:100dvh}
}
@media (prefers-reduced-motion:reduce){
  .food-focus-card,.card-modal-panel,.card-modal-backdrop{transition:none!important}
}


/* ───── Expenses v7 — approved travel-ledger preview ───── */
#expenses.app-page{padding:0 10px calc(var(--nav-h) + env(safe-area-inset-bottom) + 24px);background:
  radial-gradient(circle at 85% 8%,rgba(90,122,85,.10),transparent 28%),
  linear-gradient(180deg,#faf8f1 0%,#f5f1e7 100%)}
.expenses-hero-head{height:142px;margin:0 -10px 10px;padding:20px 15px 12px;position:relative;overflow:hidden;background:
  linear-gradient(90deg,rgba(250,248,241,.98) 0%,rgba(250,248,241,.78) 47%,rgba(250,248,241,.10) 100%),
  var(--expense-panda) center right/cover no-repeat}
.expenses-hero-head:after{content:"";position:absolute;inset:auto 0 0;height:34px;background:linear-gradient(180deg,transparent,#faf8f1)}
.expenses-hero-title{position:relative;z-index:2;padding-top:7px}.expenses-hero-title h1{font:700 35px/.95 var(--cn-serif);margin:0;color:#173a2c}.lang-en .expenses-hero-title h1{font-family:var(--serif);font-size:34px}.expenses-hero-title p{font-size:10px;color:#6e7b73;margin:7px 0 0}.expense-refresh{position:absolute;z-index:3;right:13px;top:16px;border:1px solid rgba(45,80,62,.12);background:rgba(255,255,255,.62);backdrop-filter:blur(8px);width:33px;height:33px;border-radius:50%;display:grid;place-items:center;color:var(--forest)}
.expense-overview-card{margin-top:-18px;position:relative;z-index:4;border-radius:26px;padding:16px 16px 14px;background:linear-gradient(140deg,rgba(255,254,249,.97),rgba(247,244,234,.96));border:1px solid rgba(70,91,75,.12);box-shadow:0 13px 30px rgba(53,65,54,.09);overflow:hidden}
.expense-overview-card:after{content:"";position:absolute;width:175px;height:145px;right:-35px;top:-12px;opacity:.18;background:
  radial-gradient(ellipse at 20% 80%,transparent 0 43%,#5e7c60 44% 46%,transparent 47%),
  radial-gradient(ellipse at 42% 58%,transparent 0 42%,#7b9675 43% 45%,transparent 46%);
  transform:rotate(-18deg);pointer-events:none}
.expense-overview-label{font:650 16px var(--cn-serif);position:relative;z-index:1}.lang-en .expense-overview-label{font-family:var(--serif)}
.expense-overview-amount{font:700 42px/1 var(--serif);letter-spacing:-1px;color:#163729;margin-top:6px;position:relative;z-index:1}.expense-overview-fx{font:500 12px var(--serif);color:#78827a;margin-top:3px}
.expense-overview-rule{height:1px;background:rgba(65,81,69,.12);margin:13px 0 11px}
.expense-overview-pair{display:grid;grid-template-columns:1fr 1px 1fr;align-items:center;gap:12px}.expense-overview-divider{height:40px;background:rgba(65,81,69,.12)}
.expense-metric{display:grid;grid-template-columns:31px 1fr;gap:8px;align-items:center}.expense-metric-icon{width:31px;height:31px;border-radius:50%;display:grid;place-items:center;background:#eef0e5;color:#365f49}.expense-metric-icon .icon{width:17px;height:17px}.expense-metric small{display:block;font-size:8px;color:#737d75}.expense-metric b{display:block;font:650 17px var(--serif);color:#27392f;margin-top:1px}
.expense-focus-tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin:9px 0 10px;padding:3px;border-radius:19px;background:rgba(246,243,234,.92);border:1px solid rgba(68,83,71,.08)}
.expense-focus-tab{border:0;border-radius:16px;background:transparent;padding:9px 4px 8px;color:#44574b;cursor:pointer;min-width:0}.expense-focus-tab.active{background:#254e39;color:#fff;box-shadow:0 7px 16px rgba(34,72,51,.17)}.expense-focus-tab .tab-main{display:block;font:600 11px var(--cn-serif);white-space:nowrap}.lang-en .expense-focus-tab .tab-main{font-family:var(--serif);font-size:10px}.expense-focus-tab .tab-sub{display:block;font:500 7px var(--serif);opacity:.72;margin-top:1px}
.expense-section-card{border-radius:22px;background:rgba(255,254,249,.84);border:1px solid rgba(67,83,71,.09);box-shadow:0 8px 18px rgba(50,63,52,.045);margin:9px 0;padding:11px 11px}
.expense-section-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:9px}.expense-section-head h3{font:650 16px/1.2 var(--cn-serif);margin:0}.lang-en .expense-section-head h3{font-family:var(--serif)}.expense-section-link{border:0;background:transparent;color:#66756b;font-size:8.5px;display:flex;align-items:center;gap:3px;padding:3px;cursor:pointer}
.member-balance-card{cursor:pointer;overflow:hidden;transition:padding .34s ease,box-shadow .34s ease}.member-balance-summary{display:flex;align-items:center;min-height:50px}.member-overlap{display:flex;align-items:center;flex:1;padding-left:4px;min-width:0}.member-overlap .balance-avatar{margin-left:-14px}.member-overlap .balance-avatar:first-child{margin-left:0}
.balance-avatar{width:43px;height:43px;border-radius:50%;object-fit:cover;border:2px solid #faf8f1;box-shadow:0 3px 9px rgba(37,57,43,.12);background:#e7eadf;flex:none}
.member-balance-summary-copy{text-align:right;margin-left:8px}.member-balance-summary-copy b{display:block;font:650 12px var(--cn-serif)}.member-balance-summary-copy small{font-size:8px;color:#7c847d}
.member-balance-grid-wrap{display:grid;grid-template-rows:0fr;opacity:0;transition:grid-template-rows .38s cubic-bezier(.2,.75,.25,1),opacity .24s ease,margin .34s ease;margin-top:0}.member-balance-card.expanded .member-balance-grid-wrap{grid-template-rows:1fr;opacity:1;margin-top:9px}.member-balance-grid-clip{overflow:hidden}.member-balance-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px 7px;padding:4px 1px 3px;border-top:1px solid rgba(67,83,71,.08);padding-top:12px}
.member-balance-person{text-align:center;min-width:0}.member-balance-person img{width:48px;height:48px;border-radius:50%;object-fit:cover;border:2px solid #f8f5ec;box-shadow:0 3px 8px rgba(44,61,48,.10);margin:auto}.member-balance-person b{display:block;font:600 9.5px var(--serif);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:4px}.member-balance-person span{display:block;font:650 10px var(--serif);margin-top:2px}.balance-positive{color:#307447}.balance-negative{color:#b64f4d}.balance-zero{color:#858b84;font-size:8px!important}
.expense-recent-list{display:grid;gap:6px}.expense-recent-row{display:grid;grid-template-columns:48px 1fr auto 14px;gap:9px;align-items:center;padding:7px 8px;border-radius:15px;background:rgba(255,255,255,.72);border:1px solid rgba(69,84,72,.07);cursor:pointer;transition:transform .15s ease,box-shadow .15s ease}.expense-recent-row:active{transform:scale(.992)}.expense-thumb{width:48px;height:43px;border-radius:11px;object-fit:cover}.expense-recent-main{min-width:0}.expense-recent-main b{display:block;font:600 11.5px var(--cn-serif);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.lang-en .expense-recent-main b{font-family:var(--serif)}.expense-recent-main small{display:block;font-size:8px;color:#7b827c;margin-top:3px}.expense-recent-money{text-align:right}.expense-recent-money b{display:block;font:650 15px var(--serif)}.expense-recent-money small{display:block;font-size:8px;color:#7b827c;margin-top:2px}.expense-row-chevron{color:#89928a;font-size:16px}
.settlement-card .settlement-row{display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:8px;padding:7px 1px;border-top:1px solid rgba(70,84,73,.07)}.settlement-card .settlement-row:first-of-type{border-top:0}.settlement-route{display:flex;align-items:center;gap:6px;min-width:0}.settlement-route img{width:26px;height:26px;border-radius:50%;object-fit:cover;border:1px solid #eee9de}.settlement-route b{font:600 8.5px var(--serif);white-space:nowrap}.settlement-arrow{color:#4e745e}.settlement-amount{font:650 11px var(--serif)}.settlement-remind{border:0;border-radius:10px;background:#e4eedf;color:#385f49;padding:7px 10px;font-size:8px}
.expense-fab{position:fixed;z-index:175;right:max(17px,calc((100vw - 460px)/2 + 17px));bottom:calc(var(--nav-h) + env(safe-area-inset-bottom) + 16px);width:55px;height:55px;border-radius:50%;border:0;background:#2c5940;color:#fff;font:300 33px/1 var(--sans);box-shadow:0 12px 25px rgba(32,73,50,.26);cursor:pointer}.expense-fab:active{transform:scale(.96)}
.expense-cloud-note{text-align:right;margin:-4px 2px 5px;font-size:7px;color:#9a9e97}
.expense-avatar-picker{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:5px}.expense-avatar-choice{border:0;background:transparent;padding:0;cursor:pointer;min-width:0}.expense-avatar-choice img{width:46px;height:46px;border-radius:50%;object-fit:cover;border:2px solid transparent;box-shadow:0 2px 8px rgba(45,61,49,.08)}.expense-avatar-choice.selected img{border-color:var(--forest);box-shadow:0 0 0 2px #dce9dc}.expense-avatar-choice span{display:block;font-size:6.8px;color:#777f78;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.expense-detail-backdrop{position:fixed;z-index:300;inset:0;display:grid;place-items:center;padding:18px 14px calc(var(--nav-h) + env(safe-area-inset-bottom) + 12px);background:rgba(27,39,31,.34);opacity:0;transition:opacity .26s ease;backdrop-filter:blur(2px)}
.expense-detail-panel{width:min(100%,360px);max-height:72dvh;overflow:auto;background:#fbf9f2;border-radius:25px;padding:13px 14px 14px;box-shadow:0 25px 70px rgba(28,42,33,.28);opacity:0;will-change:transform,opacity,border-radius;transform-origin:center;transition:transform .30s cubic-bezier(.22,.8,.24,1),opacity .22s ease,border-radius .30s ease}
.expense-detail-title{display:flex;justify-content:space-between;gap:8px}.expense-detail-title h2{font:700 18px var(--cn-serif);margin:0}.lang-en .expense-detail-title h2{font-family:var(--serif)}.expense-detail-title small{display:block;font-size:8px;color:#7c837d;margin-top:4px}.expense-detail-amount{font:700 31px var(--serif);margin:12px 0 9px}.expense-detail-list{border-top:1px solid rgba(65,81,69,.10)}.expense-detail-item{display:grid;grid-template-columns:38% 1fr;gap:7px;padding:10px 2px;border-bottom:1px solid rgba(65,81,69,.08);font-size:9px}.expense-detail-item span{color:#7c847e}.expense-detail-item b{text-align:right;font-weight:600}.expense-detail-primary{width:100%;border:0;border-radius:14px;padding:11px;background:#29583f;color:#fff;margin-top:11px;font-size:10px}.expense-detail-delete{width:100%;border:0;background:transparent;color:#9b5f58;font-size:8px;padding:8px}
.expense-sheet-backdrop{position:fixed;z-index:305;inset:0;display:grid;place-items:center;padding:18px 14px calc(var(--nav-h) + env(safe-area-inset-bottom) + 12px);background:rgba(27,39,31,.34)}.expense-sheet-panel{width:min(100%,390px);max-height:78dvh;overflow:auto;border-radius:25px;background:#fbf9f2;padding:14px 15px 16px;box-shadow:0 24px 65px rgba(25,40,31,.26)}
@media(max-width:360px){.expense-focus-tab .tab-main{font-size:9.5px}.balance-avatar{width:39px;height:39px}.member-overlap .balance-avatar{margin-left:-13px}.expense-overview-amount{font-size:36px}}


/* ───── Expenses v8: exact approved-preview proportions ───── */
#expenses.app-page{
  padding:0 8px calc(var(--nav-h) + env(safe-area-inset-bottom) + 18px);
  background:
    radial-gradient(circle at 92% 3%,rgba(111,143,106,.07),transparent 25%),
    linear-gradient(180deg,#fbf9f2 0%,#f4efe4 100%);
}
.expenses-hero-head{
  height:152px;
  margin:0 -8px 0;
  padding:20px 14px 12px;
  border-radius:0;
  background:
    linear-gradient(90deg,rgba(250,248,241,.98) 0%,rgba(250,248,241,.88) 40%,rgba(250,248,241,.18) 70%,rgba(250,248,241,.02) 100%),
    var(--expense-panda) center right/cover no-repeat;
}
.expenses-hero-head:after{
  height:24px;
  background:linear-gradient(180deg,transparent,#f8f5ec);
}
.expenses-hero-title{padding-top:5px}
.expenses-hero-title h1{
  font:700 34px/.95 var(--cn-serif);
  letter-spacing:-1px;
  color:#17382b;
}
.lang-en .expenses-hero-title h1{font:700 32px/.96 var(--serif)}
.expenses-hero-title p{
  margin-top:6px;
  font-size:9px;
  color:#64756b;
}
.expense-refresh{
  top:14px;
  right:12px;
  width:32px;height:32px;
  background:rgba(253,252,247,.78);
  border:1px solid rgba(51,84,63,.12);
  box-shadow:0 5px 14px rgba(40,61,47,.06);
}
.expense-cloud-note{
  height:0; overflow:hidden; margin:0; padding:0;
  opacity:0; pointer-events:none;
}
.expense-overview-card{
  margin:-23px 3px 0;
  border-radius:24px;
  padding:16px 16px 13px;
  min-height:168px;
  background:
    linear-gradient(135deg,rgba(255,254,250,.98),rgba(247,244,235,.96));
  border:1px solid rgba(69,91,73,.11);
  box-shadow:0 14px 28px rgba(53,68,55,.10);
}
.expense-overview-card:after{
  width:205px;height:165px;
  right:-54px;top:-18px;opacity:.14;
}
.expense-overview-label{
  font:650 16px/1.2 var(--cn-serif);
  color:#20352a;
}
.expense-overview-amount{
  margin-top:5px;
  font:700 40px/.98 var(--serif);
  letter-spacing:-1.4px;
}
.expense-overview-fx{
  margin-top:5px;
  font:500 11px var(--serif);
}
.expense-overview-rule{margin:12px 0 10px}
.expense-overview-pair{gap:13px}
.expense-metric{grid-template-columns:30px 1fr;gap:8px}
.expense-metric-icon{width:30px;height:30px}
.expense-metric small{font-size:7.8px}
.expense-metric b{font-size:16px}

.expense-focus-tabs{
  margin:10px 3px 10px;
  padding:3px;
  gap:4px;
  border-radius:19px;
  background:rgba(247,244,235,.95);
  box-shadow:inset 0 0 0 1px rgba(69,84,72,.07);
}
.expense-focus-tab{
  min-height:46px;
  border-radius:16px;
  padding:7px 3px 6px;
}
.expense-focus-tab.active{
  background:linear-gradient(180deg,#2f6046,#244f39);
  box-shadow:0 7px 15px rgba(37,78,55,.18);
}
.expense-focus-tab .tab-main{
  font:600 10.5px var(--cn-serif);
}
.lang-en .expense-focus-tab .tab-main{font:600 9px/1.05 var(--serif)}

.expense-section-card{
  margin:8px 3px;
  padding:10px 10px;
  border-radius:21px;
  background:rgba(255,254,249,.91);
  border:1px solid rgba(70,84,73,.09);
  box-shadow:0 7px 17px rgba(52,65,54,.045);
}
.expense-section-head{margin-bottom:8px}
.expense-section-head h3{
  font:650 15px/1.2 var(--cn-serif);
}
.expense-section-link{font-size:8px}

.member-balance-card{padding-bottom:11px}
.member-balance-summary{min-height:45px}
.balance-avatar{
  width:41px;height:41px;
  border:2px solid #fbf8ef;
}
.member-overlap{padding-left:2px}
.member-overlap .balance-avatar{margin-left:-13px}
.member-balance-summary-copy b{font-size:11px}
.member-balance-summary-copy small{font-size:7.5px}
.member-balance-grid{
  grid-template-columns:repeat(4,1fr);
  gap:10px 6px;
  padding-top:11px;
}
.member-balance-person img,.member-balance-person .avatar{
  width:46px;height:46px;
}
.member-balance-person b{font-size:8.8px}
.member-balance-person span{font-size:9.4px}

.expense-recent-list{gap:5px}
.expense-recent-row{
  min-height:58px;
  grid-template-columns:52px 1fr auto 12px;
  gap:8px;
  padding:6px 7px;
  border-radius:15px;
  background:rgba(255,255,255,.75);
}
.expense-thumb{
  width:52px;height:46px;border-radius:11px;
}
.expense-recent-main b{
  font:600 11px/1.2 var(--cn-serif);
}
.expense-recent-main small{
  font-size:7.6px;margin-top:3px;
}
.expense-recent-money b{font-size:14px}
.expense-recent-money small{font-size:7.4px}

.settlement-card .settlement-row{
  min-height:42px;
  padding:6px 1px;
}
.settlement-route{gap:5px}
.settlement-route img,.settlement-route .avatar{
  width:24px;height:24px;
}
.settlement-remind{
  padding:6px 9px;
  font-size:7.6px;
  border-radius:9px;
}

.expense-fab{
  width:54px;height:54px;
  right:max(14px,calc((100vw - 460px)/2 + 14px));
  bottom:calc(var(--nav-h) + env(safe-area-inset-bottom) + 14px);
  background:linear-gradient(180deg,#315e46,#244f39);
  box-shadow:0 11px 23px rgba(32,73,50,.24);
}

/* Empty states should not stretch the preview structure into giant white blocks. */
#expenses .state-card{
  min-height:74px;
  padding:14px 10px;
  border:0;
  background:transparent;
  box-shadow:none;
}
#expenses .state-card h3{
  font:600 14px var(--cn-serif);
  margin:0 0 4px;
}
#expenses .state-card p{
  margin:0;
  font-size:8px;
  color:#7f877f;
}

/* Keep the bottom navigation visually locked like the approved mockup. */
#expenses ~ .bottom-nav,
.bottom-nav{
  background:rgba(251,249,242,.97);
  border-top:1px solid rgba(66,81,70,.09);
  box-shadow:0 -6px 18px rgba(49,60,51,.035);
}

/* Modals match the preview's compact central panel. */
.expense-detail-backdrop,.expense-sheet-backdrop{
  padding:18px 14px calc(var(--nav-h) + env(safe-area-inset-bottom) + 14px);
}
.expense-detail-panel{
  width:min(86vw,350px);
  border-radius:25px;
  background:#fbf9f2;
}
.expense-sheet-panel{
  width:min(90vw,380px);
  border-radius:25px;
}


/* ───── Expenses v9 — member balance morph animation ───── */
.member-balance-morph{
  cursor:pointer;
  overflow:hidden;
  will-change:height;
}
.member-balance-stage-row{
  display:flex;
  align-items:center;
  min-height:48px;
  transition:min-height .38s cubic-bezier(.22,.78,.25,1);
}
.member-balance-stage{
  flex:1;
  min-width:0;
  display:flex;
  align-items:center;
  position:relative;
  height:48px;
  padding-left:2px;
  transition:height .38s cubic-bezier(.22,.78,.25,1);
}
.member-morph-item{
  width:42px;
  min-width:42px;
  position:relative;
  margin-left:-13px;
  z-index:calc(30 - var(--member-i));
  will-change:transform;
}
.member-morph-item:first-child{margin-left:0}
.member-morph-avatar{
  display:block;
  width:42px;
  height:42px;
  border-radius:50%;
  object-fit:cover;
  border:2px solid #fbf8ef;
  box-shadow:0 3px 9px rgba(37,57,43,.12);
  background:#e7eadf;
}
.member-morph-meta{
  position:absolute;
  left:50%;
  top:47px;
  transform:translateX(-50%);
  width:74px;
  text-align:center;
  opacity:0;
  pointer-events:none;
}
.member-morph-meta b{
  display:block;
  font:600 8.7px/1.15 var(--serif);
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.member-morph-meta span{
  display:block;
  margin-top:2px;
  font:650 9.2px/1 var(--serif);
}
.member-balance-morph .member-balance-summary-copy{
  opacity:1;
  max-width:95px;
  transition:opacity .18s ease,max-width .32s ease,margin .32s ease;
}
.member-balance-morph.expanded .member-balance-stage-row{
  min-height:155px;
}
.member-balance-morph.expanded .member-balance-stage{
  height:155px;
  display:grid;
  grid-template-columns:repeat(4,1fr);
  grid-template-rows:repeat(2,72px);
  gap:8px 5px;
  align-items:start;
  padding:3px 1px 0;
}
.member-balance-morph.expanded .member-morph-item{
  width:auto;
  min-width:0;
  margin-left:0;
  z-index:1;
  display:flex;
  flex-direction:column;
  align-items:center;
}
.member-balance-morph.expanded .member-morph-avatar{
  width:46px;
  height:46px;
}
.member-balance-morph.expanded .member-morph-meta{
  position:static;
  transform:none;
  width:100%;
  margin-top:4px;
  opacity:1;
}
.member-balance-morph.expanded .member-balance-summary-copy{
  opacity:0;
  max-width:0;
  margin-left:0;
  overflow:hidden;
}
@media(max-width:360px){
  .member-morph-item{width:39px;min-width:39px;margin-left:-12px}
  .member-morph-avatar{width:39px;height:39px}
  .member-balance-morph.expanded .member-morph-avatar{width:44px;height:44px}
}
@media(prefers-reduced-motion:reduce){
  .member-balance-morph,.member-balance-stage-row,.member-balance-stage,
  .member-balance-summary-copy{transition:none!important}
}


/* ───── Expenses v10 avatar centering + faster synchronized morph ───── */
.member-morph-avatar,
.balance-avatar,
.member-balance-person img,
.expense-avatar-choice img,
.settlement-route img{
  object-fit:cover!important;
  object-position:50% 50%!important;
}
.member-balance-morph{
  transition:height .30s cubic-bezier(.22,.78,.25,1),box-shadow .24s ease!important;
}
.member-balance-stage-row{
  transition:min-height .30s cubic-bezier(.22,.78,.25,1)!important;
}
.member-balance-stage{
  transition:height .30s cubic-bezier(.22,.78,.25,1)!important;
}
.member-balance-morph .member-balance-summary-copy{
  transition:opacity .14s ease,max-width .24s ease,margin .24s ease!important;
}
.member-morph-meta{
  transition:none!important;
}


/* ───── Expenses v11 polish ───── */
.expense-refresh{display:none!important}

.member-balance-actions{
  display:flex;
  align-items:center;
  gap:7px;
}
.member-add-btn{
  border:1px solid rgba(45,83,61,.12);
  background:#edf2e9;
  color:#355d47;
  border-radius:999px;
  padding:5px 8px;
  font-size:7.8px;
  line-height:1;
  cursor:pointer;
  white-space:nowrap;
}
.member-add-btn:active{transform:scale(.97)}

/* Layout state changes are instant while JS handles the visual FLIP. */
.member-balance-morph.morph-measuring,
.member-balance-morph.morph-measuring .member-balance-stage-row,
.member-balance-morph.morph-measuring .member-balance-stage,
.member-balance-morph.morph-measuring .member-balance-summary-copy{
  transition:none!important;
}

/* Remove competing CSS timing: avatar movement + card height are JS-synchronized. */
.member-balance-stage-row,
.member-balance-stage,
.member-balance-morph,
.member-balance-morph .member-balance-summary-copy{
  transition:none!important;
}

/* Ensure avatar artwork stays visually centered in every circular bubble. */
.member-morph-avatar,
.balance-avatar,
.member-balance-person img,
.expense-avatar-choice img,
.settlement-route img{
  object-fit:cover!important;
  object-position:center center!important;
}

/* Avatar picker gets enough room to be a clear, usable member-creation window. */
.expense-avatar-picker{
  grid-template-columns:repeat(5,1fr)!important;
  gap:10px 7px!important;
  margin:8px 0 3px!important;
}
.expense-avatar-choice img{
  width:50px!important;
  height:50px!important;
}
.expense-avatar-choice span{
  font-size:7px!important;
  margin-top:4px!important;
}

/* Settlement card now shows every calculated transfer cleanly. */
.settlement-card{
  overflow:visible;
}
.settlement-card .settlement-row{
  grid-template-columns:minmax(0,1fr) auto auto!important;
}


/* ───── Expenses v12 member manager + canonical avatars ───── */
.member-manage-btn{
  border:0;
  background:transparent;
  color:#52695b;
  font-size:7.8px;
  padding:5px 4px;
  cursor:pointer;
  white-space:nowrap;
}
.member-manage-btn:active{transform:scale(.97)}

.member-manager-list{
  display:grid;
  gap:8px;
  margin:8px 0 12px;
}
.member-manage-row{
  display:grid;
  grid-template-columns:46px minmax(0,1fr);
  gap:9px;
  padding:10px;
  border-radius:16px;
  border:1px solid rgba(65,82,69,.09);
  background:rgba(255,255,255,.66);
}
.member-manage-row.inactive{opacity:.58}
.member-manage-avatar{
  width:46px;
  height:46px;
  border-radius:50%;
  object-fit:cover;
  object-position:center center;
  border:2px solid #f8f4ea;
  box-shadow:0 3px 8px rgba(41,58,46,.10);
}
.member-manage-copy{min-width:0}
.member-manage-copy b{
  display:block;
  font:600 11px var(--cn-serif);
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.lang-en .member-manage-copy b{font-family:var(--serif)}
.member-manage-copy small{
  display:block;
  color:#838a84;
  font-size:7.5px;
  margin-top:3px;
}
.member-manage-actions{
  grid-column:1/-1;
  display:flex;
  gap:5px;
  flex-wrap:wrap;
  padding-left:55px;
}
.member-action{
  border:1px solid rgba(58,85,67,.11);
  background:#eef2e9;
  color:#3d5d4a;
  border-radius:10px;
  padding:6px 8px;
  font-size:7.5px;
  cursor:pointer;
}
.member-action.me{background:#e3eee0}
.member-action.danger{
  background:#f7ece8;
  color:#9a554d;
  border-color:rgba(154,85,77,.10);
}
.expense-avatar-choice img,
.member-morph-avatar,
.member-manage-avatar{
  object-fit:cover!important;
  object-position:50% 50%!important;
}


/* ───── v14 prettier member manage chip ───── */
.member-balance-actions{
  display:flex;
  align-items:center;
  gap:8px;
}
.member-manage-btn{
  border:1px solid rgba(77,102,81,.10);
  background:linear-gradient(180deg, rgba(252,250,244,.98) 0%, rgba(245,241,232,.98) 100%);
  color:#355341;
  border-radius:14px;
  padding:7px 10px;
  display:inline-flex;
  align-items:center;
  gap:8px;
  box-shadow:0 6px 18px rgba(44,58,48,.06);
  cursor:pointer;
  min-width:92px;
}
.member-manage-btn:active{transform:scale(.985)}
.member-manage-btn-icon{
  width:22px;height:22px;
  display:grid;place-items:center;
  border-radius:999px;
  background:rgba(75,109,82,.10);
  color:#40634c;
  font-size:10px;
  flex:0 0 22px;
}
.member-manage-btn-copy{
  display:flex;
  flex-direction:column;
  align-items:flex-start;
  line-height:1.05;
}
.member-manage-btn-copy b{
  font:700 9.2px var(--cn-serif);
  letter-spacing:.01em;
  color:#355341;
}
.lang-en .member-manage-btn-copy b{
  font-family:var(--serif);
  font-size:8.9px;
}
.member-manage-btn-copy small{
  font-size:6.6px;
  color:#879083;
  margin-top:2px;
}


/* ───── Expenses v15 manage chip + wallet arrows ───── */
.member-balance-actions{
  display:flex;
  align-items:center;
  gap:7px;
}
.member-manage-btn{
  border:1px solid rgba(67,89,72,.12)!important;
  background:linear-gradient(180deg,#fbfaf5 0%,#f1eee5 100%)!important;
  color:#355341!important;
  border-radius:13px!important;
  padding:6px 9px!important;
  display:inline-flex!important;
  align-items:center!important;
  gap:7px!important;
  box-shadow:0 5px 14px rgba(45,60,49,.06)!important;
  cursor:pointer!important;
  min-width:92px!important;
}
.member-manage-btn-icon{
  width:21px;height:21px;
  border-radius:50%;
  display:grid;place-items:center;
  background:#e9efe7;
  color:#3f654c;
  font-size:9px;
  flex:0 0 21px;
}
.member-manage-btn-copy{
  display:flex;
  flex-direction:column;
  align-items:flex-start;
  line-height:1.05;
}
.member-manage-btn-copy b{
  font:700 8.8px var(--cn-serif)!important;
  color:#355341!important;
  white-space:nowrap;
}
.lang-en .member-manage-btn-copy b{
  font-family:var(--serif)!important;
  font-size:8.2px!important;
}
.member-manage-btn-copy small{
  margin-top:2px;
  font-size:6.5px;
  color:#8a9189;
  white-space:nowrap;
}
.expense-metric-icon .icon{width:18px;height:18px}


/* ───── Expenses v16 direct net settlement flow ───── */
.settlement-flow-card{overflow:hidden;position:relative}
.settlement-flow-sub{display:block;margin-top:3px;font-size:7.2px;color:#89918a;font-weight:400}
.settlement-flow-hint{margin:0 1px 9px;padding:7px 9px;border-radius:12px;background:#eef3ea;color:#56705e;font-size:7.8px;text-align:center}
.settlement-flow-board{position:relative;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:44px;min-height:118px}
.settlement-flow-svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none;z-index:2}
.settlement-flow-col{position:relative;z-index:3;min-width:0}
.settlement-flow-col-title{display:flex;align-items:center;justify-content:space-between;gap:6px;margin-bottom:6px;padding:0 3px;font:650 10px/1.2 var(--cn-serif);color:#314b3b}
.lang-en .settlement-flow-col-title{font-family:var(--serif);font-size:9px}
.settlement-flow-col-title span{min-width:18px;height:18px;display:grid;place-items:center;border-radius:999px;background:#edf2e9;color:#53705d;font:600 7px var(--sans)}
.settlement-flow-list{display:grid;gap:7px}
.settlement-person{width:100%;min-width:0;min-height:56px;border:1px solid rgba(70,84,73,.08);border-radius:15px;padding:7px;background:rgba(255,255,255,.74);box-shadow:0 5px 13px rgba(46,59,49,.035);display:grid;grid-template-columns:38px minmax(0,1fr) auto;align-items:center;gap:7px;position:relative;text-align:left}
button.settlement-person{appearance:none;color:inherit;cursor:pointer}
.settlement-person:active{transform:scale(.988)}
.settlement-payer.active{background:linear-gradient(180deg,#2f694a,#285d42);border-color:transparent;color:#fff;box-shadow:0 8px 18px rgba(40,92,63,.18)}
.settlement-flow-avatar{width:38px;height:38px;border-radius:50%;object-fit:cover;object-position:center;border:2px solid #f8f4ea;box-shadow:0 2px 6px rgba(40,55,45,.08)}
.settlement-payer.active .settlement-flow-avatar{border-color:rgba(255,255,255,.72)}
.settlement-person-copy{min-width:0}
.settlement-person-copy b{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font:600 9.2px/1.15 var(--serif)}
.settlement-person-copy small{display:block;margin-top:3px;color:#7f8880;font-size:7px;line-height:1.15}
.settlement-person-copy small strong{font:650 8px var(--serif);color:#a95c4d}
.settlement-payer.active .settlement-person-copy small,.settlement-payer.active .settlement-person-copy small strong{color:rgba(255,255,255,.84)}
.settlement-person-chevron{font-size:15px;color:#829087}
.settlement-payer.active .settlement-person-chevron{color:#fff}
.settlement-receiver{transition:opacity .18s ease,transform .18s ease,box-shadow .18s ease}
.settlement-receiver.linked{border-color:rgba(45,106,75,.18);box-shadow:0 7px 17px rgba(45,106,75,.08);transform:translateX(2px)}
.settlement-receiver.dimmed{opacity:.34}
.settlement-receiver-amount{font:650 8.4px var(--serif);color:#2d6a4b;white-space:nowrap}
.settlement-flow-path{fill:none;stroke:#2d6a4b;stroke-width:2.2;stroke-linecap:round;opacity:.92;transition:stroke-dashoffset .38s cubic-bezier(.22,.78,.25,1);transition-delay:var(--flow-delay);filter:drop-shadow(0 1px 1px rgba(45,106,75,.08))}
@media(max-width:360px){.settlement-flow-board{gap:34px}.settlement-person{grid-template-columns:34px minmax(0,1fr);min-height:52px}.settlement-flow-avatar{width:34px;height:34px}.settlement-person-chevron,.settlement-receiver-amount{grid-column:2;justify-self:start}.settlement-receiver-amount{margin-top:-3px}}


/* ───── Expenses v17 settlement i18n + arrow geometry ───── */
.settlement-flow-board{
  grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;
  gap:52px!important;
}
.settlement-flow-svg{
  z-index:2!important;
}
.settlement-flow-col{
  z-index:3!important;
}
.settlement-flow-path{
  stroke-width:2.35!important;
  stroke:#2d6a4b!important;
  fill:none!important;
  stroke-linecap:round!important;
  stroke-linejoin:round!important;
}
.settlement-flow-origin{
  fill:#2d6a4b;
  opacity:.9;
}
.settlement-receiver.linked{
  transform:none!important;
  border-color:rgba(45,106,75,.20)!important;
  box-shadow:0 7px 17px rgba(45,106,75,.08)!important;
}
.settlement-receiver.dimmed{opacity:.28!important}
.settlement-flow-hint{
  font-size:8px!important;
  letter-spacing:0!important;
}
.settlement-flow-sub{
  font-size:7.4px!important;
  color:#89918a!important;
}
@media(max-width:380px){
  .settlement-flow-board{gap:40px!important}
}

'''
BODY_OPEN = r'''
</head>
<body>
<div class="app-shell">
'''
BODY_SHELL = r'''

  <main>
    <section id="home" class="page active"></section>
    <section id="food" class="page"></section>
    <section id="expenses" class="page"></section>
  </main>
  <nav class="bottom-nav" aria-label="Main navigation"></nav>
</div>

'''
SCRIPT_CORE = r'''<script>
const DATA=__DATA__;
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const days=DATA.days;
let lang='zh', currentPage='home', foodCategory='all', foodRadius=2, foodPoolRadius=0, swipeDayIdx=0, swipeFlipped=false, wx=null;
let userLocation=null,locationTimestamp=0,geoStatus='idle',foodPois=[],foodLoading=false,foodError='',selectedFood=null,foodQuery='',foodSearchTimer=null,lastOverpassAt=0;
let pendingAmapKind='',pendingAmapWindow=null;
let expenseTab='overview',expenseFocus='paid',memberBalancesExpanded=false,ledger={members:[],expenses:[],splits:[],settlements:[]},cloudStatus='local',fxRate=null;

const I18N={
 zh:{
  nav_home:'首页',nav_food:'美食',nav_expenses:'花费',switch_lang:'切换为英文',
  morning:'早上好，',afternoon:'下午好，',evening:'晚上好，',home_line:'和家人，一起看更大的世界。',hero_1:'成都，',hero_2:'刚刚好。',
  weather_loading:'天气更新中',sunny:'晴',partly:'晴间多云',cloudy:'多云',fog:'雾',rain:'有雨',snow:'有雪',showers:'阵雨',storm:'雷雨',chengdu:'成都',chongqing:'重庆',
  food_title:'附近美食',food_sub:'我现在在这里，附近有什么值得吃？',search_food:'搜索附近店铺',range:'范围',retry:'重试',location_title:'需要当前位置',location_body:'允许一次定位，才能查找真正位于你附近的店。应用不会持续追踪位置。',locate:'获取当前位置',locating:'正在寻找你的位置…',location_denied:'定位权限未开启',location_denied_body:'请在浏览器设置中允许定位，然后再试一次。',location_insecure:'需要安全连接',location_insecure_body:'请使用 HTTPS，或在本机用 localhost / 127.0.0.1 打开后重试。',location_unavailable:'暂时无法获取位置',location_unavailable_body:'这通常不是因为你不在成都。请确认设备定位已开启，稍后重试。',nearby_services:'附近服务',opens_amap:'点击后自动打开高德',opening_amap:'正在打开高德…',popup_blocked:'浏览器阻止了新窗口，请允许弹出窗口后重试。',
  all:'全部',sichuan:'川菜',hotpot:'火锅',snacks:'小吃',noodles:'面食',coffee:'咖啡',dessert:'甜品',more:'更多',
  nothing_food:'附近还没找到合适的店。',wider:'换个距离再看看。',service_down:'附近搜索暂时不可用。',cached:'正在显示上次缓存的结果。',smart_score:'推荐分',limited:'数据有限',high_conf:'高可信',open:'营业中',hours_listed:'有营业时间资料',walk:'步行约 {n} 分钟',
  more_recommendations:'更多推荐',sorted_by_score:'按推荐排序',food_categories:'食物类别',category_unknown:'类别资料有限',no_hours:'暂无营业时间资料',hours:'营业时间',data_source:'资料来源',data_status:'数据状态',osm_notice:'资料来自 OpenStreetMap，可能不包含最新菜单、价格或完整营业时间，建议到店前再确认。',open_amap:'在高德地图中打开',
  tag_hotpot:'火锅',tag_sichuan:'川菜',tag_chinese:'中餐',tag_noodles:'面食',tag_seafood:'海鲜',tag_bbq:'烧烤',tag_curry:'咖喱',tag_malaysian:'马来西亚菜',tag_southeast_asian:'东南亚菜',tag_thai:'泰国菜',tag_vietnamese:'越南菜',tag_japanese:'日料',tag_korean:'韩餐',tag_western:'西餐',tag_burger:'汉堡',tag_pizza:'披萨',tag_fastfood:'快餐',tag_dessert:'甜品',tag_icecream:'冰淇淋',tag_coffee:'咖啡',tag_tea:'茶饮',tag_bakery:'烘焙',tag_dimsum:'点心',tag_dumpling:'饺子',tag_vegetarian:'素食',tag_rice:'米饭类',tag_snacks:'小吃',
  food_detail:'店铺详情',category:'类别',distance:'距离',walking:'步行',status:'状态',price:'价格',unknown:'暂无资料',navigate:'高德导航',search_dp:'大众点评搜索',search_red:'小红书搜索',amap_nearby:'打开高德搜索附近',
  attractions:'景点',convenience:'便利店',toilets:'厕所',pharmacy:'药房',shopping_places:'商场',hotels:'酒店',food:'美食',nearby_loading:'正在查找附近地点…',
  expenses_title:'花费',expenses_sub:'旅行账本与家庭分账',overview:'总览',bills:'账单',split:'分账',members:'成员',local_mode:'本机模式：数据只保存在这个浏览器。配置 Supabase 后即可与家人同步。',cloud_mode:'家庭共享已开启',syncing:'正在同步',sync_failed:'同步失败，已保留本机数据',refresh:'刷新',
  trip_expense_sub:'成都家庭旅行 · {n}人',view_all:'查看全部',collapse:'收起',member_balance:'成员结余',members_count:'{n}位成员',balances_count:'{n}人有结余',recent_expenses:'最近花费',settlement_suggestions:'结算建议',view_details:'查看详情',remind:'提醒',done:'完成',expense_details:'账单详情',choose_avatar:'选择头像',change_avatar:'更换头像',my_payments:'我付了',owed_to_me_tab:'别人欠我',i_owe_others:'我欠别人',paid_by_short:'{name} 支付 · {n}人',settled_short:'已结清',avatar_1:'熊猫旅行家',avatar_2:'熊猫优雅女',avatar_3:'熊猫潮酷男',avatar_4:'熊猫时尚女',avatar_5:'熊猫摄影师',avatar_6:'熊猫活力青年',avatar_7:'三星堆少年',avatar_8:'三星堆少女',avatar_9:'熊猫美食家',avatar_10:'熊猫山城旅人',
  actual_spend:'我的实际花费',i_paid:'我已付款',owed_to_me:'别人欠我',i_owe:'我欠别人',unsettled:'尚未结清',no_me:'请先在“成员”中选择“这是我”。',no_expenses:'还没有账单。',start_today:'第一笔就从今天开始吧。',add_expense:'新增账单',record_payment:'记录还款',settled:'已结清',mark_settled:'标记已结清',
  food_cat:'餐饮',transport:'交通',tickets:'门票',shopping_expense:'购物',lodging:'住宿',other:'其他',amount:'金额',description:'说明 / 备注',optional:'可选',paid_by:'谁付款',participants:'参与成员',split_method:'分账方式',equal:'平均分',exact:'指定金额',percentage:'百分比',shares:'按份数',save:'保存',cancel:'取消',invalid_total:'分账合计必须等于账单金额。',select_participant:'请至少选择一位参与成员。',saved:'已保存',queued_offline:'已保存到本机，联网后会自动同步',
  paid_total:'已付款',allocated:'应承担',net_balance:'净余额',from:'付款人',to:'收款人',payment_amount:'还款金额',no_balances:'目前没有需要结清的款项。',
  add_member:'添加成员',member_name:'成员姓名',this_is_me:'这是我',rename:'重命名',deactivate:'停用',activate:'启用',inactive_label:'已停用',member_needed:'请先添加家庭成员。',member_exists:'这个名字已经存在。',cannot_deactivate_me:'请先选择另一位“这是我”的成员。',
  skip:'跳过',brand:'我们的<br>成都故事',family_journey:'一家人的旅程',landing_note:'慢一点，<br>和家人在一起。',landing_dates:'2026年10月15–20日 · 家庭旅行',enter:'开启我们的成都之旅',before:'成都之前',after:'旅程之后',
  day:'第{n}天',close:'关闭',delete:'删除',confirm_deactivate:'确定停用这位成员吗？',confirm_delete_expense:'确定删除这笔账单吗？',cny:'人民币',myr:'马币参考'
 },
 en:{
  nav_home:'Home',nav_food:'Food',nav_expenses:'Expenses',switch_lang:'Switch to Chinese',
  morning:'Good morning,',afternoon:'Good afternoon,',evening:'Good evening,',home_line:'See a bigger world, together as a family.',hero_1:'Chengdu.',hero_2:'Just right.',
  weather_loading:'Weather updating',sunny:'Sunny',partly:'Partly cloudy',cloudy:'Cloudy',fog:'Fog',rain:'Rain',snow:'Snow',showers:'Showers',storm:'Thunderstorms',chengdu:'Chengdu',chongqing:'Chongqing',
  food_title:'Nearby Food',food_sub:'What is worth eating near me right now?',search_food:'Search nearby places',range:'Distance',retry:'Retry',location_title:'Location needed',location_body:'Allow one location check to find places truly near you. The app does not track continuously.',locate:'Use My Location',locating:'Finding your location…',location_denied:'Location permission is off',location_denied_body:'Allow location in your browser settings, then try again.',location_insecure:'Secure connection required',location_insecure_body:'Open the app over HTTPS, or use localhost / 127.0.0.1 when running it locally.',location_unavailable:'Location is temporarily unavailable',location_unavailable_body:'This is not caused by being outside Chengdu. Check that device location is on, then try again.',nearby_services:'Nearby Services',opens_amap:'Tap to open AMap automatically',opening_amap:'Opening AMap…',popup_blocked:'Your browser blocked the new window. Allow pop-ups and try again.',
  server_search_now:'Search nearby places',server_search_hint:'Location ready. Tap to search nearby places.',
  all:'All',sichuan:'Sichuan',hotpot:'Hot Pot',snacks:'Snacks',noodles:'Noodles',coffee:'Coffee',dessert:'Dessert',more:'More',
  nothing_food:'Nothing suitable nearby yet.',wider:'Try a wider radius.',service_down:'Nearby search is temporarily unavailable.',cached:'Showing the last cached results.',smart_score:'Smart Score',limited:'Limited data',high_conf:'High confidence',open:'Open',hours_listed:'Hours available',walk:'~{n} min walk',
  more_recommendations:'More recommendations',sorted_by_score:'Recommended first',food_categories:'Food categories',category_unknown:'Limited category data',no_hours:'No hours data',hours:'Opening hours',data_source:'Data source',data_status:'Data status',osm_notice:'Data comes from OpenStreetMap and may not include the latest menu, prices, or complete opening hours. Please confirm before visiting.',open_amap:'Open in AMap',
  tag_hotpot:'Hot Pot',tag_sichuan:'Sichuan',tag_chinese:'Chinese',tag_noodles:'Noodles',tag_seafood:'Seafood',tag_bbq:'Barbecue',tag_curry:'Curry',tag_malaysian:'Malaysian',tag_southeast_asian:'Southeast Asian',tag_thai:'Thai',tag_vietnamese:'Vietnamese',tag_japanese:'Japanese',tag_korean:'Korean',tag_western:'Western',tag_burger:'Burgers',tag_pizza:'Pizza',tag_fastfood:'Fast Food',tag_dessert:'Dessert',tag_icecream:'Ice Cream',tag_coffee:'Coffee',tag_tea:'Tea',tag_bakery:'Bakery',tag_dimsum:'Dim Sum',tag_dumpling:'Dumplings',tag_vegetarian:'Vegetarian',tag_rice:'Rice',tag_snacks:'Snacks',
  food_detail:'Place Details',category:'Category',distance:'Distance',walking:'Walking',status:'Status',price:'Price',unknown:'Not available',navigate:'Navigate',search_dp:'Search Dianping',search_red:'Search Xiaohongshu',amap_nearby:'Search Nearby in AMap',
  attractions:'Attractions',convenience:'Convenience',toilets:'Toilets',pharmacy:'Pharmacy',shopping_places:'Shopping',hotels:'Hotels',food:'Food',nearby_loading:'Finding nearby places…',
  expenses_title:'Expenses',expenses_sub:'Trip spending and family splitting',overview:'Overview',bills:'Expenses',split:'Split',members:'Members',local_mode:'Local mode: data stays in this browser. Configure Supabase to share with family.',cloud_mode:'Family sharing is active',syncing:'Syncing',sync_failed:'Sync failed; local data is safe',refresh:'Refresh',
  trip_expense_sub:'Chengdu Family Trip · {n}',view_all:'View all',collapse:'Collapse',member_balance:'Member balances',members_count:'{n} members',balances_count:'{n} with balance',recent_expenses:'Recent expenses',settlement_suggestions:'Settlement suggestions',view_details:'View details',remind:'Remind',done:'Done',expense_details:'Expense details',choose_avatar:'Choose avatar',change_avatar:'Change avatar',my_payments:'My payments',owed_to_me_tab:'Owed to me',i_owe_others:'I owe others',paid_by_short:'Paid by {name} · {n}',settled_short:'Settled',avatar_1:'Panda Traveler',avatar_2:'Elegant Panda',avatar_3:'Trendy Panda Male',avatar_4:'Fashion Panda Female',avatar_5:'Panda Photographer',avatar_6:'Active Young Panda',avatar_7:'Sanxingdui Boy',avatar_8:'Sanxingdui Girl',avatar_9:'Panda Foodie',avatar_10:'Panda Mountain Traveler',
  actual_spend:'My Actual Spend',i_paid:'I Paid',owed_to_me:'Owed to Me',i_owe:'I Owe',unsettled:'Unsettled',no_me:'Choose “This is me” under Members first.',no_expenses:'No expenses yet.',start_today:"Start with today's first one.",add_expense:'Add Expense',record_payment:'Record Payment',settled:'Settled',mark_settled:'Mark Settled',
  food_cat:'Food',transport:'Transport',tickets:'Tickets',shopping_expense:'Shopping',lodging:'Lodging',other:'Other',amount:'Amount',description:'Description / note',optional:'Optional',paid_by:'Paid by',participants:'Participants',split_method:'Split method',equal:'Split equally',exact:'Exact amounts',percentage:'Percentage',shares:'Shares',save:'Save',cancel:'Cancel',invalid_total:'The split total must equal the expense amount.',select_participant:'Select at least one participant.',saved:'Saved',queued_offline:'Saved locally; it will sync when you are online',
  paid_total:'Paid total',allocated:'Allocated share',net_balance:'Net balance',from:'From',to:'To',payment_amount:'Payment amount',no_balances:'Nothing needs settling right now.',
  add_member:'Add Member',member_name:'Member name',this_is_me:'This is me',rename:'Rename',deactivate:'Deactivate',activate:'Activate',inactive_label:'Inactive',member_needed:'Add a family member first.',member_exists:'That name already exists.',cannot_deactivate_me:'Choose another “This is me” member first.',
  skip:'SKIP',brand:'Our<br>Chengdu Story',family_journey:'A FAMILY JOURNEY',landing_note:'Slower steps.<br>Richer memories.',landing_dates:'15–20 October 2026 · Family journey',enter:'Begin our Chengdu journey',before:'Before Chengdu',after:'After the journey',
  day:'Day {n}',close:'Close',delete:'Delete',confirm_deactivate:'Deactivate this member?',confirm_delete_expense:'Delete this expense?',cny:'CNY',myr:'MYR estimate'
 }
};
const PLACE_EN={
 '初见山城':'Hello Chongqing','山城漫游':'Mountain City','渝蓉之间':'Chongqing to Chengdu','熊猫都江':'Pandas & Dujiangyan','成都慢游':'Slow Chengdu','带回成都':'Homeward',
 '三星堆':'Sanxingdui','人民公园':"People's Park",'IFS':'IFS','春熙路':'Chunxi Road','天府机场':'Tianfu International Airport','高铁前往重庆':'High-Speed Rail to Chongqing','抵达重庆':'Arrive in Chongqing','自由活动':'Free Time','山城步道':'Shancheng Trail','十八梯':'Shibati','下浩里':'Xiahaoli','解放碑':'Jiefangbei','朝天门广场':'Chaotianmen Square','洪崖洞':'Hongya Cave','磁器口':'Ciqikou Ancient Town','李子坝':'Liziba','八一路好吃街':'Bayi Road Food Street','返回成都':'Return to Chengdu','熊猫基地':'Panda Base','花花':'Hua Hua','都江堰':'Dujiangyan','灌县古城':'Guanxian Ancient City','钟书阁':'Zhongshuge','南桥':'Nanqiao Bridge','蓝眼泪夜景':'Blue Tears Night View','成都自由日':'Free Day in Chengdu','酒店出发':'Leave Hotel','返程':'Journey Home'
};
const CAT_KEYS={餐饮:'food_cat',交通:'transport',门票:'tickets',购物:'shopping_expense',住宿:'lodging',其他:'other'};
const L=(k,v={})=>{
  let s=(I18N[lang]&&I18N[lang][k])||(I18N.zh&&I18N.zh[k])||k;
  Object.entries(v).forEach(([a,b])=>s=s.replaceAll(`{${a}}`,String(b)));
  return s
};
const proper=s=>lang==='en'?(PLACE_EN[s]||s):s;
const catLabel=c=>L(CAT_KEYS[c]||c);
const money=n=>`¥ ${Number(n||0).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})}`;

/* Safe storage (falls back to memory if the frame blocks localStorage) */
const mem={};
const store={get(k){try{return localStorage.getItem(k)}catch(e){return mem[k]??null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){mem[k]=v}}};
lang=store.get('chengduLang')==='en'?'en':'zh';
const CFG=DATA.config||{};
function browserSafeSupabaseKey(key){
  const k=String(key||'');if(!k||k.toLowerCase().startsWith('sb_secret_')||k.toLowerCase().includes('service_role'))return false;
  if(k.split('.').length===3)try{const p=JSON.parse(atob(k.split('.')[1].replace(/-/g,'+').replace(/_/g,'/')));if(p.role==='service_role')return false}catch(e){}
  return true;
}
const CLOUD=!!(CFG.supabase_url&&browserSafeSupabaseKey(CFG.supabase_key)), TRIP_ID=CFG.trip_id||'chengdu-family-2026';
const uid=()=>globalThis.crypto&&crypto.randomUUID?crypto.randomUUID():`${Date.now()}-${Math.random().toString(16).slice(2)}`;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function toast(msg){const old=$('.toast');if(old)old.remove();const el=document.createElement('div');el.className='toast';el.textContent=msg;document.body.appendChild(el);setTimeout(()=>el.remove(),2300)}
function toggleLang(){lang=lang==='zh'?'en':'zh';store.set('chengduLang',lang);applyLanguage()}
function applyLanguage(){
  document.documentElement.lang=lang==='zh'?'zh-CN':'en';
  document.body.classList.toggle('lang-en',lang==='en');
  foodPois.forEach(p=>{p.name=osmName(p.tags);p.status=p.tags.opening_hours==='24/7'?L('open'):(p.tags.opening_hours?L('hours_listed'):'');p.confidence=p.hasRatingEvidence&&p.reviewEvidence>=5?L('high_conf'):L('limited')});
  const keepDay=swipeDayIdx,keepFlip=swipeFlipped;renderHome(keepDay);if(keepFlip)flipTopCard(true);
  nav();renderLandingText();
  if(currentPage==='food')renderFood();
  if(currentPage==='expenses')renderExpenses();
  showPage(currentPage,false);
}

/* ───── icons ───── */
const ICONS={
 home:'<path d="M3 10.8 10 4l7 6.8v7.1a1.1 1.1 0 0 1-1.1 1.1H4.1A1.1 1.1 0 0 1 3 17.9Z"/><path d="M7.6 19v-5.4h4.8V19"/>',
 homeSolid:'<path d="M10 2.6 2.3 9.5a.6.6 0 0 0 .4 1H4v7.1a1 1 0 0 0 1 1h3.3v-5h3.4v5H15a1 1 0 0 0 1-1v-7.1h1.3a.6.6 0 0 0 .4-1Z" fill="currentColor" stroke="none"/>',
 food:'<path d="M6 3v6M4 3v4a2 2 0 0 0 4 0V3M6 9v8M13 3v14M13 3c3 2 3 6 0 8"/>',
 compass:'<circle cx="10" cy="10" r="7.5"/><path d="m12.8 7.2-1.7 3.9-3.9 1.7 1.7-3.9Z"/>',
 wallet:'<rect x="2" y="6" width="16" height="11.5" rx="2.2"/><path d="M4 6l9-3a1 1 0 0 1 1.3 1v2M13 11.7h5v3h-5a1.5 1.5 0 0 1 0-3Z"/>',
 walletOut:'<rect x="2.3" y="6.2" width="12.2" height="10.8" rx="2"/><path d="M4 6.2l7-2.5a1 1 0 0 1 1.3.9v1.6M11.5 11h5M14 8.5l2.5 2.5L14 13.5"/>',
 walletIn:'<rect x="5.5" y="6.2" width="12.2" height="10.8" rx="2"/><path d="M7 6.2l7-2.5a1 1 0 0 1 1.3.9v1.6M8.5 11h-5M6 8.5 3.5 11 6 13.5"/>',
 calendar:'<rect x="3" y="5" width="14" height="13" rx="2"/><path d="M6 3v4M14 3v4M3 9h14M7 12h.01M10 12h.01M13 12h.01M7 15h.01M10 15h.01"/>',
 chevron:'<path d="m8 4 6 6-6 6"/>', back:'<path d="m12.5 4-6 6 6 6"/>', close:'<path d="M5.5 5.5l9 9M14.5 5.5l-9 9"/>',
 search:'<circle cx="8.7" cy="8.7" r="5.7"/><path d="m13 13 4.5 4.5"/>',
 pin:'<path d="M16 8.5c0 5-6 9-6 9s-6-4-6-9a6 6 0 1 1 12 0Z"/><circle cx="10" cy="8.5" r="2"/>',
 plane:'<path d="m2 12 6-2 3-7 2 .8-1 6.5 4.8 1.9c1.7.7 1 2.5-.5 2.4l-5-.6-3 4-1.5-.6 1.3-4.6-5.6.9Z"/>',
 hotel:'<path d="M3 18V5h9v13M12 9h5v9M6 8h2M6 11h2M6 14h2M15 12h.01M15 15h.01"/>',
 landmark:'<path d="M3 18h14M5 18V9h10v9M3 9h14L10 3 3 9ZM8 12h4M8 15h4"/>',
 leaf:'<path d="M17 3C8 3 4 7 4 13c0 2 1 3 3 3 6 0 9-5 10-13Z"/><path d="M4 18c2-5 5-8 10-11"/>',
 coffee:'<path d="M4 7h10v4a5 5 0 0 1-10 0ZM14 8h1.2a2.3 2.3 0 0 1 0 4.6H14M5 4c1-1 2 1 3 0s2 1 3 0"/>',
 shopping:'<path d="M4 7h12l-1 11H5Z"/><path d="M7 8V6a3 3 0 0 1 6 0v2"/>',
 toilet:'<circle cx="6" cy="4" r="1.5"/><circle cx="14" cy="4" r="1.5"/><path d="M4 8h4v4H7v6H5v-6H4ZM12 8h4l1 5h-2v5h-2v-5h-2Z"/>',
 pharmacy:'<path d="M3 7h14v10H3ZM7 3h6v4M10 9v6M7 12h6"/>',
 trash:'<path d="M4 6h12M8 6V4h4v2M6 6l.7 11h6.6L14 6"/>',
 receive:'<path d="M4 5.5h12v10H4z"/><path d="M7 3.5h6M10 2v7M7.5 6.5 10 9l2.5-2.5"/>',
 refresh:'<path d="M16 6V2l-2 2a7 7 0 1 0 2 9M16 2h-4"/>',
 plus:'<path d="M10 3v14M3 10h14"/>',
 users:'<circle cx="7" cy="7" r="3"/><circle cx="14" cy="8" r="2.5"/><path d="M2 17c.6-3 2.2-5 5-5s4.4 2 5 5M12 13c3-.3 5 1.2 6 4"/>',
 check:'<path d="m3.5 10.5 4 4 9-9"/>',
 edit:'<path d="m4 14-.7 3.7L7 17l9-9-3-3Z"/><path d="m11.5 6.5 3 3"/>',
 locate:'<circle cx="10" cy="10" r="3"/><circle cx="10" cy="10" r="7"/><path d="M10 1v2M10 17v2M1 10h2M17 10h2"/>'
};
const icon=(n,c='')=>`<svg class="icon ${c}" viewBox="0 0 20 20" aria-hidden="true">${ICONS[n]||ICONS.leaf}</svg>`;
const esc=s=>String(s??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));

/* ───── time (China Standard Time; ?now=YYYY-MM-DDTHH:MM overrides for testing) ───── */
function chinaNow(){
  let ov=null;try{ov=new URLSearchParams(window.parent.location.search).get('now')}catch(e){}
  if(ov&&/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(ov))return{iso:ov.slice(0,10),h:+ov.slice(11,13),m:+ov.slice(14,16)};
  const p=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(new Date());
  const o=Object.fromEntries(p.map(x=>[x.type,x.value]));
  return{iso:`${o.year}-${o.month}-${o.day}`,h:+o.hour,m:+o.minute};
}
const hm=t=>{const [h,m]=t.split(':').map(Number);return h*60+m};
function phase(){const n=chinaNow();if(n.iso<'2026-10-15')return'before';if(n.iso>'2026-10-20')return'after';return n.iso==='2026-10-20'?'return':'during'}
function currentDay(){const n=chinaNow();if(n.iso<'2026-10-15')return 1;if(n.iso>'2026-10-20')return 6;return Math.max(1,Math.min(6,Number(n.iso.slice(-2))-14))}
function greeting(){const h=chinaNow().h;return h<12?L('morning'):h<18?L('afternoon'):L('evening')}
function greetingEN(){return''}
function weatherCN(c){if(c===null||c===undefined)return L('weather_loading');if(c<=1)return c===0?L('sunny'):L('partly');if(c<=3)return L('cloudy');if(c<=48)return L('fog');if(c<=67)return L('rain');if(c<=77)return L('snow');if(c<=82)return L('showers');if(c<=99)return L('storm');return L('weather_loading')}

'''
LOCATION_JAVASCRIPT = r'''/* ───── Location + Overpass shared engine ───── */
const FOOD_FILTERS=['all','sichuan','hotpot','snacks','noodles','coffee','dessert'];
const AMAP_NEARBY_TYPES=['attractions','convenience','toilets','pharmacy','coffee','shopping','hotels'];
const rad=x=>x*Math.PI/180;
function distanceM(a,b,c,d){const R=6371000,p=rad(c-a),q=rad(d-b),h=Math.sin(p/2)**2+Math.cos(rad(a))*Math.cos(rad(c))*Math.sin(q/2)**2;return 2*R*Math.asin(Math.sqrt(h))}
function distanceText(m){return m<1000?`${Math.round(m/10)*10} m`:`${(m/1000).toFixed(m<3000?1:0)} km`}
function outOfChina(lat,lon){return lon<72.004||lon>137.8347||lat<0.8293||lat>55.8271}
function gcjTransformLat(x,y){let r=-100+2*x+3*y+.2*y*y+.1*x*y+.2*Math.sqrt(Math.abs(x));r+=(20*Math.sin(6*x*Math.PI)+20*Math.sin(2*x*Math.PI))*2/3;r+=(20*Math.sin(y*Math.PI)+40*Math.sin(y/3*Math.PI))*2/3;r+=(160*Math.sin(y/12*Math.PI)+320*Math.sin(y*Math.PI/30))*2/3;return r}
function gcjTransformLon(x,y){let r=300+x+2*y+.1*x*x+.1*x*y+.1*Math.sqrt(Math.abs(x));r+=(20*Math.sin(6*x*Math.PI)+20*Math.sin(2*x*Math.PI))*2/3;r+=(20*Math.sin(x*Math.PI)+40*Math.sin(x/3*Math.PI))*2/3;r+=(150*Math.sin(x/12*Math.PI)+300*Math.sin(x/30*Math.PI))*2/3;return r}
function wgs84ToGcj02(lat,lon){if(outOfChina(lat,lon))return{lat,lon};const a=6378245,ee=.006693421622965943,dLat=gcjTransformLat(lon-105,lat-35),dLon=gcjTransformLon(lon-105,lat-35),radLat=lat/180*Math.PI,magic=1-ee*Math.sin(radLat)**2,sqrt=Math.sqrt(magic);return{lat:lat+(dLat*180)/((a*(1-ee))/(magic*sqrt)*Math.PI),lon:lon+(dLon*180)/(a/sqrt*Math.cos(radLat)*Math.PI)}}
function amapNavigationUrl(p){const c=wgs84ToGcj02(p.lat,p.lon),q=encodeURIComponent(p.name);return`https://uri.amap.com/navigation?to=${c.lon.toFixed(6)},${c.lat.toFixed(6)},${q}&mode=walk&policy=1&src=chengdu-story&callnative=1`}
function amapNearbyUrl(kind='all'){if(!userLocation)return'https://uri.amap.com/';const c=wgs84ToGcj02(userLocation.lat,userLocation.lon),names={food:lang==='zh'?'美食':'Food',attractions:lang==='zh'?'景点':'Attractions',convenience:lang==='zh'?'便利店':'Convenience Store',toilets:lang==='zh'?'厕所':'Toilets',coffee:lang==='zh'?'咖啡':'Coffee',pharmacy:lang==='zh'?'药房':'Pharmacy',shopping:lang==='zh'?'商场':'Shopping',hotels:lang==='zh'?'酒店':'Hotels',all:lang==='zh'?'附近':'Nearby'};return`https://uri.amap.com/search?keyword=${encodeURIComponent(names[kind]||names.all)}&center=${c.lon.toFixed(6)},${c.lat.toFixed(6)}&view=map&src=chengdu-story&callnative=1`}
function finishAmapOpen(){
  if(!pendingAmapKind)return;
  const url=amapNearbyUrl(pendingAmapKind),w=pendingAmapWindow;
  pendingAmapKind='';pendingAmapWindow=null;
  if(w&&!w.closed){try{w.location.href=url;w.opener=null;return}catch(e){}}
  const opened=window.open(url,'_blank','noopener');if(!opened)toast(L('popup_blocked'))
}
function cancelAmapOpen(){const w=pendingAmapWindow;pendingAmapKind='';pendingAmapWindow=null;if(w&&!w.closed)try{w.close()}catch(e){}}
function openAmapNearby(kind){
  expireLocationIfNeeded();
  if(locationFresh()){const opened=window.open(amapNearbyUrl(kind),'_blank','noopener');if(!opened)toast(L('popup_blocked'));return}
  pendingAmapKind=kind;pendingAmapWindow=window.open('about:blank','_blank');
  if(pendingAmapWindow)try{pendingAmapWindow.document.write(`<meta name="viewport" content="width=device-width,initial-scale=1"><p style="font-family:sans-serif;padding:24px">${L('opening_amap')}</p>`)}catch(e){}
  requestLocation('amap')
}
function cacheRead(k,maxAge=30*60*1000){try{const x=JSON.parse(store.get(k)||'null');return x&&Date.now()-x.ts<maxAge?x.data:null}catch(e){return null}}
function cacheAny(k){try{const x=JSON.parse(store.get(k)||'null');return x?x.data:null}catch(e){return null}}
function cacheWrite(k,data){store.set(k,JSON.stringify({ts:Date.now(),data}))}
function locCache(){return userLocation?`${Math.round(userLocation.lat*500)}:${Math.round(userLocation.lon*500)}`:'none'}
let foodRequestSeq=0,foodRequestKey='';
const LOCATION_MAX_AGE=12*60*1000;
const locationFresh=()=>!!(userLocation&&locationTimestamp&&Date.now()-locationTimestamp<=LOCATION_MAX_AGE);
function expireLocationIfNeeded(){if(userLocation&&!locationFresh()){userLocation=null;locationTimestamp=0;geoStatus='idle';foodPois=[];selectedFood=null}}
function foodServerUrl(force=false,poolRadius=foodRadius){
  if(!userLocation)return'';
  let base='';
  try{base=window.parent.location.href}catch(e){}
  if(!base)base=document.referrer||'';
  if(!base||base==='about:srcdoc')return'';
  const u=new URL(base);
  u.searchParams.set('food_lat',Number(userLocation.lat).toFixed(4));
  u.searchParams.set('food_lon',Number(userLocation.lon).toFixed(4));
  u.searchParams.set('food_r',String(poolRadius));
  u.searchParams.set('food_cat',String(foodCategory||'all'));
  if(force)u.searchParams.set('food_refresh',String(Date.now()));
  else u.searchParams.delete('food_refresh');
  return u.toString()
}
function requestServerFood(force=false,poolRadius=foodRadius){
  if(!userLocation)return;
  const href=foodServerUrl(force,poolRadius);
  if(!href){foodLoading=false;foodError='failed';if(currentPage==='food')renderFood();return}
  foodLoading=true;foodError='';
  if(currentPage==='food')renderFood();

  // This function is called from an actual tap/click (search/filter/radius).
  // A real target=_top link is reliable inside Streamlit's component sandbox.
  const a=document.createElement('a');
  a.href=href;
  a.target='_top';
  a.rel='noopener';
  a.style.display='none';
  document.body.appendChild(a);
  a.click();
  setTimeout(()=>a.remove(),1000)
}
function requestLocation(source='food'){
  const redraw=()=>{if(currentPage==='food')renderFood()};
  if(locationFresh()){
    geoStatus='ready';redraw();return
  }
  if(!window.isSecureContext){geoStatus='insecure';redraw();return}
  if(!navigator.geolocation){geoStatus='unavailable';redraw();return}
  geoStatus='pending';redraw();

  const acceptPosition=p=>{
    locationTimestamp=Date.now();
    userLocation={
      lat:p.coords.latitude,
      lon:p.coords.longitude,
      accuracy:p.coords.accuracy,
      ts:locationTimestamp
    };
    geoStatus='ready';
    store.set('chengduLastLocation',JSON.stringify(userLocation));
    if(source==='amap'){finishAmapOpen();return}
    // IMPORTANT: do not attempt top-frame navigation inside this async
    // geolocation callback. Mobile Safari/Streamlit sandbox may block it.
    // Render a second explicit "search nearby" button instead.
    redraw()
  };
  const failFinal=e=>{
    if(source==='amap')cancelAmapOpen();
    if(userLocation){geoStatus='ready';redraw();return}
    geoStatus=e&&e.code===1?'denied':'unavailable';
    redraw()
  };

  navigator.geolocation.getCurrentPosition(
    acceptPosition,
    firstErr=>{
      if(firstErr&&firstErr.code===1){failFinal(firstErr);return}
      navigator.geolocation.getCurrentPosition(
        acceptPosition,
        failFinal,
        {enableHighAccuracy:true,timeout:15000,maximumAge:5*60*1000}
      )
    },
    {enableHighAccuracy:false,timeout:20000,maximumAge:10*60*1000}
  )
}
function cleanFoodQueryParams(){}
function osmPhoto(t){if(t.image&&/^https?:/i.test(t.image))return t.image;if(t.wikimedia_commons){const f=t.wikimedia_commons.replace(/^File:/,'');return`https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(f)}?width=800`}return''}
function osmName(t){return t[lang==='zh'?'name:zh':'name:en']||t.name||t['name:zh']||t['name:en']||L('unknown')}
function foodCategoryOf(t){const c=(t.cuisine||'').toLowerCase(),a=t.amenity||'';if(a==='cafe')return'coffee';if(a==='ice_cream'||/dessert|ice_cream|cake/.test(c))return'dessert';if(/hot_pot|hotpot/.test(c))return'hotpot';if(/noodle|ramen/.test(c))return'noodles';if(a==='fast_food'||a==='food_court')return'snacks';if(/sichuan|chinese/.test(c))return'sichuan';return'more'}
function foodLabel(k){return L(k)}
function smartScore(p){const r=parseFloat(p.tags.rating||p.tags['rating:google']||0),reviews=parseInt(p.tags.review_count||p.tags['reviews']||0,10),evidence=Number.isFinite(r)&&r>0;let s=50+Math.max(0,10-Math.round(p.distance/300));if(p.tags.opening_hours)s+=4;if(p.tags.website||p.tags.phone||p.tags['contact:phone'])s+=4;if(p.tags.cuisine)s+=3;if(p.photo)s+=2;if(evidence)s+=Math.round(Math.min(5,r)*5)+(reviews>=20?5:reviews>=5?2:0);p.hasRatingEvidence=evidence;p.reviewEvidence=reviews;return Math.max(50,Math.min(evidence?94:76,s))}
function normalizePois(elements,kind){return elements.map(e=>{const t=e.tags||{},lat=e.lat??e.center?.lat,lon=e.lon??e.center?.lon;if(lat==null||lon==null)return null;const name=osmName(t),p={id:String(e.type)+e.id,lat,lon,tags:t,name,photo:osmPhoto(t),distance:userLocation?distanceM(userLocation.lat,userLocation.lon,lat,lon):0};p.foodCat=foodCategoryOf(t);p.score=smartScore(p);p.walk=Math.max(1,Math.ceil(p.distance/78));p.status=t.opening_hours==='24/7'?L('open'):(t.opening_hours?L('hours_listed'):'');p.confidence=p.hasRatingEvidence&&p.reviewEvidence>=5?L('high_conf'):L('limited');return p}).filter(p=>p&&(kind!=='food'||p.name!==L('unknown'))).sort((a,b)=>kind==='food'?b.score-a.score:a.distance-b.distance)}

'''
NAVIGATION_JAVASCRIPT = r'''/* ───── Navigation ───── */
function nav(){
  const items=[['home','nav_home'],['food','nav_food'],['expenses','nav_expenses']],ic={home:'home',food:'food',expenses:'wallet'};
  $('.bottom-nav').innerHTML=items.map(x=>`<button class="nav-btn" data-page="${x[0]}" onclick="showPage('${x[0]}')"><span data-ic="${x[0]}"></span><span>${L(x[1])}</span></button>`).join('');
  $$('.nav-btn').forEach(b=>{b.dataset.icon=ic[b.dataset.page]});
}
function showPage(name,rerender=true){
  if(name==='food')expireLocationIfNeeded();
  currentPage=name;
  $$('.page').forEach(p=>p.classList.toggle('active',p.id===name));
  $$('.nav-btn').forEach(b=>{
    const on=b.dataset.page===name;b.classList.toggle('active',on);
    b.firstElementChild.innerHTML=icon(b.dataset.page==='home'&&on?'homeSolid':b.dataset.icon);
  });
  if(rerender){if(name==='home')sizeSwipe();if(name==='food')renderFood();if(name==='expenses')renderExpenses()}
  settleAtTop();
  requestAnimationFrame(fitFrame);
  setTimeout(fitFrame,80);
}
function scrollHome(){try{document.scrollingElement.scrollTo({top:0,left:0,behavior:'instant'})}catch(e){}document.documentElement.scrollTop=0;document.body.scrollTop=0;try{window.parent.scrollTo({top:0,left:0,behavior:'instant'})}catch(e){}}
function settleAtTop(){scrollHome();requestAnimationFrame(()=>{scrollHome();requestAnimationFrame(scrollHome)})}

'''
BOOT_AND_DOCUMENT_END = r'''/* ───── boot ───── */
ledger=loadLocalLedger();
try{const savedLoc=JSON.parse(store.get('chengduLastLocation')||'null');if(savedLoc&&Number.isFinite(savedLoc.lat)&&Number.isFinite(savedLoc.lon)&&Number.isFinite(savedLoc.ts)&&Date.now()-savedLoc.ts<=LOCATION_MAX_AGE){userLocation=savedLoc;locationTimestamp=savedLoc.ts;geoStatus='ready'}}catch(e){}
if(DATA.server_food){
  const sf=DATA.server_food;
  if(Number.isFinite(+sf.lat)&&Number.isFinite(+sf.lon)){
    locationTimestamp=Date.now();
    userLocation={lat:+sf.lat,lon:+sf.lon,accuracy:null,ts:locationTimestamp};
    geoStatus='ready';
    store.set('chengduLastLocation',JSON.stringify(userLocation));
  }
  if(Number.isFinite(+sf.radius))foodPoolRadius=+sf.radius;
  if(Number.isFinite(+sf.view_radius))foodRadius=+sf.view_radius;
  else if(Number.isFinite(+sf.radius))foodRadius=+sf.radius;
  if(sf.view_category)foodCategory=sf.view_category;
  foodPois=normalizePois(sf.elements||[],'food').filter(p=>p.distance<=foodPoolRadius*1000);
  foodError=sf.status==='stale'?'cached':(sf.status==='failed'?'failed':'');
  foodLoading=false;
  cleanFoodQueryParams();
}
prepareLanding();nav();renderHome();renderExpenses();showPage(DATA.initial_page||'home');fitFrame();loadWeather();loadFx();if(CLOUD)syncLedger();
window.addEventListener('resize',()=>{fitFrame();sizeSwipe()});
window.addEventListener('online',()=>{if(CLOUD)syncLedger()});
setInterval(()=>{const g=$('#greet'),ge=$('#greetEn');if(g)g.textContent=greeting();if(ge)ge.textContent=greetingEN();if(currentPage==='home'&&swipeFlipped){const i=swipeDayIdx;renderSwipeStack(i);flipTopCard(true)}},60000);
setInterval(loadWeather,15*60*1000);
</script>
</body>
</html>'''


def build_html(payload: str) -> str:
    """Assemble page modules in their original byte order."""
    import expenses
    import food
    import home
    import landing

    template = "".join(
        [
            HTML_PREFIX,
            home.CSS,
            NAV_CSS,
            SHARED_PAGES_CSS,
            FUNCTIONAL_PAGES_CSS,
            landing.CSS,
            BODY_OPEN,
            landing.MARKUP,
            BODY_SHELL,
            SCRIPT_CORE,
            home.JAVASCRIPT,
            LOCATION_JAVASCRIPT,
            food.JAVASCRIPT,
            expenses.JAVASCRIPT,
            NAVIGATION_JAVASCRIPT,
            landing.JAVASCRIPT,
            BOOT_AND_DOCUMENT_END,
        ]
    )
    return template.replace("__DATA__", payload)
