import streamlit as st
import requests
import json
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Idea Vault", page_icon="💡")

# Ensure API Key is present in Streamlit Secrets
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("Please add OPENROUTER_API_KEY to your Streamlit Secrets!")
    st.stop()

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

def get_roadmap_from_openrouter(idea):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "google/gemini-2.5-flash", # You can also change this to "meta-llama/llama-3.3-70b-instruct" if you want
        "messages": [
            {
                "role": "user", 
                "content": f"Provide a practical business roadmap for this idea in Hinglish (Hindi + English): {idea}"
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        st.error(f"Error from OpenRouter: {response.text}")
        return None

# --- UI ---
st.title("💡 Personal Idea Vault (Powered by OpenRouter)")
st.write("No more Google Cloud headaches. Just type your idea below.")

idea_text = st.text_area("What is your business idea?", placeholder="Type here...", height=150)

if st.button("Generate Strategy"):
    if idea_text:
        with st.spinner("AI is working on your roadmap..."):
            roadmap = get_roadmap_from_openrouter(idea_text)
            
            if roadmap:
                st.subheader("Your AI Roadmap")
                st.markdown(roadmap)
                
                # Download locally
                st.download_button(
                    label="📥 Save Idea to My Computer",
                    data=f"IDEA:\n{idea_text}\n\nROADMAP:\n{roadmap}",
                    file_name="my_idea_roadmap.txt",
                    mime="text/plain"
                )
    else:
        st.error("Please enter an idea first.")

st.divider()
st.caption("Simple setup. No logs kept. Download your ideas directly.")
