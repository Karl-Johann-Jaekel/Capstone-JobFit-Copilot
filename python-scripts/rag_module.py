#🔎 LangChain version: 1.1.1
#🔎 Supabase version: 2.4.3
#Langchain Community: 0.2.14
#Langchain Groq: 1.1.0
# rag_module.py  (RAG backend module)

from dotenv import load_dotenv
import os

# --- Load environment variables ---
load_dotenv()

# --- Vector store & DB ---
from supabase import create_client, Client
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

# --- LLM ---
from langchain_groq import ChatGroq

# --- LangChain Core ---
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ------------------------------------------------------
# 1) Init Supabase + Embeddings + VectorStore (global)
# ------------------------------------------------------
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

vector_store = SupabaseVectorStore(
    client=supabase,
    table_name="job_chunks_python",
    query_name="match_documents",
    embedding=embeddings,
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})


# ------------------------------------------------------
# 2) Init LLM (Groq)
# ------------------------------------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY")  # explicit key is ok
)


# ------------------------------------------------------
# 3) Reusable Function: run RAG Query
# ------------------------------------------------------
def run_rag(query: str) -> str:
    """Return an answer using Supabase + HuggingFace + Groq."""

    # Retrieve docs
    docs = retriever.invoke(query)
    context = "\n\n".join([d.page_content for d in docs])

    # --- Prompt ---
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are JobFit Copilot, an expert career assistant.\n"
            "Use ONLY the job data from the context below to answer.\n"
            "If the context does not contain an answer, say:\n"
            "'No matching jobs found in the current database.'\n\n"
            "💼 **Question:** {question}\n\n"
            "📄 **Job Data:**\n{context}\n\n"
            "✍️ **Answer Requirements:**\n"
            "- List 2–5 matching jobs if available (title, company, location, URL)\n"
            "- Be short and helpful (max 6 lines)\n"
            "- Do NOT hallucinate or add new companies\n"
            "- Answer in the same language as the question.\n\n"
            "🎯 **Your Answer:**"
        )    
    )

    # Build final prompt to LLM
    final_input = prompt.format(
        context=context,
        question=query
    )

    # Run through the model + parse text
    result = llm.invoke(final_input)
    return StrOutputParser().invoke(result)


# ------------------------------------------------------
# 4) Optional Test (runs ONLY if file executed directly)
# ------------------------------------------------------
if __name__ == "__main__":
    print("🧪 Test RAG:", run_rag("Please find a remote job"))

