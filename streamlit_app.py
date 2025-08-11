import streamlit as st
import pandas as pd
import httpx
import os
from dotenv import load_dotenv

# ------------------ CONFIG ------------------
# Load .env file (optional for local dev)
load_dotenv()

# Try Streamlit secrets first, then environment variables, then fallback
AIPROXY_TOKEN = st.secrets.get("AIPROXY_TOKEN", os.getenv("AIPROXY_TOKEN", ""))

if not AIPROXY_TOKEN:
    st.error("❌ No API token found. Set it in Streamlit secrets or .env file.")
    st.stop()

AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

# ------------------ UI ------------------
st.set_page_config(page_title="Data Analyst Agent", page_icon="🧠", layout="wide")

st.title("🧠 Data Analyst Agent (IITM AI Proxy)")
st.write("Upload a CSV file and describe the task. Example: *'Give summary statistics'*.")

task = st.text_input("Task:")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# ------------------ API CALL ------------------
def get_ai_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful data analyst. Respond clearly and concisely."},
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
            st.error("❌ Unauthorized: Check your API token.")
        else:
            st.error(f"API error {e.response.status_code}: {e.response.text}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

# ------------------ PROCESS ------------------
if st.button("Analyze") and uploaded_file and task:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()

    prompt = (
        f"Perform the following task on this dataset:\n"
        f"Task: {task}\n\n"
        f"Data (first 10 rows):\n{df.head(10).to_csv(index=False)}"
    )

    with st.spinner("Analyzing..."):
        ai_response = get_ai_response(prompt)

        if ai_response:
            try:
                result = ai_response["choices"][0]["message"]["content"]
                st.subheader("📝 Result")
                st.write(result)
            except KeyError:
                st.error("Invalid API response format.")
else:
    st.caption("⬆️ Upload a CSV and enter a task, then click 'Analyze'.")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit + IITM AI Proxy")
