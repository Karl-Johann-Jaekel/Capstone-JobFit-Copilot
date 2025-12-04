import streamlit as st
import requests
import base64
import json

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="JobFit Copilot", page_icon="💼")

WEBHOOK_URL = "https://n8n.n8npress.website/webhook/cc9a93ba-c055-4f17-ba25-0a44fa32fbaa" 

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []     # chat history

if "cv_base64" not in st.session_state:
    st.session_state.cv_base64 = None  # uploaded CV content


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🔧 JobFit Copilot Settings")

location = st.sidebar.text_input("Location")
job_title = st.sidebar.text_input("Job Title")
notes = st.sidebar.text_area("Additional Notes")

# File upload (CV PDF or TXT)
uploaded_cv = st.sidebar.file_uploader("Upload your CV (PDF or TXT)", type=["pdf", "txt"])

if uploaded_cv:
    st.sidebar.success("CV uploaded!")
    st.session_state.cv_base64 = base64.b64encode(uploaded_cv.read()).decode("utf-8")


# ---------------------------------------------------------
# MAIN CHAT INTERFACE
# ---------------------------------------------------------
st.title("JobFit Copilot 💼")
st.write("Chat with Career-Coach AI powered by n8n & Supabase.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ---------------------------------------------------------
# HANDLE USER MESSAGE
# ---------------------------------------------------------
user_text = st.chat_input("Write your message...")

if user_text:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("user"):
        st.write(user_text)

    # Build n8n payload
    payload = {
        "message": user_text,
        "profile": {
            "location": location,
            "job_title": job_title,
            "notes": notes,
        },
        "cv_base64": st.session_state.cv_base64,
        "history": st.session_state.messages,   # full chat history
    }

    # Send to n8n webhook
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=30)
        n8n_reply = response.json().get("reply", "(empty response)")

    except Exception as e:
        n8n_reply = f"⚠️ Error contacting webhook: {e}"

    # Show AI assistant reply
    with st.chat_message("assistant"):
        st.write(n8n_reply)

    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": n8n_reply})