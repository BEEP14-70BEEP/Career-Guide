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
# 2. API Key & Client Authentication
# -----------------------------------------------------------------------------
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

if not api_key:
    st.info("Please add your Gemini API Key in the sidebar to get started.", icon="🔑")
    st.stop()

# Keep the client alive across user interface reruns by saving it to session state
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

# -----------------------------------------------------------------------------
# 3. Chatbot System Instructions
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
# 4. Sidebar Control: Clear Chat History Function
# -----------------------------------------------------------------------------
def reset_chat():
    if "chat" in st.session_state:
        del st.session_state.chat
    if "messages" in st.session_state:
        del st.session_state.messages

with st.sidebar:
    st.markdown("### Controls")
    st.button("🧹 Clear Chat History", on_click=reset_chat, use_container_width=True)
    st.markdown("---")
    st.caption("Clearing the history resets the AI's memory back to the initial welcoming state.")

# -----------------------------------------------------------------------------
# 5. Session State & Chat History Management
# -----------------------------------------------------------------------------
# Initializing using gemini-2.5-flash for maximum reliability and proper SDK routing
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
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
# 6. Suggested Prompts Feature
# -----------------------------------------------------------------------------
suggested_prompt = None

if len(st.session_state.messages) <= 1:
    st.markdown("### 💡 Quick Starters")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔬 I am in 12th (Physics, Chemistry, Math)", use_container_width=True):
            suggested_prompt = "I am in 12th grade studying Physics, Chemistry, and Mathematics. What national and international options do I have besides traditional Engineering?"
        if st.button("🎨 Creative Careers (Art + Tech)", use_container_width=True):
            suggested_prompt = "I love Design, Tech, and Psychology. What interdisciplinary career options explore these fields globally?"
            
    with col2:
        if st.button("📊 Commerce & Finance Pathways", use_container_width=True):
            suggested_prompt = "I am a commerce student interested in Investment Banking and Data Analytics. Tell me about top global colleges and exams."
        if st.button("🌿 Bio-Tech & Healthcare Outlook", use_container_width=True):
            suggested_prompt = "What are the emerging career options for someone with Biology and Computer Science backgrounds internationally?"

# -----------------------------------------------------------------------------
# 7. Handling User Input and Generating Responses
# -----------------------------------------------------------------------------
user_prompt = st.chat_input("Ask about careers, colleges, exams, or industries...")

if suggested_prompt:
    user_prompt = suggested_prompt

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            response = st.session_state.chat.send_message(user_prompt)
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            if "client" in st.session_state:
                del st.session_state.client
                del st.session_state.chat
