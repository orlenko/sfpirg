import re

try:
    import simplejson as json
except ImportError:
    import json

from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import traceback


CKEDITOR_CONFIGS = dict((k, json.dumps(v)) for k, v in settings.CKEDITOR_CONFIGS.items())
FILEBROWSER_PRESENT = True # 'filebrowser' in getattr(settings, 'INSTALLED_APPS', [])
GRAPPELLI_PRESENT = True # 'grappelli' in getattr(settings, 'INSTALLED_APPS', [])

MEDIA = getattr(settings, 'CKEDITOR_MEDIA_URL',
                '%s' % settings.STATIC_URL.rstrip('/')).rstrip('/')

_CSS_FILE = 'grappelli.css' if GRAPPELLI_PRESENT else 'standard.css'

class CKEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        attrs['class'] = 'django-ckeditor'
        kwargs['attrs'] = attrs
        self.ckeditor_config = kwargs.pop('ckeditor_config', 'default')
        super(CKEditor, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):
        rendered = super(CKEditor, self).render(name, value, attrs)
        ckconfig = CKEDITOR_CONFIGS[self.ckeditor_config]
        context = {
            'name': name,
            'config': ckconfig,
            'filebrowser': FILEBROWSER_PRESENT,

            # This "regex" should match the ID attribute of this field.
            # The reason we use a regex is so we can handle inlines, which will have
            # IDs like: id_subsection-6-description
            'regex': attrs.get('id', '').replace('__prefix__', r'\d+'),
        }
        return rendered +  mark_safe(render_to_string(
            'ckeditor/ckeditor_script.html', context
        ))

    def value_from_datadict(self, data, files, name):
        val = data.get(name, u'')
        r = re.compile(r"""(.*?)(\s*<br\s*/?>\s*)*\Z""", re.MULTILINE | re.DOTALL)
        m = r.match(val)
        return m.groups()[0].strip()

    class Media:
        js = (
            MEDIA + '/ckeditor/ckeditor/ckeditor.js',
            MEDIA + '/ckeditor/init.js',
        )
        css = {
            'screen': (
                MEDIA + '/ckeditor/css/' + _CSS_FILE,
            ),
        }



class AdminCKEditor(admin_widgets.AdminTextareaWidget, CKEditor):
    pass

