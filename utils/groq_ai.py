import requests
import os
import pandas as pd 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  


def get_health_advice(data):
    if isinstance(data, str):
        prompt = f"This is a medical report text:\n{data}\n\nPlease analyze this and give health advice in simple language."
    elif isinstance(data, pd.DataFrame):
        prompt = f"Given this health data table:\n{data.head().to_string()}\n\nWhat can you infer? Provide health advice in simple terms."
    else:
        return "Unsupported data format for health advice."

    return get_groq_response(prompt)

def get_groq_response(prompt, model="llama3-70b-8192"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a medical expert AI assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error from Groq API: {response.status_code} - {response.text}"
