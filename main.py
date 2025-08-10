import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai

st.set_page_config(page_title="📊 Data Analyst Agent with Charts (Gemini)")
st.title("📊 Data Analyst Agent with Chart Support (Gemini)")
st.write("Upload a CSV file and describe the task, e.g., 'Show histogram of sales', 'plot price vs rating', etc.")

# Load API Key from Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

task = st.text_area("What do you want to do?", placeholder="Example: Generate a scatter plot of X vs Y")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if st.button("Analyze") and uploaded_file and task:
    try:
        df = pd.read_csv(uploaded_file)
        csv_preview = df.head(20).to_csv(index=False)

        prompt = f"""
You are a data analyst. You will be given a CSV file preview and a task. 
- If the task involves plotting, output ONLY valid Python matplotlib code inside triple backticks, no explanations.
- If not plotting, output plain text.

CSV preview:
{csv_preview}

Task:
{task}
        """

        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        result = response.text.strip()

        if "```python" in result:
            code = result.split("```python")[1].split("```")[0]
            st.subheader("Generated Python Code:")
            st.code(code, language="python")

            try:
                safe_env = {"df": df, "plt": plt, "pd": pd}
                exec(code, {"__builtins__": {}}, safe_env)
                fig = plt.gcf()
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e:
                st.error(f"Plotting Error: {e}")
        else:
            st.subheader("Answer:")
            st.write(result)

    except Exception as e:
        st.error(f"Error: {e}")
