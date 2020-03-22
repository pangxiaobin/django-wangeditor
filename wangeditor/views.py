#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
from datetime import datetime

from django.views import generic

from wangeditor.backends import registry
from wangeditor.utils import storage, slugify_filename, get_media_url
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


def get_upload_filename(upload_name):

    # Generate date based path to put uploaded file.
    # If CKEDITOR_RESTRICT_BY_DATE is True upload file to date specific path.
    if getattr(settings, 'WANGEDITOR_RESTRICT_BY_DATE', True):
        date_path = datetime.now().strftime('%Y/%m/%d')
    else:
        date_path = ''
    WANGEDITOR_UPLOAD_PATH = getattr(settings, 'WANGEDITOR_UPLOAD_PATH', 'uploads/')
    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(WANGEDITOR_UPLOAD_PATH, date_path)
    if getattr(settings, 'WANGEDITOR_UPLOAD_SLUGIFY_FILENAME', True):
        upload_name = slugify_filename(upload_name)

    # 返回基于name参数的文件名称，它在目标储存系统中可用于写入新的内容。
    # 如果提供了max_length，文件名称长度不会超过它。如果不能找到可用的、唯一的文件名称，会抛出SuspiciousFileOperation 异常。
    # 如果name命名的文件已存在，一个下划线加上随机7个数字或字母的字符串会添加到文件名称的末尾，扩展名之前。
    return storage.get_available_name(
        os.path.join(upload_path, upload_name)
    )


class ImageUploadView(generic.View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        """
        Uploads a file and send back its URL to WANGEditor.
        """
        uploaded_files = request.FILES

        backend = registry.get_backend()
        url_list = []
        err_no = 0
        msg = 'success'
        for file_name, uploaded_file in uploaded_files.items():
            file_wrapper = backend(storage, uploaded_file)
            if not file_wrapper.is_image:
                err_no = 1
                msg = '%s is invalid file type' % file_name
                break
            filepath = get_upload_filename(file_name)
            saved_path = file_wrapper.save_as(filepath)
            url = get_media_url(saved_path)
            url_list.append(url)
        ret_data = {
            "errno": err_no,
            "data": url_list,
            'msg': msg
        }
        return JsonResponse(ret_data)


upload = csrf_exempt(ImageUploadView.as_view())