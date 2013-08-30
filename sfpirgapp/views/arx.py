from django.template.context import RequestContext
from django.shortcuts import render_to_response


def arxlist(request):
    arxlist = {}
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arxlist.html', {}, context_instance=context)