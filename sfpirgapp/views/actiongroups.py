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


def create(request):
    user = request.user
    if user and not user.is_anonymous():
        # See if this user already has an actiongroup - no need to create then.
        for existing in ActionGroup.objects.filter(user=user):
            return HttpResponseRedirect(existing.get_absolute_url() + '?edit=1')
    form = ActionGroupCreateForm(request.POST or None, user=user)
    if request.method == 'POST' and form.is_valid():
        if not user or user.is_anonymous() or not user.profile:
            user = form.save_user()
            if user:
                login(request, user)
        actiongroup = form.save_action_group()
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
        return HttpResponseRedirect(actiongroup.get_absolute_url())
    current_item = 'Create Action Group'
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/action_group_create.html', {}, context_instance=context)
