import streamlit as st
import requests
import json
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Ultra Stable Idea Vault", page_icon="💡")

if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("Add OPENROUTER_API_KEY in Streamlit Secrets!")
    st.stop()

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

def get_roadmap(idea):
    url = "https://openrouter.api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:8501", # Required by some OpenRouter models
        "X-Title": "Idea Vault App"
    }
    
    # These are the CURRENT working Free IDs on OpenRouter
    models_to_try = [
        "google/gemini-2.0-flash-001:free",
        "google/gemini-2.0-pro-exp-02-05:free",
        "deepseek/deepseek-r1:free",
        "qwen/qwen-2.5-72b-instruct:free",
        "microsoft/phi-3-medium-128k-instruct:free"
    ]
    
    last_error = ""
    
    for model in models_to_try:
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": f"Create a short business roadmap for this idea in Hinglish: {idea}"}
            ],
            "max_tokens": 800  # Low token count prevents 'credit' errors
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
            res_json = response.json()
            
            if response.status_code == 200:
                return res_json['choices'][0]['message']['content'], model
            else:
                last_error = f"{model}: {res_json.get('error', {}).get('message', 'Unknown error')}"
                continue 
        except Exception as e:
            last_error = str(e)
            continue
            
    st.error(f"All free models are currently busy or IDs changed. \n\nLast Log: {last_error}")
    return None, None

# --- UI ---
st.title("💡 Personal Idea Vault")
st.write("Generating roadmaps using OpenRouter Free Tier.")

idea_input = st.text_area("Your Idea:", placeholder="Write your thought here...", height=100)

if st.button("Generate Strategy"):
    if idea_input:
        with st.spinner("Searching for a free AI model..."):
            roadmap, used_model = get_roadmap(idea_input)
            if roadmap:
                st.success(f"Generated using: {used_model}")
                st.markdown("---")
                st.markdown(roadmap)
                
                st.download_button("📥 Save Roadmap", roadmap, file_name="idea.txt")
    else:
        st.error("Please enter your idea first.")

st.divider()
st.info("Tip: If it fails, wait 30 seconds and try again. Free models have strict rate limits.")
