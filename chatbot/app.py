# chatbot/app.py
import streamlit as st
import sys
import os
from datetime import datetime

# Add the current directory to path so we can import chatbot_core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from chatbot_core import get_response, patterns

# Page configuration
st.set_page_config(
    page_title="FitBot - Fitness Coach",
    page_icon="💪",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: #2193b0;
        color: white;
        text-align: right;
        margin-left: 20%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .bot-message {
        background: #034a5c;    
        color: white;
        text-align: left;
        margin-right: 20%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
        border-radius: 20px;
        padding: 10px 20px;
        border: 2px solid transparent;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 2px rgba(118, 75, 162, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        padding: 10px 30px;
        border: none;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/fitness.png", width=100)
    st.title("FitBot")
    st.markdown("---")
    st.markdown("### About")
    st.info(
        "Your personal AI fitness coach! Ask about:\n\n"
        "• Workout plans\n"
        "• Weight loss\n"
        "• Muscle gain\n"
        "• Nutrition\n"
        "• Recovery\n"
        "• Motivation"
    )
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main chat area
st.title("FitBot - Your Personal Fitness Coach")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey! I'm FitBot, your personal fitness coach. What fitness goal are you working towards today?"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-message user-message">'
            f'<b>🧑 You:</b> {msg["content"]}'
            f'<br><small>{datetime.now().strftime("%H:%M")}</small>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-message bot-message">'
            f'<b>🤖 FitBot:</b> {msg["content"]}'
            f'<br><small>{datetime.now().strftime("%H:%M")}</small>'
            f'</div>',
            unsafe_allow_html=True
        )

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    response = get_response(user_input)
    
    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update display
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<center><small>FitBot - NLP Assignment | Created with using Streamlit</small></center>",
    unsafe_allow_html=True
)