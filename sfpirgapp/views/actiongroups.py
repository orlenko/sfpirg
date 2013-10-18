import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from sfpirgapp.forms import ActionGroupForm
from sfpirgapp.models import ActionGroup, Category


log = logging.getLogger(__name__)


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


def actiongroup(request, slug):
    actiongroup = get_object_or_404(ActionGroup, slug=slug)
    page = actiongroup
    current_item = page.title
    form = None

    if 'edit' in request.REQUEST:
        form = ActionGroupForm(request.POST or None, request.FILES or None, instance=actiongroup)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponseRedirect(actiongroup.get_absolute_url())

    context = RequestContext(request, locals())
    return render_to_response('pages/actiongroup.html', {}, context_instance=context)


@login_required
def create(request):
    # See if this user already has an actiongroup - no need to create then.
    for existing in ActionGroup.objects.filter(user=request.user):
        return HttpResponseRedirect(existing.get_absolute_url() + '?edit=1')
    initial = {'user': request.user, 'status': 1, '_order': 0}
    cat = Category.objects.filter(title='Action Groups')
    if len(cat):
        initial['category'] = cat[0]
    form = ActionGroupForm(request.POST or None, request.FILES or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect(form.instance.get_absolute_url())
    user = request.user
    current_item = 'Create Action Group'
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/action_group_create.html', {}, context_instance=context)
