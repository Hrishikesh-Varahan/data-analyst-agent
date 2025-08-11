import streamlit as st
import requests

API_TOKEN = st.secrets["AIPROXY_TOKEN"]  # from secrets.toml

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "model": "openai/gpt-4.1-nano",
    "input": "What is 2 + 2?"
}

response = requests.post(
    "https://aipipe.org/openrouter/v1/responses",
    headers=headers,
    json=data
)

st.write(response.json())
