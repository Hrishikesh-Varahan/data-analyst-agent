from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import openai, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from io import BytesIO
import base64
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/api/")
async def analyze(questions: UploadFile = File(...), files: list[UploadFile] = File([])):
    q_text = (await questions.read()).decode()
    file_data = {}
    for file in files:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(await file.read()))
            file_data[file.filename] = df.to_csv(index=False)
        elif file.filename.endswith(".json"):
            file_data[file.filename] = (await file.read()).decode()

    prompt = f"""Answer the following questions using any attached CSV or JSON data if relevant.

Questions:
{q_text}

Attached files:
{list(file_data.keys())}
"""

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(model="gpt-4o", messages=messages)
    answer = response.choices[0].message.content

    return JSONResponse(content={"answer": answer})
