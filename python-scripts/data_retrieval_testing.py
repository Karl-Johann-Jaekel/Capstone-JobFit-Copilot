#🔎 LangChain version: 1.1.1
#🔎 Supabase version: 2.4.3
#Langchain Community: 0.2.14
#Langchain Groq: 1.1.0


import langchain
#print("🔎 LangChain version:", langchain.__version__)
import supabase

print("🔎 Supabase version:",supabase.__version__)
import importlib.metadata as metadata
print("Langchain Community:", metadata.version("langchain-community"))
import langchain_groq
#print("Langchain Groq:", langchain_groq.__version__)
# --- Core Types ---
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

# --- Vectorstore ---
from langchain_community.vectorstores import SupabaseVectorStore

# --- Embeddings (Google Gemini) ---
#from langchain_google_genai import GoogleGenerativeAIEmbeddings

# --- RAG Chains (LangChain 0.3.x API) ---
#from langchain.chains.combine_documents import create_stuff_documents_chain
#from langchain.chains import create_retrieval_chain

# --- LLM (Groq) ---
from langchain_groq import ChatGroq

# --- Supabase ---
from supabase import create_client, Client

from langchain_huggingface import HuggingFaceEmbeddings

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

print("🔐 Using key:", supabase_key[:15] + "...")

supabase: Client = create_client(supabase_url, supabase_key)
print("🟢 Supabase client created!")
# ------------------------------------------------------------------------------
# 2. Embeddings (Google Gemini text-embedding-004)
#    → Uses the same high-quality embedding model as n8n (dimension: 768)
# ------------------------------------------------------------------------------
#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
#embeddings = GoogleGenerativeAIEmbeddings(
#    model="models/text-embedding-004",
#    google_api_key=GOOGLE_API_KEY
#)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)


# ------------------------------------------------------------------------------
# 3. Vector Store Retriever
# ------------------------------------------------------------------------------

vector_store = SupabaseVectorStore(
    client=supabase,
    table_name="job_chunks_python",
    query_name="match_documents",  # MUST MATCH
    embedding=embeddings,
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})
docs = retriever.invoke("test")
print(docs)
#retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# ------------------------------------------------------------------------------
# 4. LLM (Groq)
# ------------------------------------------------------------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",   # 🚀 currently best for reasoning + long context
    temperature=0.1
)

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Prompt ---
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful assistant for job search.\n"
        "Use the provided job postings to answer the question.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n"
        "Answer in a short, helpful way."
    ),
)

# --- Build RAG Pipeline ---
rag_chain = (
    retriever
    | (lambda docs: {"context": "\n\n".join([d.page_content for d in docs])})
    | (lambda d: {"context": d["context"], "question": query})
    | prompt
    | llm
    | StrOutputParser()
)

# --- Ask a question ---
query = ""
while query != "exit": 
    query = input(" Enter your question about the job postings: ")
    response = rag_chain.invoke(query)
    print("\n🧠 RAG Answer:\n", response)