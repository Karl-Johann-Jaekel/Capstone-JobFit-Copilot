# streamlit_app.py
import streamlit as st
from supabase import create_client
from sentence_transformers import SentenceTransformer
import numpy as np

# Setup
supabase = create_client("...", "...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

st.title("JobFit Copilot")

st.sidebar.header("Dein Profil")
skills = st.sidebar.text_area("Skills (kommagetrennt)")
location_pref = st.sidebar.text_input("Bevorzugter Standort")
remote_pref = st.sidebar.selectbox("Remote?", ["egal", "ja", "nein"])

query = st.text_input("Wonach suchst du? (z.B. 'Data Analyst Python in Stuttgart')")
if st.button("Passende Jobs finden") and query:
    # 1) Query-Embedding
    q_emb = model.encode([query])[0].tolist()

    # 2) RPC auf Supabase (ähnlich wie match_documents)
    res = supabase.rpc(
        "match_documents",
        {
            "query_embedding": q_emb,
            "match_count": 10,
            "filter": {}  # optional nach location/remote filtern
        }
    ).execute().data

    st.subheader("Empfohlene Jobs")
    for doc in res:
        meta = doc["metadata"]
        st.markdown(f"### {meta['title']} – {meta['company_name']}")
        st.write(meta.get("location", ""))
        st.write(doc["content"][:400] + "...")
        st.write("---")

