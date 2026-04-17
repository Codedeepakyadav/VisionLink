import streamlit as st
import requests
import json
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Free Idea Vault", page_icon="💡")

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
    
    # We use a :free model and set max_tokens to stay under credit limits
    payload = {
        "model": "google/gemini-2.0-flash-exp:free", 
        "messages": [
            {
                "role": "user", 
                "content": f"Provide a practical business roadmap for this idea in Hinglish: {idea}"
            }
        ],
        "max_tokens": 1000  # This limits the response length so it stays FREE
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['choices'][0]['message']['content']
        else:
            # Check for specific error messages
            error_msg = res_json.get('error', {}).get('message', 'Unknown Error')
            st.error(f"API Error: {error_msg}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# --- UI ---
st.title("💡 Free Idea Vault AI")
st.write("Using OpenRouter Free Models - No Credits Required.")

idea_text = st.text_area("What is your idea?", placeholder="Type here...", height=150)

if st.button("Generate Strategy"):
    if idea_text:
        with st.spinner("AI is thinking..."):
            roadmap = get_roadmap(idea_text)
            
            if roadmap:
                st.subheader("Your AI Roadmap")
                st.markdown(roadmap)
                
                # Simple Download
                st.download_button(
                    label="📥 Save to My Device",
                    data=f"IDEA: {idea_text}\n\nSTRATEGY:\n{roadmap}",
                    file_name="business_roadmap.txt"
                )
    else:
        st.error("Please enter an idea.")

st.divider()
st.caption("Model: Gemini 2.0 Flash (Free version)")
