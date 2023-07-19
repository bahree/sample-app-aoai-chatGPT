# Importing required packages
import streamlit as st
import openai
import os

from typing import List

# pip install streamlit-chat 
from streamlit_chat import message

#pip install python-dotenv
from dotenv import load_dotenv

# Loading the .env file
load_dotenv()

# Get API key from environment variable
#AOAI_KEY = os.getenv("OPENAI_API_KEY")  

# Set up OpenAI API credentials
openai.api_type = "azure"
openai.api_base = 'https://xxxxxx.openai.azure.com/'
openai.api_version = "2023-03-15-preview"
#openai.api_key = OPENAI_API_KEY

# Defining the app title and layout
st.title("PetTalker- powered by ChatGPT")
language = st.selectbox("Select Language", ["Python", "JavaScript"])
code_input = st.text_area("Enter code to explain")
st.button("Explain")

# Temperature and token slider
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.1
)

tokens = st.sidebar.slider(
    "Tokens",
    min_value=64,
    max_value=2048,
    value=256,
    step=64
)


def chat_completion(ai_model: str, messages: List[dict]) -> dict:
    openai.api_key = st.secrets.api_credentials.api_key
    completion = openai.ChatCompletion.create(
        model=ai_model,
        messages=messages,
    )
    return completion


def show_chat(ai_content: str, user_text: str) -> None:
    if ai_content not in st.session_state.generated:
        # store the ai content
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state.generated:
        for i in range(len(st.session_state.generated)):
            message(st.session_state.past[i], is_user=True, key=str(i) + "_user", avatar_style="micah")
            message("", key=str(i))
            st.markdown(st.session_state.generated[i])

