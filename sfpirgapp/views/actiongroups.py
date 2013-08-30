from django.template.context import RequestContext
from django.shortcuts import render_to_response
from sfpirgapp.models import ActionGroup
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage


def aglist(request):
    aglist = ActionGroup.objects.all().order_by('title')
    paginator = Paginator(aglist, 10)
    page = request.GET.get('page')
    try:
        aglist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        aglist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        aglist = paginator.page(paginator.num_pages)
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/aglist.html', {}, context_instance=context)