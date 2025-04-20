import streamlit as st
import requests
import os
import json
from datetime import datetime

# Setup page configuration
st.set_page_config(
    page_title="StressLess Chatbot",
    page_icon="✨",
    layout="wide"
)

# Function to load environment variables
def load_api_key():
    return os.getenv("MISTRAL_API_KEY", "")

# Function to call Mistral AI API
def call_mistral_api(messages, api_key):
    url = "https://api.mistral.ai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "mistral-small-latest",  # Using the latest small model
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.7,  # Balanced between creativity and coherence
        "top_p": 0.9
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """You are StressLess, a compassionate and supportive AI assistant focused on helping users manage stress and anxiety.
        Your tone is calm, empathetic, and warm. You offer practical advice for stress relief based on evidence-based techniques like deep breathing,
        mindfulness, positive reframing, and gentle physical activity. You ask clarifying questions to better understand the user's situation.
        You avoid giving medical advice or diagnosing conditions. Instead, you encourage seeking professional help when appropriate.
        Focus on providing immediate, practical coping strategies rather than long-term solutions. Use a conversational, friendly tone that makes
        the user feel heard and supported. Start each conversation with a warm greeting and check-in about how they're feeling."""},
        {"role": "assistant", "content": "Hi there! I'm StressLess, your supportive companion for stressful moments. How are you feeling right now? I'm here to listen and help you find some calm."}
    ]

# Title and introduction
st.title("✨ StressLess: Your Stress Relief Companion")
st.markdown("""
    Share what's on your mind, and I'll be here to listen and offer support.
    I can suggest relaxation techniques, provide a different perspective, or simply be a compassionate ear.
""")

# API key handling
api_key = load_api_key()
if not api_key:
    st.warning("⚠️ Mistral AI API key not found. Please set the MISTRAL_API_KEY environment variable.")
    st.stop()

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't display system messages
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

# Process user input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate response with loading indicator
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        response = call_mistral_api(st.session_state.messages, api_key)
        
        if response and "choices" in response:
            assistant_response = response["choices"][0]["message"]["content"]
            # Update placeholder with response
            message_placeholder.markdown(assistant_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        else:
            message_placeholder.markdown("I'm having trouble connecting right now. Please try again later.")

# Add footer with credits
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888;">
    <small>Developed by Akanksha (12310107) and Muskan (12324757)</small>
</div>
""", unsafe_allow_html=True)

# Sidebar with stress relief tips
with st.sidebar:
    st.header("Quick Stress Relief Tips")
    
    with st.expander("Breathing Exercise"):
        st.markdown("""
        1. Inhale deeply through your nose for 4 counts
        2. Hold for 2 counts 
        3. Exhale slowly through your mouth for 6 counts
        4. Repeat 5 times
        """)
    
    with st.expander("5-4-3-2-1 Grounding Technique"):
        st.markdown("""
        Notice around you:
        - 5 things you can see
        - 4 things you can touch
        - 3 things you can hear
        - 2 things you can smell
        - 1 thing you can taste
        """)
    
    with st.expander("Quick Body Scan"):
        st.markdown("""
        Starting from your toes and moving up:
        1. Notice any tension in each body part
        2. Take a breath
        3. Consciously relax that area
        4. Move to the next part
        """)
    
    st.markdown("---")
    st.caption("Remember: This chatbot is not a substitute for professional mental health care. If you're experiencing severe distress, please contact a healthcare provider.")
    
    # Developer information
    st.markdown("---")
    st.subheader("Developed by:")
    st.markdown("""
    - **Akanksha** (Reg No: 12310107)
    - **Muskan** (Reg No: 12324757)
    """)
