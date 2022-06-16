#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件    :add_sys_path.py
@说明    :
@时间    :2022/03/04 10:12:25
@作者    :jiangtiantu
@版本    :1.0
"""
import os
import os.path
import site

from configer import Configer


def run_setup():
    config = Configer()
    root_dir = config.root_dir
    packages_path = site.getsitepackages()
    # 首先搜索可以添加的默认搜索路径
    with open(os.path.join(packages_path[0], "import_path.pth"), "w") as f:
        # 选择其中一个路径,创建pth文件
        f.write(root_dir)


if __name__ == "__main__":
    run_setup()
