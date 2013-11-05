from django.conf import settings
from django.contrib.auth import login
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from mezzanine.utils.email import send_mail_template
from sfpirgapp.forms import ActionGroupCreateForm
from sfpirgapp.forms import ActionGroupForm
from sfpirgapp.models import ActionGroup, Settings
import logging
from sfpirgapp.forms import ActionGroupRequestForm
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required
from sfpirgapp.templatetags.sfpirg_tags import _category_by_model


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
        else:
            if not (request.user.is_superuser or request.user == actiongroup.user):
                return HttpResponseRedirect(actiongroup.get_absolute_url())
    context = RequestContext(request, locals())
    return render_to_response('pages/actiongroup.html', {}, context_instance=context)


def request_group(request):
    form = ActionGroupRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect(resolve_url('thankyou'))
    current_item = 'Action Group Request'
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/action_group_request.html', {}, context_instance=context)


@login_required
def create(request):
    user = request.user
    # See if this user already has an actiongroup - no need to create then.
    for existing in ActionGroup.objects.filter(user=user):
        return HttpResponseRedirect(existing.get_absolute_url() + '?edit=1')
    initial = {'user': user, 'status': 1, '_order': 0}
    cat = _category_by_model(ActionGroup)
    initial['category'] = cat
    form = ActionGroupForm(request.POST or None, request.FILES or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        form.save()
        actiongroup = form.instance
        send_mail_template('Action Group Application Submitted: %s' % actiongroup.title,
               'sfpirg/email/ag_application',
               Settings.get_setting('SERVER_EMAIL'),
               user.email,
               context=locals(),
               attachments=None,
               fail_silently=settings.DEBUG,
               addr_bcc=None)
        send_mail_template('Action Group Application Submitted: %s' % actiongroup.title,
               'sfpirg/email/ag_admin_application',
               Settings.get_setting('SERVER_EMAIL'),
               Settings.get_setting('ACTION_GROUPS_ADMIN_EMAIL'),
               context=locals(),
               attachments=None,
               fail_silently=settings.DEBUG,
               addr_bcc=None)
        return HttpResponseRedirect(form.instance.get_absolute_url())
    current_item = 'Create Action Group'
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/action_group_create.html', {}, context_instance=context)
