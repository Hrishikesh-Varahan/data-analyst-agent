import streamlit as st
import pandas as pd
import httpx
import json

# Load IITM API key from Streamlit Secrets
IITM_API_KEY = st.secrets["IITM_API_KEY"]
IITM_API_URL = "https://proxy.iitm.ai/v1/chat/completions"

st.title("🧠 Data Analyst Agent")
st.write("Upload a CSV file and describe the task. Example: 'Give summary statistics'.")

task = st.text_input("Task:")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

async def get_ai_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {IITM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",  # Use your IITM model here
        "messages": [
            {"role": "system", "content": "You are a data analyst."},
            {"role": "user", "content": prompt}
        ]
    }
    async with httpx.AsyncClient(timeout=180) as client:
        response = await client.post(IITM_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

if st.button("Analyze") and uploaded_file and task:
    df = pd.read_csv(uploaded_file)
    prompt = f"Perform the following task on this dataset:\nTask: {task}\n\nData:\n{df.head(10).to_csv(index=False)}"
    with st.spinner("Analyzing..."):
        try:
            # Use asyncio.run() since Streamlit is sync
            import asyncio
            ai_response = asyncio.run(get_ai_response(prompt))
            result = ai_response["choices"][0]["message"]["content"]
            st.subheader("📝 Result")
            st.write(result)
        except Exception as e:
            st.error(f"API call failed: {e}")
