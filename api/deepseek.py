from openai import OpenAI
import os

deepseek_key = os.environ.get('DEEPSEEK_KEY')

client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")


def chat(message: str) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": message},
        ],
        stream=False
    )

    return response.choices[0].message.content
