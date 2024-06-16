import pandas as pd
import json

# 读取 jsonl 文件
file_path = 'D:\\Workspace\\aiops-rag\\dataset\\fourth_hotfix.jsonl'

data = []
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        data.append(json.loads(line))

# 提取需要的列
extracted_data = []
for item in data:
    extracted_data.append({
        'id': item['id'],
        'query': item['query'],
        'answer': item['answer'],
        'background': item['background']
    })

# 转换为 DataFrame
df = pd.DataFrame(extracted_data)

# 保存为 Excel 文件
output_file_path = 'output.xlsx'  # 替换为你想保存的Excel文件路径
df.to_excel(output_file_path, index=False)

print(f"数据已成功保存到 {output_file_path}")
