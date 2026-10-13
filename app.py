"""
app.py — Streamlit Web UI for the Nutrition Agentic AI Application
Run: streamlit run app.py
"""

import streamlit as st
from agent import build_agent

# ── Page config ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nutrition AI Agent",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Sidebar ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🥗 Nutrition AI Agent")
    st.markdown("Powered by **IBM WatsonX AI** via **IBM Bob**")
    st.divider()
    st.markdown("### 💡 Try asking:")
    st.markdown(
        """
- What are the macros in 100g of chicken breast?
- Plan a 1800 calorie vegetarian week
- I'm diabetic — what should I eat?
- Calculate my daily calories (70 kg, 175 cm, 28 y/o, male, moderately active)
- Suggest a keto meal plan for weight loss
- What vegan foods are high in iron?
        """
    )
    st.divider()
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# ── Session state ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    with st.spinner("Loading Nutrition AI Agent…"):
        st.session_state.agent = build_agent()

# ── Chat header ──────────────────────────────────────────────────────────────────
st.title("🥗 Nutrition Agentic AI")
st.caption("Ask me anything about nutrition, meal planning, or calorie calculations.")

# ── Render existing messages ─────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Handle new input ─────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask your nutrition question…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                result = st.session_state.agent.invoke({"input": prompt})
                response = result.get("output", "I could not generate a response. Please try again.")
            except Exception as e:
                response = f"⚠️ Error: {str(e)}\n\nPlease check your WatsonX credentials in `.env`."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
