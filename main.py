import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
import openai
import os

# Set up OpenAI (New syntax for openai>=1.0)
openai.api_key = os.getenv("OPENAI_API_KEY")

# UI
st.set_page_config(page_title="📊 Data Analyst Agent with Charts")
st.title("📊 Data Analyst Agent with Chart Support")
st.write("Upload a CSV file and describe the task, e.g., 'Show histogram of sales', 'plot price vs rating', etc.")

# Inputs
task = st.text_area("What do you want to do?", placeholder="Example: Generate a scatter plot of X vs Y")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if st.button("Analyze") and uploaded_file and task:
    try:
        df = pd.read_csv(uploaded_file)
        csv_str = df.to_csv(index=False)
        
        # Prepare prompt
        prompt = f"""
You are a data analyst. You will be given a CSV file and a task. 
1. If the task involves plotting (like histogram, bar chart, scatter plot), output Python matplotlib code to generate that plot. 
2. Otherwise, just answer in text.

Only output Python code if a chart is needed. Otherwise answer normally.

CSV:
{csv_str[:10000]}

Task:
{task}
        """

        # OpenAI call (New syntax)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful data analyst who can analyze CSVs and produce plots."},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content.strip()

        # Detect and execute Python code
        if "```python" in result:
            code = result.split("```python")[1].split("```")[0]

            st.subheader("Generated Python Code:")
            st.code(code, language="python")

            try:
                local_env = {"df": df, "plt": plt}
                exec(code, {}, local_env)
                
                fig = plt.gcf()
                st.pyplot(fig)
                plt.clf()
            except Exception as e:
                st.error(f"Plotting Error: {e}")
        else:
            st.subheader("Answer:")
            st.write(result)

    except Exception as e:
        st.error(f"Error: {e}")
