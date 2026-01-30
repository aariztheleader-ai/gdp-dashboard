import streamlit as st
from openai import OpenAI

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Jarvis",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Jarvis")
st.caption("Your personal cloud AI assistant")

# ---------- LOAD API KEY ----------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not found. Please add it in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------- MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Jarvis, a smart, polite, loyal personal assistant."}
    ]

# ---------- CHAT HISTORY ----------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- USER INPUT ----------
user_input = st.chat_input("Talk to Jarvis...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
