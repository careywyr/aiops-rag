# -*- coding: utf-8 -*-
"""
@file    : txt_processor.py
@date    : 2024-05-26
@author  : leafw

txt文档处理器
"""
import os
import consts

# 四个文件夹一个个处理看看
emsplus = consts.TXT_DATA_DIR + '/emsplus'


# 每个文件夹下面都有个nodes文件夹，这个文件夹实际上是个目录，对于txt文件处理而言，这个文件夹应该是无用的
# 此版本可以先尝试把所有文件整个向量化试试看看看得分
def read_files_in_directory(directory):
    # 遍历目录
    for entry in os.listdir(directory):
        entry_path = os.path.join(directory, entry)

        # 检查是否为文件夹
        if os.path.isdir(entry_path):
            print(f"Entering directory: {entry_path}")

            # 遍历文件夹中的文件
            for file in os.listdir(entry_path):
                file_path = os.path.join(entry_path, file)

                # 检查是否为文件
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r') as f:
                            print(f"Reading {file_path} contents:")
                            # # 输出文件内容
                            # print(f.read())
                            print("-" * 40)  # 添加分隔线
                    except Exception as e:
                        print(f"Failed to read {file_path}: {e}")
        else:
            print(f"Skipping file: {entry_path}")



