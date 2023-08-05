# -*- coding: utf-8 -*-
# author:      hj
# create_time: 2019/7/8 15:38
# update_time: 2019/7/8 15:38
from distutils.core import setup

setup(
    name='qa_tech_basic_37',  # 对外我们模块的名字
    version='0.1.1',  # 版本号
    description='齐安科技基础包',  # 描述
    author='hj',  # 作者
    author_email='56172032@qq.com',
    py_modules=['qa_tech_basic_37.configuration', 'qa_tech_basic_37.regex_utils', 'qa_tech_basic_37.time_utils',
                'qa_tech_basic_37.yaml_configuration_utils']
)


"""
version=0.1.1
更新日期：2020-01-09
更新人：hj
增加基础包：YamlConfigurationUtils，从yaml文件中读取配置文件
"""


