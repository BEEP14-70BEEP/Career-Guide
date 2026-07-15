import streamlit as st
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. Page Configuration & UI Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FuturePath AI - Career Guide",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 FuturePath AI")
st.subheader("Your All-in-One Global Career & College Counselor")
st.caption("Enter your subjects, core interests, or dream industries to map out your national and international career options.")

# -----------------------------------------------------------------------------
# 2. API Key Authentication
# -----------------------------------------------------------------------------
# Check for API key in Streamlit secrets or sidebar
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

if not api_key:
    st.info("Please add your Gemini API Key in the sidebar to get started.", icon="🔑")
    st.stop()

# Initialize the Gemini Client
client = genai.Client(api_key=api_key)

# -----------------------------------------------------------------------------
# 3. Chatbot System Instructions (The Secret Sauce)
# -----------------------------------------------------------------------------
SYSTEM_INSTRUCTION = """
You are "FuturePath AI", an empathetic, elite, and highly knowledgeable career guidance counselor. 
Your goal is to help students and professionals discover their ideal career paths based on their subjects, skills, or core interests.

When a user provides their subjects or core interests, your response must be structured, clear, and comprehensive. Cover both National and International horizons.

For the career paths you suggest, aim to provide:
1. 🌟 Career Overview: What the field is and why it's growing.
2. 🗺️ Global Options: Distinct pathways for both Domestic/National and International (US, UK, Europe, Asia, etc.) contexts.
3. 🏛️ Elite Academic Institutions:
   - Top National Colleges/Academies (with specific entrance exams if applicable).
   - Top International Universities/Institutes (mention required exams like SAT, GRE, IELTS/TOEFL if relevant).
4. 📈 Growth & Salary Outlook: A quick reality check on job prospects globally.
5. 🚀 Actionable Next Steps: What they should do right now (internships, projects, certifications).

Tone: Supportive, insightful, direct, and highly encouraging. Use markdown tables, bold text, and bullet points to ensure the advice is easy to read.
"""

# -----------------------------------------------------------------------------
# 4. Session State & Chat History Management
# -----------------------------------------------------------------------------
# Initialize the chat session if it doesn't exist
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7,
        )
    )

# Initialize locally displayed message history for Streamlit UI
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Career Guide. Tell me about your favorite subjects, your core strengths, or a field you are curious about (e.g., 'I took Physics, Math, and Art' or 'What can I do in Biotech internationally?')."}
    ]

# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------------------------------------------------------
# 5. Handling User Input and Generating Responses
# -----------------------------------------------------------------------------
if user_prompt := st.chat_input("Ask about careers, colleges, exams, or industries..."):
    
    # Display user message immediately
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Generate response from Gemini using the ongoing chat session
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Send message to the persistent chat object
            response = st.session_state.chat.send_message(user_prompt)
            
            # Display response
            message_placeholder.markdown(response.text)
            
            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
