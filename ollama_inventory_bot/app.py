import streamlit as st
import ollama
import base64
from tools import tools_metadata, available_functions

# --- BACKGROUND CONFIGURATION ---
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string.decode()}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        /* Make chat messages semi-transparent so you can see your face */
        [data-testid="stChatMessage"] {{
            background-color: rgba(30, 30, 30, 0.8) !important;
            color: white !important;
            border-radius: 15px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Use the exact path shown in your VS Code 'assets' folder
try:
    add_bg_from_local('assets/WhatsApp Image 2026-01-22 at 4.36.48 PM.jpeg')
except FileNotFoundError:
    st.error("Image not found! Please check the filename in assets folder.")

# --- CHAT INTERFACE ---
st.title("🤖 Ollama Inventory Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    if message["role"] != "tool": 
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How many Macbooks are left?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        # 1. First call to Ollama with tools enabled
        response = ollama.chat(
            model='llama3.1',
            messages=st.session_state.messages,
            tools=tools_metadata
        )

        # 2. Check if AI wants to use a Python tool
        if response['message'].get('tool_calls'):
            for tool in response['message']['tool_calls']:
                func_name = tool['function']['name']
                args = tool['function']['arguments']
                
                # Execute the real Python function
                result = available_functions[func_name](**args)
                
                # Feed the data back to the AI
                st.session_state.messages.append(response['message'])
                st.session_state.messages.append({
                    "role": "tool",
                    "content": str(result),
                    "name": func_name
                })
            
            # 3. Final call so AI can explain the result
            final_res = ollama.chat(model='llama3.1', messages=st.session_state.messages)
            bot_text = final_res['message']['content']
        else:
            bot_text = response['message']['content']

        st.markdown(bot_text)
        st.session_state.messages.append({"role": "assistant", "content": bot_text})