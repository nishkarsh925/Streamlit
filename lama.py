import streamlit as st
import requests
import json
import pandas as pd
import time  # Import time module for sleep

# Function to call GaiaNet API
def call_gaianet_api(user_input):
    url = 'https://llamatool.us.gaianet.network/v1/chat/completions'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    
    # API request body
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        "model": "llama"  # Your model name
    }

    # Sending the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Return the response from the AI
    if response.status_code == 200:
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', 'No response from the AI')
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit app
def main():
    st.title("💬 CyberSphere")
    st.caption("🚀 Your True Tech Navigator")

    # Initialize session state for messages if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you today?"}]

    # Sidebar options
    with st.sidebar:
        st.header("Options")
        app_mode = st.radio("Select an option:", ["New Chat", "Chat History"])
        
        if app_mode == "New Chat":
            # Reset messages for a new chat
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you today?"}]
            st.subheader("Start a new chat")
        
        elif app_mode == "Chat History":
            st.subheader("View chat history")
            # Display chat history if it exists
            if st.session_state["messages"]:
                for msg in st.session_state.messages:
                    st.write(f"{msg['role'].capitalize()}: {msg['content']}")
            else:
                st.write("No chat history available.")

        st.header("Upload File")
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt", "xlsx", "pdf"])

        if uploaded_file is not None:
            # Read and display the file based on its type
            file_type = uploaded_file.type
            file_content = ""

            if file_type == "text/csv":
                df = pd.read_csv(uploaded_file)
              
                file_content = df.to_string()  # Convert DataFrame to string for analysis

            elif file_type == "text/plain":
                file_content = uploaded_file.read().decode("utf-8")
             

            elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                df = pd.read_excel(uploaded_file)
              
                file_content = df.to_string()  # Convert DataFrame to string for analysis

            elif file_type == "application/pdf":
             
                # Placeholder for PDF text extraction
                file_content = "Uploaded PDF file needs text extraction to analyze."

            else:
                st.error("Unsupported file type")

            if file_content:  # If there's content to analyze
                analyze_button = st.button("Analyze Document")
                if analyze_button:
                    # Call the GaiaNet API with the file content
                    with st.spinner('Analyzing document...'):
                        time.sleep(1)  # Optional: simulate a delay for demonstration purposes
                        response = call_gaianet_api(file_content)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.chat_message("assistant").write(response)

    # Chat functionality
    if app_mode == "New Chat":
        # Display chat messages
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input():
            # Append user message to session state
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            # Call the GaiaNet API to get the response with a loading animation
            with st.spinner('Processing...'):
                time.sleep(1)  # Optional: simulate a delay for demonstration purposes
                response = call_gaianet_api(prompt)

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

if __name__ == '__main__':
    main()
