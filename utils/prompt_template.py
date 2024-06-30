# -*- coding: utf-8 -*-
"""
@file    : prompt_template.py
@date    : 2024-05-26
@author  : leafw
"""


def find_doc(content: str, question: str):
    return f"""
        我现在有一些html组成的知识库文档，下面这个是它所有文档名组成的节点树的json：

        {content}

        我现在有一个基于这个知识库考察的一个问题:
         {question}

        请你帮我看看这个问题的答案最有可能出现在哪几个文档中？你返回的规则如下：
        1. 给出不超过5个文档的名称，注意只给出文档名称即可，不要说任何其他的话,多个文档名称之间用英文逗号隔开。
        
            举个例子，你想输出 更新历史, 获取途径与意见反馈, 联系中兴通讯技术支持 这几个文档名称，那么你输出的内容如下：
            
            更新历史, 获取途径与意见反馈, 联系中兴通讯技术支持
        
        2. 如果你觉得这些文档都与问题无关或者你不确定，请直接回复无关
        3. 除了文档名称，绝对禁止输出任何无关内容

        """


def extract_keyword_system():
    return """
    你是一名运维技术专家，能阅读并理解运维相关的技术文档，熟悉当前市面上的各种运维产品，对于常见的品牌如华为/中兴等的硬件设备都很熟悉。
    现在我将会给你发送一些运维文档的段落内容，你需要从段落中提取这段内容的关键词，并遵守以下规则：
    1. 多个关键词用英文逗号隔开，如 关键词1,关键词2,关键词3
    2. 关键词必须在原文中出现过，不可以随便臆造
    3. 允许出现某个关键词包含了另一个关键词的情况，举个例子：高等数学,数学。这两个关键词有包含关系，但允许同时出现。
    请务必按照规则给我提取关键词。
    """


def find_question(content: str, question: str):
    return f"""
        我有一些关于运维知识相关的参考资料，内容如下:
        
        {content}
        
        我需要你根据背景知识回答问题，要求如下：
        1. 首先仔细阅读每一段背景知识，根据问题的关键词找到最相关的段落
        2. 理解对应段落的内容，准确回答问题。
        3. 答案中不要出现"根据背景知识得到"或"根据您提供的参考资料"这种类似的话语，直接回答问题即可
        
        现在请你回答下面的问题:
        
        {question}
    """


def check_relationship(question: str, content: str):
    return f"""
           我有一段关于运维的材料的文本，内容如下:

           {content}

           然后我现在需要根据上述文本内容回答一个问题如下：
           {question}
           
           你觉得依靠这些内容能回答这个问题么？如果能，回复是；如果不能，回复否。
           
           重要提示：
            - 不要添加任何解释和文本。
       """


extract_kg_prompt = """
你是一个顶级算法工程师，旨在从结构化格式的文本中提取信息，以构建知识图谱。你的任务是从给定的文本中识别用户提示中请求的实体和关系。
你必须生成包含JSON对象列表的输出。每个对象应具有以下键：“head”、“head_type”、“relation”、“tail”和“tail_type”。
“head”键必须包含从提供的列表中提取的实体文本。
“head_type”键必须包含提取的head实体的类型
“relation”键必须包含head和tail之间关系的类型
“tail”键必须表示提取实体的文本，该实体是关系的tail
“tail_type”键必须包含提取的tail实体的类型

尝试提取尽可能多的实体和关系。保持实体一致性：在提取实体时，确保一致性非常重要。如果一个实体（例如“John Doe”）在文本中多次提到，但使用不同的名称或代词（例如“Joe”、“他”），始终使用最完整的标识符来表示该实体。知识图谱应该是连贯且易于理解的，因此保持实体引用的一致性至关重要。
重要提示：
- 不要添加任何解释和文本。
"""


multi_query = """
你是一名顶级运维工程师，可以针对用户的输入问题生成多个子查询问题，每个问题独立一行输出。
首先你需要判断用户是否真的问了多个问题，如果没有，你就原样输出用户问题；
如果用户真的询问了多个问题，请你拆解成多个子问题。

重要提示：
- 不要添加任何解释和文本。
"""

keyword_extract = """
你是一名顶级运维工程师，可以针对用户的输入问题精准提取关键词，每个关键词独立一行输出。
关键词必须来源于问题本身，不可以脱离原问题
关键词可以是个短句，但最好不要超过10个字
关键词可以是句子中某几个部分的合体，比如 'RCP扩容时需要注意哪些事项？'的关键词可以 'RCP扩容注意事项'
多个关键词之间可以存在包含关系

重要提示：
- 不要添加任何解释和文本。
"""


def hyde_prompt(content: str):
    return f"""
    请写一段话回答问题
    尽量包含关键细节。
    
    {content}
    
    """

