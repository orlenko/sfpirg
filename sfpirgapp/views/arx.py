from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from mezzanine.utils.email import send_mail_template
from sfpirgapp.forms import ApplicationForm
from sfpirgapp.forms import MultiApplicationForm
from sfpirgapp.forms import ProjectForm
from sfpirgapp.models import Application, Settings
from sfpirgapp.models import Project
from sfpirgapp.templatetags.sfpirg_tags import _category_by_model
import logging
from django.contrib import messages
from sfpirgapp.models import Liaison
from django.shortcuts import resolve_url


log = logging.getLogger(__name__)


def arxlist(request):
    arxlist = {}
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arxlist.html', {}, context_instance=context)


def require_organization(request):
    profile = request.user.profile
    log.debug('Profile: %s' % profile)
    if not profile:
        return HttpResponseRedirect('/account/update/?profile=1next=%s' % request.get_full_path())
    organization = profile.organization
    log.debug('Organization: %s' % organization)
    if not organization:
        return HttpResponseRedirect('/profile/organization/?next=%s' % request.get_full_path())
    return organization


def project(request, slug):
    user = request.user
    project = get_object_or_404(Project, slug=slug)
    was_submitted = project.is_submitted
    form = None
    if 'edit' in request.REQUEST:
        # User must belong to an organization
        organization = require_organization(request)
        if isinstance(organization, HttpResponseRedirect):
            return organization
        if request.method == 'POST':
            form = ProjectForm(request.POST, request.FILES, instance=project)
            if form.is_valid():
                form.save()
                if not project.is_submitted:
                    # Project draft was saved.
                    action = 'updating'
                    send_mail_template('ARX Project updated: %s' % project.title,
                                       'sfpirg/email/arx_draft',
                                       Settings.get_setting('SERVER_EMAIL'),
                                       request.user.email,
                                       context=locals(),
                                       attachments=None,
                                       fail_silently=settings.DEBUG,
                                       addr_bcc=None)
                elif not was_submitted:
                    # Project was not submitted before, but now it is.
                    send_mail_template('ARX Project submitted: %s' % project.title,
                                       'sfpirg/email/arx_submitted',
                                       Settings.get_setting('SERVER_EMAIL'),
                                       request.user.email,
                                       context=locals(),
                                       attachments=None,
                                       fail_silently=settings.DEBUG,
                                       addr_bcc=None)
                    send_mail_template('ARX Project submitted: %s' % project.title,
                                       'sfpirg/email/arx_admin_submitted',
                                       Settings.get_setting('SERVER_EMAIL'),
                                       Settings.get_setting('ARX_ADMIN_EMAIL'),
                                       context=locals(),
                                       attachments=None,
                                       fail_silently=settings.DEBUG,
                                       addr_bcc=None)
                messages.info(request, 'Thank you! Please check your email for a confirmation message. Check your spam folder if you don\'t see it. We will get back to you very soon.')
                return HttpResponseRedirect(project.get_absolute_url())
        else:
            form = ProjectForm(instance=project)
    page = project
    current_item = page.title
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arx_project.html', {}, context_instance=context)


SELECTED_PROJECTS = 'selected_projects'


def toggle_project_selection(request, project):
    project_id = int(project)
    if request.method == 'POST':
        if request.POST.get('include') == 'true':
            request.session[SELECTED_PROJECTS] = list(set([project_id] + request.session.get(SELECTED_PROJECTS, [])))
        else:
            request.session[SELECTED_PROJECTS] = list(set([x for x in request.session.get(SELECTED_PROJECTS, []) if x != project_id]))
    return HttpResponse(simplejson.dumps({SELECTED_PROJECTS: request.session.get(SELECTED_PROJECTS, [])}),
                        content_type='application/json')



def multi_apply(request):
    form = MultiApplicationForm()
    project_ids = request.session.get(SELECTED_PROJECTS, [])
    request.session[SELECTED_PROJECTS] = []
    count = len(project_ids)
    current_item = 'Apply for Projects'
    projects = Project.objects.filter(pk__in=project_ids)
    if request.method == 'POST':
        form = MultiApplicationForm(request.POST)
        name = form.data['name']
        email = form.data['email']
        comments = form.data['message']
        if form.is_valid():
            for proj_id in project_ids:
                Application.objects.create(name=name, email=email, project_id=proj_id, message=comments)
            send_mail_template('ARX Project application submitted',
               'sfpirg/email/arx_application',
               Settings.get_setting('SERVER_EMAIL'),
               email,
               context=locals(),
               attachments=None,
               fail_silently=settings.DEBUG,
               addr_bcc=None)
            send_mail_template('ARX Project application submitted',
               'sfpirg/email/arx_admin_application',
               Settings.get_setting('SERVER_EMAIL'),
               Settings.get_setting('ARX_ADMIN_EMAIL'),
               context=locals(),
               attachments=None,
               fail_silently=settings.DEBUG,
               addr_bcc=None)
            return HttpResponseRedirect(resolve_url('thankyou'))
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arx_multi_projects_apply.html', {}, context_instance=context)


def project_apply(request, slug):
    project = get_object_or_404(Project, slug=slug)
    form = ApplicationForm(initial={'project': project,
                                    'user': request.user})
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(project.get_absolute_url())
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arx_project_apply.html', {}, context_instance=context)


@login_required
def create(request):
    user = request.user
    # User must belong to an organization
    organization = require_organization(request)
    if isinstance(organization, HttpResponseRedirect):
        return organization
    initial = {'user': request.user}
    if not organization.liaisons.count():
        user = request.user
        liaison = Liaison.objects.create(name=(user.get_full_name() or user.username),
                                         email=user.email,
                                         organization=organization)
        initial = {'liaison': liaison}
    cat = _category_by_model(Project)
    initial['category'] = cat
    form = ProjectForm(request.POST or None, request.FILES or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        form.save()
        action = 'creating'
        project = form.instance
        send_mail_template('ARX Project created: %s' % project.title,
               'sfpirg/email/arx_draft',
               Settings.get_setting('SERVER_EMAIL'),
               request.user.email,
               context=locals(),
               attachments=None,
               fail_silently=settings.DEBUG,
               addr_bcc=None)
        if project.is_submitted:
            send_mail_template('ARX Project submitted: %s' % project.title,
                               'sfpirg/email/arx_submitted',
                               Settings.get_setting('SERVER_EMAIL'),
                               request.user.email,
                               context=locals(),
                               attachments=None,
                               fail_silently=settings.DEBUG,
                               addr_bcc=None)
            send_mail_template('ARX Project submitted: %s' % project.title,
                               'sfpirg/email/arx_admin_submitted',
                               Settings.get_setting('SERVER_EMAIL'),
                               Settings.get_setting('ARX_ADMIN_EMAIL'),
                               context=locals(),
                               attachments=None,
                               fail_silently=settings.DEBUG,
                               addr_bcc=None)
        messages.info(request, 'Thank you! Please check your email for a confirmation message. Check your spam folder if you don\'t see it. We will get back to you very soon.')
        return HttpResponseRedirect(form.instance.get_absolute_url())
    log.debug('Form errors: %s' % form.errors)
    user = request.user
    current_item = 'Create Project'
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arx_project_create.html', {}, context_instance=context)
