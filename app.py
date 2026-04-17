import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Setup Gemini
# In Streamlit Cloud, add GEMINI_API_KEY to Settings -> Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Simple Idea Vault", page_icon="💡")

st.title("💡 Simple Idea Vault")
st.write("Enter your idea, get an AI roadmap, and download it instantly.")

# 2. User Input
idea_text = st.text_area("What's your idea?", placeholder="e.g. A coffee shop for coders...", height=150)

if st.button("Generate Roadmap"):
    if idea_text:
        with st.spinner("AI is thinking..."):
            # Call Gemini
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Provide a business roadmap for this idea in Hinglish: {idea_text}"
            response = model.generate_content(prompt)
            roadmap = response.text
            
            # Display Result
            st.subheader("Your AI Roadmap")
            st.markdown(roadmap)
            
            # 3. Simple Save (Download to your PC)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            st.download_button(
                label="📥 Download & Save Idea",
                data=f"IDEA:\n{idea_text}\n\nROADMAP:\n{roadmap}",
                file_name=f"idea_{timestamp}.txt",
                mime="text/plain"
            )
    else:
        st.error("Please type something first!")

st.divider()
st.caption("No databases. No logs. Just you and the AI.")
