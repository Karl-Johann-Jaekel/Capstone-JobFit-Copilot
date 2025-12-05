import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

fn_sql = """
create or replace function match_documents (
  query_embedding vector(768),
  match_count int default 10
)
returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    j.id,
    j.content,
    j.metadata,
    1 - (j.embedding <=> query_embedding) as similarity
  from job_chunks_python j
  order by j.embedding <=> query_embedding
  limit match_count;
end;
$$;
"""

endpoint = f"{SUPABASE_URL}/rest/v1/rpc/execute"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.pgrst.object+json"
}

payload = {
    "query": fn_sql
}

print("⏳ Uploading match_documents function...")
res = requests.post(endpoint, json=payload, headers=headers)

print("🔍 Status:", res.status_code)
print("🔎 Response:", res.text)
