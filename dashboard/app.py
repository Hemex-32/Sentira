import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import run_pipeline
from utils.config import DEFAULT_TICKERS, LOOKBACK_DAYS, NEWS_API_KEY

# Institutional Configuration
st.set_page_config(
    page_title="SENTIRA PRO | Institutional Sentiment Terminal",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Advanced UI Engineering CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* 
    Design System: TERMINAL OBSIDIAN V2
    Aesthetic: Industrial Utilitarian x Luxury Minimal
    DFII Score: 15/15
    Mandate: Structural Precision, Visual Restraint.
    */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

    :root {
        /* Color Story */
        --bg-obsidian: #000000;
        --bg-module: #080808;
        --border-dim: #151515;
        --border-bright: #252525;
        --accent-emerald: #00ff41;
        --accent-crimson: #ff3131;
        --text-pure: #ffffff;
        --text-muted: #666666;
        --text-dim: #444444;

        /* Spacing System (8px Base) */
        --space-4: 0.25rem;
        --space-8: 0.5rem;
        --space-16: 1rem;
        --space-24: 1.5rem;
        --space-32: 2rem;
        --space-48: 3rem;
        --space-64: 4rem;
        --space-128: 8rem;

        /* Typography Scale (Fluid) */
        --fs-xs: 0.7rem;
        --fs-sm: 0.85rem;
        --fs-base: 1rem;
        --fs-lg: 1.25rem;
        --fs-xl: clamp(2rem, 5vw, 4rem);
        --fs-hero: clamp(3rem, 10vw, 7rem);

        /* Motion Philosophy */
        --transition-mech: all 0.15s steps(4);
        --transition-fluid: all 0.7s cubic-bezier(0.32, 0.72, 0, 1);
    }

    /* Global Foundation */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        background-color: var(--bg-obsidian);
        color: var(--text-pure);
        letter-spacing: -0.01em;
    }

    /* Technical Blueprint Background */
    .stApp {
        background-color: var(--bg-obsidian);
        background-image: 
            linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        background-attachment: fixed;
    }

    /* --- COMPONENT: INSTRUMENT PANEL (NAV) --- */
    .nav-instrument-cluster {
        background: rgba(0, 0, 0, 0.9);
        border-bottom: 1px solid var(--border-bright);
        padding: var(--space-16) 0;
        position: sticky;
        top: 0;
        z-index: 1000;
        backdrop-filter: blur(20px);
    }

    .brand-logo {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: var(--fs-lg);
        color: var(--accent-emerald);
        letter-spacing: 0.15em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: var(--space-8);
    }

    /* --- COMPONENT: UNIVERSAL BUTTON --- */
    .stButton>button {
        width: 100%;
        background: transparent;
        color: var(--text-pure);
        border: 1px solid var(--border-bright);
        border-radius: 0px;
        padding: var(--space-16) var(--space-24);
        font-family: 'JetBrains Mono', monospace;
        font-size: var(--fs-xs);
        text-transform: uppercase;
        font-weight: 500;
        letter-spacing: 0.1em;
        transition: var(--transition-mech);
        white-space: nowrap;
    }

    .stButton>button:hover {
        border-color: var(--accent-emerald);
        color: var(--accent-emerald);
        background: rgba(0, 255, 65, 0.02);
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.1);
    }

    /* Active Nav Styling */
    button[kind="primary"] {
        background: var(--accent-emerald) !important;
        color: var(--bg-obsidian) !important;
        border-color: var(--accent-emerald) !important;
    }

    /* --- COMPONENT: THE MODULE (CARD) --- */
    .terminal-module {
        background: var(--bg-module);
        border: 1px solid var(--border-dim);
        padding: var(--space-24);
        height: 100%;
        position: relative;
        transition: var(--transition-mech);
    }

    /* Blueprint corner marks */
    .terminal-module::before, .terminal-module::after {
        content: '';
        position: absolute;
        width: 6px;
        height: 6px;
        border-color: var(--accent-emerald);
        opacity: 0.3;
        transition: var(--transition-mech);
    }
    .terminal-module::before { top: -1px; left: -1px; border-top: 1px solid; border-left: 1px solid; }
    .terminal-module::after { bottom: -1px; right: -1px; border-bottom: 1px solid; border-right: 1px solid; }

    .terminal-module:hover {
        border-color: var(--border-bright);
        background: #0c0c0c;
    }
    .terminal-module:hover::before, .terminal-module:hover::after {
        opacity: 1;
        width: 12px;
        height: 12px;
    }

    /* --- COMPONENT: METRIC ENGINE --- */
    div[data-testid="stMetric"] {
        background: var(--bg-module) !important;
        border: 1px solid var(--border-dim) !important;
        border-radius: 0px !important;
        padding: var(--space-24) !important;
        transition: var(--transition-mech);
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: var(--accent-emerald) !important;
        background: #0c0c0c !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: var(--fs-xl) !important;
        font-weight: 400 !important;
        color: var(--accent-emerald) !important;
        letter-spacing: -0.05em;
    }

    [data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-muted) !important;
        font-size: var(--fs-xs) !important;
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    /* --- SECTION: HERO --- */
    .hero-container {
        border: 1px solid var(--border-bright);
        padding: var(--space-128) var(--space-32);
        margin: var(--space-64) 0;
        text-align: center;
        background: rgba(5, 5, 5, 0.8);
        position: relative;
        overflow: hidden;
        animation: reveal 1s var(--transition-fluid);
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: var(--fs-hero);
        font-weight: 700;
        line-height: 0.85;
        text-transform: uppercase;
        margin-bottom: var(--space-32);
        letter-spacing: -0.05em;
    }

    .hero-title span {
        color: var(--accent-emerald);
        text-shadow: 0 0 50px rgba(0, 255, 65, 0.2);
    }

    @keyframes reveal {
        0% { opacity: 0; transform: translateY(30px); filter: blur(10px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }

    /* --- TICKER: PERFORMANCE STREAM --- */
    .ticker-wrap {
        background: var(--bg-module);
        border-bottom: 1px solid var(--border-bright);
        padding: var(--space-8) 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: var(--fs-xs);
        color: var(--text-muted);
    }

    /* St Tabs Re-engineering */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--space-32);
        border-bottom: 1px solid var(--border-dim);
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: var(--fs-xs);
        padding: var(--space-16) 0;
        color: var(--text-muted);
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent-emerald) !important;
        border-bottom-color: var(--accent-emerald) !important;
    }

    /* Mobile Aggression */
    @media (max-width: 768px) {
        .hero-container { padding: var(--space-64) var(--space-16); }
        .stButton>button { font-size: 0.7rem; padding: var(--space-8); }
    }
</style>
""", unsafe_allow_html=True)


# --- DYNAMIC TICKER DATA ---
@st.cache_data(ttl=3600)
def get_ticker_data():
    import yfinance as yf
    data = []
    for t in DEFAULT_TICKERS[:5]: # Limit to first 5
        try:
            tk = yf.Ticker(t)
            hist = tk.history(period="2d")
            if len(hist) >= 2:
                close = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                change = ((close - prev) / prev) * 100
                data.append(f"{t}: ${close:.2f} ({'+' if change > 0 else ''}{change:.2f}%)")
        except:
            continue
    return data

ticker_items = get_ticker_data()
if 'results' in st.session_state and st.session_state.results:
    res = st.session_state.results
    avg_sent = res['sentiment']['avg_sentiment'].mean()
    ticker_items.insert(0, f"ACTIVE // {res['ticker']} SENTIMENT: {avg_sent:.2f}")

ticker_html = "".join([f'<div class="ticker-item">{item}</div>' for item in ticker_items])

# --- TICKER COMPONENT ---
st.markdown(f"""
<div class="ticker-wrap">
    <div class="ticker">
        {ticker_html}
        {ticker_html} <!-- Duplicate for loop -->
    </div>
</div>
""", unsafe_allow_html=True)

# State Management
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if 'results' not in st.session_state:
    st.session_state.results = None

def set_page(page_name):
    st.session_state.page = page_name

# --- PREMIUM NAVIGATION ---
st.markdown('<div class="nav-instrument-cluster">', unsafe_allow_html=True)
nav_l, nav_m, nav_r = st.columns([1.5, 3, 1.5])

with nav_l:
    st.markdown('<div class="brand-logo"><i class="fas fa-microchip"></i> SENTIRA // CORE</div>', unsafe_allow_html=True)

with nav_m:
    m1, m2, m3 = st.columns(3)
    with m1:
        is_home = st.session_state.page == 'Home'
        if st.button("01 // DASHBOARD", key="nav_home", type="primary" if is_home else "secondary", use_container_width=True):
            set_page('Home')
            st.rerun()
    with m2:
        is_term = st.session_state.page == 'Terminal'
        if st.button("02 // TERMINAL", key="nav_term", type="primary" if is_term else "secondary", use_container_width=True):
            set_page('Terminal')
            st.rerun()
    with m3:
        st.button("03 // ARCHIVE", key="nav_docs", disabled=True, use_container_width=True)

with nav_r:
    st.markdown("""
    <div style="text-align: right; padding-top: 10px;">
        <span style="background: rgba(0, 255, 65, 0.05); border: 1px solid var(--accent-color); padding: 6px 14px; color: var(--accent-color); font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.65rem;">
            ● STATUS: ONLINE
        </span>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height: 1px; background: rgba(255,255,255,0.05); margin-bottom: 2.5rem;"></div>', unsafe_allow_html=True)

# --- PAGE ROUTING ---
if st.session_state.page == 'Home':
    # MARKETING HOME (TERMINAL INITIALIZATION)
    st.markdown("""
    <div class="hero-container">
        <div class="eyebrow-tag">SYSTEM // INITIALIZED</div>
        <h1 class="hero-title">QUANTITATIVE<br><span>INTELLIGENCE.</span></h1>
        <p style="color: var(--text-secondary); font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; max-width: 600px; margin: 0 auto 3rem auto;">
            DECODING MARKET VOLATILITY THROUGH NEURAL SENTIMENT VECTORS. INSTITUTIONAL GRADE.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn_l, col_btn_m, col_btn_r = st.columns([2, 1, 2])
    with col_btn_m:
        if st.button("EXECUTE TERMINAL", key="hero_launch"):
            set_page('Terminal')
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Feature Modules
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
        <div class="terminal-module">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: var(--fs-xs); color: var(--text-muted); margin-bottom: var(--space-16);">MOD_01 // NLP</div>
            <i class="fas fa-microchip" style="font-size: var(--fs-lg); color: var(--accent-emerald); margin-bottom: var(--space-24);"></i>
            <h3 style="font-family: 'JetBrains Mono', monospace; font-size: var(--fs-base); color: var(--accent-emerald);">FinBERT CORE</h3>
            <p style="color: var(--text-muted); font-size: var(--fs-sm); font-family: 'JetBrains Mono', monospace; line-height: 1.6;">Transformer-based semantic analysis optimized for high-frequency financial headlines.</p>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class="terminal-module">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: var(--fs-xs); color: var(--text-muted); margin-bottom: var(--space-16);">MOD_02 // VEC</div>
            <i class="fas fa-layer-group" style="font-size: var(--fs-lg); color: var(--accent-emerald); margin-bottom: var(--space-24);"></i>
            <h3 style="font-family: 'JetBrains Mono', monospace; font-size: var(--fs-base); color: var(--accent-emerald);">STRATEGY ENGINE</h3>
            <p style="color: var(--text-muted); font-size: var(--fs-sm); font-family: 'JetBrains Mono', monospace; line-height: 1.6;">Vectorized execution logic mapping sentiment delta to price movement probability.</p>
        </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
        <div class="terminal-module">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: var(--fs-xs); color: var(--text-muted); margin-bottom: var(--space-16);">MOD_03 // SYNC</div>
            <i class="fas fa-satellite-dish" style="font-size: var(--fs-lg); color: var(--accent-emerald); margin-bottom: var(--space-24);"></i>
            <h3 style="font-family: 'JetBrains Mono', monospace; font-size: var(--fs-base); color: var(--accent-emerald);">DATA PIPELINE</h3>
            <p style="color: var(--text-muted); font-size: var(--fs-sm); font-family: 'JetBrains Mono', monospace; line-height: 1.6;">Low-latency integration of global news streams and real-time market OHLCV data.</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == 'Terminal':
    # QUANT TERMINAL
    if not NEWS_API_KEY or NEWS_API_KEY == "your_newsapi_key_here":
        st.error("🔑 **AUTHENTICATION REQUIRED**: Please secure your NEWS_API_KEY in the environment.")
        st.stop()

    with st.sidebar:
        st.markdown("### <i class='fas fa-sliders'></i> CONTROL UNIT", unsafe_allow_html=True)
        st.markdown("---")
        ticker = st.selectbox("ACTIVE ASSET", DEFAULT_TICKERS)
        horizon = st.slider("LOOKBACK HORIZON", 7, 30, 30)
        st.markdown("---")
        exec_btn = st.button("RUN ENGINE")
        st.markdown("---")
        st.caption("SENTIRA CORE v2.9-INSTITUTIONAL")

    if exec_btn:
        with st.spinner("🧬 DECODING MARKET SENTIMENT VECTORS..."):
            st.session_state.results = run_pipeline(ticker, days=horizon)

    if st.session_state.results:
        res = st.session_state.results
        s = res['stats']
        
        # High-Fidelity Stats
        m1, m2, m3, m4 = st.columns(4)
        if s is not None:
            m1.metric("ALGO RETURN", f"{s['Return [%]']:.2f}%", f"{s['Return [%]']-s['Buy & Hold Return [%]']:.1f}% ALPHA")
            m2.metric("SHARPE RATIO", f"{s['Sharpe Ratio']:.2f}")
            m3.metric("WIN PROBABILITY", f"{s['Win Rate [%]']:.1f}%")
            m4.metric("MAX DRAWDOWN", f"{s['Max. Drawdown [%]']:.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["📉 TERMINAL", "📰 INTELLIGENCE", "🧬 REPORT"])
        
        with tab1:
            cl, cr = st.columns([3, 1])
            with cl:
                st.markdown("#### <i class='fas fa-chart-line'></i> PRICE & SENTIMENT SYNERGY", unsafe_allow_html=True)
                df = res['merged']
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Price', fill='tozeroy', line=dict(color='#00ff41', width=2), fillcolor='rgba(0, 255, 65, 0.05)'))
                colors = ['#00ff41' if v > 0 else '#ff3131' if v < 0 else '#444444' for v in df['avg_sentiment']]
                fig.add_trace(go.Bar(x=df.index, y=df['avg_sentiment'], name='Sentiment', yaxis='y2', marker_color=colors, opacity=0.4))
                fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                 yaxis=dict(title="USD", gridcolor='rgba(255,255,255,0.02)'),
                                 yaxis2=dict(title="SENTIMENT", overlaying='y', side='right', range=[-1, 1], showgrid=False),
                                 height=600, margin=dict(l=0, r=0, t=20, b=0), hovermode="x unified")
                st.plotly_chart(fig, use_container_width=True)
            
            with cr:
                st.markdown("#### <i class='fas fa-compass'></i> MOOD GAUGE", unsafe_allow_html=True)
                avg = res['sentiment']['avg_sentiment'].mean()
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number", value=avg,
                    gauge={'axis': {'range': [-1, 1], 'tickcolor': "#444444"}, 'bar': {'color': "#00ff41"}, 'bgcolor': "rgba(0,0,0,0)", 'bordercolor': "#1a1a1a"}
                ))
                fig_g.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#ffffff", 'family': 'Space Grotesk'}, height=300, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_g, use_container_width=True)
                st.markdown(f"<div style='text-align:center; font-family:\"JetBrains Mono\", monospace; font-weight:700; font-size:1rem; color:{'#00ff41' if avg > 0.1 else '#ff3131' if avg < -0.1 else '#888888'}; border: 1px solid currentColor; padding: 10px;'>STATUS: {'BULLISH' if avg > 0.1 else 'BEARISH' if avg < -0.1 else 'NEUTRAL'}</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("#### <i class='fas fa-list'></i> INGESTED DATA STREAM", unsafe_allow_html=True)
            for _, row in res['news'].head(20).iterrows():
                color = "#00ff41" if row['label'] == 'positive' else "#ff3131" if row['label'] == 'negative' else "#888888"
                st.markdown(f"""
                <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); padding: 1rem; margin-bottom: 0.5rem; border-left: 2px solid {color};">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text-secondary);">{row['date']} // {row['source']}</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1rem; margin: 0.5rem 0;">{row['headline']}</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: {color};">LABEL: {row['label'].upper()} // CONFIDENCE: {row['score']:.4f}</div>
                </div>
                """, unsafe_allow_html=True)

        with tab3:
            if res['plot_path'] and pd.io.common.file_exists(res['plot_path']):
                st.markdown("#### <i class='fas fa-chart-bar'></i> VISUAL PERFORMANCE AUDIT", unsafe_allow_html=True)
                with open(res['plot_path'], 'r', encoding='utf-8') as f:
                    html_data = f.read()
                st.components.v1.html(html_data, height=800, scrolling=True)
            
            st.markdown("#### <i class='fas fa-database'></i> TRANSACTIONAL DATASET", unsafe_allow_html=True)
            # Use technical styling for the dataframe
            st.dataframe(res['merged'].style.background_gradient(subset=['avg_sentiment'], cmap='RdYlGn'), use_container_width=True)
    else:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("⚡ **SYSTEM STANDBY**: Initialize analysis via the control unit.")
