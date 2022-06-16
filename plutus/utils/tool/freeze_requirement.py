# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/21 0021 13:38
# @Author  : jtt
# @File    : freeze_requirement.py


import os
import platform
import sys

# 找到当前目录
project_root = os.path.dirname(os.path.realpath(__file__))
print(f"当前目录:{project_root}")
# 不同的系统,使用不同的命令语句
if platform.system() == "Linux":
    command = sys.executable + " -m pip freeze > " + project_root + "/requirements.txt"
if platform.system() == "Windows":
    command = (
        '"'
        + sys.executable
        + '"'
        + ' -m pip freeze > "'
        + project_root
        + '\\requirements.txt"'
    )

# 执行命令
# os.system(command)  #路径有空格不管用
os.popen(command)  # 路径有空格,可用
