import streamlit as st
import google.generativeai as genai
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Idea Vault AI", page_icon="💡", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextArea textarea { font-size: 1.1rem !important; }
    .stButton button { background-color: #007bff; color: white; border-radius: 8px; border: none; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- CONNECTIONS ---
def init_connections():
    try:
        # 1. Setup Gemini
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # 2. Setup Google Sheets
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        # This pulls the dictionary directly from Streamlit Secrets
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        gs_client = gspread.authorize(creds)
        return gs_client
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# --- AI LOGIC ---
def get_ai_solution(idea):
    # Using gemini-1.5-flash (Better for Free Tier)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are a Strategic Business Consultant.
    The user has a new idea: "{idea}"
    
    Please provide a detailed roadmap in 'Hinglish' (Mix of Hindi and English).
    Format the output beautifully with the following sections:
    1. 📝 Executive Summary (Short overview)
    2. 🚀 Execution Steps (Phase 1, Phase 2, Phase 3)
    3. 🛠 Tech Stack & Tools (What to use)
    4. ⚠️ Challenges & Solutions (Risks to avoid)
    5. 💰 Monetization (How to make money)
    """
    response = model.generate_content(prompt)
    return response.text

# --- APP UI ---
def main():
    st.title("💡 Personal Idea Vault AI")
    st.markdown("##### Transform your raw thoughts into professional business roadmaps.")
    
    gs_client = init_connections()
    
    # Initialize Session State to keep results visible
    if 'solution' not in st.session_state:
        st.session_state.solution = ""

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("Your Idea")
        idea_input = st.text_area("Write or paste your idea here...", height=250, placeholder="Example: Ek app jo local farmers ko shehar ke restaurants se directly connect kare...")
        
        btn_generate = st.button("Analyze & Secure to Vault")

    with col2:
        st.subheader("Actionable Roadmap")
        
        if btn_generate:
            if not idea_input:
                st.warning("Please enter your idea first!")
            else:
                with st.spinner("AI is thinking..."):
                    # Generate Solution
                    solution = get_ai_solution(idea_input)
                    st.session_state.solution = solution
                    
                    # Save to Google Sheets
                    if gs_client:
                        try:
                            sheet = gs_client.open_by_key(st.secrets["SHEET_ID"]).sheet1
                            current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                            sheet.append_row([current_date, idea_input, solution])
                            st.success("✅ Idea & Strategy saved to Google Sheets!")
                        except Exception as e:
                            st.error(f"Failed to save to Sheets: {e}")

        # Display Solution if it exists in session
        if st.session_state.solution:
            st.markdown(st.session_state.solution)
            st.download_button(
                label="📥 Download as Text File",
                data=st.session_state.solution,
                file_name="my_business_idea.txt",
                mime="text/plain"
            )

    st.divider()
    st.info("Built with Gemini 1.5 Flash API. Your data is private and secured in your Google Sheet.")

if __name__ == "__main__":
    main()
