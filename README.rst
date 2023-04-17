
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

3.Run the collectstatic management command: `$ ./manage.py collectstatic.` This will copy static CKEditor required media resources into the directory given by the STATIC_ROOT setting. See Django's documentation on managing static files for more info.


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


Use upload local pictures
++++++++++++++++++++++++++
1.Add a WANGEDITOR_UPLOAD_PATH setting to the project's settings.py file. This setting specifies a relative path to your wangeditor media upload directory. CKEditor uses Django's storage API. By default, Django uses the file system storage backend (it will use your MEDIA_ROOT and MEDIA_URL)::

 MEDIA_URL = '/media/'
 MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

 WANGEDITOR_UPLOAD_PATH = "uploads/"


2.Include the wangeditor URLconf in your project urls.py like this::

  from django.conf.urls.static import static
  from django.conf import settings
  # django >= 2.0
  path('wangeditor/', include('wangeditor.urls'))
  # django < 2.0
  url(r'wangeditor/', include('wangeditor.urls'))
  if settings.DEBUG:
      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



-------
config
-------
Optional - customizing wangEditor editor Add a WANGEDITOR_CONFIGS setting to the project's settings.py file.::

 WANGEDITOR_CONFIGS = {
  "default": {
    "toolbar_config":{
      "modalAppendToBody": False,
    }
    "menu_conf": {
       "uploadImage": {
          "server": "/wangeditor/img_upload/",
        },
        "uploadVideo": {
          "server": "/wangeditor/video_upload/"
        }
    }
 }
 # toobar_config and menu_conf cong please see https://www.wangeditor.com/v5/toolbar-config.html and https://www.wangeditor.com/v5/menu-config.html

-----------
Update Log
-----------
version-2.0.0

1、update wangeditor to wangeditor-v5;

version-1.0.2

1、Resolve compatibility issues with django 4.0


Refer to the configuration for more information, please see `https://www.kancloud.cn/wangfupeng/wangeditor3/332599`
