import streamlit as st
import pandas as pd
import google.generativeai as genai

# Load API key from Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🧠 Data Analyst Agent (Gemini)")
st.write("Upload a CSV file and describe the task. Example: 'Give summary statistics'.")

task = st.text_input("Task:")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if st.button("Analyze") and uploaded_file and task:
    df = pd.read_csv(uploaded_file)
    prompt = f"Perform the following task on this dataset:\nTask: {task}\n\nData:\n{df.head(10).to_csv(index=False)}"

    with st.spinner("Analyzing..."):
        model = genai.GenerativeModel("gemini-1.5-pro")  # 'pro' is best for reasoning
        response = model.generate_content(prompt)

        st.subheader("📝 Result")
        st.write(response.text)
