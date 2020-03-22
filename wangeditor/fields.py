#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 20-3-17 上午10:41
# @Author  : Hubery
# @File    : fields.py
# @Software: PyCharm

from __future__ import absolute_import

from django import forms
from django.db import models

from .widgets import WangEditorWidget


class WangRichTextField(models.TextField):

    # 表单字段
    def formfield(self, **kwargs):
        defaults = {
            'form_class': self._get_form_class(),
        }
        defaults.update(kwargs)
        return super(WangRichTextField, self).formfield(**defaults)

    @staticmethod
    def _get_form_class():
        return WangRichTextFormField


class WangRichTextFormField(forms.fields.CharField):

    def __init__(self,  *args, **kwargs):
        kwargs.update({'widget': WangEditorWidget()})
        super(WangRichTextFormField, self).__init__(*args, **kwargs)