import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_health_advice(input_data):
    try:
        if not isinstance(input_data, str):
            input_data = input_data.to_string()

        messages = [
            {
                "role": "system",
                "content": "You are a professional health advisor. Analyze the following patient report and provide helpful insights."
            },
            {
                "role": "user",
                "content": input_data
            }
        ]

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI request failed: {str(e)}"
