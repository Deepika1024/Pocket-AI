import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
import os
import json
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Title
st.title("Hello! I am Pocket AI")

# Session state for memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Gemini LLM Init
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite-preview-06-17",
    api_key=gemini_api_key
)

# Chat input UI
user_query = st.chat_input("Talk to Pocket AI...")

if user_query:
    # Add user message to history
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Invoke LLM with full chat history
    response = llm.invoke(st.session_state.chat_history)

    # Add bot response to history
    st.session_state.chat_history.append(AIMessage(content=response.content))

    # Show AI response
    with st.chat_message("assistant"):
        st.markdown(response.content)

    # Log conversation
    log_entry = {
        "input": user_query,
        "response": response.content
    }
    with open("mentor_chat_logs.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# Optional: Show conversation history in sidebar
with st.sidebar:
    st.subheader("🧠 Conversation History")
    for msg in st.session_state.chat_history:
        role = "👤 You" if isinstance(msg, HumanMessage) else "🤖 MentorAI"
        st.markdown(f"**{role}:** {msg.content}")
