"""Streamlit chat app — run with: uv run streamlit run streamlit_app.py"""

import streamlit as st

from example import chat_once

st.title("Claude Chat")
st.caption("Powered by claude-haiku-4-5-20251001 · folder 12")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Message…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            reply = chat_once(prompt, history=st.session_state.messages[:-1])
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
