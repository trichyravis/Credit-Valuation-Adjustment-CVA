
"""
Credit Valuation Adjustment (CVA) — Interactive Learning Lab
The Mountain Path Academy | Prof. V. Ravichandran
Based on the CVA Illustration Excel workbook
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import base64

# ══════════════════════════════════════════════════════════
# DESIGN SYSTEM  (identical to ARIMA app)
# ══════════════════════════════════════════════════════════
GOLD = "#FFD700"; BLUE = "#003366"; MID = "#004d80"; CARD = "#112240"
TXT = "#e6f1ff"; MUTED = "#8892b0"; GRN = "#28a745"; RED = "#dc3545"
LB = "#ADD8E6"; WARN = "#FFC107"; ORANGE = "#fd7e14"; TEAL = "#17a2b8"
PURPLE = "#6f42c1"; BG_GRAD = "linear-gradient(135deg,#1a2332,#243447,#2a3f5f)"

st.set_page_config(
    page_title="CVA — The Mountain Path Academy",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.html(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
.stApp {{ background:{BG_GRAD}; font-family:'Source Sans 3',sans-serif; }}
section[data-testid="stSidebar"] {{ background:linear-gradient(180deg,#0a1628 0%,#112240 50%,#0a1628 100%) !important; border-right:2px solid {GOLD} !important; }}
section[data-testid="stSidebar"] * {{ color:{TXT} !important; -webkit-text-fill-color:{TXT} !important; }}
section[data-testid="stSidebar"] .stRadio label[data-checked="true"] span {{ color:{GOLD} !important; -webkit-text-fill-color:{GOLD} !important; font-weight:600 !important; }}
.stTabs [data-baseweb="tab-list"] {{ gap:0.5rem; background:rgba(17,34,64,0.6); border-radius:12px; padding:6px; }}
.stTabs [data-baseweb="tab"] {{ color:{MUTED} !important; background:transparent !important; border-radius:8px !important; }}
.stTabs [aria-selected="true"] {{ color:{GOLD} !important; background:rgba(255,215,0,0.12) !important; border-bottom:2px solid {GOLD} !important; }}
[data-testid="stMetric"] {{ background:{CARD} !important; border:1px solid rgba(255,215,0,0.2) !important; border-radius:12px !important; padding:16px !important; }}
[data-testid="stMetricValue"] {{ color:{GOLD} !important; -webkit-text-fill-color:{GOLD} !important; font-family:'JetBrains Mono',monospace !important; font-size:1.6rem !important; }}
[data-testid="stMetricLabel"] {{ color:{TXT} !important; -webkit-text-fill-color:{TXT} !important; }}
.stSlider label,.stNumberInput label,.stSelectbox label {{ color:{TXT} !important; -webkit-text-fill-color:{TXT} !important; }}
footer {{visibility:hidden;}} #MainMenu {{visibility:hidden;}}
</style>""")

# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
def mp_header(title, sub=""):
    s = f'<div style="color:{MUTED};-webkit-text-fill-color:{MUTED};font-size:1rem;margin-top:4px;">{sub}</div>' if sub else ""
    st.html(f'<div style="margin-bottom:18px;"><div style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-family:Playfair Display,serif;font-size:2rem;font-weight:700;">{title}</div>{s}<div style="height:3px;background:linear-gradient(90deg,{GOLD},transparent);border-radius:2px;margin-top:8px;width:40%;"></div></div>')

def mp_sub(title):
    st.html(f'<div style="color:{LB};-webkit-text-fill-color:{LB};font-family:Playfair Display,serif;font-size:1.35rem;font-weight:600;margin:20px 0 10px 0;">{title}</div>')

def mp_card(content, border=GOLD):
    st.html(f'<div style="background:{CARD};border:1px solid {border};border-left:4px solid {border};border-radius:10px;padding:18px 22px;margin:10px 0;"><div style="color:{TXT};-webkit-text-fill-color:{TXT};font-size:0.95rem;line-height:1.7;">{content}</div></div>')

def mp_insight(title, content):
    st.html(f'<div style="background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.3);border-left:4px solid {GOLD};border-radius:10px;padding:16px 20px;margin:12px 0;"><div style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-family:Playfair Display,serif;font-size:1rem;font-weight:700;margin-bottom:6px;"> {title}</div><div style="color:{TXT};-webkit-text-fill-color:{TXT};font-size:0.92rem;line-height:1.7;">{content}</div></div>')

def mp_warn(title, content):
    st.html(f'<div style="background:rgba(220,53,69,0.08);border:1px solid rgba(220,53,69,0.3);border-left:4px solid {RED};border-radius:10px;padding:16px 20px;margin:12px 0;"><div style="color:{RED};-webkit-text-fill-color:{RED};font-size:0.95rem;font-weight:700;margin-bottom:6px;">⚠️ {title}</div><div style="color:{TXT};-webkit-text-fill-color:{TXT};font-size:0.92rem;line-height:1.7;">{content}</div></div>')

def mp_formula(label, formula, expl=""):
    ex = f'<div style="color:{MUTED};-webkit-text-fill-color:{MUTED};font-size:0.85rem;margin-top:6px;">{expl}</div>' if expl else ""
    st.html(f'<div style="background:rgba(0,51,102,0.4);border:1px solid rgba(173,216,230,0.25);border-radius:10px;padding:14px 20px;margin:8px 0;"><div style="color:{LB};-webkit-text-fill-color:{LB};font-size:0.85rem;font-weight:600;margin-bottom:4px;">{label}</div><div style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-family:JetBrains Mono,monospace;font-size:1.02rem;">{formula}</div>{ex}</div>')

def mp_step(num, title, desc):
    st.html(f'<div style="display:flex;gap:14px;align-items:flex-start;background:{CARD};border-radius:10px;padding:14px 18px;margin:6px 0;border-left:4px solid {ORANGE};"><div style="background:{ORANGE};color:white;-webkit-text-fill-color:white;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.9rem;flex-shrink:0;">{num}</div><div><div style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-weight:600;font-size:0.95rem;">{title}</div><div style="color:{TXT};-webkit-text-fill-color:{TXT};font-size:0.88rem;margin-top:3px;line-height:1.6;">{desc}</div></div></div>')

def plotly_theme(fig, title="", h=420):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Playfair Display", size=18, color=GOLD), x=0.5),
        paper_bgcolor="rgba(17,34,64,0.85)", plot_bgcolor="rgba(17,34,64,0.4)",
        font=dict(family="Source Sans 3", color=TXT, size=13), height=h,
        margin=dict(l=50, r=30, t=60, b=50),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TXT)),
        xaxis=dict(gridcolor="rgba(136,146,176,0.15)", zerolinecolor="rgba(136,146,176,0.15)"),
        yaxis=dict(gridcolor="rgba(136,146,176,0.15)", zerolinecolor="rgba(136,146,176,0.15)"))
    return fig

def fmt_currency(v, prefix="£", decimals=2):
    return f"{prefix}{v:,.{decimals}f}"

# ══════════════════════════════════════════════════════════
# CVA CALCULATION ENGINES
# ══════════════════════════════════════════════════════════
def calc_coupon_bond_cva(face, coupon_rate, tenor, redemption, rfr, recovery, annual_pd):
    """Discrete compounding coupon bond CVA (Excel sheet 1 & 2 approach)."""
    coupon = face * coupon_rate
    lgd = 1 - recovery
    rows = []
    # Build exposure recursively from the last year
    # EE(t) = CF(t) + EE(t+1) / (1 + rfr)
    years = list(range(1, tenor + 1))
    cfs = [coupon] * tenor
    cfs[-1] += redemption  # add redemption to final year
    # Compute EE backwards
    ee = [0.0] * tenor
    ee[-1] = cfs[-1]
    for i in range(tenor - 2, -1, -1):
        ee[i] = cfs[i] + ee[i + 1] / (1 + rfr)
    # Compute marginal PD forward
    pd_vals = [annual_pd]
    for i in range(1, tenor):
        pd_vals.append(pd_vals[i - 1] * (1 - annual_pd))
    for i, yr in enumerate(years):
        df = 1 / (1 + rfr) ** yr
        el = ee[i] * lgd * pd_vals[i]
        pv_el = el * df
        rows.append({
            "Year": yr, "CF": cfs[i], "Exp Exposure": ee[i],
            "LGD": lgd, "PD": pd_vals[i], "EL": el,
            "Disc Factor": df, "PV of EL": pv_el
        })
    cva = sum(r["PV of EL"] for r in rows)
    # Risk-free bond price
    rf_price = sum(cfs[i] / (1 + rfr) ** (i + 1) for i in range(tenor))
    risky_price = rf_price - cva
    # Risky yield (Newton-Raphson approximation)
    def bond_price(y):
        return sum(cfs[i] / (1 + y) ** (i + 1) for i in range(tenor))
    y = rfr
    for _ in range(200):
        f = bond_price(y) - risky_price
        fp = sum(-(i + 1) * cfs[i] / (1 + y) ** (i + 2) for i in range(tenor))
        y -= f / fp if fp != 0 else 0
    credit_spread = y - rfr
    return pd.DataFrame(rows), cva, rf_price, risky_price, y, credit_spread

def calc_zcb_cva(face, maturity, cds_bps, recovery, rfr):
    """Zero coupon bond CVA with continuous compounding."""
    lam = (cds_bps / 10000) / (1 - recovery)
    lgd = 1 - recovery
    rows = []
    prev_s = 1.0
    for t in range(1, maturity + 1):
        ee = face * math.exp(-rfr * (maturity - t))
        df = math.exp(-rfr * t)
        s = math.exp(-lam * t)
        mpd = prev_s - s
        cva_t = lgd * ee * mpd * df
        rows.append({"Year": t, "Exp Exposure": ee, "Disc Factor": df,
                     "Survival": s, "Marginal PD": mpd, "LGD": lgd, "CVA Contrib": cva_t})
        prev_s = s
    cva = sum(r["CVA Contrib"] for r in rows)
    rf_price = face * math.exp(-rfr * maturity)
    risky_price = rf_price - cva
    return pd.DataFrame(rows), cva, rf_price, risky_price, lam

def calc_cds_flat_cva(notional, maturity, cds_bps, recovery, rfr, flat_ee):
    """CVA with flat expected exposure from CDS (continuous)."""
    lam = (cds_bps / 10000) / (1 - recovery)
    lgd = 1 - recovery
    rows = []
    prev_s = 1.0
    for t in range(1, maturity + 1):
        df = math.exp(-rfr * t)
        s = math.exp(-lam * t)
        mpd = prev_s - s
        cva_t = lgd * flat_ee * mpd * df
        rows.append({"Year": t, "Disc Factor": df, "Survival S(t)": s,
                     "Marginal PD": mpd, "EE": flat_ee, "LGD": lgd, "CVA Contrib": cva_t})
        prev_s = s
    cva = sum(r["CVA Contrib"] for r in rows)
    return pd.DataFrame(rows), cva, lam

def calc_cds_termstruct_cva(notional, maturity, cds_spreads_bps, recovery, rfr, ee_profile):
    """CVA with term-structure CDS and amortising exposure (continuous)."""
    lgd = 1 - recovery
    rows = []
    prev_s = 1.0
    for i, t in enumerate(range(1, maturity + 1)):
        lam_t = (cds_spreads_bps[i] / 10000) / (1 - recovery)
        s = math.exp(-lam_t * t)
        mpd = prev_s - s
        df = math.exp(-rfr * t)
        ee = ee_profile[i]
        cva_t = lgd * ee * mpd * df
        rows.append({"Year": t, "CDS Spread (bps)": cds_spreads_bps[i],
                     "Hazard Rate λ": lam_t, "Survival S(t)": s,
                     "Marginal PD": mpd, "EE": ee, "Disc Factor": df, "CVA Contrib": cva_t})
        prev_s = s
    cva = sum(r["CVA Contrib"] for r in rows)
    return pd.DataFrame(rows), cva

def calc_irs_cva(notional, maturity, cds_bps, recovery, rfr, vol_factor):
    """IRS CVA with hump-shaped exposure (continuous)."""
    lam = (cds_bps / 10000) / (1 - recovery)
    lgd = 1 - recovery
    rows = []
    prev_s = 1.0
    T = maturity
    for t in range(1, maturity + 1):
        sqrt_t = math.sqrt(t)
        mat_factor = (T - t) / T
        ee = notional * vol_factor * sqrt_t * mat_factor
        df = math.exp(-rfr * t)
        s = math.exp(-lam * t)
        mpd = prev_s - s
        cva_t = lgd * ee * mpd * df
        rows.append({"Year": t, "√t": sqrt_t, "(T-t)/T": mat_factor,
                     "Exp Exposure": ee, "Disc Factor": df,
                     "Survival S(t)": s, "Marginal PD": mpd, "LGD": lgd, "CVA Contrib": cva_t})
        prev_s = s
    cva = sum(r["CVA Contrib"] for r in rows)
    return pd.DataFrame(rows), cva

def calc_cds_pd(cds_spreads_bps, recovery):
    """CDS spreads → PD/survival (discrete, credit triangle)."""
    rows = []
    for t, s_bps in enumerate(cds_spreads_bps, 1):
        pd_annual = (s_bps / 10000) / (1 - recovery)
        survival = (1 - pd_annual) ** t
        cum_pd = 1 - survival
        rows.append({"Tenor (yr)": t, "CDS Spread (bps)": s_bps,
                     "Implied Annual PD": pd_annual, "Survival to Year-end": survival,
                     "Cumulative Default": cum_pd})
    return pd.DataFrame(rows)

def calc_general_cva(ee_profile_k, cds_spreads_bps, recovery, rfr):
    """General CVA calc linking CDS & PD tab to exposure (discrete)."""
    lgd = 1 - recovery
    pd_annual = (cds_spreads_bps / 10000) / (1 - recovery)
    rows = []
    prev_s = 1.0
    for t, ee in enumerate(ee_profile_k, 1):
        df = 1 / (1 + rfr) ** t
        s = (1 - pd_annual) ** t
        mpd = prev_s - s
        disc_el = lgd * ee * mpd * df
        rows.append({"Year": t, "EE (£000s)": ee, "Disc Factor": df,
                     "Survival Start": prev_s, "Survival End": s,
                     "Marginal PD": mpd, "Disc EL (£000s)": disc_el})
        prev_s = s
    cva_k = sum(r["Disc EL (£000s)"] for r in rows)
    return pd.DataFrame(rows), cva_k

# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
EMBLEM_SVG = """
<svg viewBox="0 0 300 388" xmlns="http://www.w3.org/2000/svg" width="150" height="194">

  <!-- ═══ ARCH/TOMBSTONE BADGE SHAPE ═══ -->
  <!-- Cream background fill -->
  <path d="M8,168 A142,142 0 0,1 292,168 L292,385 L8,385 Z" fill="#f2ede3"/>
  <!-- Outer border (thick dark navy) -->
  <path d="M8,168 A142,142 0 0,1 292,168 L292,385 L8,385 Z"
        fill="none" stroke="#0e2040" stroke-width="7" stroke-linejoin="round"/>
  <!-- Inner border (thin dark navy) -->
  <path d="M19,168 A131,131 0 0,1 281,168 L281,381 L19,381 Z"
        fill="none" stroke="#0e2040" stroke-width="1.8" stroke-linejoin="round"/>

  <!-- ═══ TOP TEXT ═══ -->
  <!-- THE -->
  <text x="150" y="53" text-anchor="middle"
        font-family="Georgia,'Times New Roman',serif"
        font-size="15" fill="#0e2040" letter-spacing="6">THE</text>
  <!-- MOUNTAIN -->
  <text x="150" y="97" text-anchor="middle"
        font-family="Georgia,'Times New Roman',serif"
        font-size="37" fill="#0e2040" font-weight="bold" letter-spacing="0.5">MOUNTAIN</text>
  <!-- PATH -->
  <text x="150" y="139" text-anchor="middle"
        font-family="Georgia,'Times New Roman',serif"
        font-size="37" fill="#0e2040" font-weight="bold" letter-spacing="7">PATH</text>

  <!-- ─ ACADEMY ─  (gold) -->
  <line x1="29"  y1="153" x2="82"  y2="153" stroke="#9a7b3e" stroke-width="1.8"/>
  <text x="150" y="160" text-anchor="middle"
        font-family="Georgia,'Times New Roman',serif"
        font-size="13" fill="#9a7b3e" letter-spacing="5" font-weight="600">ACADEMY</text>
  <line x1="218" y1="153" x2="271" y2="153" stroke="#9a7b3e" stroke-width="1.8"/>

  <!-- ═══ MOUNTAIN SCENE ═══ -->
  <!-- Sky (pale blue) -->
  <rect x="20" y="169" width="260" height="132" fill="#dce8f5"/>

  <!-- LAYER 1 — Farthest mountains (palest) -->
  <polygon points="20,278 74,234 112,250 150,218 190,244 234,230 270,242 280,236 280,278"
           fill="#b0c8dc"/>

  <!-- LAYER 2 — Mid mountains (slate blue) -->
  <polygon points="20,278 58,252 86,264 114,244 150,258 180,244 210,256 242,240 270,250 280,246 280,278"
           fill="#6588a8"/>

  <!-- LAYER 3 — Central peak (dark navy) with snow -->
  <polygon points="90,278 132,208 156,233 180,216 215,278" fill="#2a4e7e"/>
  <!-- Snow cap -->
  <polygon points="132,208 145,229 150,241 140,243 126,233 119,220" fill="#eef3ff" opacity="0.93"/>
  <polygon points="156,233 165,222 171,235 167,243 157,242"           fill="#eef3ff" opacity="0.80"/>
  <!-- Flanking side peaks -->
  <polygon points="20,278 50,254 70,265 92,278" fill="#2a4e7e" opacity="0.72"/>
  <polygon points="213,278 240,250 262,263 280,278" fill="#2a4e7e" opacity="0.72"/>

  <!-- LAYER 4 — Foreground dark mountains -->
  <polygon points="20,278 48,258 72,268 98,254 126,267 150,255 174,267 202,253 230,265 258,253 278,263 280,258 280,278"
           fill="#1a3456"/>

  <!-- ── PINE TREES LEFT (4 clusters, back to front) ── -->
  <g fill="#1e3a5a">
    <polygon points="20,278 28,255 36,278"/>
    <polygon points="22,268 28,251 34,268"/>
  </g>
  <g fill="#162e4c">
    <polygon points="32,278 43,251 54,278"/>
    <polygon points="35,264 43,247 51,264"/>
    <polygon points="38,253 43,243 48,253"/>
  </g>
  <g fill="#0f2444">
    <polygon points="48,278 61,247 74,278"/>
    <polygon points="52,262 61,243 70,262"/>
    <polygon points="56,249 61,239 66,249"/>
  </g>
  <g fill="#0d1e3a">
    <polygon points="66,278 82,243 98,278"/>
    <polygon points="70,260 82,239 94,260"/>
    <polygon points="74,245 82,235 90,245"/>
  </g>

  <!-- ── PINE TREES RIGHT (mirror) ── -->
  <g fill="#0d1e3a">
    <polygon points="202,278 218,243 234,278"/>
    <polygon points="206,260 218,239 230,260"/>
    <polygon points="210,245 218,235 226,245"/>
  </g>
  <g fill="#0f2444">
    <polygon points="226,278 239,247 252,278"/>
    <polygon points="230,262 239,243 248,262"/>
    <polygon points="234,249 239,239 244,249"/>
  </g>
  <g fill="#162e4c">
    <polygon points="246,278 257,251 268,278"/>
    <polygon points="249,264 257,247 265,264"/>
    <polygon points="252,253 257,243 262,253"/>
  </g>
  <g fill="#1e3a5a">
    <polygon points="264,278 272,255 280,278"/>
    <polygon points="266,268 272,251 278,268"/>
  </g>

  <!-- ── WINDING PATH (cream) from foreground toward mountains ── -->
  <!-- Outer edge/shadow -->
  <path d="M152,286 C148,276 143,266 139,256 C135,246 133,236 134,226"
        stroke="#c4b694" stroke-width="30" fill="none"
        stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Cream surface -->
  <path d="M152,286 C148,276 143,266 139,256 C135,246 133,236 134,226"
        stroke="#ede5cf" stroke-width="20" fill="none"
        stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Foreground ground strip (dark) -->
  <rect x="20" y="274" width="260" height="7" fill="#0c1d38" opacity="0.4"/>

  <!-- Scene-to-text fade: cream overlay at scene bottom -->
  <rect x="20" y="278" width="260" height="23" fill="#f2ede3"/>

  <!-- ═══ BOTTOM TEXT ═══ -->
  <!-- Separator line -->
  <line x1="27" y1="316" x2="273" y2="316" stroke="#0e2040" stroke-width="0.5" opacity="0.2"/>

  <text x="150" y="339" text-anchor="middle"
        font-family="Georgia,'Times New Roman',serif"
        font-size="14.5" fill="#0e2040" font-weight="bold" letter-spacing="1.8">KNOWLEDGE TODAY.</text>
  <text x="150" y="361" text-anchor="middle"
        font-family="Georgia,'Times New Roman',serif"
        font-size="14.5" fill="#0e2040" font-weight="bold" letter-spacing="1.8">FREEDOM TOMORROW.</text>

  <!-- Bottom ornament: gold rule — diamond — gold rule -->
  <line x1="52"  y1="375" x2="137" y2="375" stroke="#9a7b3e" stroke-width="1.6"/>
  <polygon points="150,371 154,375 150,379 146,375" fill="#9a7b3e"/>
  <line x1="163" y1="375" x2="248" y2="375" stroke="#9a7b3e" stroke-width="1.6"/>

</svg>
"""

# ── Convert SVG → base64 data URI (works in all Streamlit contexts) ──
_EMBLEM_B64 = base64.b64encode(EMBLEM_SVG.strip().encode("utf-8")).decode("utf-8")
EMBLEM_SRC  = f"data:image/svg+xml;base64,{_EMBLEM_B64}"

with st.sidebar:
    st.markdown(f"""
<div style="text-align:center;padding:18px 0 6px 0;">
  <img src="{EMBLEM_SRC}" width="148" height="192"
       style="display:block;margin:0 auto;
              filter:drop-shadow(0 4px 14px rgba(0,0,0,0.55));
              border-radius:6px;"/>
  <div style="color:{MUTED};font-size:0.72rem;letter-spacing:1px;margin-top:8px;">World of Finance</div>
  <div style="height:2px;background:linear-gradient(90deg,transparent,{GOLD},transparent);
              margin:8px auto 0 auto;width:80%;"></div>
</div>""", unsafe_allow_html=True)
    st.html(f'<div style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-family:Playfair Display,serif;font-size:1rem;font-weight:700;margin:20px 0 8px 0;"> Navigate</div>')
    page = st.radio("Topic", [
        " Home",
        "1️⃣ CVA Foundations",
        "2️⃣ Credit Triangle & PD",
        "3️⃣ Coupon Bond CVA",
        "4️⃣ Zero-Coupon Bond CVA",
        "5️⃣ CDS CVA — Flat Exposure",
        "6️⃣ CDS CVA — Term Structure",
        "7️⃣ Interest Rate Swap CVA",
        "8️⃣ Live CVA Calculator",
        "9️⃣ Q&A Practice",
    ], label_visibility="collapsed")
    st.html(f"""<div style="position:fixed;bottom:0;left:0;width:inherit;padding:12px 16px;background:rgba(10,22,40,0.95);border-top:1px solid rgba(255,215,0,0.2);text-align:center;">
        <div style="color:{MUTED};-webkit-text-fill-color:{MUTED};font-size:0.7rem;">Prof. V. Ravichandran</div>
        <div style="margin-top:4px;"><a href="https://themountainpathacademy.com" target="_blank" style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-size:0.7rem;text-decoration:none;">themountainpathacademy.com</a></div>
        <div style="margin-top:3px;">
            <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-size:0.65rem;text-decoration:none;margin-right:8px;">LinkedIn</a>
            <a href="https://github.com/trichyravis" target="_blank" style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-size:0.65rem;text-decoration:none;">GitHub</a>
        </div></div>""")

# ══════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════
if page == " Home":
    st.markdown(f"""
<div style="text-align:center;padding:30px 20px 10px 20px;">
  <img src="{EMBLEM_SRC}" width="118" height="153"
       style="display:block;margin:0 auto 16px auto;
              filter:drop-shadow(0 6px 22px rgba(0,0,0,0.6));
              border-radius:6px;"/>
  <div style="color:{GOLD};font-family:'Playfair Display',serif;font-size:0.9rem;
              letter-spacing:4px;font-weight:600;">THE MOUNTAIN PATH ACADEMY</div>
  <div style="color:white;font-family:'Playfair Display',serif;font-size:2.8rem;
              font-weight:800;margin-top:12px;">Credit Valuation Adjustment</div>
  <div style="color:{LB};font-size:1.15rem;margin-top:10px;">
      Interactive Learning Lab — CVA from First Principles</div>
  <div style="height:3px;background:linear-gradient(90deg,transparent,{GOLD},transparent);
              margin:20px auto;width:50%;"></div>
  <div style="color:{MUTED};font-size:0.85rem;">Prof. V. Ravichandran</div>
</div>""", unsafe_allow_html=True)

    # Hero chart — IRS CVA hump exposure
    df_hero, cva_hero = calc_irs_cva(10_000_000, 5, 200, 0.40, 0.03, 0.05)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_hero["Year"], y=df_hero["Exp Exposure"] / 1000,
        name="Expected Exposure (£K)", marker_color=TEAL, opacity=0.75
    ))
    fig.add_trace(go.Scatter(
        x=df_hero["Year"], y=df_hero["CVA Contrib"] * 1000,
        name="CVA Contribution (£)", mode="lines+markers",
        line=dict(color=GOLD, width=3), marker=dict(size=10)
    ))
    fig.add_trace(go.Scatter(
        x=df_hero["Year"], y=df_hero["Marginal PD"] * 100,
        name="Marginal PD (%)", mode="lines+markers",
        line=dict(color=RED, width=2, dash="dot"), marker=dict(size=7), yaxis="y2"
    ))
    fig = plotly_theme(fig, "Interest Rate Swap — Exposure Hump & CVA Profile", 420)
    fig.update_layout(
        yaxis=dict(title="£ Thousands / CVA £", gridcolor="rgba(136,146,176,0.15)"),
        yaxis2=dict(title="Marginal PD (%)", overlaying="y", side="right", gridcolor="rgba(0,0,0,0)"),
        barmode="overlay",
    )
    fig.update_xaxes(title="Year")
    st.plotly_chart(fig, use_container_width=True)

    mp_sub(" What You Will Learn")
    topics = [
        ("", "CVA Foundations", "The core formula, key terms (EE, PD, LGD, DF) and how the three ingredients multiply together"),
        ("", "Credit Triangle", "Convert CDS spreads into default probabilities — the engine behind every CVA calculation"),
        ("", "Coupon Bond CVA", "Step-by-step exposure roll-back, marginal PDs and the credit spread — exactly as in the Excel workbook"),
        ("0️⃣", "Zero-Coupon Bond CVA", "Why a ZCB has a large CVA (≈8%) — exposure rises to par, all principal at risk"),
        ("", "CDS CVA Methods", "Flat EE versus term-structure CDS spreads; investment grade vs high-yield comparison"),
        ("↕️", "IRS CVA", "The exposure hump — √t growth versus (T−t)/T decay — and why swap CVA is small (≈0.24%)"),
        ("️", "Live Calculator", "Adjust every parameter in real time and watch CVA, survival curves and EL profiles change instantly"),
        ("", "Q&A Practice", "35 questions spanning theory, calculation, pitfalls and comparisons"),
    ]
    cols = st.columns(4)
    for i, (icon, title, desc) in enumerate(topics):
        with cols[i % 4]:
            st.html(f'<div style="background:{CARD};border:1px solid rgba(255,215,0,0.15);border-radius:12px;padding:18px;text-align:center;min-height:160px;margin-bottom:8px;"><div style="font-size:1.8rem;margin-bottom:6px;">{icon}</div><div style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-family:Playfair Display,serif;font-size:0.95rem;font-weight:700;">{title}</div><div style="color:{TXT};-webkit-text-fill-color:{TXT};font-size:0.82rem;margin-top:6px;line-height:1.55;">{desc}</div></div>')

    mp_sub(" Workbook Illustrations Covered")
    ills = [
        ("Coupon Bond CVA (Sheets 1 & 2)", "Discrete compounding, step-by-step expected-loss build-up, 5 steps to credit spread", GRN),
        ("Zero-Coupon Bond CVA (Sheets 3a & 3b)", "Rising pull-to-par exposure; continuous compounding; CVA ≈ 8% of face", TEAL),
        ("CDS CVA — Flat EE (Sheet 4)", "Investment-grade name, flat exposure, hazard from CDS triangle", GOLD),
        ("CDS CVA — Term Structure (Sheet 5)", "BB-rated name, upward-sloping curve, amortising exposure profile", ORANGE),
        ("Interest Rate Swap CVA (Sheet 6)", "Hump-shaped EE via √t × (T−t)/T; CVA ≈ 0.24% of notional", PURPLE),
        ("General CVA Calculator (Sheet: CVA Calc)", "Custom exposure profile linked to CDS & PD tab; full formula", RED),
    ]
    for name, desc, clr in ills:
        st.html(f'<div style="background:{CARD};border-left:4px solid {clr};border-radius:8px;padding:12px 16px;margin:5px 0;"><div style="color:{clr};-webkit-text-fill-color:{clr};font-weight:700;font-size:0.92rem;">{name}</div><div style="color:{TXT};-webkit-text-fill-color:{TXT};font-size:0.85rem;margin-top:3px;">{desc}</div></div>')

# ══════════════════════════════════════════════════════════
# CVA FOUNDATIONS
# ══════════════════════════════════════════════════════════
elif page == "1️⃣ CVA Foundations":
    mp_header("CVA Foundations", "What it is, why it matters, and the three drivers")

    mp_card(f'<b style="color:{GOLD};-webkit-text-fill-color:{GOLD};">CVA</b> is the price of counterparty credit risk — the amount subtracted from the risk-free value of a trade to reflect the possibility that the counterparty might default before they finish paying. Any deal where someone owes you money over time carries this risk.')

    mp_formula("The Fundamental Identity",
               "Risky Value  =  Risk-free Value  −  CVA",
               "CVA is always non-negative (it reduces your position's value)")

    mp_formula("Core CVA Formula",
               "CVA  =  LGD × Σ [ EE(t) × Marginal PD(t) × DF(t) ]",
               "Sum over all future periods t: expected loss each period, discounted to today")

    mp_sub(" Key Terms — From the Overview Tab")
    terms = [
        ("Counterparty", "The other side of your trade — the party who owes you money over time.", "A bank you hold a swap or bond with."),
        ("Exposure / EE(t)", "How much the counterparty owes you at a point in time (the amount at risk).", "A swap in your favour by £1L → £1L at risk if they default."),
        ("Probability of Default (PD)", "Chance the counterparty fails to pay in a given period.", "2% PD ≈ 2 in 100 such firms default within a year."),
        ("Recovery Rate (R)", "Fraction of what you are owed that you get back on default.", "Recover £40 per £100 owed → R = 40%."),
        ("Loss Given Default (LGD)", "The fraction you LOSE if they default = 1 − Recovery.", "R = 40% → LGD = 60%."),
        ("Survival Probability S(t)", "Chance the counterparty is still alive (no default) all the way to time t.", "S(1) = 97% → about 3% chance of default by year 1."),
        ("Hazard Rate λ", "Default intensity — the engine behind the survival curve.", "Survival S(t) = exp(−λt). Continuous model."),
        ("CDS Spread", "Annual cost (basis points) to insure against the counterparty defaulting.", "200 bps = £2L per year to insure £1cr of exposure."),
        ("Discount Factor DF(t)", "Converts a future amount into today's money.", "DF(t) = exp(−r·t) or 1/(1+r)^t."),
        ("Credit Triangle", "Ties CDS spread, default intensity and recovery together.", "λ ≈ Spread / (1 − Recovery)."),
    ]
    for term, defn, ex in terms:
        st.html(f'<div style="background:{CARD};border-left:4px solid {TEAL};border-radius:8px;padding:12px 16px;margin:5px 0;"><div style="display:flex;gap:12px;flex-wrap:wrap;"><div style="min-width:180px;"><div style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-weight:700;font-size:0.92rem;">{term}</div></div><div style="flex:1;"><div style="color:{TXT};-webkit-text-fill-color:{TXT};font-size:0.88rem;">{defn}</div><div style="color:{MUTED};-webkit-text-fill-color:{MUTED};font-size:0.8rem;margin-top:3px;font-style:italic;">{ex}</div></div></div></div>')

    mp_sub(" The Three Drivers of CVA")
    cols = st.columns(3)
    drivers = [
        ("Exposure", "EE(t)", "How much is at risk?", "Reduced by: Netting, Collateral (CSA)", TEAL),
        ("Probability of Default", "PD(t)", "How likely is default?", "Reduced by: Counterparty selection, Credit triggers", GOLD),
        ("Loss Given Default", "LGD = 1−R", "How bad is the loss?", "Reduced by: Collateral, Guarantees, Seniority", ORANGE),
    ]
    for col, (name, symbol, question, mitigation, clr) in zip(cols, drivers):
        with col:
            st.html(f'<div style="background:{CARD};border-top:4px solid {clr};border-radius:12px;padding:20px;text-align:center;min-height:210px;"><div style="color:{clr};-webkit-text-fill-color:{clr};font-family:JetBrains Mono,monospace;font-size:1.8rem;font-weight:800;">{symbol}</div><div style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-family:Playfair Display,serif;font-size:1rem;font-weight:700;margin:6px 0;">{name}</div><div style="color:{TXT};-webkit-text-fill-color:{TXT};font-size:0.85rem;">{question}</div><div style="color:{MUTED};-webkit-text-fill-color:{MUTED};font-size:0.78rem;margin-top:8px;font-style:italic;">{mitigation}</div></div>')

    mp_sub(" The Five Steps (Box-Jenkins for CVA)")
    steps = [
        ("Identify Exposure", "Determine how much is at risk at each future point — this depends on the instrument (bond, swap, loan)."),
        ("Model Default Probability", "Extract marginal PDs from CDS spreads using the credit triangle: λ ≈ s/(1−R). Build survival curve S(t)."),
        ("Apply LGD", "LGD = 1 − Recovery Rate. Multiply exposure by LGD to get the loss if default occurs."),
        ("Discount", "Each expected loss is a future cashflow — discount it back to today using DF(t) = exp(−r·t)."),
        ("Sum All Periods", "CVA = Σ [LGD × EE(t) × Marginal PD(t) × DF(t)] over all future periods."),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        mp_step(str(i), title, desc)

    mp_insight("Why CVA Matters Post-2008",
        "During the 2008 financial crisis, <b>two-thirds of credit losses</b> from OTC derivatives came from CVA mark-to-market losses, not actual defaults. "
        "Basel III now requires banks to hold capital against CVA volatility, and IFRS 13 mandates fair-value inclusion of CVA in derivative pricing.")

# ══════════════════════════════════════════════════════════
# CREDIT TRIANGLE & PD
# ══════════════════════════════════════════════════════════
elif page == "2️⃣ Credit Triangle & PD":
    mp_header("Credit Triangle & Default Probabilities", "Converting CDS spreads into survival curves")

    mp_card(f'A CDS (Credit Default Swap) spread is the annual cost of insuring against default. The <b style="color:{GOLD};-webkit-text-fill-color:{GOLD};">credit triangle</b> converts that market price into a default probability. This is the engine that powers every CVA calculation.')

    mp_formula("The Credit Triangle",
               "λ ≈ CDS Spread ÷ (1 − Recovery Rate)",
               "λ = hazard rate (default intensity). Then: S(t) = exp(−λt)  and  Marginal PD(t) = S(t-1) − S(t)")

    mp_formula("Discrete Version",
               "Annual PD ≈ (Spread bps / 10,000) ÷ (1 − R)",
               "Survival to year t = (1 − PD)^t    |    Cumulative default = 1 − Survival")

    mp_sub("️ Interactive: CDS Spread → Survival Curve")
    c1, c2 = st.columns(2)
    with c1:
        recovery = st.slider("Recovery Rate R", 0, 80, 40, 5, format="%d%%") / 100
    with c2:
        cds_flat = st.slider("CDS Spread (bps, flat)", 50, 800, 200, 25)

    lam = (cds_flat / 10000) / (1 - recovery)
    pd_annual = lam  # continuous approximation
    years_arr = list(range(1, 11))
    survival_cont = [math.exp(-lam * t) for t in years_arr]
    survival_disc = [(1 - pd_annual) ** t for t in years_arr]
    cum_pd_cont = [1 - s for s in survival_cont]

    c1m, c2m, c3m = st.columns(3)
    with c1m: st.metric("Hazard Rate λ", f"{lam:.4f}")
    with c2m: st.metric("1-yr Survival (continuous)", f"{survival_cont[0]:.4%}")
    with c3m: st.metric("5-yr Survival (continuous)", f"{survival_cont[4]:.4%}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years_arr, y=survival_cont, mode="lines+markers", name="Survival S(t) [continuous]",
                             line=dict(color=GRN, width=2.5), marker=dict(size=7)))
    fig.add_trace(go.Scatter(x=years_arr, y=survival_disc, mode="lines+markers", name="Survival [discrete]",
                             line=dict(color=TEAL, width=2, dash="dot"), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=years_arr, y=cum_pd_cont, mode="lines+markers", name="Cumulative PD",
                             line=dict(color=RED, width=2.5), marker=dict(size=7)))
    fig = plotly_theme(fig, f"Survival & Cumulative Default — CDS={cds_flat}bps, R={recovery:.0%}", 400)
    fig.update_yaxes(title="Probability", tickformat=".1%")
    fig.update_xaxes(title="Year")
    st.plotly_chart(fig, use_container_width=True)

    mp_sub(" Worked Example — From Excel CDS & PD Tab")
    mp_card(f"<b>Recovery Rate:</b> 40%  |  <b>CDS Spreads:</b> 100, 110, 120, 130, 140 bps (upward-sloping curve)")
    ex_spreads = [100, 110, 120, 130, 140]
    df_pd = calc_cds_pd(ex_spreads, 0.40)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df_pd["Tenor (yr)"], y=df_pd["Implied Annual PD"],
                          name="Annual PD", marker_color=ORANGE, opacity=0.8))
    fig2.add_trace(go.Scatter(x=df_pd["Tenor (yr)"], y=df_pd["Survival to Year-end"],
                              name="Survival", mode="lines+markers",
                              line=dict(color=GRN, width=2.5), marker=dict(size=8), yaxis="y"))
    fig2.add_trace(go.Scatter(x=df_pd["Tenor (yr)"], y=df_pd["Cumulative Default"],
                              name="Cumulative PD", mode="lines+markers",
                              line=dict(color=RED, width=2), marker=dict(size=7)))
    fig2 = plotly_theme(fig2, "CDS → PD/Survival (Excel Sheet: CDS & PD)", 380)
    fig2.update_yaxes(title="Probability", tickformat=".2%")
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df_pd.style.format({
        "Implied Annual PD": "{:.4%}", "Survival to Year-end": "{:.4%}", "Cumulative Default": "{:.4%}"
    }), use_container_width=True)

    mp_insight("Upward-Sloping vs Flat Curve",
        "An upward-sloping CDS curve (higher spreads for longer tenors) means the market sees <b>increasing default risk over time</b> — typical for most credits. "
        "A flat or inverted curve can signal near-term stress. Always use the full term structure for accuracy.")

# ══════════════════════════════════════════════════════════
# COUPON BOND CVA
# ══════════════════════════════════════════════════════════
elif page == "3️⃣ Coupon Bond CVA":
    mp_header("Coupon Bond CVA", "Step-by-step expected-loss method — Excel Sheets 1 & 2")

    mp_card(f'A risky coupon bond is worth <b>less</b> than an identical risk-free bond. That gap is the CVA. We compute it by rolling out expected loss period by period — exposure × LGD × PD — discounted to today.')

    mp_sub("️ Adjust Parameters")
    c1, c2, c3 = st.columns(3)
    with c1:
        face = st.number_input("Face Value (£)", 100.0, 10000.0, 100.0, 100.0)
        coupon_r = st.slider("Coupon Rate (%)", 1.0, 20.0, 5.0, 0.5, format="%.1f%%") / 100
    with c2:
        tenor = st.slider("Tenor (years)", 1, 10, 5, 1)
        rfr = st.slider("Risk-free Rate (%)", 1.0, 15.0, 3.0, 0.5, format="%.1f%%") / 100
    with c3:
        recovery = st.slider("Recovery Rate", 0, 80, 40, 5, format="%d%%") / 100
        annual_pd = st.slider("Annual Default Probability (%)", 0.1, 20.0, 2.0, 0.1, format="%.1f%%") / 100

    df_bond, cva, rf_price, risky_price, risky_yield, credit_spread = calc_coupon_bond_cva(
        face, coupon_r, tenor, face, rfr, recovery, annual_pd)

    c1m, c2m, c3m, c4m = st.columns(4)
    with c1m: st.metric("CVA (£)", f"£{cva:.2f}", delta=f"{cva/rf_price:.2%} of RF price", delta_color="inverse")
    with c2m: st.metric("Risk-free Price (£)", f"£{rf_price:.2f}")
    with c3m: st.metric("Risky Price (£)", f"£{risky_price:.2f}")
    with c4m: st.metric("Credit Spread (bps)", f"{credit_spread*10000:.1f} bps")

    mp_sub(" Step 1 — CVA Table (Expected Loss per Period)")
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Expected Exposure & EL", "PV of Expected Loss (CVA Build-up)"])
    fig.add_trace(go.Bar(x=df_bond["Year"], y=df_bond["Exp Exposure"],
                         name="Exp Exposure (£)", marker_color=TEAL, opacity=0.7), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_bond["Year"], y=df_bond["EL"], mode="lines+markers",
                             name="Expected Loss", line=dict(color=ORANGE, width=2.5), marker=dict(size=8)), row=1, col=1)
    fig.add_trace(go.Bar(x=df_bond["Year"], y=df_bond["PV of EL"],
                         name="PV of EL (£)", marker_color=GOLD, opacity=0.85), row=1, col=2)
    fig = plotly_theme(fig, "Coupon Bond CVA — EL and PV(EL) by Year", 400)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_bond.style.format({
        "CF": "£{:.2f}", "Exp Exposure": "£{:.2f}", "LGD": "{:.2%}",
        "PD": "{:.4%}", "EL": "£{:.4f}", "Disc Factor": "{:.4f}", "PV of EL": "£{:.4f}"
    }), use_container_width=True)

    mp_sub(" Steps 2–5 — Pricing & Credit Spread")
    c1c, c2c = st.columns(2)
    with c1c:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=["Risk-free Price", "CVA", "Risky Price"],
                              y=[rf_price, -cva, risky_price],
                              marker_color=[GRN, RED, GOLD], opacity=0.85,
                              text=[f"£{rf_price:.2f}", f"−£{cva:.2f}", f"£{risky_price:.2f}"],
                              textposition="outside"))
        fig2 = plotly_theme(fig2, "Waterfall: RF Price → CVA → Risky Price", 380)
        fig2.update_yaxes(title="Price (£)")
        st.plotly_chart(fig2, use_container_width=True)
    with c2c:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=["Risk-free Yield", "Risky Yield"],
                                  y=[rfr * 100, risky_yield * 100],
                                  mode="markers+text", marker=dict(size=20, color=[GRN, GOLD]),
                                  text=[f"{rfr*100:.2f}%", f"{risky_yield*100:.2f}%"],
                                  textposition="top center"))
        fig3.add_shape(type="line", x0=0, x1=1, y0=rfr * 100, y1=risky_yield * 100,
                       line=dict(color=ORANGE, width=3, dash="dot"))
        fig3 = plotly_theme(fig3, f"Credit Spread = {credit_spread*10000:.1f} bps", 380)
        fig3.update_yaxes(title="Yield (%)")
        st.plotly_chart(fig3, use_container_width=True)

    mp_insight("How Exposure Works for a Bond",
        "For a coupon bond, the Expected Exposure at time t equals the <b>remaining cash flows discounted back from that point</b>. "
        "It is the present value (as of time t) of all future coupons plus redemption. This decreases over time as coupons are paid. "
        "In contrast, a swap's exposure <b>humps</b> in the middle before falling to zero.")

# ══════════════════════════════════════════════════════════
# ZERO-COUPON BOND CVA
# ══════════════════════════════════════════════════════════
elif page == "4️⃣ Zero-Coupon Bond CVA":
    mp_header("Zero-Coupon Bond CVA", "Rising exposure, big CVA — Excel Sheets 3a & 3b")

    mp_card(f'Unlike a coupon bond, a zero-coupon bond pays <b>nothing until maturity</b>. The entire principal is at risk right to the end — so the expected exposure <b>rises</b> over time, producing a large CVA (≈ 8% of face in the base case).')

    mp_formula("ZCB Expected Exposure",
               "EE(t)  =  Face × exp(−r × (T − t))",
               "The ZCB 'pulls to par' as maturity approaches — EE rises continuously to the full face value")

    mp_sub("️ Adjust Parameters")
    c1, c2, c3 = st.columns(3)
    with c1:
        face_zcb = st.number_input("Face Value (£)", 1_000_000, 50_000_000, 10_000_000, 1_000_000)
        maturity_zcb = st.slider("Maturity (years)", 1, 10, 5, 1)
    with c2:
        cds_zcb = st.slider("CDS Spread (bps)", 50, 800, 200, 25)
        recovery_zcb = st.slider("Recovery Rate", 0, 80, 40, 5, format="%d%%") / 100
    with c3:
        rfr_zcb = st.slider("Risk-free Rate (%)", 1.0, 15.0, 3.0, 0.5, format="%.1f%%") / 100

    df_zcb, cva_zcb, rf_zcb, risky_zcb, lam_zcb = calc_zcb_cva(face_zcb, maturity_zcb, cds_zcb, recovery_zcb, rfr_zcb)

    c1m, c2m, c3m, c4m = st.columns(4)
    with c1m: st.metric("CVA (£)", f"£{cva_zcb:,.0f}", delta=f"{cva_zcb/face_zcb:.2%} of face", delta_color="inverse")
    with c2m: st.metric("Risk-free Price (£)", f"£{rf_zcb:,.0f}")
    with c3m: st.metric("Risky Price (£)", f"£{risky_zcb:,.0f}")
    with c4m: st.metric("Hazard Rate λ", f"{lam_zcb:.4f}")

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Exposure Rising to Par", "CVA Contributions by Year"])
    fig.add_trace(go.Scatter(x=df_zcb["Year"], y=df_zcb["Exp Exposure"] / 1000,
                             mode="lines+markers", name="EE (£K)",
                             line=dict(color=TEAL, width=3), marker=dict(size=9)), row=1, col=1)
    fig.add_shape(type="line", x0=0, x1=maturity_zcb + 0.3, y0=face_zcb / 1000, y1=face_zcb / 1000,
                  line=dict(color=MUTED, dash="dot", width=1.5), row=1, col=1)
    fig.add_trace(go.Bar(x=df_zcb["Year"], y=df_zcb["CVA Contrib"] / 1000,
                         name="CVA Contrib (£K)", marker_color=GOLD, opacity=0.85), row=1, col=2)
    fig.add_trace(go.Scatter(x=df_zcb["Year"], y=df_zcb["Survival"],
                             mode="lines+markers", name="Survival S(t)",
                             line=dict(color=GRN, width=2, dash="dot"), marker=dict(size=7), yaxis="y2"), row=1, col=2)
    fig = plotly_theme(fig, "Zero-Coupon Bond — Exposure Profile & CVA", 420)
    fig.update_yaxes(title="£ Thousands", row=1, col=1)
    fig.update_yaxes(title="£ Thousands / Survival", row=1, col=2)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_zcb.style.format({
        "Exp Exposure": "£{:,.0f}", "Disc Factor": "{:.4f}", "Survival": "{:.4%}",
        "Marginal PD": "{:.4%}", "LGD": "{:.2%}", "CVA Contrib": "£{:,.0f}"
    }), use_container_width=True)

    mp_insight("Why ZCB CVA is So Large",
        "The ZCB has <b>no intermediate cash flows</b>. The full principal is outstanding until maturity, so exposure rises toward par. "
        "For the base case (£10M, 5yr, 200bps), CVA ≈ £790K ≈ 7.9% of face. "
        "Compare this to a 5-year swap, where exposure humps then vanishes — CVA ≈ 0.24%. "
        "The difference is the <b>exposure profile shape</b>: rising vs humped vs declining.")

    mp_warn("Discrete vs Continuous",
        "This sheet uses <b>continuous compounding</b> (exp(−r·t) discount factors, exp(−λt) survival). "
        "The first coupon bond tab uses <b>discrete compounding</b> (1/(1+r)^t). "
        "The two give slightly different numbers — always be consistent within a trade.")

# ══════════════════════════════════════════════════════════
# CDS CVA — FLAT EE
# ══════════════════════════════════════════════════════════
elif page == "5️⃣ CDS CVA — Flat Exposure":
    mp_header("CDS CVA — Flat Exposure (Investment Grade)", "Excel Sheet 4: Hazard rate → CVA with constant EE")

    mp_card(f'The simplest CVA model: assume the expected exposure is <b>flat</b> (constant) over the life of the trade. This is a useful first approximation for trades where exposure is relatively stable, like an at-inception swap or a fixed-notional guarantee.')

    mp_formula("CDS Approach",
               "λ = CDS_bps / 10,000 / (1 − R)    →    S(t) = exp(−λt)    →    ΔPD(t) = S(t−1) − S(t)",
               "CVA = LGD × flat_EE × Σ [ ΔPD(t) × DF(t) ]")

    mp_sub("️ Adjust Parameters")
    c1, c2, c3 = st.columns(3)
    with c1:
        notional_cds = st.number_input("Notional (USD)", 1_000_000, 100_000_000, 10_000_000, 1_000_000)
        maturity_cds = st.slider("Maturity (years)", 1, 10, 5, 1)
    with c2:
        cds_bps_flat = st.slider("CDS Spread (bps)", 50, 800, 200, 25)
        recovery_cds = st.slider("Recovery Rate", 0, 80, 40, 5, format="%d%%") / 100
    with c3:
        rfr_cds = st.slider("Risk-free Rate (%)", 1.0, 15.0, 3.0, 0.5, format="%.1f%%") / 100
        ee_pct = st.slider("Flat EE (% of Notional)", 1, 20, 5, 1, help="Simplified flat expected exposure")

    flat_ee = notional_cds * ee_pct / 100
    df_cds, cva_cds, lam_cds = calc_cds_flat_cva(notional_cds, maturity_cds, cds_bps_flat, recovery_cds, rfr_cds, flat_ee)

    c1m, c2m, c3m, c4m = st.columns(4)
    with c1m: st.metric("CVA (USD)", f"${cva_cds:,.0f}")
    with c2m: st.metric("CVA % of Notional", f"{cva_cds/notional_cds:.3%}")
    with c3m: st.metric("Hazard Rate λ", f"{lam_cds:.4f}")
    with c4m: st.metric("5-yr Survival", f"{math.exp(-lam_cds*5):.3%}")

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Survival & Marginal PD", "CVA Contributions by Year"])
    fig.add_trace(go.Scatter(x=df_cds["Year"], y=df_cds["Survival S(t)"],
                             mode="lines+markers", name="Survival S(t)",
                             line=dict(color=GRN, width=2.5), marker=dict(size=8)), row=1, col=1)
    fig.add_trace(go.Bar(x=df_cds["Year"], y=df_cds["Marginal PD"],
                         name="Marginal PD", marker_color=RED, opacity=0.75), row=1, col=1)
    fig.add_trace(go.Bar(x=df_cds["Year"], y=df_cds["CVA Contrib"],
                         name="CVA Contrib (USD)", marker_color=GOLD, opacity=0.85), row=1, col=2)
    fig = plotly_theme(fig, f"Flat-EE CVA — CDS={cds_bps_flat}bps, EE=${flat_ee:,.0f}", 420)
    fig.update_yaxes(tickformat=".3%", row=1, col=1)
    fig.update_yaxes(tickformat="$,.0f", row=1, col=2)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_cds.style.format({
        "Disc Factor": "{:.4f}", "Survival S(t)": "{:.4%}", "Marginal PD": "{:.4%}",
        "EE": "${:,.0f}", "LGD": "{:.2%}", "CVA Contrib": "${:,.0f}"
    }), use_container_width=True)

    mp_insight("Flat EE Assumption",
        "The flat EE assumption overestimates CVA for swaps (where EE humps then falls) and underestimates for bonds (where EE falls). "
        "It is, however, a <b>useful regulatory and initial-pricing approximation</b> — particularly for Basel II EPE calculations. "
        "Always replace with a simulated profile for accurate trade-level CVA.")

# ══════════════════════════════════════════════════════════
# CDS CVA — TERM STRUCTURE
# ══════════════════════════════════════════════════════════
elif page == "6️⃣ CDS CVA — Term Structure":
    mp_header("CDS CVA — Term Structure & High-Yield", "Excel Sheet 5: Upward-sloping CDS curve + amortising exposure")

    mp_card(f'A <b>BB-rated (high-yield) counterparty</b> with an upward-sloping CDS curve and an amortising exposure profile (typical of a 5-year interest rate swap). This example shows how weaker credit quality and term-structure effects combine to produce a higher CVA.')

    mp_sub("️ Adjust Parameters")
    c1, c2 = st.columns(2)
    with c1:
        notional_hy = st.number_input("Notional (USD)", 1_000_000, 100_000_000, 25_000_000, 1_000_000)
        recovery_hy = st.slider("Recovery Rate (HY)", 0, 70, 25, 5, format="%d%%") / 100
        rfr_hy = st.slider("Risk-free Rate (%)", 1.0, 15.0, 4.5, 0.5, format="%.1f%%") / 100
    with c2:
        st.html(f'<div style="color:{LB};-webkit-text-fill-color:{LB};font-size:0.88rem;margin-bottom:8px;font-weight:600;">CDS Spreads by Year (bps) — edit below:</div>')
        spreads_hy = []
        spread_defaults = [250, 300, 350, 400, 450]
        cols_s = st.columns(5)
        for i, col in enumerate(cols_s):
            with col:
                s = st.number_input(f"Year {i+1}", 50, 1000, spread_defaults[i], 25, key=f"hys{i}")
                spreads_hy.append(s)

    ee_profile_hy = [1_500_000, 2_200_000, 1_800_000, 1_100_000, 400_000]
    st.html(f'<div style="color:{MUTED};-webkit-text-fill-color:{MUTED};font-size:0.82rem;margin:4px 0 8px 0;">Exposure profile (from Excel): £1.5M → £2.2M → £1.8M → £1.1M → £0.4M (amortising IRS profile)</div>')

    df_hy, cva_hy = calc_cds_termstruct_cva(notional_hy, 5, spreads_hy, recovery_hy, rfr_hy, ee_profile_hy)

    # Comparison with IG (Sheet 4 base case)
    _, cva_ig, _ = calc_cds_flat_cva(10_000_000, 5, 200, 0.40, 0.03, 500_000)

    c1m, c2m, c3m, c4m = st.columns(4)
    with c1m: st.metric("CVA — HY (USD)", f"${cva_hy:,.0f}")
    with c2m: st.metric("CVA % of Notional", f"{cva_hy/notional_hy:.3%}")
    with c3m: st.metric("CVA — IG Comparison", f"${cva_ig:,.0f}")
    with c4m: st.metric("LGD (HY)", f"{(1-recovery_hy):.0%}", delta=f"{(1-recovery_hy)*100-60:.0f}pp vs IG")

    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=["CDS Spreads & Hazard Rates", "EE Profile & CVA Contributions"])
    fig.add_trace(go.Bar(x=list(range(1, 6)), y=spreads_hy,
                         name="CDS Spread (bps)", marker_color=RED, opacity=0.75), row=1, col=1)
    fig.add_trace(go.Scatter(x=list(range(1, 6)), y=df_hy["Hazard Rate λ"],
                             mode="lines+markers", name="Hazard Rate λ",
                             line=dict(color=ORANGE, width=2.5), marker=dict(size=8), yaxis="y2"), row=1, col=1)
    fig.add_trace(go.Bar(x=list(range(1, 6)), y=[e / 1000 for e in ee_profile_hy],
                         name="Exp Exposure (£K)", marker_color=TEAL, opacity=0.75), row=1, col=2)
    fig.add_trace(go.Scatter(x=list(range(1, 6)), y=df_hy["CVA Contrib"],
                             mode="lines+markers", name="CVA Contrib (USD)",
                             line=dict(color=GOLD, width=3), marker=dict(size=10)), row=1, col=2)
    fig = plotly_theme(fig, "High-Yield CDS CVA — Term Structure & Amortising Exposure", 420)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_hy.style.format({
        "CDS Spread (bps)": "{:.0f}", "Hazard Rate λ": "{:.4f}", "Survival S(t)": "{:.4%}",
        "Marginal PD": "{:.4%}", "EE": "${:,.0f}", "Disc Factor": "{:.4f}", "CVA Contrib": "${:,.0f}"
    }), use_container_width=True)

    mp_sub(" IG vs HY Comparison (from Excel Sheet 5)")
    compare_data = {
        "Metric": ["Notional", "Recovery Rate", "Avg CDS (bps)", "LGD", "Total CVA"],
        "IG (Sheet 4)": ["$10M", "40%", "200 bps", "60%", f"${cva_ig:,.0f}"],
        "HY (Sheet 5)": [f"${notional_hy/1e6:.0f}M", f"{recovery_hy:.0%}", f"{sum(spreads_hy)/5:.0f} bps", f"{(1-recovery_hy):.0%}", f"${cva_hy:,.0f}"]
    }
    st.dataframe(pd.DataFrame(compare_data), use_container_width=True)

    mp_insight("Key Takeaways from the HY Example",
        "• <b>Lower recovery (25% vs 40%)</b> raises LGD from 60% to 75% — directly amplifying CVA.<br>"
        "• <b>Upward-sloping CDS curve</b> increases marginal PDs in later years.<br>"
        "• <b>Amortising exposure</b> concentrates CVA in early-to-mid years when EE is highest.<br>"
        "• Despite the exposure falling in years 4–5, CVA is materially higher than the IG case due to weaker credit.")

# ══════════════════════════════════════════════════════════
# INTEREST RATE SWAP CVA
# ══════════════════════════════════════════════════════════
elif page == "7️⃣ Interest Rate Swap CVA":
    mp_header("Interest Rate Swap CVA", "The exposure hump — Excel Sheet 6")

    mp_card(f'A swap\'s exposure profile is driven by two competing forces: uncertainty <b>grows</b> over time (more rate drift), but <b>fewer cash flows remain</b> as maturity approaches. Their product — EE(t) = N × Vol × √t × (T−t)/T — peaks in the middle, creating the characteristic <b>hump</b>.')

    mp_formula("IRS Expected Exposure",
               "EE(t)  =  Notional × Vol × √t × (T−t)/T",
               "√t = time growth factor (uncertainty rises). (T−t)/T = remaining maturity factor (falls to 0 at expiry).")

    mp_sub("️ Adjust Parameters")
    c1, c2, c3 = st.columns(3)
    with c1:
        notional_irs = st.number_input("Notional (£)", 1_000_000, 100_000_000, 10_000_000, 1_000_000)
        maturity_irs = st.slider("Swap Maturity (years)", 2, 15, 5, 1)
    with c2:
        cds_irs = st.slider("CDS Spread (bps)", 50, 800, 200, 25)
        recovery_irs = st.slider("Recovery Rate", 0, 80, 40, 5, format="%d%%") / 100
    with c3:
        rfr_irs = st.slider("Risk-free Rate (%)", 1.0, 15.0, 3.0, 0.5, format="%.1f%%") / 100
        vol_irs = st.slider("Exposure Volatility Factor (%)", 1.0, 20.0, 5.0, 0.5, format="%.1f%%", help="Drives the hump height") / 100

    df_irs, cva_irs = calc_irs_cva(notional_irs, maturity_irs, cds_irs, recovery_irs, rfr_irs, vol_irs)

    c1m, c2m, c3m, c4m = st.columns(4)
    with c1m: st.metric("CVA (£)", f"£{cva_irs:,.0f}", delta=f"{cva_irs/notional_irs:.3%} of notional", delta_color="inverse")
    with c2m: st.metric("Peak EE (£)", f"£{df_irs['Exp Exposure'].max():,.0f}")
    with c3m: st.metric("Peak EE Year", f"Year {df_irs.loc[df_irs['Exp Exposure'].idxmax(), 'Year']}")
    with c4m: st.metric("Hazard Rate λ", f"{(cds_irs/10000)/(1-recovery_irs):.4f}")

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Exposure Hump Decomposition", "CVA Build-up"])
    yrs = df_irs["Year"].tolist()
    fig.add_trace(go.Scatter(x=yrs, y=df_irs["Exp Exposure"] / 1000,
                             mode="lines+markers", name="EE(t) (£K)",
                             line=dict(color=TEAL, width=3), marker=dict(size=9)), row=1, col=1)
    fig.add_trace(go.Scatter(x=yrs, y=[notional_irs * vol_irs * math.sqrt(t) / 1000 for t in yrs],
                             mode="lines", name="N×Vol×√t (growth)",
                             line=dict(color=GRN, width=1.5, dash="dot")), row=1, col=1)
    fig.add_trace(go.Scatter(x=yrs, y=[notional_irs * vol_irs * (maturity_irs - t) / maturity_irs / 1000 for t in yrs],
                             mode="lines", name="N×Vol×(T−t)/T (decay)",
                             line=dict(color=RED, width=1.5, dash="dot")), row=1, col=1)
    fig.add_trace(go.Bar(x=yrs, y=df_irs["CVA Contrib"],
                         name="CVA Contrib (£)", marker_color=GOLD, opacity=0.85), row=1, col=2)
    fig.add_trace(go.Scatter(x=yrs, y=df_irs["Survival S(t)"],
                             mode="lines+markers", name="Survival S(t)",
                             line=dict(color=GRN, width=2, dash="dash"), marker=dict(size=7), yaxis="y2"), row=1, col=2)
    fig = plotly_theme(fig, "IRS CVA — Hump Exposure & CVA Contributions", 430)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_irs.style.format({
        "√t": "{:.3f}", "(T-t)/T": "{:.3f}", "Exp Exposure": "£{:,.0f}",
        "Disc Factor": "{:.4f}", "Survival S(t)": "{:.4%}",
        "Marginal PD": "{:.4%}", "LGD": "{:.2%}", "CVA Contrib": "£{:,.0f}"
    }), use_container_width=True)

    mp_insight("The Hump Explained",
        "At early maturities, √t is small (little rate drift yet) → exposure is low. "
        "At late maturities, (T−t)/T → 0 (very few cash flows left) → exposure falls. "
        "The product peaks around <b>t ≈ T/3</b> for a 5-year swap, typically at year 2 or 3. "
        "This is why IRS CVA is <b>much smaller than ZCB CVA</b> — the exposure is self-limiting.")

    mp_sub(" Exposure Shape Comparison")
    fig4 = go.Figure()
    yr_arr = list(range(1, maturity_irs + 1))
    irs_ee = [notional_irs * vol_irs * math.sqrt(t) * (maturity_irs - t) / maturity_irs / notional_irs * 100 for t in yr_arr]
    zcb_ee = [math.exp(-rfr_irs * (maturity_irs - t)) * 100 for t in yr_arr]
    coupon_ee_approx = [100 * (maturity_irs - t + 1) / maturity_irs for t in yr_arr]
    fig4.add_trace(go.Scatter(x=yr_arr, y=irs_ee, mode="lines+markers", name="IRS (hump)",
                              line=dict(color=TEAL, width=2.5), marker=dict(size=7)))
    fig4.add_trace(go.Scatter(x=yr_arr, y=zcb_ee, mode="lines+markers", name="ZCB (rising to par)",
                              line=dict(color=ORANGE, width=2.5), marker=dict(size=7)))
    fig4.add_trace(go.Scatter(x=yr_arr, y=coupon_ee_approx, mode="lines+markers", name="Coupon Bond (declining)",
                              line=dict(color=GRN, width=2.5, dash="dot"), marker=dict(size=7)))
    fig4 = plotly_theme(fig4, "Exposure Profiles: IRS vs ZCB vs Coupon Bond (% of Notional)", 380)
    fig4.update_yaxes(title="EE as % of Face / Notional")
    fig4.update_xaxes(title="Year")
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════
# LIVE CVA CALCULATOR
# ══════════════════════════════════════════════════════════
elif page == "8️⃣ Live CVA Calculator":
    mp_header("Live CVA Calculator", "Full interactive CVA — adjust every parameter in real time")

    tabs = st.tabs([" General CVA", " Sensitivity Analysis", " Compare Instruments"])

    with tabs[0]:
        mp_sub("General CVA — Custom Exposure Profile (linked to CDS & PD tab)")
        mp_card(f'Mirrors the Excel <b>"CVA Calc"</b> sheet. Enter a custom exposure profile and a flat CDS spread; the tool computes survival, marginal PD, and discounted expected loss.')

        c1, c2 = st.columns([1, 2])
        with c1:
            rfr_gen = st.slider("Risk-free Rate (%)", 1.0, 15.0, 3.0, 0.5, format="%.1f%%", key="gen_rfr") / 100
            recovery_gen = st.slider("Recovery Rate", 0, 80, 40, 5, format="%d%%", key="gen_rec") / 100
            cds_gen = st.slider("CDS Spread (bps, flat)", 50, 800, 200, 25, key="gen_cds")
            st.html(f'<div style="color:{MUTED};-webkit-text-fill-color:{MUTED};font-size:0.82rem;margin-top:8px;">LGD = {1-recovery_gen:.0%}  |  λ = {(cds_gen/10000)/(1-recovery_gen):.4f}</div>')
        with c2:
            st.html(f'<div style="color:{LB};-webkit-text-fill-color:{LB};font-size:0.88rem;font-weight:600;margin-bottom:6px;">Expected Exposure by Year (£000s):</div>')
            ee_defaults = [80, 100, 90, 60, 30]
            ee_gen = []
            cols_ee = st.columns(5)
            for i, col in enumerate(cols_ee):
                with col:
                    v = st.number_input(f"Yr {i+1}", 0.0, 10000.0, float(ee_defaults[i]), 5.0, key=f"ee{i}")
                    ee_gen.append(v)

        df_gen, cva_gen_k = calc_general_cva(ee_gen, cds_gen, recovery_gen, rfr_gen)
        cva_gen = cva_gen_k * 1000  # convert from £K to £

        c1m, c2m, c3m = st.columns(3)
        with c1m: st.metric("CVA (£000s)", f"£{cva_gen_k:.3f}K")
        with c2m: st.metric("CVA (£)", f"£{cva_gen:,.0f}")
        with c3m: st.metric("Total EL %", f"{cva_gen_k / sum(ee_gen) * 100:.3f}% of avg EE")

        fig = make_subplots(rows=1, cols=2, subplot_titles=["EE & Discounted EL", "Survival & Marginal PD"])
        fig.add_trace(go.Bar(x=df_gen["Year"], y=df_gen["EE (£000s)"],
                             name="EE (£K)", marker_color=TEAL, opacity=0.75), row=1, col=1)
        fig.add_trace(go.Scatter(x=df_gen["Year"], y=df_gen["Disc EL (£000s)"],
                                 mode="lines+markers", name="Disc EL (£K)",
                                 line=dict(color=GOLD, width=3), marker=dict(size=10)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df_gen["Year"], y=df_gen["Survival End"],
                                 mode="lines+markers", name="Survival S(t)",
                                 line=dict(color=GRN, width=2.5), marker=dict(size=8)), row=1, col=2)
        fig.add_trace(go.Bar(x=df_gen["Year"], y=df_gen["Marginal PD"],
                             name="Marginal PD", marker_color=RED, opacity=0.75), row=1, col=2)
        fig = plotly_theme(fig, "General CVA — EE, EL, Survival & PD", 400)
        fig.update_yaxes(row=1, col=2, tickformat=".3%")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_gen.style.format({
            "EE (£000s)": "{:.1f}", "Disc Factor": "{:.4f}", "Survival Start": "{:.4%}",
            "Survival End": "{:.4%}", "Marginal PD": "{:.4%}", "Disc EL (£000s)": "{:.4f}"
        }), use_container_width=True)

    with tabs[1]:
        mp_sub("CVA Sensitivity Analysis — CS01, LGD Sensitivity, Rate Sensitivity")

        c1, c2 = st.columns(2)
        with c1:
            base_cds = st.slider("Base CDS (bps)", 50, 600, 200, 25, key="sa_cds")
            sa_rec = st.slider("Recovery Rate", 0, 80, 40, 5, format="%d%%", key="sa_rec") / 100
        with c2:
            sa_rfr = st.slider("Risk-free Rate (%)", 1.0, 15.0, 3.0, 0.5, format="%.1f%%", key="sa_rfr") / 100
            sa_notional = st.number_input("Notional", 1_000_000, 100_000_000, 10_000_000, 1_000_000, key="sa_n")

        # CS01 sweep
        spread_range = list(range(25, 601, 25))
        cva_by_spread = []
        for s in spread_range:
            _, c, _ = calc_cds_flat_cva(sa_notional, 5, s, sa_rec, sa_rfr, sa_notional * 0.05)
            cva_by_spread.append(c)

        cs01 = (calc_cds_flat_cva(sa_notional, 5, base_cds + 1, sa_rec, sa_rfr, sa_notional * 0.05)[1] -
                calc_cds_flat_cva(sa_notional, 5, base_cds, sa_rec, sa_rfr, sa_notional * 0.05)[1])

        # Recovery sweep
        rec_range = [i / 100 for i in range(0, 81, 10)]
        cva_by_rec = [calc_cds_flat_cva(sa_notional, 5, base_cds, r, sa_rfr, sa_notional * 0.05)[1] for r in rec_range]

        c1m, c2m = st.columns(2)
        with c1m: st.metric("CS01 ($ per bp)", f"${cs01:,.0f}")
        with c2m: st.metric("Base CVA", f"${calc_cds_flat_cva(sa_notional, 5, base_cds, sa_rec, sa_rfr, sa_notional*0.05)[1]:,.0f}")

        fig = make_subplots(rows=1, cols=2, subplot_titles=["CVA vs CDS Spread", "CVA vs Recovery Rate"])
        fig.add_trace(go.Scatter(x=spread_range, y=cva_by_spread, mode="lines",
                                 name="CVA ($)", line=dict(color=GOLD, width=2.5)), row=1, col=1)
        fig.add_vline(x=base_cds, line_dash="dot", line_color=ORANGE, line_width=2, row=1, col=1)
        fig.add_trace(go.Scatter(x=[r * 100 for r in rec_range], y=cva_by_rec, mode="lines+markers",
                                 name="CVA ($)", line=dict(color=TEAL, width=2.5), marker=dict(size=7)), row=1, col=2)
        fig.add_vline(x=sa_rec * 100, line_dash="dot", line_color=ORANGE, line_width=2, row=1, col=2)
        fig = plotly_theme(fig, "CVA Sensitivity Analysis", 420)
        fig.update_xaxes(title="CDS Spread (bps)", row=1, col=1)
        fig.update_xaxes(title="Recovery Rate (%)", row=1, col=2)
        st.plotly_chart(fig, use_container_width=True)
        mp_insight("CS01 Interpretation",
            f"A 1 basis point rise in the counterparty CDS spread increases CVA by approximately <b>${cs01:,.0f}</b>. "
            "This is the 'CS01' — the primary risk measure for CVA desks. "
            "Hedging CVA means buying CDS protection in an amount equal to your CS01.")

    with tabs[2]:
        mp_sub("Compare Instruments: Bond vs ZCB vs IRS — Same Credit, Same Parameters")

        notional_cmp = 10_000_000
        cds_cmp = st.slider("CDS Spread (bps)", 50, 600, 200, 25, key="cmp_cds")
        recovery_cmp = st.slider("Recovery Rate", 0, 80, 40, 5, format="%d%%", key="cmp_rec") / 100
        rfr_cmp = st.slider("Risk-free Rate (%)", 1.0, 15.0, 3.0, 0.5, format="%.1f%%", key="cmp_rfr") / 100

        _, cva_bond_cmp, rf_cmp, _, _, _ = calc_coupon_bond_cva(notional_cmp, 0.05, 5, notional_cmp, rfr_cmp, recovery_cmp, (cds_cmp / 10000) / (1 - recovery_cmp))
        _, cva_zcb_cmp, _, _, _ = calc_zcb_cva(notional_cmp, 5, cds_cmp, recovery_cmp, rfr_cmp)
        _, cva_irs_cmp = calc_irs_cva(notional_cmp, 5, cds_cmp, recovery_cmp, rfr_cmp, 0.05)

        instruments = ["Coupon Bond\n(5yr, 5%)", "Zero-Coupon Bond\n(5yr)", "Interest Rate Swap\n(5yr, hump EE)"]
        cvas = [cva_bond_cmp, cva_zcb_cmp, cva_irs_cmp]
        pcts = [v / notional_cmp * 100 for v in cvas]
        colors = [TEAL, ORANGE, GOLD]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=instruments, y=cvas, marker_color=colors, opacity=0.85,
                             text=[f"£{v:,.0f}\n({p:.2f}%)" for v, p in zip(cvas, pcts)],
                             textposition="outside"))
        fig = plotly_theme(fig, f"CVA Comparison — £10M, CDS={cds_cmp}bps, R={recovery_cmp:.0%}", 420)
        fig.update_yaxes(title="CVA (£)")
        st.plotly_chart(fig, use_container_width=True)

        compare_df = pd.DataFrame({
            "Instrument": instruments,
            "CVA (£)": [f"£{v:,.0f}" for v in cvas],
            "CVA % Notional": [f"{p:.3f}%" for p in pcts],
            "Exposure Shape": ["Declining (rolling PV)", "Rising to par", "Hump (√t × (T−t)/T)"]
        })
        st.dataframe(compare_df, use_container_width=True)
        mp_insight("Why the Differences?",
            "• <b>ZCB</b> has the largest CVA because the full face value is always at risk — exposure rises to par.<br>"
            "• <b>Coupon Bond</b> starts high (present value of all remaining flows) and declines as coupons are paid.<br>"
            "• <b>IRS</b> has the smallest CVA because the exposure self-limits — it humps then falls to zero at maturity.<br>"
            "The exposure <b>shape</b> determines CVA, not just the notional size.")

# ══════════════════════════════════════════════════════════
# Q&A PRACTICE
# ══════════════════════════════════════════════════════════
elif page == "9️⃣ Q&A Practice":
    mp_header("Q&A Practice — Self-Assessment", "35 questions covering CVA theory, calculation and pitfalls")
    mp_card(f' Try answering each question in your head <b>before</b> clicking to reveal the answer.')

    qa_sections = {
        "Foundations (Q1–Q10)": [
            ("Q1", "What does CVA stand for and what does it measure?",
             "Credit Valuation Adjustment. It measures the <b style='color:#FFD700;-webkit-text-fill-color:#FFD700;'>market value of counterparty credit risk</b> — the discount applied to the risk-free value of a trade to reflect the possibility that the counterparty defaults."),
            ("Q2", "State the fundamental CVA identity.",
             "<b>Risky Value = Risk-free Value − CVA.</b> CVA is always non-negative — it reduces the position's fair value."),
            ("Q3", "Write the core CVA formula.",
             "CVA = LGD × Σ [ EE(t) × Marginal PD(t) × DF(t) ]<br>Three ingredients: Exposure, Default Probability, Loss rate — each discounted to today."),
            ("Q4", "What is the credit triangle?",
             "The relationship: <b style='color:#FFD700;-webkit-text-fill-color:#FFD700;'>λ ≈ CDS Spread / (1 − Recovery)</b>. It converts a CDS market quote into a hazard rate (default intensity), which drives the survival curve S(t) = exp(−λt)."),
            ("Q5", "Define Expected Exposure (EE).",
             "The <b>expected amount owed to you</b> at a future point in time. Only positive MtM counts (if counterparty owes us). EE(t) = E[max(MtM(t), 0)]."),
            ("Q6", "What is Loss Given Default (LGD)?",
             "LGD = 1 − Recovery Rate. The fraction of exposure you <b>lose</b> if the counterparty defaults. If R = 40%, LGD = 60%."),
            ("Q7", "What is a marginal PD?",
             "The probability of default <b>during</b> a specific period. Marginal PD(t) = S(t−1) − S(t) = probability of surviving to t−1 but defaulting before t."),
            ("Q8", "Why is CVA always negative from the buyer's perspective?",
             "Because counterparty default risk always reduces the value of what you are owed. CVA subtracts from the risk-free price. A deal with CVA = 0 would mean either zero exposure or zero default risk."),
            ("Q9", "What is a Credit Default Swap (CDS)?",
             "A contract that pays the buyer the LGD if the reference entity defaults, in exchange for a periodic premium (the spread). CDS spreads are the primary market source of risk-neutral PDs for CVA."),
            ("Q10", "Why do we use risk-neutral (CDS-implied) PD rather than historical PD?",
             "CVA is a <b>market price</b> — it must use market-implied, risk-neutral probabilities. Historical PDs are lower (≈ 5× for investment grade) and produce CVA that understates the true cost of hedging."),
        ],
        "Calculation (Q11–Q20)": [
            ("Q11", "How is exposure calculated for a coupon bond?",
             "EE(t) = Present value of all remaining cash flows as of time t. Computed recursively from maturity back: EE(T) = Final CF; EE(t) = CF(t) + EE(t+1)/(1+r). Exposure <b>declines</b> as coupons are paid."),
            ("Q12", "Why does a zero-coupon bond have a higher CVA than an equivalent coupon bond?",
             "The ZCB pays nothing until maturity — the full principal is at risk throughout. EE(t) = Face × exp(−r(T−t)) rises toward par. A coupon bond's exposure declines as coupons are received."),
            ("Q13", "Describe the exposure profile of an interest rate swap.",
             "The IRS exposure has a characteristic <b>hump shape</b>: EE = N × Vol × √t × (T−t)/T. It peaks around t = T/3, then falls to zero at maturity. This makes IRS CVA much smaller (≈ 0.24%) than ZCB CVA (≈ 8%)."),
            ("Q14", "What drives the hump in an IRS exposure profile?",
             "Two opposing forces: <b>√t</b> grows over time (more rate drift → bigger potential MtM). <b>(T−t)/T</b> falls to zero (fewer remaining cash flows). Their product peaks in the middle years."),
            ("Q15", "For a 5Y IRS: Notional £10M, CDS 200bps, Recovery 40%, Risk-free 3%, Vol Factor 5% — estimate CVA.",
             "λ = 0.02/0.60 = 0.0333. EE peaks around year 2 (≈ £180K). Total CVA ≈ £24K ≈ 0.24% of notional. The hump profile means exposure self-limits."),
            ("Q16", "What is a discount factor in CVA and why is it needed?",
             "DF(t) = exp(−r·t) (continuous) or 1/(1+r)^t (discrete). CVA is a <b>present value</b> concept — each future expected loss must be brought back to today's money before summing."),
            ("Q17", "What is the continuous-compounding survival formula?",
             "S(t) = exp(−λt) where λ is the hazard rate. Under continuous compounding, the marginal default probability for period [t−1, t] is S(t−1) − S(t) = exp(−λ(t−1)) − exp(−λt)."),
            ("Q18", "What is the discrete-compounding survival formula?",
             "S(t) = (1 − PD)^t where PD is the annual default probability from the credit triangle. This is used in the coupon bond tabs — not directly comparable to the continuous version."),
            ("Q19", "How does a higher CDS spread affect CVA?",
             "Higher CDS spread → higher λ → lower survival probability → higher marginal PDs → higher CVA. CVA is approximately linear in CDS spread for short maturities."),
            ("Q20", "What is CS01 and why does the CVA desk care about it?",
             "CS01 = change in CVA for a 1bp rise in the counterparty's CDS spread. It is the primary credit sensitivity of CVA. Hedging CVA means buying CDS protection with a notional equal to CS01 × (some duration measure)."),
        ],
        "Concepts & Pitfalls (Q21–Q28)": [
            ("Q21", "What is Wrong-Way Risk?",
             "Exposure and default probability are positively correlated — the counterparty is most likely to default when you are owed the most. Example: selling a currency put to an oil exporter — if oil prices collapse, both exposure (currency depreciation) and PD rise together."),
            ("Q22", "What is DVA?",
             "Debit Valuation Adjustment — the CVA from the counterparty's perspective on you. DVA = gain from your own credit risk. Bilateral CVA = CVA + DVA. Controversial: as your own credit worsens, DVA rises (a gain), which is perverse."),
            ("Q23", "Name the xVA family of adjustments.",
             "CVA (counterparty risk), DVA (own default), FVA (funding cost), KVA (capital cost), MVA (initial margin cost), ColVA (collateral optionality). All stem from the reality that derivatives are not purely risk-free bilateral contracts."),
            ("Q24", "What is a Credit Support Annex (CSA) and how does it reduce CVA?",
             "A CSA requires periodic posting of collateral (cash or securities) against negative MtM. Exposure is reduced to the uncollected gap during the Margin Period of Risk (MPoR, typically 10 days). CVA can be reduced by 80–90% with a daily-margined CSA."),
            ("Q25", "What is the Margin Period of Risk (MPoR)?",
             "The time between the last margin call before default and when the position is fully closed out. Typically 10 business days (bilateral) or 5 days (cleared). Residual exposure during MPoR means CVA is never zero even with a CSA."),
            ("Q26", "Why do we use discrete compounding in some tabs and continuous in others?",
             "Historical convention: bond pricing typically uses discrete compounding (1/(1+r)^t). CVA and derivative pricing use continuous compounding (exp(−r·t)). Always be <b>consistent</b> within a calculation and state your convention."),
            ("Q27", "What is netting and how does it reduce CVA?",
             "Under a netting agreement (ISDA Master Agreement), all trades with a counterparty are combined if they default. Net exposure = max(Σ MtM, 0) ≤ Σ max(MtM, 0). Netting dramatically reduces exposure and hence CVA."),
            ("Q28", "What regulatory change forced banks to compute CVA?",
             "Basel III (2010) required banks to hold capital against <b>CVA volatility</b> (not just credit losses). IFRS 13 requires CVA to be included in the fair value of derivative liabilities. The CVA capital charge was one of the largest sources of losses in 2007–2009."),
        ],
        "Advanced (Q29–Q35)": [
            ("Q29", "Explain the Basel III CVA capital charge.",
             "Banks must hold capital against the <b>volatility of CVA</b>, not just the expected loss. Under FRTB-CVA (effective 2025): SA-CVA uses delta/vega/curvature sensitivities; BA-CVA is a simpler fallback. The regulatory alpha multiplier of 1.4× applies to EPE."),
            ("Q30", "What is EPE (Expected Positive Exposure) and how does it relate to CVA?",
             "EPE = time-average of EE(t) over the life of the trade. Used in regulatory capital: Regulatory Exposure = 1.4 × EPE. The 1.4× alpha multiplier was calibrated to account for model risk in EPE estimates."),
            ("Q31", "What is wrong with using a flat EE assumption?",
             "It overstates CVA for swaps (whose exposure humps then falls) and understates for bonds or loans. The flat EE is useful for initial pricing estimates and regulatory capital but should be replaced by simulated profiles for trade-level accuracy."),
            ("Q32", "Describe the Monte Carlo approach to computing EE.",
             "1. Simulate thousands of paths for each risk factor (rates, FX, credit spreads). 2. Reprice all trades on each path at each future date. 3. Apply netting and collateral. 4. EE(t) = average of max(net MtM, 0) across paths. 5. Apply CVA formula."),
            ("Q33", "What is a CDS term structure and why does it matter for CVA?",
             "A CDS term structure shows spreads for different maturities (1Y, 2Y, 3Y, 4Y, 5Y). An upward-sloping curve means higher default risk in later years. Using a term structure rather than a flat spread produces a more accurate — usually higher — CVA for long-dated trades."),
            ("Q34", "How does recovery rate affect CVA?",
             "CVA is directly proportional to LGD = 1 − R. Doubling the recovery rate (e.g., 20% → 40%) halves the LGD (80% → 60%) and reduces CVA proportionally. Senior secured trades have higher recovery, lower CVA. Sub-investment grade has lower recovery."),
            ("Q35", "Summarise the five illustrations from the Excel workbook.",
             "<b>1. Coupon Bond:</b> Rolling EE, discrete PD, 5-step method → credit spread.<br>"
             "<b>2. Zero-Coupon Bond:</b> Rising EE to par, continuous, large CVA ≈ 8%.<br>"
             "<b>3. CDS Flat EE:</b> Simplest model, hazard from credit triangle, flat exposure.<br>"
             "<b>4. CDS Term Structure:</b> HY name, upward curve, amortising EE, higher CVA.<br>"
             "<b>5. IRS:</b> Hump exposure (√t × (T−t)/T), small CVA ≈ 0.24%, continuous compounding."),
        ]
    }

    for sec_name, questions in qa_sections.items():
        mp_sub(sec_name)
        qa_html = ""
        for qid, question, answer in questions:
            qa_html += f"""<details style="background:#112240;border:1px solid rgba(255,215,0,0.18);border-radius:10px;margin:8px 0;overflow:hidden;">
                <summary style="padding:14px 20px;cursor:pointer;list-style:none;display:flex;align-items:center;gap:10px;">
                    <span style="color:#FFD700;-webkit-text-fill-color:#FFD700;font-family:JetBrains Mono,monospace;font-size:0.82rem;font-weight:700;min-width:32px;">{qid}</span>
                    <span style="color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;font-size:0.92rem;line-height:1.5;">{question}</span>
                    <span style="margin-left:auto;color:#FFD700;-webkit-text-fill-color:#FFD700;font-size:1.1rem;">▶</span>
                </summary>
                <div style="padding:0 20px 16px 20px;border-top:1px solid rgba(255,215,0,0.12);">
                    <div style="background:rgba(0,51,102,0.35);border-left:4px solid #FFD700;border-radius:0 8px 8px 0;padding:14px 18px;margin-top:12px;">
                        <div style="color:#FFD700;-webkit-text-fill-color:#FFD700;font-size:0.75rem;font-weight:700;letter-spacing:1px;margin-bottom:8px;">ANSWER</div>
                        <div style="color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;font-size:0.92rem;line-height:1.85;">{answer}</div>
                    </div>
                </div>
            </details>"""
        st.html(f'<style>details summary::-webkit-details-marker{{display:none;}}details[open] summary span:last-child{{transform:rotate(90deg);}}</style>{qa_html}')

# ══════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════
st.html(f"""<div style="text-align:center;padding:30px 0 15px 0;margin-top:40px;border-top:1px solid rgba(255,215,0,0.2);">
    <div style="height:2px;background:linear-gradient(90deg,transparent,{GOLD},transparent);margin:0 auto 18px auto;width:40%;"></div>
    <div style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-family:Playfair Display,serif;font-size:1.1rem;font-weight:700;">The Mountain Path Academy</div>
    <div style="color:{MUTED};-webkit-text-fill-color:{MUTED};font-size:0.78rem;margin-top:4px;">World of Finance — Prof. V. Ravichandran</div>

    <div style="margin-top:10px;"><a href="https://themountainpathacademy.com" target="_blank" style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-size:0.82rem;text-decoration:none;font-weight:600;">themountainpathacademy.com</a></div>
    <div style="margin-top:6px;">
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-size:0.75rem;text-decoration:none;margin-right:12px;">LinkedIn</a>
        <a href="https://github.com/trichyravis" target="_blank" style="color:{GOLD};-webkit-text-fill-color:{GOLD};font-size:0.75rem;text-decoration:none;">GitHub</a>
    </div></div>""")
