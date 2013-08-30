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
    context['news'] = models.NewsPost.objects.filter(publish_date__lt=datetime.datetime.now()).order_by('-publish_date')[:20]
    t = get_template('news/news_widget.html')
    return t.render(Context(context))