import streamlit as st
import pandas as pd
import httpx

# Load IITM AI Proxy token from Streamlit Secrets
AIPROXY_TOKEN = st.secrets["AIPROXY_TOKEN"]
AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

st.title("🧠 Data Analyst Agent (IITM AI Proxy)")
st.write("Upload a CSV file and describe the task. Example: 'Give summary statistics'.")

task = st.text_input("Task:")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

def get_ai_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful data analyst."},
            {"role": "user", "content": prompt},
        ],
    }
    try:
        with httpx.Client(timeout=180) as client:
            response = client.post(AIPROXY_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            st.error("❌ Unauthorized: Check your API token in Streamlit secrets.")
        else:
            st.error(f"API error {e.response.status_code}: {e.response.text}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

if st.button("Analyze") and uploaded_file and task:
    df = pd.read_csv(uploaded_file)
    prompt = (
        f"Perform the following task on this dataset:\n"
        f"Task: {task}\n\n"
        f"Data (first 10 rows):\n{df.head(10).to_csv(index=False)}"
    )
    with st.spinner("Analyzing..."):
        ai_response = get_ai_response(prompt)
        if ai_response:
            result = ai_response["choices"][0]["message"]["content"]
            st.subheader("📝 Result")
            st.write(result)
