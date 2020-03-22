
=================
django-wangeditor
=================

Quick start
------------

1.Install or add django-wangeditor to your python path.::

    pip install django-wangeditor

2.Add "wangeditor" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ... 
        'wangeditor',
    ]

3.Include the polls URLconf in your project urls.py like this::

    path('wangeditor/', include('wangeditor.urls'))

4.Run the collectstatic management command: `$ ./manage.py collectstatic.` This will copy static CKEditor required media resources into the directory given by the STATIC_ROOT setting. See Django's documentation on managing static files for more info.

5.Add a WANGEDITOR_UPLOAD_PATH setting to the project's settings.py file. This setting specifies a relative path to your wangeditor media upload directory. CKEditor uses Django's storage API. By default, Django uses the file system storage backend (it will use your MEDIA_ROOT and MEDIA_URL)::

 WANGEDITOR_UPLOAD_PATH = "uploads/"

-----
Usage
-----

Field
++++++
The quickest way to add rich text editing capabilities to your models is to use the included RichTextField model field type.
For example::

 from django.db import models
 from wangeditor.fields import WangRichTextField

 class Post(models.Model):
     content = WangRichTextField()

-------
config
-------
Optional - customizing wangEditor editor
Add a WANGEDITOR_CONFIGS setting to the project's settings.py file.::

    WANGEDITOR_CONFIGS = {
    'default': {
        'menus': ['head', 'bold', 'fontSize', 'fontName', 'italic', 'underline', 'strikeThrough', 'foreColor',
                  'backColor',
                  'link', 'list', 'justify', 'quote', 'emoticon', 'image', 'table', 'video', 'code', 'undo', 'redo'],
        'pasteFilterStyle': True,  # 是否关闭粘贴样式的过滤
        'pasteIgnoreImg': False,  # 是否忽略粘贴内容中的图片
        'colors': [
            '#000000',
            '#eeece0',
            '#1c487f',
            '#4d80bf',
        ],  # 自定义配置颜色（字体颜色、背景色）可以添加更多的色号
        'showLinkImg': False,
    }
    }

Refer to the configuration for more information, please see `https://www.kancloud.cn/wangfupeng/wangeditor3/332599`
