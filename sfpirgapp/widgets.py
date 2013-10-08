from django import forms
from django.template.loader import render_to_string
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class SelectWithPopUp(forms.Select):
    model = None

    def __init__(self, model=None, attrs=None, choices=()):
        self.model = model
        super(SelectWithPopUp, self).__init__(attrs, choices)

    def render(self, name, *args, **kwargs):
        html = super(SelectWithPopUp, self).render(name, *args, **kwargs)
        log.debug('Rendering %s: %s' % (name, html))

        if not self.model:
            self.model = name

        popupplus = render_to_string("includes/formpopup.html", {'field': name, 'model': self.model})
        return html + popupplus