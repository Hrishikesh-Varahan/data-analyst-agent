import streamlit as st
import pandas as pd
import openai
import os

# Set your OpenAI API key (can be from secret env later)
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...")

st.title("🧠 Data Analyst Agent")
st.write("Upload a CSV file and describe the task. Example: 'Give summary statistics'.")

task = st.text_input("Task:")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if st.button("Analyze") and uploaded_file and task:
    df = pd.read_csv(uploaded_file)
    prompt = f"Perform the following task on this dataset:\nTask: {task}\n\nData:\n{df.head(10).to_csv(index=False)}"
    
    with st.spinner("Analyzing..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content
        st.subheader("📝 Result")
        st.write(result)
