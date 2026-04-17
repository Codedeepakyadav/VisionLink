import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Setup API Key
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Please add GEMINI_API_KEY to your Streamlit Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Simple Idea Vault", page_icon="💡")

st.title("💡 Simple Idea Vault")

idea_text = st.text_area("What's your idea?", placeholder="Type here...", height=150)

if st.button("Generate Roadmap"):
    if idea_text:
        with st.spinner("AI is thinking..."):
            try:
                # Use 'gemini-1.5-flash' - it's the most compatible
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Provide a business roadmap for this idea in Hinglish: {idea_text}"
                
                response = model.generate_content(prompt)
                
                # Check if response exists
                if response.text:
                    st.subheader("Your AI Roadmap")
                    st.markdown(response.text)
                    
                    # Download Button
                    st.download_button(
                        label="📥 Download & Save Idea",
                        data=f"IDEA:\n{idea_text}\n\nROADMAP:\n{response.text}",
                        file_name=f"roadmap_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                # This will tell you exactly what is wrong (Region, Key, or Model)
                st.error(f"AI Error: {e}")
    else:
        st.error("Please type something first!")
