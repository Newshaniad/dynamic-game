
# streamlit_app.py
import streamlit as st
import matplotlib.pyplot as plt
import random

# Payoff matrix
game_matrix = {
    ('A', 'X'): (4, 3),
    ('A', 'Y'): (0, 0),
    ('A', 'Z'): (1, 4),
    ('B', 'X'): (0, 0),
    ('B', 'Y'): (2, 1),
    ('B', 'Z'): (0, 0)
}

st.set_page_config(page_title="2-Period Dynamic Game", page_icon="🎮")
st.title("🎮 2-Period Dynamic Game")

# 📘 Game description
st.markdown("""
## Instructions:
In this game, you will play **two periods** of a strategic interaction.
- Player 1 chooses: A or B  
- Player 2 chooses: X, Y, or Z  
- After Period 1, both players see the result and make decisions in Period 2.
- Your total payoff = sum of your two rounds.
""")

# 🧑 Enter student name
student_name = st.text_input("Enter your full name to begin:")

if student_name:
    # 🔀 Randomly assign role
    role = random.choice(['Player 1', 'Player 2'])
    st.success(f"🎲 You have been randomly assigned as **{role}**")

    # Proceed to game only when role is shown
    st.subheader("🔵 Period 1")
    if role == 'Player 1':
        p1_move_1 = st.selectbox("Your move (A or B):", options=["A", "B"])
        p2_move_1 = st.selectbox("Opponent move (X, Y, Z):", options=["X", "Y", "Z"])
    else:
        p1_move_1 = st.selectbox("Opponent move (A or B):", options=["A", "B"])
        p2_move_1 = st.selectbox("Your move (X, Y, Z):", options=["X", "Y", "Z"])

    if st.button("▶ Play Period 1"):
        payoff1 = game_matrix[(p1_move_1, p2_move_1)]
        st.success(f"🎯 Period 1 Outcome: P1 = {p1_move_1}, P2 = {p2_move_1} → Payoffs = {payoff1}")

        st.subheader("🟢 Period 2")
        if role == 'Player 1':
            p1_move_2 = st.selectbox("Your move (A or B):", options=["A", "B"], key="p1_2")
            p2_move_2 = st.selectbox("Opponent move (X, Y, Z):", options=["X", "Y", "Z"], key="p2_2")
        else:
            p1_move_2 = st.selectbox("Opponent move (A or B):", options=["A", "B"], key="p1_2")
            p2_move_2 = st.selectbox("Your move (X, Y, Z):", options=["X", "Y", "Z"], key="p2_2")

        if st.button("▶ Play Period 2"):
            payoff2 = game_matrix[(p1_move_2, p2_move_2)]
            total_p1 = payoff1[0] + payoff2[0]
            total_p2 = payoff1[1] + payoff2[1]

            st.success(f"🎮 Period 2 Outcome: P1 = {p1_move_2}, P2 = {p2_move_2} → Payoffs = {payoff2}")
            st.markdown(f"### 🏁 Final Total Payoffs")
            st.markdown(f"- **Player 1:** {payoff1[0]} + {payoff2[0]} = {total_p1}")
            st.markdown(f"- **Player 2:** {payoff1[1]} + {payoff2[1]} = {total_p2}")

            # Bar plot
            labels = ["P1-T1", "P2-T1", "P1-T2", "P2-T2"]
            values = [payoff1[0], payoff1[1], payoff2[0], payoff2[1]]
            colors = ['blue', 'orange', 'blue', 'orange']

            fig, ax = plt.subplots()
            bars = ax.bar(labels, values, color=colors)
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + 0.2, f'{height}', ha='center')
            ax.set_ylim(0, max(values) + 2)
            ax.set_ylabel("Payoff")
            ax.set_title("Payoffs per Period")
            st.pyplot(fig)
