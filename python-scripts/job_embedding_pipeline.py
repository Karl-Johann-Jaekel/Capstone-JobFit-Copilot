import os
import requests
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client

load_dotenv()

# ---------------------------------------------------------------
# Supabase
# ---------------------------------------------------------------
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# ---------------------------------------------------------------
# Embedding model (LangChain HF embedding wrapper)
# You can replace this with the model from your notebook
# ---------------------------------------------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
# all-mpnet-base-v2 → 768 dims


# ---------------------------------------------------------------
# Chunker
# ---------------------------------------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=200
)


# ---------------------------------------------------------------
# Fetch Arbeitnow jobs
# ---------------------------------------------------------------
def fetch_jobs(page=1):
    url = f"https://www.arbeitnow.com/api/job-board-api?page={page}"
    print("Fetching:", url)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


# ---------------------------------------------------------------
# Convert job into a plain text string
# ---------------------------------------------------------------
def job_to_text(job):
    fields = [
        f"Title: {job.get('title','')}",
        f"Company: {job.get('company_name','')}",
        f"Location: {job.get('location','')}",
        "Description:\n" + (job.get('description') or "")
    ]
    return "\n\n".join(fields)


# ---------------------------------------------------------------
# Vector store
# ---------------------------------------------------------------
vector_store = SupabaseVectorStore(
    client=supabase,
    table_name="job_chunks_python",
    embedding=embedding_model
)


# ---------------------------------------------------------------
# Ingest pipeline
# ---------------------------------------------------------------
def ingest_jobs(max_pages=5):
    for page in range(1, max_pages + 1):
        data = fetch_jobs(page)
        if not data or "data" not in data:
            print("No more pages or error")
            break

        for job in data["data"]:
            text = job_to_text(job)

            # split into chunks
            chunks = splitter.split_text(text)

            metadata = {
                "job_id": job.get("slug"),
                "url": job.get("url"),
                "company": job.get("company_name"),
                "location": job.get("location"),
            }

            # Insert into Supabase
            vector_store.add_texts(
                texts=chunks,
                metadatas=[metadata] * len(chunks)
            )

        # Stop if API has no more pages
        if not data.get("links", {}).get("next"):
            break


if __name__ == "__main__":
    ingest_jobs(max_pages=20)
    print("Finished inserting embeddings into Supabase!")



