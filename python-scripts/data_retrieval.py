
import langchain
print("🔎 LangChain version:", langchain.__version__)
# --- Core Types ---
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

# --- Vectorstore ---
from langchain_community.vectorstores import SupabaseVectorStore

# --- Embeddings (Google Gemini) ---
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# --- RAG Chains (LangChain 0.3.x API) ---
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# --- LLM (Groq) ---
from langchain_groq import ChatGroq

# --- Supabase ---
from supabase import create_client, Client

# --- Misc ---
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ------------------------------------------------------------------------------
# 1. Supabase Client
# ------------------------------------------------------------------------------
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

# ------------------------------------------------------------------------------
# 2. Embeddings (Google Gemini text-embedding-004)
#    → Uses the same high-quality embedding model as n8n (dimension: 768)
# ------------------------------------------------------------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=GOOGLE_API_KEY
)

# ------------------------------------------------------------------------------
# 3. Vector Store Retriever
# ------------------------------------------------------------------------------
vector_store = SupabaseVectorStore(
    client=supabase,
    table_name="job_chunks",   # the table created by n8n
    embedding=embeddings,
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# ------------------------------------------------------------------------------
# 4. LLM (Groq)
# ------------------------------------------------------------------------------
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0
)

# ------------------------------------------------------------------------------
# 5. Prompt Template
# ------------------------------------------------------------------------------
prompt = PromptTemplate.from_template("""
You are a job-matching assistant. Use the following job descriptions
to answer the user's question.

Context:
{context}

Question: {input}

Answer:
""")

# ------------------------------------------------------------------------------
# 6. RAG Chain (latest LangChain 0.3.x syntax)
# ------------------------------------------------------------------------------
#print("🔎 LangChain version:", langchain.__version__)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# 2) Retrieval chain
document_chain = create_stuff_documents_chain(
    llm,          # pass positionally
    prompt        # pass positionally
)

rag_chain = create_retrieval_chain(
    retriever,        # first arg: retriever
    document_chain    # second arg: combine_docs_chain
)

# 3) Ask question
query = "Find me remote Python developer jobs"
result = rag_chain.invoke({"input": query})
print(result["answer"])