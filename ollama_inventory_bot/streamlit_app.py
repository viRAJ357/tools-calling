import streamlit as st
import base64
import os

# 1. FUNCTION TO SET BACKGROUND
def set_bg(image_path):
    """
    Encodes a local image to base64 and injects it as a CSS background.
    """
    if not os.path.exists(image_path):
        # Improved error message to help you debug paths
        st.error(f"❌ File not found at: {os.path.abspath(image_path)}")
        return

    # Determine the extension to set the correct MIME type
    ext = image_path.split('.')[-1].lower()
    mime_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"

    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:{mime_type};base64,{encoded}");
            background-attachment: fixed;
            background-size: cover;
        }}
        /* Semi-transparent overlay to make text readable */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.6);
            z-index: -1;
        }}
        .stChatMessage {{
            background-color: rgba(30, 30, 30, 0.9) !important;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 2. APP CONFIGURATION
st.set_page_config(page_title="Ollama Inventory Bot", layout="wide")

# IMPORTANT: This matches the filename exactly from your VS Code screenshot
# If you rename the file to 'background.jpg', change this string!
target_image = "assets/WhatsApp Image 2026-01-22 at 4.36.48 PM.jpeg"
set_bg(target_image)

# 3. HEADER
st.title("🤖 Ollama Inventory Assistant")
st.info("I can help you check stock levels and manage inventory via Ollama.")
st.markdown("---")

# 4. CHAT INTERFACE INITIALIZATION
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. CHAT INPUT LOGIC
if prompt := st.chat_input("Ask about inventory (e.g., 'How many laptops are in stock?')"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # --- INTEGRATION POINT ---
            # This is where you will call your functions from tools.py
            # Example: response = my_tools.query_ollama(prompt)
            full_response = f"I've received your query: '{prompt}'. [Link your tools.py here to get real inventory data]"
            
            st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})