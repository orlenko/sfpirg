import datetime
from django.template import Context
from django.template.loader import get_template
from mezzanine import template
import logging

from .. import models


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

register = template.Library()


@register.render_tag
def calendar_event_slider(context, token):
    context['events'] = models.Event.objects.filter(start__gt=datetime.datetime.now()).order_by('start')[:20]
    t = get_template('calendar/event_slider.html')
    return t.render(Context(context))
