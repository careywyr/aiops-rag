from openai import OpenAI
import os
from utils import prompt_template
from pre.pojo import GraphExtract
import json

deepseek_key = os.environ.get('DEEPSEEK_KEY')
client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")


def chat(message: str, system_prompt: str = "You are a helpful assistant") -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        stream=False
    )

    return response.choices[0].message.content


def extract_keywords(text: str):
    keywords_output = chat(text, prompt_template.extract_keyword_system())
    keywords = keywords_output.split(",")
    return keywords


def extract_knowledge_graph(text: str) -> [GraphExtract]:
    output = chat(text, prompt_template.extract_kg_prompt)
    if '```json' in output:
        output = output.replace('```json', '').replace('```', '')
    print(output)
    data = json.loads(output)
    return [GraphExtract(d.get('head'), d.get('head_type'), d.get('relation'), d.get('tail'), d.get('tail_type')) for d in data]


