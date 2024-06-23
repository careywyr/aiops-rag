from zhipuai import ZhipuAI
import os
from utils import prompt_template, common
from pre.pojo import GraphExtract
import json


glm_key = os.environ.get('GLM_KEY')
client = ZhipuAI(api_key=glm_key)


def chat(message: str, system_prompt: str = "You are a helpful assistant") -> str:
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=0.5
    )
    return response.choices[0].message.content


def extract_knowledge_graph(text: str) -> [GraphExtract]:
    output = chat(text, prompt_template.extract_kg_prompt)
    if '```json' in output:
        output = output.replace('```json', '').replace('```', '')

    if not common.is_json_string(output):
        print(output)
        output = amend_json(output)
    print(output)
    data = json.loads(output)
    return [GraphExtract(d.get('head'), d.get('head_type'), d.get('relation'), d.get('tail'), d.get('tail_type')) for d in data]


def amend_json(json_str: str):
    system = """
    你是一名json专家，如果有json字符串不符合规范，你可以进行一些调整，比如补充遗漏的符号，去除多余的符号的方法修改字符串，并将修正后的json字符串返回回来。如果是正确的，你就直接返回原json字符串
    重要提示：
    - 不要添加任何解释和文本，直接输出json字符串
    """
    output = chat(json_str, system)
    if '```json' in output:
        output = output.replace('```json', '').replace('```', '')
    return output