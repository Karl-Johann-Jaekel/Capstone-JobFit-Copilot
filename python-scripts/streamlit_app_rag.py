import streamlit as st
import base64

# 👉 Import our local RAG function
from rag_module import run_rag


# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="JobFit Copilot", page_icon="💼")


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
st.write("Chat with your Career-Coach AI powered by Supabase + Groq (local).")

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

    with st.chat_message("user"):  # show in UI
        st.write(user_text)

    # 👇 NEW: Call Python RAG function directly!
    try:
        rag_reply = run_rag(user_text)
    except Exception as e:
        rag_reply = f"⚠️ RAG Error: {e}"

    # Show AI assistant reply
    with st.chat_message("assistant"):
        st.write(rag_reply)

    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": rag_reply})
