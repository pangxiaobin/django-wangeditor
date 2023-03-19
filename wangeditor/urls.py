'''
Author: pangxiaobin panglaibin2013@163.com
Date: 2023-03-19 19:10:52
LastEditors: pangxiaobin panglaibin2013@163.com
LastEditTime: 2023-03-19 19:12:18
FilePath: /django-wangeditor/wangeditor/urls.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.admin.views.decorators import staff_member_required  # 验证用户是否已登录
from . import views
try:
    from django.conf.urls import url
    urlpatterns = [
        url(r'^upload/$', staff_member_required(views.upload), name='upload')
    ]
except ImportError:
    from django.urls import path
    urlpatterns = [
        path('upload/', staff_member_required(views.upload), name='upload')
    ]