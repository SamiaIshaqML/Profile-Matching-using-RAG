import os
import streamlit as st
from supabase import create_client
import openai
from openai import OpenAI
import dotenv
from dotenv import load_dotenv

# environment variables'
SUPABASE_URL="https://qllafsgiqcgzzazvwfwr.supabase.co";
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFsbGFmc2dpcWNnenphenZ3ZndyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE4OTk4MjIsImV4cCI6MjA1NzQ3NTgyMn0.vLneDXWFjl2jT3EVFsABCqAeQJA0ZmeKPyVAlaCGvng" 
load_dotenv()
openai_api_key= os.getenv("OPENAI_API_KEY")

# Initialize supabaseclients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = OpenAI(api_key=openai_api_key)

st.title("🔍 Job Candidate Search Agent")
query_skills = st.text_input("Enter skills", "")
query_experience = st.text_input("Enter experience years", "")

def explanation_bot(candidates, query):
    reasoning_response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an AI recruiter explaining candidate matches. Make sure to explain why the candidate is a good fit for the query in 2-3 sentences only"},
                            {"role": "user", "content": f"Explain why these candidates match the query: {query}\n\n{candidates}"}
                        ]
                    )
    return reasoning_response.choices[0].message.content

if st.button("Search"):
    if query_skills or query_experience:
        with st.spinner("Fetching candidates..."):
            query_text =  query_skills + " " + query_experience + " years duration"
            query_embedding = client.embeddings.create(
                input=query_text,
                model="text-embedding-3-large"
            )
            query_embedding = query_embedding.data[0].embedding
            response = supabase.rpc("match_candidates", {"query_embedding": query_embedding}).execute()
            data = response.data
            if data:
                st.subheader("🧑‍💻 Matched Candidates")
                for candidate in data:
                    st.markdown(f"**{candidate['name']}**")
                    st.markdown(f"📌 *Similarity Score:* {candidate['similarity']}")
                    st.markdown(f"📌 *Skills:* {candidate['skills']}")
                    st.markdown(f"📝 *Experience:* {candidate['work_experience']}")
                    st.markdown(f"📝 *Reasoning:* {explanation_bot(candidate, query_text)}")
                    st.markdown("---")
            else:
                st.warning("No candidates found. Try a different query.")
    else:
        st.warning("Please enter skills and experience.")