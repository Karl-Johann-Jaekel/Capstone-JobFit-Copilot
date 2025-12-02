from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> np.ndarray:
    return model.encode(texts, show_progress_bar=True)

# aus DB holen:
rows = supabase.table("jobs").select("*").execute().data
texts = [r["text_for_embedding"] for r in rows]
embs = embed_texts(texts)

# in job_embeddings-Tabelle schreiben (content + metadata + embedding)
payload = []
for row, emb in zip(rows, embs):
    payload.append({
        "job_id": row["id"],
        "content": row["text_for_embedding"],
        "metadata": {
            "title": row["title"],
            "company_name": row["company_name"],
            "location": row["location"],
            "source": row["source"],
        },
        "embedding": emb.tolist(),   # Supabase pgvector erwartet Array
    })

supabase.table("job_embeddings").insert(payload).execute()


