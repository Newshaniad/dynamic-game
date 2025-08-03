
import streamlit as st
import random

# Initialize session state variables
if "players" not in st.session_state:
    st.session_state.players = []
if "assignments" not in st.session_state:
    st.session_state.assignments = {}
if "period1_choices" not in st.session_state:
    st.session_state.period1_choices = {}
if "period2_choices" not in st.session_state:
    st.session_state.period2_choices = {}
if "show_results1" not in st.session_state:
    st.session_state.show_results1 = False
if "show_results2" not in st.session_state:
    st.session_state.show_results2 = False

st.title("🎮 2-Period Dynamic Game")

st.markdown("### 🎯 Game Description")
st.markdown("""
Two players interact over **2 periods**, playing this game each time:

|        | X   | Y   | Z   |
|--------|-----|-----|-----|
| **A**  |4,3  |0,0  |1,4  |
| **B**  |0,0  |2,1  |0,0  |

- Player 1 chooses A or B  
- Player 2 chooses X, Y, or Z  
- They see their payoffs  
- In Period 2, they can adjust strategy based on Period 1’s play  
""")
st.markdown("Please enter your name to start:")

name = st.text_input("👤 Your name:")
if st.button("Submit") and name:
    if name not in st.session_state.players:
        st.session_state.players.append(name)

# Wait for two players
if len(st.session_state.players) < 2:
    st.info("⏳ Waiting for another player to join...")
    st.stop()

# Assign roles randomly once both joined
if not st.session_state.assignments:
    random.shuffle(st.session_state.players)
    st.session_state.assignments[st.session_state.players[0]] = "Player 1"
    st.session_state.assignments[st.session_state.players[1]] = "Player 2"

role = st.session_state.assignments[name]
st.success(f"You are **{role}**.")

# PERIOD 1 CHOICE
st.markdown("## 🔁 Period 1")

if role == "Player 1":
    move1 = st.radio("Choose your action (Player 1):", ["A", "B"])
    if st.button("Lock Player 1 Move (Period 1)"):
        st.session_state.period1_choices["P1"] = move1
elif role == "Player 2":
    move2 = st.radio("Choose your action (Player 2):", ["X", "Y", "Z"])
    if st.button("Lock Player 2 Move (Period 1)"):
        st.session_state.period1_choices["P2"] = move2

# Display result of Period 1
if "P1" in st.session_state.period1_choices and "P2" in st.session_state.period1_choices:
    a, b = st.session_state.period1_choices["P1"], st.session_state.period1_choices["P2"]
    payoff_matrix = {
        ("A", "X"): (4, 3),
        ("A", "Y"): (0, 0),
        ("A", "Z"): (1, 4),
        ("B", "X"): (0, 0),
        ("B", "Y"): (2, 1),
        ("B", "Z"): (0, 0),
    }
    p1_payoff, p2_payoff = payoff_matrix[(a, b)]
    st.markdown(f"🎯 Period 1 Result: P1 = {a}, P2 = {b} → Payoffs = ({p1_payoff}, {p2_payoff})")
    st.session_state.show_results1 = True

# PERIOD 2
if st.session_state.show_results1:
    st.markdown("## 🔁 Period 2")
    if role == "Player 1":
        move1_2 = st.radio("Choose your action (Player 1):", ["A", "B"], key="p1r2")
        if st.button("Lock Player 1 Move (Period 2)"):
            st.session_state.period2_choices["P1"] = move1_2
    elif role == "Player 2":
        move2_2 = st.radio("Choose your action (Player 2):", ["X", "Y", "Z"], key="p2r2")
        if st.button("Lock Player 2 Move (Period 2)"):
            st.session_state.period2_choices["P2"] = move2_2

if "P1" in st.session_state.period2_choices and "P2" in st.session_state.period2_choices:
    a2, b2 = st.session_state.period2_choices["P1"], st.session_state.period2_choices["P2"]
    payoff_matrix = {
        ("A", "X"): (4, 3),
        ("A", "Y"): (0, 0),
        ("A", "Z"): (1, 4),
        ("B", "X"): (0, 0),
        ("B", "Y"): (2, 1),
        ("B", "Z"): (0, 0),
    }
    p1p2, p2p2 = payoff_matrix[(a2, b2)]
    st.markdown(f"🎯 Period 2 Result: P1 = {a2}, P2 = {b2} → Payoffs = ({p1p2}, {p2p2})")
    st.session_state.show_results2 = True
