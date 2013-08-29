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
def news_list(context, token):
    return ''