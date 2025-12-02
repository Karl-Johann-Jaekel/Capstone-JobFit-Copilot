# Import necessary libraries
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEndpoint
import warnings
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()
warnings.filterwarnings("ignore")

# Instantiate ChatGroq with llama
llm = ChatGroq(
    model= "llama3-70b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,)