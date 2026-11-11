from __future__ import annotations

import html
import itertools
import math
from typing import List, Tuple

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="지폭 구성 계산기",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Theme / layout — compact header + isolated SVG renderer + TEST sequence control + inline roll width editor + compact top spacing (v5)
# -----------------------------------------------------------------------------
CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');
:root {
  --navy:#17264c; --navy2:#263968; --blue:#2563eb; --sky:#0ea5e9;
  --ink:#111a32; --muted:#69758d; --line:#dce5f5; --panel:#f4f7ff;
}
html, body, [class*="css"] { font-family:'Noto Sans KR','Malgun Gothic',sans-serif; }
.stApp { background:linear-gradient(180deg,#f4f7ff 0%,#ffffff 42%,#f8faff 100%); color:var(--ink); }
header[data-testid="stHeader"] { background:transparent; }
#MainMenu, footer { visibility:hidden; }
[data-testid="stToolbar"] { visibility:hidden; height:0; }
section[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#eef2ff 0%,#f7f8ff 100%);
  border-right:1px solid #dce4f7;
  min-width:300px; max-width:300px;
}
section[data-testid="stSidebar"] > div { padding-top:1.25rem !important; padding-bottom:.65rem !important; }
section[data-testid="stMain"] > div { padding-top:1.25rem !important; padding-left:1.05rem; padding-right:1.05rem; padding-bottom:.7rem !important; max-width:none; }
section[data-testid="stMain"] .block-container { padding-top:1.25rem !important; padding-bottom:.7rem !important; }
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding-top:1.25rem !important; }
.global-header {
  position:fixed; z-index:999999; top:0; left:0; width:100vw; height:68px;
  background:linear-gradient(105deg,#1a2b55 0%,#2d416f 52%,#17264b 100%);
  box-shadow:0 4px 18px rgba(18,35,76,.18); display:flex; align-items:center;
  padding:0 20px; box-sizing:border-box; color:white;
}
.brand-icon { width:48px; height:48px; margin-right:13px; flex:0 0 auto; }
.brand-title { font-size:23px; line-height:1.12; font-weight:900; letter-spacing:-1.2px; color:#fff; white-space:nowrap; }
.brand-sub { font-size:11px; margin-top:3px; color:#e3eaff; font-weight:500; white-space:nowrap; }
.sidebar-title { font-size:22px; font-weight:900; color:#15254d; margin:0 0 18px 0; letter-spacing:-.7px; }
.sidebar-section { font-size:17px; font-weight:800; color:#18264a; margin:16px 0 8px; }
.sidebar-note {font-size:12px;color:#697792; line-height:1.5; margin-top:2px;}
div[data-testid="stNumberInput"] label, div[data-testid="stRadio"] label {font-weight:650!important;color:#27375f!important;}
div[data-testid="stNumberInput"] input {font-weight:700!important;color:#17264c!important;}
div[data-testid="stNumberInput"] > div {border-radius:10px!important;}
div[data-testid="stRadio"] > label {font-size:15px!important;}
.stButton > button {
  border:0!important; border-radius:12px!important; min-height:50px!important;
  background:linear-gradient(105deg,#3346e9,#2536d8)!important; color:#fff!important;
  font-weight:850!important; font-size:16px!important; box-shadow:0 6px 14px rgba(45,64,221,.18);
}
.stButton > button:hover {filter:brightness(1.04); border:0!important;}
.summary-card {
  min-height:82px; border-radius:15px; border:1px solid #d8e2f7;
  background:linear-gradient(145deg,#ffffff 0%,#f0f4ff 100%);
  box-shadow:0 2px 7px rgba(35,59,115,.035); padding:13px 13px 11px;
  display:flex; align-items:center; gap:12px; box-sizing:border-box;
}
.summary-card.violet {background:linear-gradient(145deg,#f6f5ff,#e9eaff); border-color:#d8d8ff;}
.summary-card.blue {background:linear-gradient(145deg,#f0f6ff,#e3edff); border-color:#cedeff;}
.summary-icon {width:36px;height:36px;flex:0 0 36px;color:#51639b;}
.summary-label {font-size:13px;color:#29375b;font-weight:800;white-space:nowrap;margin-bottom:4px;}
.summary-value {font-size:20px;line-height:1.15;font-weight:900;color:#111b3a;white-space:nowrap;letter-spacing:-.7px;}
.summary-value small {font-size:14px;font-weight:800;letter-spacing:0;}
.summary-sub {font-size:11px;color:#586783;font-weight:600;margin-top:3px;white-space:nowrap;}
.section-title {font-size:22px;font-weight:900;color:#101b3b;letter-spacing:-.6px;display:flex;align-items:center;gap:11px;margin:4px 0 8px;}
.section-icon {color:#2463ff;font-size:25px;}
.panel {background:rgba(255,255,255,.88);border:1px solid #dce6fa;border-radius:15px;padding:12px 13px 13px;box-shadow:0 2px 10px rgba(31,56,112,.025);height:100%;}
.panel-title {display:flex;align-items:center;gap:9px;font-weight:900;color:#14224b;font-size:18px;border-bottom:1px solid #e5eaf5;padding-bottom:8px;margin-bottom:8px;letter-spacing:-.4px;}
.panel-title .ico {font-size:22px;color:#2865f5;}
.green-panel {background:linear-gradient(145deg,#f1fff2,#f8fff9);border:1px solid #c9efcf;border-radius:15px;overflow:hidden;box-shadow:0 2px 10px rgba(28,140,58,.03);}
.green-title {background:linear-gradient(90deg,#e3f9e7,#effff1);color:#187632;font-size:18px;font-weight:900;padding:10px 13px;display:flex;gap:9px;align-items:center;}
.green-content {padding:10px 13px 13px;}
.checkline {display:flex;gap:9px;align-items:flex-start;margin:0 0 9px;font-size:13px;line-height:1.45;color:#14233b;font-weight:700;}
.check {color:#189b39;font-size:20px;line-height:1;font-weight:900;}
.kv {display:flex;justify-content:space-between;gap:8px;padding:6px 1px;border-bottom:1px solid #e5eaf3;font-size:13px;line-height:1.35;}
.kv:last-child{border-bottom:0;}
.kv .k{font-weight:750;color:#293650;}
.kv .v{font-weight:850;color:#111a32;text-align:right;}
.roll-wrap {margin-top:2px;margin-bottom:3px;}
.roll-editor-head {font-size:13px;font-weight:900;color:#23365f;margin:3px 0 5px;display:flex;align-items:center;gap:7px;}
.roll-editor-head span {color:#2865f5;font-size:17px;}
.roll-editor-label {font-size:10px;font-weight:850;color:#34476f;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin:0 0 2px;}
.roll-editor-label.test {color:#a85100;}
div[data-testid="stNumberInput"].roll-width-input input {text-align:center!important;font-size:13px!important;font-weight:850!important;padding-left:3px!important;padding-right:3px!important;}
.roll-editor-note {font-size:10px;color:#7b879e;margin:1px 0 5px;}
.warning-panel {background:linear-gradient(145deg,#fff8ed,#fffdf8);border:1px solid #f2d6aa;border-radius:15px;overflow:hidden;box-shadow:0 2px 10px rgba(160,105,25,.03);}
.warning-title {background:linear-gradient(90deg,#fff0d5,#fff8eb);color:#9a5a00;font-size:18px;font-weight:900;padding:10px 13px;display:flex;gap:9px;align-items:center;}
.warning-content {padding:10px 13px 13px;}
.roll-caption {font-size:12px;color:#8290a8;margin:0 0 4px 2px;}
.width-table {width:100%;border-collapse:separate;border-spacing:0;overflow:hidden;border-radius:10px;font-size:12px;}
.width-table th {background:#eaf0fc;color:#293755;padding:8px 5px;font-weight:850;border-right:1px solid #dce5f3;border-bottom:1px solid #dce5f3;text-align:center;}
.width-table td {background:#fff;color:#16213d;padding:7px 5px;text-align:center;border-right:1px solid #e7edf8;border-bottom:1px solid #e7edf8;font-weight:600;white-space:nowrap;}
.width-table tr:nth-child(even) td {background:#f7f9fe;}
.width-table .total-row td {background:#eaf0fc;font-weight:900;color:#101b38;}
.pill-test {background:#ffe0b3;color:#874000;padding:2px 8px;border-radius:6px;font-weight:900;}
.pill-normal {background:#dce8ff;color:#1d4d9b;padding:2px 8px;border-radius:6px;font-weight:800;}
.csv-button {display:block;text-decoration:none;border:1px solid #a9c4ff;border-radius:10px;padding:10px 12px;text-align:center;color:#193a9e;font-size:15px;font-weight:900;background:linear-gradient(180deg,#f4f8ff,#e5eeff);}
.info-pill {display:inline-block;background:linear-gradient(90deg,#dce8ff,#eef3ff);border-radius:30px;padding:7px 17px;font-size:14px;font-weight:850;color:#142859;}
.total-pill {display:inline-block;background:linear-gradient(110deg,#192c58,#354977);border-radius:30px;padding:7px 24px;font-size:15px;font-weight:900;color:white;box-shadow:0 4px 10px rgba(18,34,75,.16);}
hr {border-color:#e7ecf5!important;}
@media(max-width:1100px){
 .summary-card{gap:6px;padding:10px 7px;}.summary-icon{width:30px;height:30px;flex-basis:30px;}.summary-value{font-size:18px;}
}
@media(max-width:800px){
 .global-header{height:62px;padding:0 14px}.brand-title{font-size:21px}.brand-sub{font-size:10px}.brand-icon{width:42px;height:42px}
 section[data-testid="stMain"] > div{padding-top:1.05rem!important;padding-left:.55rem;padding-right:.55rem}
 section[data-testid="stMain"] .block-container{padding-top:1.05rem!important}
 section[data-testid="stSidebar"] > div{padding-top:1.05rem!important}
 section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{padding-top:1.05rem!important}
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

HEADER = r"""
<div class="global-header">
 <svg class="brand-icon" viewBox="0 0 100 100" aria-hidden="true">
  <defs><linearGradient id="paper" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#fff"/><stop offset=".55" stop-color="#e8edfa"/><stop offset="1" stop-color="#aebbd7"/></linearGradient><linearGradient id="core" x1="0" x2="1"><stop stop-color="#d3d9e8"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#8795b5"/></linearGradient></defs>
  <path d="M14 34 61 12Q70 8 77 14l9 7Q91 25 88 34L67 73Q63 81 54 84L17 69Q8 65 9 55L10 43Q10 37 14 34Z" fill="url(#paper)" stroke="#f8fbff" stroke-width="2"/>
  <path d="M19 37 61 20Q68 17 75 22L82 27 60 65Q56 72 49 73L18 61Q13 59 14 52L14 44Q14 40 19 37Z" fill="#f8fbff" opacity=".93"/>
  <ellipse cx="25" cy="51" rx="16" ry="23" transform="rotate(-18 25 51)" fill="url(#core)" stroke="#fff" stroke-width="3"/>
  <ellipse cx="25" cy="51" rx="8" ry="13" transform="rotate(-18 25 51)" fill="#7786a7" stroke="#fff" stroke-width="3"/>
  <path d="M28 31 66 16M37 71 61 78" stroke="#fff" stroke-width="3" opacity=".9" fill="none"/>
 </svg>
 <div><div class="brand-title">지폭 구성 계산기</div><div class="brand-sub">제지회사 지폭 구성 시뮬레이션</div></div>
</div>
"""
st.markdown(HEADER, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SVG roll illustration
# -----------------------------------------------------------------------------

def build_roll_svg(segments: List[dict], left_trim: float, right_trim: float) -> str:
    """Render proportional paper strips inside a cylindrical roll, preserving text aspect ratio."""
    W, H = 1200, 178
    x0, x1 = 136.0, 1110.0
    body_w = x1 - x0
    count = len(segments)
    trim_visual = max(4.0, min(9.0, (left_trim + right_trim) * 0.19))
    product_area = max(1.0, body_w - count * 2 * trim_visual)
    product_sum = sum(float(s["width"]) for s in segments) or 1.0

    normal_colors = [
        ("#e7efff", "#a9c4f1", "#557bbd"),
        ("#e5f7ff", "#a6ddf3", "#309cc9"),
        ("#e7efff", "#a9c4f1", "#557bbd"),
        ("#e5f7ff", "#a6ddf3", "#309cc9"),
        ("#e7efff", "#a9c4f1", "#557bbd"),
    ]
    out = [f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="원롤 분할 시각화">
    <defs>
      <linearGradient id="rollShell" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f9fbff"/><stop offset=".12" stop-color="#dce4f2"/><stop offset=".48" stop-color="#fff"/><stop offset=".88" stop-color="#cbd3e2"/><stop offset="1" stop-color="#eef1f7"/></linearGradient>
      <linearGradient id="rollFace" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#aeb7c7"/><stop offset=".22" stop-color="#fff"/><stop offset=".55" stop-color="#e5e9f0"/><stop offset=".82" stop-color="#fff"/><stop offset="1" stop-color="#a4adbe"/></linearGradient>
      <linearGradient id="trimGrad" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#9ca5b5"/><stop offset=".38" stop-color="#fff"/><stop offset=".7" stop-color="#dce1e9"/><stop offset="1" stop-color="#a1aab9"/></linearGradient>
      <linearGradient id="topSheen" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
      <radialGradient id="coreOuter"><stop stop-color="#756247"/><stop offset=".42" stop-color="#d9c49d"/><stop offset=".68" stop-color="#83745e"/><stop offset=".85" stop-color="#eee2c9"/><stop offset="1" stop-color="#777f8d"/></radialGradient>
      <filter id="shadow" x="-20%" y="-40%" width="140%" height="190%"><feGaussianBlur stdDeviation="5"/></filter>
      <clipPath id="rollClip"><path d="M93 24 C49 24 20 52 20 89 C20 126 49 154 93 154 L1110 154 C1153 154 1180 126 1180 89 C1180 52 1153 24 1110 24 Z"/></clipPath>
      <pattern id="fineLines" width="4" height="4" patternUnits="userSpaceOnUse"><path d="M0 0L4 4" stroke="#9aa4b2" stroke-width=".55" opacity=".55"/></pattern>
    </defs>
    <ellipse cx="602" cy="162" rx="550" ry="7" fill="#26344f" opacity=".16" filter="url(#shadow)"/>
    <path d="M93 24 C49 24 20 52 20 89 C20 126 49 154 93 154 L1110 154 C1153 154 1180 126 1180 89 C1180 52 1153 24 1110 24 Z" fill="url(#rollShell)" stroke="#aeb8c8" stroke-width="1.2"/>
    <g clip-path="url(#rollClip)">
      <rect x="20" y="24" width="1160" height="130" fill="url(#rollShell)"/>
    """]
    x = x0
    segment_geom = []
    for idx, seg in enumerate(segments):
        width = float(seg["width"])
        prod_vis = product_area * width / product_sum
        left_start, left_end = x, x + trim_visual
        prod_start, prod_end = left_end, left_end + prod_vis
        right_start, right_end = prod_end, prod_end + trim_visual
        segment_geom.append((seg, left_start, left_end, prod_start, prod_end, right_start, right_end, prod_vis))
        x = right_end

    for idx, (seg, l0, l1, p0, p1, r0, r1, prod_vis) in enumerate(segment_geom):
        is_test = seg["kind"] == "TEST"
        if is_test:
            c0, c1, c2 = ("#ffe1b7", "#f6a033", "#d9780b")
        else:
            c0, c1, c2 = normal_colors[idx % len(normal_colors)]
        out.append(f"""<rect x="{p0:.2f}" y="25" width="{max(1,p1-p0):.2f}" height="128" fill="{c1}"/>
        <rect x="{p0:.2f}" y="25" width="{max(1,p1-p0):.2f}" height="128" fill="url(#topSheen)" opacity=".8"/>
        <rect x="{l0:.2f}" y="25" width="{trim_visual:.2f}" height="128" fill="url(#trimGrad)"/>
        <rect x="{l0:.2f}" y="25" width="{trim_visual:.2f}" height="128" fill="url(#fineLines)"/>
        <rect x="{r0:.2f}" y="25" width="{trim_visual:.2f}" height="128" fill="url(#trimGrad)"/>
        <rect x="{r0:.2f}" y="25" width="{trim_visual:.2f}" height="128" fill="url(#fineLines)"/>
        <path d="M{p0:.2f} 26 Q{p0+10:.2f} 89 {p0:.2f} 152" stroke="#ffffff" stroke-width="1.2" opacity=".82" fill="none"/>
        <path d="M{p1:.2f} 26 Q{p1-10:.2f} 89 {p1:.2f} 152" stroke="{c2}" stroke-width="1" opacity=".52" fill="none"/>
        """)
        cx = (p0 + p1) / 2
        seq = int(seg["seq"])
        title = f"지폭 {seq}"
        width_txt = f'{float(seg["width"]):,.1f} mm'
        title_fs = max(9, min(16, prod_vis * 0.15))
        width_fs = max(9, min(20, prod_vis * 0.18))
        if is_test:
            badge_txt = str(seg["label"])
            badge_w = min(100, max(42, prod_vis * 0.80))
            badge_fs = max(8, min(13, badge_w * 0.14))
            out.append(f"""<rect x="{cx-badge_w/2:.2f}" y="42" width="{badge_w:.2f}" height="22" rx="8" fill="#ed790d"/>
              <text x="{cx:.2f}" y="57" text-anchor="middle" font-family="Malgun Gothic, Noto Sans CJK KR, sans-serif" font-size="{badge_fs:.1f}" font-weight="900" fill="white">{html.escape(badge_txt)}</text>""")
        out.append(f"""<text x="{cx:.2f}" y="94" text-anchor="middle" font-family="Malgun Gothic, Noto Sans CJK KR, sans-serif" font-size="{title_fs:.1f}" font-weight="900" fill="#111b34">{title}</text>
          <text x="{cx:.2f}" y="121" text-anchor="middle" font-family="Malgun Gothic, Noto Sans CJK KR, sans-serif" font-size="{width_fs:.1f}" font-weight="900" fill="#111b34">{width_txt}</text>
        """)

    out.append("""
      <rect x="20" y="24" width="1160" height="23" fill="url(#topSheen)" opacity=".75"/>
      <path d="M90 25 C49 25 22 53 22 89 C22 125 49 153 90 153" stroke="#fff" stroke-width="2.5" opacity=".8" fill="none"/>
      <path d="M1112 25 C1154 25 1178 53 1178 89 C1178 125 1154 153 1112 153" stroke="#8f9bad" stroke-width="1.8" opacity=".7" fill="none"/>
      <path d="M98 27 L1110 27" stroke="#fff" stroke-width="2.5" opacity=".55"/>
      <path d="M98 151 L1110 151" stroke="#7c8798" stroke-width="1.5" opacity=".28"/>
    </g>
    <ellipse cx="77" cy="89" rx="53" ry="65" fill="url(#rollFace)" stroke="#b8c0cf" stroke-width="1.7"/>
    <ellipse cx="77" cy="89" rx="39" ry="52" fill="none" stroke="#fff" stroke-width="1.8" opacity=".8"/>
    <ellipse cx="77" cy="89" rx="25" ry="34" fill="url(#coreOuter)" stroke="#f7f4ec" stroke-width="2.5"/>
    <ellipse cx="77" cy="89" rx="13" ry="21" fill="#65583f" stroke="#e8d8b7" stroke-width="3"/>
    <ellipse cx="77" cy="89" rx="6" ry="13" fill="#2e3542" opacity=".8"/>
    <path d="M34 58 Q44 36 67 28 M35 120 Q48 142 69 150" stroke="#fff" stroke-width="2.3" opacity=".55" fill="none"/>
    </svg>""")
    return "".join(out)


# -----------------------------------------------------------------------------

# Sidebar inputs + configurable TEST slits
# -----------------------------------------------------------------------------
MANUAL_MODE = "폭 직접 입력\n(사용자 지정)"

def _sync_test_sidebar_to_roll(test_no: int) -> None:
    key = f"test_width_{test_no}"
    st.session_state[f"roll_test_width_{test_no}"] = float(st.session_state[key])

def _sync_test_roll_to_sidebar(test_no: int) -> None:
    key = f"roll_test_width_{test_no}"
    st.session_state[f"test_width_{test_no}"] = float(st.session_state[key])

def _sync_manual_sidebar_to_roll(index: int) -> None:
    st.session_state[f"roll_general_width_{index}"] = float(st.session_state[f"manual_general_{index}"])

def _sync_roll_general_to_manual(index: int) -> None:
    value = float(st.session_state[f"roll_general_width_{index}"])
    st.session_state[f"manual_general_{index}"] = value
    # Editing a normal slit on the roll switches the calculation to custom widths.
    st.session_state["mode_choice"] = MANUAL_MODE

with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ 입력 조건</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">전체 지폭 (고정)</div>', unsafe_allow_html=True)
    deckle = st.number_input("전체 지폭 (mm)", min_value=100.0, max_value=20000.0, value=4850.0, step=10.0, key="deckle", label_visibility="collapsed")

    st.markdown('<div class="sidebar-section">구성할 지폭 개수 (n)</div>', unsafe_allow_html=True)
    n = int(st.number_input("구성할 지폭 개수", min_value=1, max_value=20, value=5, step=1, key="n", label_visibility="collapsed"))

    max_test_count = min(5, n)
    if int(st.session_state.get("test_count", 1)) > max_test_count:
        st.session_state["test_count"] = max_test_count
    st.markdown('<div class="sidebar-section">TEST 지폭 개수 (최대 5개)</div>', unsafe_allow_html=True)
    test_count = int(st.number_input("TEST 지폭 개수", min_value=1, max_value=max_test_count, value=1, step=1, key="test_count", label_visibility="collapsed"))

    st.markdown('<div class="sidebar-section">TEST 지폭 설정 (폭 · 배치)</div>', unsafe_allow_html=True)
    test_widths = []
    test_positions = {}
    used_positions = set()
    for test_no in range(1, test_count + 1):
        width_col, position_col = st.columns([1.05, 0.95], gap="small")
        test_key = f"test_width_{test_no}"
        if test_key not in st.session_state:
            st.session_state[test_key] = 800.0
        with width_col:
            test_width = st.number_input(
                f"TEST {test_no} 폭 (mm)",
                min_value=0.0, max_value=20000.0, step=10.0,
                key=test_key,
                on_change=_sync_test_sidebar_to_roll,
                args=(test_no,),
            )
        test_widths.append(float(test_width))

        pos_key = f"test_position_{test_no}"
        available = [p for p in range(1, n + 1) if p not in used_positions]
        current = st.session_state.get(pos_key, test_no)
        if current not in available:
            current = available[0]
            st.session_state[pos_key] = current
        with position_col:
            selected_pos = st.selectbox(
                f"TEST {test_no} 위치",
                options=available,
                index=available.index(current),
                format_func=lambda p: f"{p}번",
                key=pos_key,
            )
        test_positions[test_no] = int(selected_pos)
        used_positions.add(int(selected_pos))

    st.markdown('<div class="sidebar-section">여폭 설정 (지폭별) ⓘ</div>', unsafe_allow_html=True)
    trim_cols = st.columns(2)
    with trim_cols[0]:
        left_trim = st.number_input("좌측 여폭 (mm)", min_value=0.0, max_value=100.0, value=12.0, step=1.0, key="left_trim")
    with trim_cols[1]:
        right_trim = st.number_input("우측 여폭 (mm)", min_value=0.0, max_value=100.0, value=12.0, step=1.0, key="right_trim")

    st.markdown('<div class="sidebar-section">구성 방식</div>', unsafe_allow_html=True)
    mode_options = ["균등 분할\n(일반 지폭을 동일한 폭으로)", MANUAL_MODE, "폭 조합 검색\n(조건에 맞는 조합 추천)"]
    mode = st.radio(
        "구성 방식",
        mode_options,
        index=0,
        key="mode_choice",
        label_visibility="collapsed",
    )

    general_count = n - test_count
    manual_values: List[float] = []
    search_min, search_max, search_step = 500.0, 1200.0, 10.0
    test_total = sum(test_widths)

    if general_count > 0 and mode.startswith("폭 직접 입력"):
        st.markdown('<div class="sidebar-note">일반 지폭 제품 폭을 왼쪽부터 순서대로 입력하세요.</div>', unsafe_allow_html=True)
        remaining_for_general = max(0.0, deckle - n * (left_trim + right_trim) - test_total)
        each_default = remaining_for_general / general_count
        for i in range(general_count):
            manual_key = f"manual_general_{i}"
            st.session_state.setdefault(manual_key, float(each_default))
            value = st.number_input(
                f"일반 지폭 {i+1} 제품 폭 (mm)",
                min_value=0.0, max_value=20000.0,
                step=0.5, key=manual_key,
                on_change=_sync_manual_sidebar_to_roll,
                args=(i,),
            )
            manual_values.append(float(value))
    elif general_count > 0 and mode.startswith("폭 조합 검색"):
        st.markdown('<div class="sidebar-note">일반 지폭에 적용할 폭 검색 범위를 설정하세요.</div>', unsafe_allow_html=True)
        search_min = st.number_input("최소 폭 (mm)", min_value=1.0, max_value=20000.0, value=500.0, step=10.0, key="search_min")
        search_max = st.number_input("최대 폭 (mm)", min_value=float(search_min), max_value=20000.0, value=max(float(search_min), min(1200.0, float(deckle))), step=10.0, key="search_max")
        search_step = st.number_input("검색 간격 (mm)", min_value=0.5, max_value=100.0, value=10.0, step=0.5, key="search_step")

    st.markdown('<div class="sidebar-note">※ 모든 지폭의 좌·우에 각각 입력한 여폭을 적용합니다.</div>', unsafe_allow_html=True)
    calculate_clicked = st.button("▦  지폭 구성 계산하기", use_container_width=True)

# -----------------------------------------------------------------------------
# Core calculation
# -----------------------------------------------------------------------------
per_width_trim = left_trim + right_trim
total_trim = per_width_trim * n
product_target = deckle - total_trim
general_target = product_target - test_total
general_widths: List[float] = []
calculation_error = None
search_matches: List[Tuple[float, ...]] = []

if product_target < -1e-9:
    calculation_error = "지폭별 여폭 합계가 전체 지폭을 초과합니다. 여폭 또는 지폭 개수를 줄여주세요."
elif test_total > product_target + 1e-9:
    calculation_error = "TEST 제품 폭 합계가 여폭을 제외한 유효 제품 폭보다 큽니다. TEST 폭을 줄여주세요."
elif general_count == 0 and abs(general_target) > 1e-6:
    calculation_error = f"일반 지폭이 없으므로 TEST 제품 폭 합계가 {product_target:,.1f} mm여야 합니다."
elif general_target < -1e-9:
    calculation_error = "TEST 제품 폭 합계가 나머지 일반 지폭을 배치할 수 있는 폭을 초과합니다."
else:
    if general_count == 0:
        general_widths = []
    elif mode.startswith("균등 분할"):
        each = general_target / general_count
        general_widths = [float(each)] * general_count
    elif mode.startswith("폭 직접 입력"):
        if len(manual_values) == general_count:
            general_widths = [float(v) for v in manual_values]
            input_sum = sum(general_widths)
            if abs(input_sum - general_target) > 1e-6:
                calculation_error = (
                    f"직접 입력한 일반 지폭 합계가 목표와 다릅니다. "
                    f"일반 지폭 합계는 {general_target:,.1f} mm여야 합니다. 현재 {input_sum:,.1f} mm입니다."
                )
    else:
        scale = 2  # half-mm precision
        start_i = int(math.ceil(search_min * scale - 1e-9))
        stop_i = int(math.floor(search_max * scale + 1e-9))
        step_i = max(1, int(round(search_step * scale)))
        candidates = list(range(start_i, stop_i + 1, step_i))
        target_i = int(round(general_target * scale))
        if len(candidates) > 180 or general_count > 8:
            calculation_error = "검색 범위가 너무 큽니다. 폭 범위·간격을 조정하거나 일반 지폭 수를 줄여주세요."
        else:
            center_order = sorted(
                range(len(candidates)),
                key=lambda j: (abs(candidates[j] / scale - general_target / general_count), candidates[j]),
            )
            def dfs(pos: int, slots: int, left: int, path: List[int]):
                if len(search_matches) >= 500:
                    return
                if slots == 0:
                    if left == 0:
                        search_matches.append(tuple(v / scale for v in path))
                    return
                if pos >= len(candidates):
                    return
                smallest, largest = candidates[pos], candidates[-1]
                if left < slots * smallest or left > slots * largest:
                    return
                for j in center_order:
                    if j < pos:
                        continue
                    candidate = candidates[j]
                    if candidate > left:
                        continue
                    if slots > 1 and (
                        left - candidate < (slots - 1) * candidate
                        or left - candidate > (slots - 1) * largest
                    ):
                        continue
                    dfs(j, slots - 1, left - candidate, path + [candidate])
                    if len(search_matches) >= 500:
                        return
            dfs(0, general_count, target_i, [])
            if search_matches:
                target_each = general_target / general_count
                search_matches.sort(
                    key=lambda sol: (sum((v - target_each) ** 2 for v in sol), max(sol) - min(sol), sol)
                )
                search_options = [
                    " / ".join(f"{v:,.1f}".rstrip("0").rstrip(".") for v in sol) + " mm"
                    for sol in search_matches
                ]
                chosen = st.selectbox(
                    "추천 조합 선택",
                    options=list(range(len(search_matches))),
                    format_func=lambda i: f"조합 {i+1}: {search_options[i]}",
                )
                general_widths = list(search_matches[chosen])
            else:
                calculation_error = "검색 조건에 맞는 조합을 찾지 못했습니다. 최소·최대 폭 또는 간격을 조정해주세요."

# Merge TEST and general slits into their user-selected positions.
segments: List[dict] = []
if len(general_widths) == general_count and product_target >= -1e-9 and test_total <= product_target + 1e-9:
    test_by_position = {}
    for test_no, width in enumerate(test_widths, start=1):
        test_by_position[test_positions[test_no]] = {
            "kind": "TEST",
            "test_no": test_no,
            "label": f"TEST {test_no}",
            "width": float(width),
        }
    general_iter = iter(general_widths)
    general_slot = 0
    for seq in range(1, n + 1):
        if seq in test_by_position:
            record = dict(test_by_position[seq])
        else:
            record = {
                "kind": "NORMAL",
                "test_no": None,
                "general_idx": general_slot,
                "label": "일반",
                "width": float(next(general_iter)),
            }
            general_slot += 1
        record["seq"] = seq
        segments.append(record)


# -----------------------------------------------------------------------------
# Top cards and dashboard
# -----------------------------------------------------------------------------
# Header / summary strip

def fmt_mm(v: float, decimals: int = 1) -> str:
    if abs(v - round(v)) < 1e-8:
        return f"{v:,.0f}"
    return f"{v:,.{decimals}f}".rstrip("0").rstrip(".")

product_width_for_display = sum(float(seg["width"]) for seg in segments) if segments else product_target

cards = [
    ("◉", "전체 지폭", fmt_mm(deckle), "mm", "", ""),
    ("▱", "지폭 개수", f"{n}", "개", f"TEST {test_count}개 포함", ""),
    ("↔", "지폭별 여폭", fmt_mm(per_width_trim), "mm", f"(좌 {fmt_mm(left_trim)} + 우 {fmt_mm(right_trim)})", ""),
    ("☑", "총 여폭", fmt_mm(total_trim), "mm", f"({fmt_mm(per_width_trim)} mm × {n})", "violet"),
    ("☑", "제품 폭 합계", fmt_mm(product_width_for_display), "mm", "", "blue"),
]
card_cols = st.columns([1.12, .92, 1.12, 1.08, 1.12], gap="small")
for col, (ico, label, value, unit, sub, tone) in zip(card_cols, cards):
    icon_svg = {
        "◉": '<svg class="summary-icon" viewBox="0 0 48 48"><ellipse cx="17" cy="24" rx="8" ry="15" fill="none" stroke="currentColor" stroke-width="3"/><path d="M17 9 37 5Q43 5 44 12L44 34Q43 40 37 41L17 39" fill="none" stroke="currentColor" stroke-width="3"/><ellipse cx="17" cy="24" rx="3" ry="7" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
        "▱": '<svg class="summary-icon" viewBox="0 0 48 48"><path d="m24 5 19 10-19 10L5 15 24 5Z M5 24l19 10 19-10 M5 33l19 10 19-10" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/></svg>',
        "↔": '<svg class="summary-icon" viewBox="0 0 48 48"><path d="M7 24h34M7 24l9-9M7 24l9 9M41 24l-9-9M41 24l-9 9" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        "☑": '<svg class="summary-icon" viewBox="0 0 48 48"><rect x="7" y="7" width="34" height="34" rx="6" fill="none" stroke="#2463ff" stroke-width="3"/><path d="m15 24 7 7 13-15" fill="none" stroke="#2463ff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    }[ico]
    with col:
        st.markdown(f'''<div class="summary-card {tone}"><div>{icon_svg}</div><div><div class="summary-label">{label}</div><div class="summary-value">{value} <small>{unit}</small></div><div class="summary-sub">{sub or '&nbsp;'}</div></div></div>''', unsafe_allow_html=True)

st.markdown("<hr style='margin:7px 0 7px;'>", unsafe_allow_html=True)
st.markdown('<div class="section-title"><span class="section-icon">▥</span> 지폭 구성 결과</div>', unsafe_allow_html=True)

if calculation_error and not segments:
    st.error(calculation_error)
    st.info("입력값을 조정하면 이 영역에 롤 시각화와 상세 구성이 표시됩니다.")
else:
    if calculation_error:
        st.warning(calculation_error + " 폭 입력란을 계속 수정하면 합계를 맞출 수 있습니다.")
    all_widths = [float(seg["width"]) for seg in segments]
    product_sum = sum(all_widths)
    actual_trim = len(all_widths) * per_width_trim
    total_required = product_sum + actual_trim
    remainder = deckle - total_required

    # Roll labels / dimension arrow
    st.markdown(f'''<div style="text-align:center;margin:0 0 1px;"><span class="total-pill">전체 지폭 : {fmt_mm(deckle)} mm</span></div>
    <div style="text-align:center;margin:0 0 -2px;"><span class="info-pill">제품 폭 합계 : {fmt_mm(product_sum)} mm &nbsp; | &nbsp; 총 여폭 : {fmt_mm(actual_trim)} mm <span style="font-size:11px;font-weight:700">({fmt_mm(per_width_trim)} mm × {len(all_widths)})</span></span></div>''', unsafe_allow_html=True)
    # dimension line as SVG
    st.markdown(f'''<svg viewBox="0 0 1200 36" width="100%" height="24" role="img" aria-label="전체 지폭 치수"><path d="M70 20 H1130 M70 8 V29 M1130 8 V29 M70 20 l10 -6 M70 20 l10 6 M1130 20 l-10 -6 M1130 20 l-10 6" fill="none" stroke="#172b64" stroke-width="2.2" stroke-linecap="round"/></svg>''', unsafe_allow_html=True)
    # SVG source is rendered in an isolated HTML iframe. Using st.markdown here
    # causes Streamlit's Markdown parser to expose multi-line SVG markup as text.
    roll_svg = build_roll_svg(segments, left_trim, right_trim)
    roll_html = f'''<!doctype html>
    <html><head><meta charset="utf-8"><style>
      html,body{{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:transparent;}}
      svg{{display:block;width:100%;height:100%;}}
    </style></head><body>{roll_svg}</body></html>'''
    components.html(roll_html, height=166, scrolling=False)
    st.markdown(f'''<div style="text-align:center;font-size:10px;color:#7c879b;margin:-2px 0 4px;">주황색 = TEST 지폭(TEST 1~5) · 파란색 계열 = 일반 지폭 · 회색 사선 = 지폭별 여폭</div>''', unsafe_allow_html=True)

    # Inline width editor: one number input aligned with each visible roll segment.
    # TEST widths sync with their sidebar fields. Editing a normal slit changes the
    # calculation mode to custom widths so the user's value is retained.
    st.markdown('<div class="roll-editor-head"><span>✎</span> 롤 지폭 폭 바로 수정 (mm)</div>', unsafe_allow_html=True)
    editor_weights = [max(250.0, float(seg["width"])) for seg in segments]
    editor_cols = st.columns(editor_weights, gap="small")
    for col, seg in zip(editor_cols, segments):
        with col:
            if seg["kind"] == "TEST":
                test_no = int(seg["test_no"])
                roll_key = f"roll_test_width_{test_no}"
                st.session_state[roll_key] = float(st.session_state.get(f"test_width_{test_no}", seg["width"]))
                label = f"TEST {test_no} · 지폭 {seg['seq']}"
                st.markdown(f'<div class="roll-editor-label test">{html.escape(label)}</div>', unsafe_allow_html=True)
                st.number_input(
                    f"TEST {test_no} 폭 직접 수정", min_value=0.0, max_value=20000.0,
                    step=0.5, key=roll_key, label_visibility="collapsed",
                    on_change=_sync_test_roll_to_sidebar, args=(test_no,),
                )
            else:
                general_idx = int(seg["general_idx"])
                roll_key = f"roll_general_width_{general_idx}"
                if mode.startswith("폭 직접 입력"):
                    inline_default = float(st.session_state.get(f"manual_general_{general_idx}", seg["width"]))
                else:
                    inline_default = float(seg["width"])
                st.session_state[roll_key] = inline_default
                label = f"일반 · 지폭 {seg['seq']}"
                st.markdown(f'<div class="roll-editor-label">{html.escape(label)}</div>', unsafe_allow_html=True)
                st.number_input(
                    f"일반 지폭 {seg['seq']} 폭 직접 수정", min_value=0.0, max_value=20000.0,
                    step=0.5, key=roll_key, label_visibility="collapsed",
                    on_change=_sync_roll_general_to_manual, args=(general_idx,),
                )
    st.markdown('<div class="roll-editor-note">위 숫자 입력란에서 각 지폭의 제품 폭을 바꾸면 롤 이미지와 계산 결과가 함께 갱신됩니다. 일반 지폭을 수정하면 구성 방식이 자동으로 직접 입력으로 전환됩니다.</div>', unsafe_allow_html=True)

    # Details and summary panels
    df = pd.DataFrame({
        "순번": [seg["seq"] for seg in segments],
        "등급": [seg["label"] for seg in segments],
        "제품 폭 (mm)": all_widths,
        "여폭 (좌/우, mm)": [f"{fmt_mm(left_trim)} / {fmt_mm(right_trim)}"] * n,
        "총 폭 (mm)": [w + per_width_trim for w in all_widths],
        "비율 (제품 폭 기준)": [w / product_sum * 100 if product_sum else 0 for w in all_widths],
    })
    table_rows = []
    for row in df.itertuples(index=False):
        seq, grade, prod, trim_txt, gross, ratio = row
        badge = f'<span class="pill-test">{html.escape(grade)}</span>' if grade.startswith("TEST") else '<span class="pill-normal">일반</span>'
        table_rows.append(f"<tr><td>{seq}</td><td>{badge}</td><td>{prod:,.1f}</td><td>{trim_txt}</td><td>{gross:,.1f}</td><td>{ratio:.2f} %</td></tr>")
    table_html = f'''<div class="panel"><div class="panel-title"><span class="ico">☷</span> 지폭 상세 내역</div><table class="width-table"><thead><tr><th>순번</th><th>등급</th><th>제품 폭 (mm)</th><th>여폭<br>(좌/우, mm)</th><th>총 폭<br>(mm)</th><th>비율<br>(제품 폭 기준)</th></tr></thead><tbody>{''.join(table_rows)}<tr class="total-row"><td colspan="2">합계</td><td>{fmt_mm(product_sum,1)}</td><td>{fmt_mm(actual_trim,1)}</td><td>{fmt_mm(total_required,1)}</td><td>100.00 %</td></tr></tbody></table></div>'''

    def kv(k: str, v: str) -> str:
        return f'<div class="kv"><span class="k">{k}</span><span class="v">{v}</span></div>'
    normal_widths = [float(seg["width"]) for seg in segments if seg["kind"] == "NORMAL"]
    if normal_widths:
        if all(abs(w - normal_widths[0]) < 1e-8 for w in normal_widths):
            other_summary = fmt_mm(normal_widths[0]) + " mm (각)"
        else:
            other_summary = " / ".join(fmt_mm(w) for w in normal_widths) + " mm"
    else:
        other_summary = "없음"
    test_summary = " / ".join(
        f'{seg["label"]}: {fmt_mm(float(seg["width"]))} mm ({seg["seq"]}번째)'
        for seg in segments if seg["kind"] == "TEST"
    )
    summary_html = f'''<div class="panel"><div class="panel-title"><span class="ico">◎</span> 구성 요약</div>
    {kv('전체 지폭',fmt_mm(deckle)+' mm')}
    {kv('지폭 개수',f'{n} 개')}
    {kv('지폭별 여폭',f'{fmt_mm(per_width_trim)} mm (좌 {fmt_mm(left_trim)} + 우 {fmt_mm(right_trim)})')}
    {kv('총 여폭',f'{fmt_mm(actual_trim)} mm ({fmt_mm(per_width_trim)} mm × {n})')}
    {kv('제품 폭 합계',fmt_mm(product_sum)+' mm')}
    {kv('TEST 지폭',test_summary)}
    {kv('나머지 지폭',other_summary)}
    </div>'''
    if abs(remainder) <= 1e-5:
        width_status = "일치"
    elif remainder > 0:
        width_status = f"미일치 · 잔여 {fmt_mm(remainder)} mm"
    else:
        width_status = f"미일치 · {fmt_mm(abs(remainder))} mm 초과"
    checks = [
        f"지폭별로 좌/우 {fmt_mm(left_trim)} mm의 여폭이 적용되었습니다.",
        f"총 여폭 : {fmt_mm(actual_trim)} mm ({fmt_mm(per_width_trim)} mm × {n})",
        f"제품 폭 합계 : {fmt_mm(product_sum)} mm",
        f"전체 지폭 : {fmt_mm(total_required)} mm ({width_status})",
    ]
    if abs(remainder) <= 1e-5:
        checks_html = '<div class="green-panel"><div class="green-title"><span style="font-size:21px">✓</span> 확인</div><div class="green-content">'+''.join(f'<div class="checkline"><span class="check">✓</span><span>{html.escape(c)}</span></div>' for c in checks)+'</div></div>'
    else:
        checks_html = '<div class="warning-panel"><div class="warning-title"><span style="font-size:21px">!</span> 폭 합계 확인 필요</div><div class="warning-content">'+''.join(f'<div class="checkline"><span style="color:#b7791f;font-size:18px;font-weight:900">•</span><span>{html.escape(c)}</span></div>' for c in checks)+'</div></div>' 

    p1, p2, p3 = st.columns([1.8, 1.08, 1.0], gap="small")
    with p1:
        st.markdown(table_html, unsafe_allow_html=True)
    with p2:
        st.markdown(summary_html, unsafe_allow_html=True)
    with p3:
        st.markdown(checks_html, unsafe_allow_html=True)
        csv_df = df.copy()
        csv_df.loc[len(csv_df)] = ["합계", "", product_sum, actual_trim, total_required, 100.0]
        csv = csv_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇  결과 CSV 다운로드",
            data=csv,
            file_name="지폭구성결과.csv",
            mime="text/csv",
            use_container_width=True,
        )

# Footer / input diagnostics
if not calculation_error and abs((sum(all_widths) + n * per_width_trim) - deckle) > 1e-5:
    st.warning("현재 구성 폭 합계가 전체 지폭과 일치하지 않습니다. 직접 입력한 지폭 합계를 확인하세요.")
