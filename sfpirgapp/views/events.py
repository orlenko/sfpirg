import datetime
from mezzanine.calendar.models import Event
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.template.context import RequestContext
from django.shortcuts import render_to_response


def eventslist(request):
    events = Event.objects.filter(start__gt=datetime.datetime.now()).order_by('start')
    paginator = Paginator(events, 10)
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
    return render_to_response('sfpirg/category.html', {}, context_instance=context)


def event(request, event):
    event = Event.objects.get(slug=event)
    page = event
    context = RequestContext(request, locals())
    return render_to_response('calendar/event.html', {}, context_instance=context)