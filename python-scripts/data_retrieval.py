import os
from dotenv import load_dotenv

from langchain_community.vectorstores import SupabaseVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Same embedding model you used during ingestion
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

vector_store = SupabaseVectorStore(
    client=supabase,
    table_name="job_chunks",
    embedding=embeddings
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}   # how many chunks to retrieve
)
