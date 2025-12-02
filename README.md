# Capstone Project: JobFit Copilot - AI-powered Matching of Applicants and Job Listings


JobFit Copilot is an end-to-end AI system that:
* Automatically collects job postings (APIs, scrapers)
* Cleans & normalizes job data
* Generates semantic embeddings using Gemini/OpenAI/HuggingFace
* Stores them in a Supabase Vector Database (pgvector)
* Retrieves the best matches via vector similarity search
* Provides personalized job recommendations based on:
    * User query
    * Skills
    * CV Text
    * Preferences (location, salary, remote, etc.)
* Exposes everything via an interactive Streamlit UI

This project combines Data Engineering + Machine Learning + NLP + RAG + Frontend UI into one production-style system.


## Requirements:

- pyenv with Python: 3.11.3

### Setup

Use the requirements file in this repo to create a new environment.

```BASH
make setup

#or

pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_dev.txt
```

The `requirements.txt` file contains the libraries needed for deployment.. of model or dashboard .. thus no jupyter or other libs used during development.


### Handling Merge Conflicts in Jupyter Notebooks

When working collaboratively, merge conflicts may occur in `.ipynb` files because notebooks are stored as JSON.  
To simplify resolving these conflicts, this project uses **nbdime** (already included in `requirements_dev.txt`).

#### Enable once
After setting up your environment, enable nbdime for Git:
```bash
nbdime config-git --enable
```

#### When a merge conflict occurs
Run the following command to open the merge tool:
```bash
nbdime mergetool
```
A browser window will open showing both notebook versions side by side.
Select the correct cells, save, and then complete the merge:
```bash
git add <notebook>.ipynb
git commit -m "Resolve notebook merge conflict"
```
That’s it — clean merges for notebooks!

# Capstone Project Outline — JobFit Copilot 
Problem Statement

* Job portals provide unstructured job postings (HTML, PDFs, text).
* Applicants rely on keyword searches, even though semantically relevant jobs may use different wording.
* Companies lose time through manual pre-screening.
* Many matching algorithms use rigid rules instead of true semantic understanding.

Objective:
Build an end-to-end system that:
1. Automatically crawls job postings (API or HTML scraping).
2. Stores job postings in structured form (Supabase).
3. Generates LLM embeddings (Google Gemini / OpenAI / HuggingFace).
4. Stores them in a vector database (Supabase pgvector).
5. Provides job–applicant matching via RAG.
6. Presents an interactive Streamlit UI where users can explore jobs or get personalized recommendations.