import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Tennis Analytics",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* ── Base ── */
    .stApp { background: #0d1117; }

    /* ── Hero header ── */
    .hero {
        background: linear-gradient(135deg, #0f3460 0%, #16213e 50%, #1a4731 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        font-size: 1rem;
        color: rgba(255,255,255,0.55);
        margin-top: 0.4rem;
        font-weight: 400;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(255,255,255,0.03);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.07);
        margin-bottom: 1.2rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 8px 18px !important;
        font-weight: 500;
        color: rgba(255,255,255,0.5) !important;
        background: transparent !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0f3460, #1a4731) !important;
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #111827 !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    .sidebar-logo {
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff;
        padding: 0.5rem 0 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1.2rem;
    }

    /* ── Section headings ── */
    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.35);
        margin-bottom: 0.6rem;
        margin-top: 0.2rem;
    }

    /* ── Metric strip ── */
    .metric-row {
        display: flex;
        gap: 12px;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        flex: 1;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1rem 1.2rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #60a5fa;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.78rem;
        color: rgba(255,255,255,0.45);
        margin-top: 0.25rem;
        font-weight: 500;
    }

    /* ── Inputs ── */
    .stTextInput input, .stNumberInput input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important;
    }
    [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
    }
    label { color: rgba(255,255,255,0.75) !important; font-weight: 500 !important; }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
    .stDataFrame thead tr th {
        background: rgba(255,255,255,0.06) !important;
        font-weight: 600;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
    }

    /* ── Alerts ── */
    [data-testid="stAlert"] { border-radius: 10px !important; }

    /* ── Hide Streamlit chrome ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_con():
    from src.db import get_connection
    return get_connection()

con = get_con()

TOURNEY_LEVEL_MAP = {
    "Grand Slam": "G",
    "Masters 1000": "M",
    "ATP 250/500": "A",
    "Olympics": "O",
    "Davis Cup": "D",
    "Tour Finals": "F",
}

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🎾 Tennis Analytics</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Global Filters</div>', unsafe_allow_html=True)
    st.selectbox(
        "Court Surface",
        ("Hard", "Clay", "Grass"),
        help="Surface type used for filtering"
    )
    year = st.number_input(
        label="Tournament Year",
        min_value=1968,
        max_value=2024,
        value=2023,
        help="Year of tournament data to explore"
    )

    st.divider()
    st.info(
        "Explore historical ATP/WTA match data.\n\n"
        "Filter by surface and year, look up player stats, "
        "compare head-to-head records, or find major upsets.\n\n"
        "Data sourced from a local **DuckDB** database.",
        icon="ℹ️"
    )

# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">Tennis Analytics Dashboard</div>
    <div class="hero-sub">Historical ATP &amp; WTA data · Matches · Players · Head-to-Head · Upsets</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📅  Match Results",
    "👤  Player Win Rate",
    "⚔️  Head to Head",
    "🏟️  Surface Stats",
    "⚡  Upsets",
])


# ── Tab 1: Match Results ───────────────────────────────────────────────────
with tab1:
    st.subheader(f"Match Results — {int(year)}")

    df = con.execute(
        "SELECT * FROM stg_matches where year(tournament_date) = ?", [year]
    ).df()

    if df.empty:
        st.warning(f"No match data found for **{int(year)}**.", icon="⚠️")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Matches", f"{len(df):,}")
        c2.metric("Unique Winners", f"{df['winner_name'].nunique():,}" if 'winner_name' in df.columns else "—")
        c3.metric("Tournaments", f"{df['tourney_name'].nunique():,}" if 'tourney_name' in df.columns else "—")
        st.dataframe(df, use_container_width=True, hide_index=True)


# ── Tab 2: Player Win Rate ─────────────────────────────────────────────────
with tab2:
    st.subheader("Player Win Rate")
    st.caption("Search any player to view their historical win-rate statistics.")

    player_name = st.text_input(
        "Player Name",
        placeholder="e.g. Federer, Serena, Djokovic…",
        label_visibility="collapsed"
    )

    if player_name:
        df = con.execute(
            "SELECT * FROM player_stats WHERE player_name ILIKE ?",
            [f'%{player_name}%']
        ).df()
        if df.empty:
            st.warning(f"No stats found for **{player_name}**. Try a different spelling.", icon="🔍")
        else:
            st.success(f"**{len(df)}** result(s) for '{player_name}'", icon="✅")
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Type a player name above to load their win-rate stats.", icon="👆")


# ── Tab 3: Head to Head ────────────────────────────────────────────────────
with tab3:
    st.subheader("Head to Head")
    st.caption("Compare the all-time record between two players.")

    col_a, col_b = st.columns(2)
    with col_a:
        player_1 = st.text_input("Player 1", placeholder="e.g. Federer")
    with col_b:
        player_2 = st.text_input("Player 2", placeholder="e.g. Nadal")

    if player_1 and player_2:
        df = con.execute(
            "SELECT * FROM head_to_head WHERE least(?, ?) = player_1 AND greatest(?, ?) = player_2",
            [player_1, player_2, player_1, player_2]
        ).df()
        if df.empty:
            st.warning(
                f"No head-to-head record found for **{player_1}** vs **{player_2}**.",
                icon="⚠️"
            )
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Enter both player names to see their head-to-head record.", icon="⚔️")


# ── Tab 4: Surface Stats ───────────────────────────────────────────────────
with tab4:
    st.subheader("Win Rate by Surface")
    st.caption("See how a player performs on Hard, Clay, and Grass courts.")

    player = st.text_input(
        "Player",
        placeholder="e.g. Serena Williams, Alcaraz…",
        label_visibility="collapsed",
        key="surface_player"
    )

    if player:
        df = con.execute(
            "SELECT * FROM per_player_per_surface where player ILIKE ?",
            [f'%{player}%']
        ).df()
        if df.empty:
            st.warning(f"No surface data found for **{player}**.", icon="🔍")
        else:
            st.success(f"**{len(df)}** surface record(s) for '{player}'", icon="✅")
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Type a player name to load their surface-by-surface win rates.", icon="🏟️")


# ── Tab 5: Upsets ──────────────────────────────────────────────────────────
with tab5:
    st.subheader("Upset Matches")
    st.caption("Matches where a lower-ranked player defeated a higher-ranked opponent.")

    col_l, col_r = st.columns(2)
    with col_l:
        tourney_level_label = st.selectbox(
            "Tournament Level",
            list(TOURNEY_LEVEL_MAP.keys()),
            index=0,
            help="Filter upsets by tournament tier"
        )
        tournament_level = TOURNEY_LEVEL_MAP[tourney_level_label]
    with col_r:
        percentage = st.number_input(
            label="Minimum Upset Threshold (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=5.0,
            help="Only show upsets where the ranking gap exceeds this percentage"
        )

    df = con.execute(
        "SELECT * FROM upset_matches WHERE tourney_level = ? "
        "AND CAST(TRIM(TRAILING '%' from upset_percentage) AS DOUBLE) > ?",
        [tournament_level, percentage]
    ).df()

    if df.empty:
        st.warning(
            f"No upsets found at **{tourney_level_label}** level above **{percentage:.0f}%**.",
            icon="⚠️"
        )
    else:
        st.success(
            f"**{len(df):,}** upset(s) at **{tourney_level_label}** level "
            f"above **{percentage:.0f}%** threshold",
            icon="⚡"
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
