import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="2-Period Dynamic Game", layout="centered")

# Description
st.title("🎮 2-Period Dynamic Game")
st.markdown("""
Welcome to the 2-player, 2-period dynamic game simulation!

**Game structure:**
- In each period, you and your partner will simultaneously choose actions.
- The outcome depends on both choices.
- After Round 1, you'll see the result and proceed to Round 2 with the same roles and same partner.

**Payoff Matrix:**
|         | X        | Y        | Z        |
|---------|----------|----------|----------|
| **A**   | (4, 3)   | (0, 0)   | (1, 4)   |
| **B**   | (0, 0)   | (2, 1)   | (0, 0)   |
""")

# Simulate backend memory for names and roles (would be a DB in real usage)
if "players" not in st.session_state:
    st.session_state.players = []

if "matched_pairs" not in st.session_state:
    st.session_state.matched_pairs = []

if "games" not in st.session_state:
    st.session_state.games = {}

# Collect name
with st.form("name_form"):
    name = st.text_input("👤 Enter your full name:")
    submitted = st.form_submit_button("Submit")

if submitted and name:
    if name not in st.session_state.players:
        st.session_state.players.append(name)

    # Try to match players in pairs
    if len(st.session_state.players) % 2 == 0:
        p1, p2 = st.session_state.players[-2:]
        pair_id = f"{p1} vs {p2}"
        st.session_state.matched_pairs.append((p1, p2))
        st.session_state.games[pair_id] = {
            "round1": {},
            "round2": {},
            "players": [p1, p2]
        }
        st.success(f"✅ Matched: {p1} is Player 1, {p2} is Player 2")
    else:
        st.info("⏳ Waiting for another player to join...")

# If matched, let them play
for pair in st.session_state.matched_pairs:
    p1, p2 = pair
    pair_id = f"{p1} vs {p2}"

    if name == p1 or name == p2:
        role = "Player 1" if name == p1 else "Player 2"
        st.subheader(f"🧑‍🤝‍🧑 {pair_id} — You are **{role}**")

        # Round 1
        if not st.session_state.games[pair_id]["round1"].get(name):
            st.write("🎯 Period 1:")
            move = st.radio("Choose your move:", ["A", "B"] if role == "Player 1" else ["X", "Y", "Z"], key=f"{name}_r1")
            if st.button("Submit Round 1 move", key=f"{name}_r1_submit"):
                st.session_state.games[pair_id]["round1"][name] = move
                st.success(f"✅ {role} submitted move: {move}")
                st.experimental_rerun()

        # After both submitted in round 1
        if len(st.session_state.games[pair_id]["round1"]) == 2:
            move_p1 = st.session_state.games[pair_id]["round1"][p1]
            move_p2 = st.session_state.games[pair_id]["round1"][p2]
            payoff_matrix = {
                ("A", "X"): (4, 3),
                ("A", "Y"): (0, 0),
                ("A", "Z"): (1, 4),
                ("B", "X"): (0, 0),
                ("B", "Y"): (2, 1),
                ("B", "Z"): (0, 0)
            }
            payoffs = payoff_matrix.get((move_p1, move_p2), (0, 0))
            st.info(f"🎯 Round 1 Outcome: {p1} chose {move_p1}, {p2} chose {move_p2}")
            st.success(f"💰 Payoffs: {p1} = {payoffs[0]}, {p2} = {payoffs[1]}")

            # Round 2
            if not st.session_state.games[pair_id]["round2"].get(name):
                st.write("🎯 Period 2:")
                move2 = st.radio("Choose your move:", ["A", "B"] if role == "Player 1" else ["X", "Y", "Z"], key=f"{name}_r2")
                if st.button("Submit Round 2 move", key=f"{name}_r2_submit"):
                    st.session_state.games[pair_id]["round2"][name] = move2
                    st.success(f"✅ {role} submitted move: {move2}")
                    st.experimental_rerun()

            if len(st.session_state.games[pair_id]["round2"]) == 2:
                move2_p1 = st.session_state.games[pair_id]["round2"][p1]
                move2_p2 = st.session_state.games[pair_id]["round2"][p2]
                payoffs2 = payoff_matrix.get((move2_p1, move2_p2), (0, 0))
                st.info(f"🎯 Round 2 Outcome: {p1} chose {move2_p1}, {p2} chose {move2_p2}")
                st.success(f"💰 Payoffs: {p1} = {payoffs2[0]}, {p2} = {payoffs2[1]}")