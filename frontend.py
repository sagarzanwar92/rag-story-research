import streamlit as st
import requests

st.set_page_config(page_title="Story Researcher", page_icon="📖")
st.title("📖 AI Story Researcher")
st.markdown("Query the database with full chat context.")



# Sidebar Status
st.sidebar.header("Backend Status")
try:
    requests.get("http://localhost:8000/docs", timeout=2)
    st.sidebar.success("✅ Backend Online")
except:
    st.sidebar.error("❌ Backend Offline")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask about the document..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    
    # Call the API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                api_url = "http://localhost:8000/ask"
                # Pass the prompt AND the current history
                payload = {
                    "prompt": prompt,
                    "history": st.session_state.messages 
                }
                
                response = requests.post(api_url, json=payload)
                response.raise_for_status()
                
                answer = response.json()["answer"]
                st.markdown(answer)
                
                # Update session state AFTER successful response
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"API Error: {e}")