#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required  # 验证用户是否已登录
from . import views

urlpatterns = [
    url(r'^upload/$', staff_member_required(views.upload), name='upload')
]