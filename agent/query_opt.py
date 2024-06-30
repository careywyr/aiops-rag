# -*- coding: utf-8 -*-
"""
@file    : retrieval.py
@date    : 2024-06-29
@author  : leafw

"""

import api.glm as glm
import utils.prompt_template as prompt_template


def multi_query(query: str):
    resp = glm.chat(query, prompt_template.multi_query)
    return resp.split('\n')


def keywords_query(query: str):
    resp = glm.chat(query, prompt_template.keyword_extract)
    return resp.split('\n')


def hyde(query: str):
    resp = glm.chat(prompt_template.hyde_prompt(query))
    return resp


