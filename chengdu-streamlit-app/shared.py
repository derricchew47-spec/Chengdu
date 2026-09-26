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


def build_payload() -> str:
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
let lang='zh', currentPage='home', foodCategory='all', foodRadius=2, swipeDayIdx=0, swipeFlipped=false, wx=null;
let userLocation=null,locationTimestamp=0,geoStatus='idle',foodPois=[],foodLoading=false,foodError='',selectedFood=null,foodQuery='',foodSearchTimer=null,lastOverpassAt=0;
let pendingAmapKind='',pendingAmapWindow=null;
let expenseTab='overview',ledger={members:[],expenses:[],splits:[],settlements:[]},cloudStatus='local',fxRate=null;

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
  all:'All',sichuan:'Sichuan',hotpot:'Hot Pot',snacks:'Snacks',noodles:'Noodles',coffee:'Coffee',dessert:'Dessert',more:'More',
  nothing_food:'Nothing suitable nearby yet.',wider:'Try a wider radius.',service_down:'Nearby search is temporarily unavailable.',cached:'Showing the last cached results.',smart_score:'Smart Score',limited:'Limited data',high_conf:'High confidence',open:'Open',hours_listed:'Hours available',walk:'~{n} min walk',
  more_recommendations:'More recommendations',sorted_by_score:'Recommended first',food_categories:'Food categories',category_unknown:'Limited category data',no_hours:'No hours data',hours:'Opening hours',data_source:'Data source',data_status:'Data status',osm_notice:'Data comes from OpenStreetMap and may not include the latest menu, prices, or complete opening hours. Please confirm before visiting.',open_amap:'Open in AMap',
  tag_hotpot:'Hot Pot',tag_sichuan:'Sichuan',tag_chinese:'Chinese',tag_noodles:'Noodles',tag_seafood:'Seafood',tag_bbq:'Barbecue',tag_curry:'Curry',tag_malaysian:'Malaysian',tag_southeast_asian:'Southeast Asian',tag_thai:'Thai',tag_vietnamese:'Vietnamese',tag_japanese:'Japanese',tag_korean:'Korean',tag_western:'Western',tag_burger:'Burgers',tag_pizza:'Pizza',tag_fastfood:'Fast Food',tag_dessert:'Dessert',tag_icecream:'Ice Cream',tag_coffee:'Coffee',tag_tea:'Tea',tag_bakery:'Bakery',tag_dimsum:'Dim Sum',tag_dumpling:'Dumplings',tag_vegetarian:'Vegetarian',tag_rice:'Rice',tag_snacks:'Snacks',
  food_detail:'Place Details',category:'Category',distance:'Distance',walking:'Walking',status:'Status',price:'Price',unknown:'Not available',navigate:'Navigate',search_dp:'Search Dianping',search_red:'Search Xiaohongshu',amap_nearby:'Search Nearby in AMap',
  attractions:'Attractions',convenience:'Convenience',toilets:'Toilets',pharmacy:'Pharmacy',shopping_places:'Shopping',hotels:'Hotels',food:'Food',nearby_loading:'Finding nearby places…',
  expenses_title:'Expenses',expenses_sub:'Trip spending and family splitting',overview:'Overview',bills:'Expenses',split:'Split',members:'Members',local_mode:'Local mode: data stays in this browser. Configure Supabase to share with family.',cloud_mode:'Family sharing is active',syncing:'Syncing',sync_failed:'Sync failed; local data is safe',refresh:'Refresh',
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
const L=(k,v={})=>{let s=(I18N[lang]&&I18N[lang][k])||I18N.zh[k]||k;Object.entries(v).forEach(([a,b])=>s=s.replaceAll(`{${a}}`,b));return s};
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
function requestLocation(source='food'){
  const redraw=()=>{if(currentPage==='food')renderFood()};
  const useCurrent=()=>{
    if(userLocation){geoStatus='ready';redraw();if(currentPage==='food'&&!foodPois.length&&!foodLoading)loadFoodPois()}
  };
  // Use a recent cached location immediately on mobile, then refresh only when stale.
  if(locationFresh()){useCurrent();return}
  if(!window.isSecureContext){geoStatus='insecure';redraw();return}
  if(!navigator.geolocation){geoStatus='unavailable';redraw();return}
  geoStatus='pending';redraw();

  const acceptPosition=async p=>{
    locationTimestamp=Date.now();
    userLocation={lat:p.coords.latitude,lon:p.coords.longitude,accuracy:p.coords.accuracy,ts:locationTimestamp};
    geoStatus='ready';
    store.set('chengduLastLocation',JSON.stringify(userLocation));
    if(currentPage==='food')await loadFoodPois(true)
  };
  const failFinal=e=>{
    // Do not destroy a previously usable location/results on refresh failure.
    if(userLocation){geoStatus='ready';redraw();return}
    geoStatus=e&&e.code===1?'denied':'unavailable';
    redraw()
  };

  // First attempt: low-power, allow recent device cache, mobile-friendly timeout.
  navigator.geolocation.getCurrentPosition(
    acceptPosition,
    firstErr=>{
      if(firstErr&&firstErr.code===1){failFinal(firstErr);return}
      // One fallback only: ask for higher accuracy if the normal request timed out/failed.
      navigator.geolocation.getCurrentPosition(
        acceptPosition,
        failFinal,
        {enableHighAccuracy:true,timeout:15000,maximumAge:5*60*1000}
      )
    },
    {enableHighAccuracy:false,timeout:20000,maximumAge:10*60*1000}
  )
}
async function fetchOverpass(query,key){
  const fresh=cacheRead(key);
  if(fresh)return{data:fresh,cached:false,stale:false};

  const stale=cacheAny(key);
  const wait=Math.max(0,1100-(Date.now()-lastOverpassAt));
  if(wait)await sleep(wait);
  lastOverpassAt=Date.now();

  const endpoints=[
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
    'https://overpass.nchc.org.tw/api/interpreter',
    'https://overpass.private.coffee/api/interpreter'
  ];

  for(const url of endpoints){
    let timer;
    try{
      const c=new AbortController();
      timer=setTimeout(()=>c.abort(),22000);
      const r=await fetch(url,{
        method:'POST',
        headers:{'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'},
        body:'data='+encodeURIComponent(query),
        signal:c.signal,
        cache:'no-store'
      });
      clearTimeout(timer);
      if(!r.ok)throw Error(String(r.status));
      const j=await r.json();
      const data=j.elements||[];
      cacheWrite(key,data);
      return{data,cached:false,stale:false}
    }catch(e){
      if(timer)clearTimeout(timer);
    }
  }

  if(stale)return{data:stale,cached:true,stale:true};
  throw Error('overpass')
}
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
}
function scrollHome(){try{document.scrollingElement.scrollTo({top:0,left:0,behavior:'instant'})}catch(e){}document.documentElement.scrollTop=0;document.body.scrollTop=0;try{window.parent.scrollTo({top:0,left:0,behavior:'instant'})}catch(e){}}
function settleAtTop(){scrollHome();requestAnimationFrame(()=>{scrollHome();requestAnimationFrame(scrollHome)})}

'''
BOOT_AND_DOCUMENT_END = r'''/* ───── boot ───── */
ledger=loadLocalLedger();
try{const savedLoc=JSON.parse(store.get('chengduLastLocation')||'null');if(savedLoc&&Number.isFinite(savedLoc.lat)&&Number.isFinite(savedLoc.lon)&&Number.isFinite(savedLoc.ts)&&Date.now()-savedLoc.ts<=LOCATION_MAX_AGE){userLocation=savedLoc;locationTimestamp=savedLoc.ts;geoStatus='ready'}}catch(e){}
prepareLanding();nav();renderHome();renderExpenses();showPage('home');fitFrame();loadWeather();loadFx();if(CLOUD)syncLedger();
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
