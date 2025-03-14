import os
import openai
from supabase import create_client
from openai import OpenAI
import json

os.environ["SUPABASE_URL"]="https://qllafsgiqcgzzazvwfwr.supabase.co";
os.environ["SUPABASE_KEY"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFsbGFmc2dpcWNnenphenZ3ZndyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE4OTk4MjIsImV4cCI6MjA1NzQ3NTgyMn0.vLneDXWFjl2jT3EVFsABCqAeQJA0ZmeKPyVAlaCGvng" 

# Initialize clients
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
openai.api_key = s.getenv("OPENAI_API_KEY")
client = OpenAI()
# Function to generate embeddings
def generate_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-large"
    )
    return response.data[0].embedding

with open("profiles.json", "r") as f:
    profiles = json.load(f)

for profile in profiles:
    profile_text = f"{profile['name']}. Experience: {profile['work_experience']}. Skills: {profile['skills']}"
    embedding = generate_embedding(profile_text)

    response = supabase.table("candidates").insert({
        "name": profile["name"],
        "work_experience": profile["work_experience"],
        "skills": profile["skills"],
        "embedding": embedding
    }).execute()

    print(f"Inserted: {profile['name']}")