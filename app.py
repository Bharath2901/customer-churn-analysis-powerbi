import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import math
from datetime import date

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="ChurnWatch — Telecom Retention Console",
    page_icon="📡",
    layout="wide"
)

# =========================
# DESIGN TOKENS
# =========================
COLORS = {
    "void": "#0A0E1A",
    "panel": "#121826",
    "panel_raised": "#1A2236",
    "signal": "#3DDC97",   # healthy / retained
    "warn": "#FFB454",     # caution
    "danger": "#FF5C7A",   # churned / at risk
    "cyan": "#5EC8FF",     # neutral data accent
    "text": "#E8ECF4",
    "muted": "#7C8AA8",
    "border": "#232C42",
}
MUTED = COLORS["muted"]

# =========================
# GLOBAL STYLE
# =========================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

.stApp {{
    background: {COLORS['void']};
    color: {COLORS['text']};
    font-family: 'Inter', sans-serif;
}}

.block-container {{ padding-top: 4.5rem; max-width: 1200px; }}

[data-testid="stHeader"] {{
    background: {COLORS['void']};
    height: 3.2rem;
}}
[data-testid="stToolbar"] {{ right: 1rem; }}

h1, h2, h3 {{
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.01em;
    color: {COLORS['text']};
}}

[data-testid="stSidebar"] {{
    background: {COLORS['panel']};
    border-right: 1px solid {COLORS['border']};
}}
[data-testid="stSidebar"] * {{ color: {COLORS['text']}; }}

[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {COLORS['panel']};
    border: 1px solid {COLORS['border']} !important;
    border-radius: 12px;
}}

footer {{ visibility: hidden; }}

/* ---- Topbar ---- */
.topbar {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-bottom: 1px solid {COLORS['border']};
    padding-bottom: 14px;
    margin-bottom: 22px;
}}
.topbar-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: {COLORS['text']};
}}
.topbar-title span {{
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
    font-size: 0.78rem;
    color: {COLORS['muted']};
    letter-spacing: 0.06em;
    margin-left: 8px;
}}
.topbar-status {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: {COLORS['muted']};
    letter-spacing: 0.04em;
}}
.status-dot {{
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: {COLORS['signal']};
    margin-right: 6px;
    box-shadow: 0 0 0 0 rgba(61,220,151, 0.7);
    animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(61,220,151, 0.5); }}
    70% {{ box-shadow: 0 0 0 6px rgba(61,220,151, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(61,220,151, 0); }}
}}
@media (prefers-reduced-motion: reduce) {{
    .status-dot {{ animation: none; }}
}}

/* ---- Eyebrow labels ---- */
.eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    color: {COLORS['muted']};
    text-transform: uppercase;
    margin-bottom: 2px;
}}

/* ---- KPI cards ---- */
.kpi-card {{
    background: {COLORS['panel']};
    border: 1px solid {COLORS['border']};
    border-left: 3px solid var(--accent, {COLORS['cyan']});
    border-radius: 10px;
    padding: 16px 18px;
    height: 108px;
}}
.kpi-eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {COLORS['muted']};
}}
.kpi-value {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    margin-top: 6px;
    color: {COLORS['text']};
}}
.kpi-sub {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: {COLORS['muted']};
    margin-top: 2px;
}}

/* ---- Signal meter (signature element) ---- */
.signal-meter {{
    display: flex;
    align-items: flex-end;
    gap: 5px;
    height: 64px;
}}
.signal-bar {{
    width: 14px;
    border-radius: 2px;
    transition: background 0.3s ease;
}}

/* ---- Risk chips ---- */
.chip {{
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    padding: 4px 10px;
    border-radius: 20px;
    margin: 3px 6px 3px 0;
    border: 1px solid {COLORS['border']};
}}
.chip-on {{ color: {COLORS['void']}; font-weight: 600; }}
.chip-off {{ color: {COLORS['muted']}; opacity: 0.55; }}
</style>
""", unsafe_allow_html=True)

# =========================
# PLOTLY THEME
# =========================
pio.templates["churnwatch"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=COLORS["text"], size=13),
        title=dict(font=dict(family="Space Grotesk, sans-serif", size=17, color=COLORS["text"])),
        xaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], linecolor=COLORS["border"]),
        yaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], linecolor=COLORS["border"]),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        colorway=[COLORS["signal"], COLORS["danger"], COLORS["cyan"], COLORS["warn"]],
    )
)
pio.templates.default = "churnwatch"
CHURN_COLOR_MAP = {"No": COLORS["signal"], "Yes": COLORS["danger"]}

# =========================
# HELPERS
# =========================
def render_topbar(record_count):
    st.markdown(f"""
    <div class="topbar">
        <div class="topbar-title">CHURNWATCH<span>/ TELECOM RETENTION CONSOLE</span></div>
        <div class="topbar-status"><span class="status-dot"></span>LIVE · {record_count:,} RECORDS · {date.today().strftime('%d %b %Y').upper()}</div>
    </div>
    """, unsafe_allow_html=True)

def kpi_card(eyebrow, value, sub="", accent=COLORS["cyan"]):
    st.markdown(f"""
    <div class="kpi-card" style="--accent: {accent};">
        <div class="kpi-eyebrow">{eyebrow}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def signal_meter(level, accent, height_px=64):
    """level: 0-5 bars lit, accent: hex color for lit bars."""
    heights = [28, 46, 64, 82, 100]
    bars = ""
    for i, h in enumerate(heights):
        color = accent if i < level else COLORS["border"]
        bars += f'<div class="signal-bar" style="height:{h}%; background:{color};"></div>'
    return f'<div class="signal-meter" style="height:{height_px}px;">{bars}</div>'

def churn_band(rate):
    """Returns (level 1-5, color, label) for a churn-style rate (higher = worse)."""
    if rate >= 70:
        return 5, COLORS["danger"], "HIGH RISK"
    elif rate >= 55:
        return 4, COLORS["danger"], "ELEVATED RISK"
    elif rate >= 40:
        return 3, COLORS["warn"], "MODERATE RISK"
    elif rate >= 20:
        return 2, COLORS["signal"], "LOW RISK"
    else:
        return 1, COLORS["signal"], "MINIMAL RISK"

def chip(label, active, color):
    cls = "chip chip-on" if active else "chip chip-off"
    style = f"background:{color}; border-color:{color};" if active else ""
    return f'<span class="{cls}" style="{style}">{label}</span>'

def eyebrow(text):
    st.markdown(f'<div class="eyebrow">{text}</div>', unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("Data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.markdown(f"""
    <div style="background:{COLORS['panel']}; border:1px solid {COLORS['danger']};
                border-radius:10px; padding:20px 24px; margin-top:40px;">
        <div class="eyebrow" style="color:{COLORS['danger']};">DATA SOURCE NOT FOUND</div>
        <p style="margin-top:8px;">Couldn't find <code>Data/WA_Fn-UseC_-Telco-Customer-Churn.csv</code>.
        Place the file at that path relative to this script and reload.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# =========================
# SIDEBAR NAV
# =========================
st.sidebar.markdown(f"""
<div style="padding: 4px 0 18px 0;">
    <div style="font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.1rem;">📡 CHURNWATCH</div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:{COLORS['muted']}; letter-spacing:0.05em;">RETENTION OPS PANEL</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["📡 Dashboard", "📊 Analytics", "🎯 Prediction"],
    label_visibility="collapsed"
)
page = page.split(" ", 1)[1]

st.sidebar.markdown(f"""
<div style="margin-top:24px; padding-top:16px; border-top:1px solid {COLORS['border']};
            font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:{COLORS['muted']};">
    DATASET<br>Telco Customer Churn<br>{len(df):,} rows loaded
</div>
""", unsafe_allow_html=True)

# =========================
# DASHBOARD PAGE
# =========================
if page == "Dashboard":
    render_topbar(len(df))
    st.markdown("### Customer Churn Overview")
    st.markdown(f"<p style='color:{MUTED}; margin-top:-8px;'>Fleet-wide retention signal at a glance.</p>", unsafe_allow_html=True)
    st.markdown("")

    total_customers = len(df)
    churned = len(df[df["Churn"] == "Yes"])
    churn_rate = round(churned / total_customers * 100, 2)
    retained = total_customers - churned
    retention_rate = round(retained / total_customers * 100, 2)

    level, color, label = churn_band(churn_rate)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("TOTAL CUSTOMERS", f"{total_customers:,}", "FULL ACCOUNT BASE", COLORS["cyan"])
    with c2:
        kpi_card("CHURN RATE", f"{churn_rate}%", label, color)
    with c3:
        kpi_card("CHURNED", f"{churned:,}", "LOST LAST PERIOD", COLORS["danger"])
    with c4:
        kpi_card("RETAINED", f"{retained:,}", f"{retention_rate}% OF BASE", COLORS["signal"])

    st.markdown("")
    with st.container(border=True):
        sc1, sc2 = st.columns([1, 2])
        with sc1:
            eyebrow("NETWORK HEALTH SIGNAL")
            st.markdown(signal_meter(level, color, height_px=80), unsafe_allow_html=True)
            st.markdown(f"<div style='font-family:JetBrains Mono,monospace; font-size:0.85rem; margin-top:8px; color:{color};'>{label}</div>", unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
            <div style="font-size:0.92rem; color:{COLORS['muted']}; padding-top:6px;">
            Of every 100 customers connected to the network, roughly
            <b style="color:{COLORS['text']};">{round(churn_rate)}</b> disconnect.
            Bars rise as the base's churn rate climbs — treat 4–5 lit bars as a signal
            to investigate contract terms, pricing, and service mix below.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            eyebrow("BY CONTRACT TYPE")
            contract_chart = px.histogram(
                df, x="Contract", color="Churn", barmode="group",
                color_discrete_map=CHURN_COLOR_MAP
            )
            contract_chart.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=360)
            st.plotly_chart(contract_chart, use_container_width=True, config={"displayModeBar": False})
    with col2:
        with st.container(border=True):
            eyebrow("BY INTERNET SERVICE")
            internet_chart = px.histogram(
                df, x="InternetService", color="Churn", barmode="group",
                color_discrete_map=CHURN_COLOR_MAP
            )
            internet_chart.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=360)
            st.plotly_chart(internet_chart, use_container_width=True, config={"displayModeBar": False})

# =========================
# ANALYTICS PAGE
# =========================
elif page == "Analytics":
    render_topbar(len(df))
    st.markdown("### Customer Analytics")
    st.markdown(f"<p style='color:{MUTED}; margin-top:-8px;'>Distributions behind the headline churn number.</p>", unsafe_allow_html=True)
    st.markdown("")

    with st.container(border=True):
        eyebrow("BY PAYMENT METHOD")
        payment_chart = px.histogram(
            df, x="PaymentMethod", color="Churn", barmode="group",
            color_discrete_map=CHURN_COLOR_MAP
        )
        payment_chart.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=380)
        st.plotly_chart(payment_chart, use_container_width=True, config={"displayModeBar": False})

    st.markdown("")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            eyebrow("MONTHLY CHARGES DISTRIBUTION")
            monthly_chart = px.histogram(df, x="MonthlyCharges", color_discrete_sequence=[COLORS["cyan"]])
            monthly_chart.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=340)
            st.plotly_chart(monthly_chart, use_container_width=True, config={"displayModeBar": False})
    with col2:
        with st.container(border=True):
            eyebrow("TENURE DISTRIBUTION (MONTHS)")
            tenure_chart = px.histogram(df, x="tenure", color_discrete_sequence=[COLORS["warn"]])
            tenure_chart.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=340)
            st.plotly_chart(tenure_chart, use_container_width=True, config={"displayModeBar": False})

# =========================
# PREDICTION PAGE
# =========================
elif page == "Prediction":
    render_topbar(len(df))
    st.markdown("### Churn Risk Prediction")
    st.markdown(f"<p style='color:{MUTED}; margin-top:-8px;'>Estimate a single customer's disconnect risk from three signals.</p>", unsafe_allow_html=True)
    st.markdown("")

    in_col, out_col = st.columns([1, 1], gap="large")

    with in_col:
        with st.container(border=True):
            eyebrow("CUSTOMER INPUTS")
            tenure = st.slider("Customer tenure (months)", min_value=0, max_value=72, value=12)
            monthly_charges = st.number_input("Monthly charges ($)", min_value=0.0, max_value=200.0, value=70.0)
            contract = st.selectbox("Contract type", ["Month-to-month", "One year", "Two year"])
            run = st.button("Run Prediction", use_container_width=True)

    with out_col:
        with st.container(border=True):
            eyebrow("RISK READOUT")
            if not run:
                st.markdown(f"<p style='color:{MUTED}; padding-top:8px;'>Set the inputs on the left and run a prediction to see the signal.</p>", unsafe_allow_html=True)
            else:
                short_tenure = tenure < 12
                high_charges = monthly_charges > 70
                flexible_contract = contract == "Month-to-month"

                score = 0
                if short_tenure:
                    score += 40
                if high_charges:
                    score += 30
                if flexible_contract:
                    score += 30
                probability = min(score, 100)
                level, color, label = churn_band(probability)

                st.markdown(signal_meter(level, color, height_px=80), unsafe_allow_html=True)
                st.markdown(f"""
                <div style="font-family:'Space Grotesk',sans-serif; font-size:2rem; font-weight:700; margin-top:10px; color:{color};">
                    {probability}%
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.8rem; color:{color}; letter-spacing:0.04em;">
                    {label}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
                eyebrow("CONTRIBUTING FACTORS")
                chips_html = (
                    chip("SHORT TENURE (+40)", short_tenure, COLORS["danger"])
                    + chip("HIGH MONTHLY CHARGES (+30)", high_charges, COLORS["warn"])
                    + chip("MONTH-TO-MONTH CONTRACT (+30)", flexible_contract, COLORS["danger"])
                )
                st.markdown(chips_html, unsafe_allow_html=True)
