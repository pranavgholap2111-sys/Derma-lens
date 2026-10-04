import sys
import asyncio

# Place this at the very top of app.py
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import json
import requests
import streamlit as st
from google import genai
from google.genai import types

# ... continue with the rest of your imports

import json
import requests
import streamlit as st
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE, SUMMARY_REQUEST_PROMPT

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
MODEL_NAME = "gemini-3.8-flash"  


@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


gemini_client = get_gemini_client()


def send_telegram_message(chat_id: str, text: str):
    """Sends a message via the Telegram Bot HTTP API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text[:4000],  # Telegram max length per message is 4096 chars
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        if data.get("ok"):
            return True, "Success"
        return False, data.get("description", "Unknown error")
    except Exception as exc:
        return False, str(exc)


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.markdown(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])


def add_message(role, kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])


def ask_gemini(parts):
    try:
        response = st.session_state.chat.send_message(parts)
        return response.text
    except Exception as error:
        return f"Sorry, something went wrong with the AI analysis: {error}"


# Onboarding View
if "onboarded" not in st.session_state:
    st.title("🧴 DermaLens AI")
    st.caption("Scan cosmetic ingredients. Flag pore-cloggers & irritants. Send safety cards to Telegram.")
    with st.form("onboarding_form"):
        name = st.text_input("Your Name")
        telegram_chat_id = st.text_input(
            "Telegram Chat ID (Numeric)",
            placeholder="e.g. 123456789 (Get it from @userinfobot)",
        )
        submitted = st.form_submit_button("Start Scanning 🔍")

    if submitted:
        if not name.strip() or not telegram_chat_id.strip():
            st.warning("Please fill in both your name and your Telegram Chat ID.")
        else:
            st.session_state.name = name.strip()
            st.session_state.chat_id = telegram_chat_id.strip()
            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            st.session_state.messages = []
            st.session_state.onboarded = True
            st.rerun()
    st.stop()

# Main Workspace
header_col, button_col = st.columns([5, 2])
with header_col:
    st.title("🧴 DermaLens AI")

with button_col:
    send_disabled = False
    #len(st.session_state.messages) <= 1
    if st.button("✈️ Send to Telegram", disabled=send_disabled, use_container_width=True):
        with st.spinner("Generating skin safety summary..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
        success, info = send_telegram_message(st.session_state.chat_id, summary)
        if success:
            st.success("Sent! Check your Telegram chat 📱")
        else:
            st.error(f"Couldn't send to Telegram: {info}")

st.caption(f"Logged in as **{st.session_state.name}** | Telegram notifications routed to ID: `{st.session_state.chat_id}`")

if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)

user_input = st.chat_input(
    "Upload a clear picture of the INCI ingredient list or type product ingredients...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "webp"],
)

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))

    if text:
        add_message("user", "text", text)
        parts.append(text)
    elif photo is not None:
        parts.append(
            "Analyze this cosmetic product label. Extract the INCI ingredients list, detect comedogenic ratings, "
            "highlight irritants, and outline which skin types this is safe or risky for."
        )

    with st.spinner("Decoding ingredients & checking safety profiles..."):
        answer = ask_gemini(parts)
    add_message("assistant", "text", answer)