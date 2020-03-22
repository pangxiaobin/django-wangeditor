#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import random
import string

from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.module_loading import import_string

IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


# Allow for a custom storage backend defined in settings.
# https://docs.djangoproject.com/en/3.0/ref/files/storage/
def get_storage_class():

    return import_string(getattr(settings, 'WANGEDITOR_STORAGE_BACKEND', 'django.core.files.storage.DefaultStorage'))()


storage = get_storage_class()


def slugify_filename(filename):
    """ Slugify filename """
    name, ext = os.path.splitext(filename)
    slugified = get_slugified_name(name)
    return slugified + ext


def get_slugified_name(filename):
    """
    slugify: 转换为ASCII。将空格转换为连字符。删除字符
    不是字母数字、下划线或连字符。转换为小写的。
    还可以删除开头和结尾的空白。
    """
    slugified = slugify(filename)
    return slugified or get_random_string()


def get_random_string():
    return ''.join(random.sample(string.ascii_lowercase * 6, 6))


def get_media_url(path):
    """
    Determine system file's media URL.
    """
    return storage.url(path)


def is_valid_image_extension(file_name):
    """验证是否为图片"""
    return file_name.split('.')[-1] in IMAGE_EXTENSIONS if file_name else False
