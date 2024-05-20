from zhipuai import ZhipuAI
import os

glm_key = os.environ.get('glm_key')
client = ZhipuAI(api_key=glm_key)


def chat(message: str) -> str:
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": message},
        ],
    )
    return response.choices[0].message.content
