
# streamlit_app.py
import streamlit as st
import matplotlib.pyplot as plt

# Game matrix
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

# Game description
st.markdown("""
## Game Description

Two players interact over 2 periods (T=2), playing the following stage game in each period:

|       | X     | Y     | Z     |
|-------|-------|-------|-------|
| **A** | 4,3   | 0,0   | 1,4   |
| **B** | 0,0   | 2,1   | 0,0   |

In the 2nd period both players know what is played in the 1st period and can condition their action on the 1st period’s outcome.  
Suppose that players do not discount the 2nd period payoffs (discount rate = 0).
""")

# Player names
p1_name = st.text_input("👤 Player 1 name:")
p2_name = st.text_input("👤 Player 2 name:")

if p1_name and p2_name:
    st.subheader("🔵 Period 1 Decisions")
    col1, col2 = st.columns(2)
    with col1:
        p1_move_1 = st.selectbox("Player 1 chooses:", options=["A", "B"], key="p1_1")
    with col2:
        p2_move_1 = st.selectbox("Player 2 chooses:", options=["X", "Y", "Z"], key="p2_1")

    if st.button("▶ Play Period 1"):
        payoff1 = game_matrix[(p1_move_1, p2_move_1)]
        st.success(f"🎯 Period 1 Outcome: P1 = {p1_move_1}, P2 = {p2_move_1} → Payoffs = {payoff1}")

        st.subheader("🟢 Period 2 Decisions (after observing Period 1)")
        col3, col4 = st.columns(2)
        with col3:
            p1_move_2 = st.selectbox("Player 1 chooses:", options=["A", "B"], key="p1_2")
        with col4:
            p2_move_2 = st.selectbox("Player 2 chooses:", options=["X", "Y", "Z"], key="p2_2")

        if st.button("▶ Play Period 2"):
            payoff2 = game_matrix[(p1_move_2, p2_move_2)]
            total_p1 = payoff1[0] + payoff2[0]
            total_p2 = payoff1[1] + payoff2[1]

            st.success(f"🎮 Period 2 Outcome: P1 = {p1_move_2}, P2 = {p2_move_2} → Payoffs = {payoff2}")
            st.markdown("### 🏁 Final Total Payoffs")
            st.markdown(f"- **{p1_name} (Player 1):** {payoff1[0]} + {payoff2[0]} = {total_p1}")
            st.markdown(f"- **{p2_name} (Player 2):** {payoff1[1]} + {payoff2[1]} = {total_p2}")

            # Bar chart
            labels = ["P1-T1", "P2-T1", "P1-T2", "P2-T2"]
            values = [payoff1[0], payoff1[1], payoff2[0], payoff2[1]]
            colors = ['blue', 'orange', 'blue', 'orange']

            fig, ax = plt.subplots()
            bars = ax.bar(labels, values, color=colors)
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + 0.2, f'{yval}', ha='center')
            ax.set_ylim(0, max(values) + 2)
            ax.set_ylabel("Payoff")
            ax.set_title("Payoffs per Period")
            st.pyplot(fig)
