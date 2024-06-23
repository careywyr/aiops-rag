import json


def is_json_string(s):
    try:
        # 尝试解析字符串为JSON对象
        obj = json.loads(s)
        # 检查解析结果的类型是否为字典或列表
        if isinstance(obj, (dict, list)):
            return True
    except ValueError:
        pass
    return False