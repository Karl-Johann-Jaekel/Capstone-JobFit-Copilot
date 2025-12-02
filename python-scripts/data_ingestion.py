import requests
import supabase
import dotenv
import langchain
import langchain_community
import langchain_huggingface
import langchain_groq
import warnings

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEndpoint
from langchain_groq import ChatGroq
from supabase import create_client


load_dotenv()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_arbeitnow_jobs(page=1, limit=10):
    url = f"https://www.arbeitnow.com/api/job-board-api?page={page}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()["data"][:limit]

def clean_job(raw):
    # JS-Logik in Python nachbauen
    # normField, strip_html, etc.
    ...
    return {
        "external_id": raw.get("slug") or raw.get("id") or raw.get("url", ""),
        "source": "arbeitnow",
        "title": title,
        "company_name": company,
        "location": location,
        "description": description,
        "tags": tags,
        "text_for_embedding": text_for_embedding,
        "url": raw.get("url", ""),
        "remote": bool(raw.get("remote")),
        "published_at": raw.get("published_at"),
    }

jobs_raw = fetch_arbeitnow_jobs()
jobs_clean = [clean_job(j) for j in jobs_raw]

supabase.table("jobs").insert(jobs_clean).execute()


