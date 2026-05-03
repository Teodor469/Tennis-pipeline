import streamlit as st
import pandas as pd
import numpy as np

@st.cache_resource
def get_con():
      from src.db import get_connection
      return get_connection()

con = get_con()




with st.sidebar:
      st.selectbox(
            "Select court surface",
            ("Hard", "Clay", "Grass")
      )
      year = st.number_input(label="Select Year of Tournament", min_value=1968, max_value=2024)
      st.info(
    "**Tennis Analytics Pipeline** — Explore historical ATP/WTA match data. "
    "Filter by court surface and year to browse match results, or look up player win rates by name. "
    "Data is sourced from a local DuckDB database built by this pipeline.",
    icon="🎾"
)

st.title("Tennis Analytics")
df = con.execute("SELECT * FROM stg_matches where year(tournament_date) = ?", [year]).df()
st.dataframe(df)

st.title('Player Win Rate')
player_name = st.text_input("Player Name")
df = con.execute("SELECT * FROM player_stats WHERE player_name ILIKE ?", [f'%{player_name}%']).df()
st.dataframe(df)

st.title('Player vs Player & Win Rate')
player_1 = st.text_input("Player 1")
player_2 = st.text_input("Player 2")
df = con.execute(
    "SELECT * FROM head_to_head WHERE least(?, ?) = player_1 AND greatest(?, ?) = player_2",
    [player_1, player_2, player_1, player_2]
).df()
st.dataframe(df)

st.title("Win rate per player per surface")
player = st.text_input("Player")
df = con.execute("SELECT * FROM per_player_per_surface where player ILIKE ?", [f'%{player}%']).df()
st.dataframe(df)

st.title("Upset matches")
tournament_level = st.selectbox(
            "Select Tournament Level",
            ("O", "M", "A", "G", "D", "F"),
            index=3
      )
percentage = st.number_input(label='Threshold Percentage')
df = con.execute("SELECT * FROM upset_matches WHERE tourney_level = ? AND CAST(TRIM(TRAILING '%' from upset_percentage) AS DOUBLE) > ?", [tournament_level, percentage]).df()
st.dataframe(df)