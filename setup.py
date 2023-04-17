'''
Author: pangxiaobin panglaibin2013@163.com
Date: 2023-03-19 19:10:52
LastEditors: pangxiaobin panglaibin2013@163.com
LastEditTime: 2023-04-17 17:13:56
FilePath: /django-wangeditor/setup.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import os
import sys
from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('python -m twine upload dist/*')
    sys.exit()

setup()
