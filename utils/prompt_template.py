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
        2. 如果你觉得这些文档都与问题无关，请直接回复无关
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

           然后我现在需要回答一个问题如下：
           {question}
           
           你觉得这段文本跟问题有关系么？如果有关系就返回是，没关系就返回否。不要返回多余的话语，返回是或否就行。
       """
