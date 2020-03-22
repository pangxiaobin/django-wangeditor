#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
from django.utils.functional import Promise
from django.utils.safestring import mark_safe

from js_asset import JS

from .configs import WANG_DEFAULT_CONFIG

try:
    # Django >=1.11
    from django.forms.widgets import get_default_renderer
except ImportError:
    # Django <1.11
    from django.template.loader import render_to_string

    def get_default_renderer():
        class DummyDjangoRenderer(object):
            @staticmethod
            def render(*args, **kwargs):
                return render_to_string(*args, **kwargs)

        return DummyDjangoRenderer

try:
    # Django >=1.7
    from django.forms.utils import flatatt
except ImportError:
    # Django <1.7
    from django.forms.util import flatatt


class LazyEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


json_encode = LazyEncoder().encode


class WangEditorWidget(forms.Textarea):

    class Media:
        # js
        js = (
            JS('wangeditor/wangeditor-init.js', {
                'id': 'wangeditor-init-script',
            }),
            'wangeditor/wangEditor.min.js',
        )

    def __init__(self, config_name='default',  *args, **kwargs):
        super(WangEditorWidget, self).__init__(*args, **kwargs)
        # Setup config from defaults.
        self.config = WANG_DEFAULT_CONFIG.copy()

        # Try to get valid config from settings.
        configs = getattr(settings, 'WANGEDITOR_CONFIGS', None)
        if configs:
            if isinstance(configs, dict):
                # Make sure the config_name exists.
                if config_name in configs:
                    config = configs[config_name]
                    # Make sure the configuration is a dictionary.
                    if not isinstance(config, dict):
                        raise ImproperlyConfigured('WANGEDITOR_CONFIGS["%s"] \
                                setting must be a dictionary type.' %
                                                   config_name)
                    # Override defaults with settings config.
                    self.config.update(config)
                else:
                    raise ImproperlyConfigured("No configuration named '%s' \
                            found in your WANGEDITOR_CONFIGS setting." %
                                               config_name)
            else:
                raise ImproperlyConfigured('WANGEDITOR_CONFIGS setting must be a\
                        dictionary type.')

    def render(self, name, value, attrs=None, renderer=None):
        if renderer is None:
            renderer = get_default_renderer()
        if value is None:
            value = ''
        final_attrs = self.build_attrs(self.attrs, attrs, name=name)
        return mark_safe(renderer.render('wangeditor/widget.html', {
            'final_attrs': flatatt(final_attrs), # flatatt  设置html 的属性, 形式key=value
            'value': force_text(value),
            'config': json_encode(self.config),
            'id': final_attrs['id'],
        }))

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        """
        Helper function for building an attribute dictionary.
        This is combination of the same method from Django<=1.10 and Django1.11+
        """
        attrs = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs