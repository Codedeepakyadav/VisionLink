import streamlit as st
import requests
import json
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Stable Idea Vault", page_icon="💡")

if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("Please add OPENROUTER_API_KEY to your Streamlit Secrets!")
    st.stop()

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

def get_roadmap(idea):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # List of FREE models to try in order (if one fails, it tries the next)
    models_to_try = [
        "google/gemini-2.0-flash-lite-preview-02-05:free",
        "deepseek/deepseek-r1:free",
        "google/gemini-2.0-flash-exp:free"
    ]
    
    last_error = ""
    
    for model in models_to_try:
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": f"Provide a practical business roadmap for this idea in Hinglish (Hindi+English): {idea}"}
            ],
            "max_tokens": 1000 # Keep it low so it stays free
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            res_json = response.json()
            
            if response.status_code == 200:
                return res_json['choices'][0]['message']['content']
            else:
                last_error = res_json.get('error', {}).get('message', 'Unknown error')
                continue # Try the next model
        except Exception as e:
            last_error = str(e)
            continue
            
    st.error(f"All free models failed. Last Error: {last_error}")
    return None

# --- UI ---
st.title("💡 Personal Idea Vault")
st.write("Using OpenRouter Free models with auto-fallback.")

idea_input = st.text_area("What's the idea?", placeholder="Type here...", height=150)

if st.button("Generate Strategy"):
    if idea_input:
        with st.spinner("AI is brainstorming (trying free models)..."):
            roadmap = get_roadmap(idea_input)
            if roadmap:
                st.subheader("Your AI Roadmap")
                st.markdown(roadmap)
                
                st.download_button(
                    label="📥 Save to My Device",
                    data=f"IDEA: {idea_input}\n\nSTRATEGY:\n{roadmap}",
                    file_name="roadmap.txt"
                )
    else:
        st.error("Enter something first!")

st.divider()
st.caption("Auto-switches between Gemini and DeepSeek free models.")
