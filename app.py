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
    # FIXED URL: changed .api to .ai
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.io", 
        "X-Title": "Idea Vault App"
    }
    
    # Current active Free IDs on OpenRouter
    models_to_try = [
        "google/gemini-2.0-flash-001:free",
        "google/gemini-2.0-flash-lite-preview-02-05:free",
        "deepseek/deepseek-r1:free",
        "mistralai/mistral-7b-instruct:free"
    ]
    
    last_error = ""
    
    for model in models_to_try:
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": f"Create a practical business roadmap for this idea in Hinglish: {idea}"}
            ],
            "max_tokens": 1000 
        }
        
        try:
            # Set a timeout so it doesn't hang forever
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
            res_json = response.json()
            
            if response.status_code == 200:
                return res_json['choices'][0]['message']['content'], model
            else:
                last_error = f"{model}: {res_json.get('error', {}).get('message', 'Unknown error')}"
                continue 
        except Exception as e:
            last_error = f"Connection error on {model}: {str(e)}"
            continue
            
    st.error(f"Failed to get a response. \n\nDebug Info: {last_error}")
    return None, None

# --- UI ---
st.title("💡 Personal Idea Vault")
st.write("Using OpenRouter Free Tier (Hinglish Support)")

idea_input = st.text_area("What is your idea?", placeholder="E.g. Ek juice bar chain jo subscription model par chale...", height=150)

if st.button("Generate Strategy"):
    if idea_input:
        with st.spinner("AI is brainstorming..."):
            roadmap, used_model = get_roadmap(idea_input)
            if roadmap:
                st.success(f"Success! Model used: {used_model}")
                st.markdown("---")
                st.markdown(roadmap)
                
                st.download_button(
                    label="📥 Save to My Device",
                    data=f"IDEA: {idea_input}\n\nSTRATEGY:\n{roadmap}",
                    file_name="my_roadmap.txt"
                )
    else:
        st.error("Please enter your idea first.")

st.divider()
st.info("Note: Free models can sometimes be busy. If it fails, wait 10 seconds and try again.")
