from django.shortcuts import render_to_response
from django.template.context import RequestContext
#from sfpirgapp import models


def homepage(request, *args, **kwargs):
    context = RequestContext(request, locals())
    return render_to_response('index.html', {'current_item': 'Home'}, context_instance=context)