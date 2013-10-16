from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from sfpirgapp.models import Project
from sfpirgapp.forms import ProjectForm
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from sfpirgapp.forms import ApplicationForm
import logging
from sfpirgapp.models import Category
from sfpirgapp.forms import MultiApplicationForm
from sfpirgapp.models import Application
from django.http.response import HttpResponse
from django.utils import simplejson


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
    project = get_object_or_404(Project, slug=slug)
    form = None
    if 'edit' in request.REQUEST:
        # User must belong to an organization
        organization = require_organization(request)
        if isinstance(organization, HttpResponseRedirect):
            return organization
        if request.method == 'POST':
            form = ProjectForm(request.POST or None, request.FILES, instance=project)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(project.get_absolute_url())
        else:
            form = ProjectForm(instance=project)
    page = project
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
    return HttpResponse(simplejson.dumps({SELECTED_PROJECTS: request.session[SELECTED_PROJECTS]}),
                        content_type='application/json')



def multi_apply(request):
    form = MultiApplicationForm()
    project_ids = request.session.get(SELECTED_PROJECTS, [])
    request.session[SELECTED_PROJECTS] = []
    count = len(project_ids)
    projects = Project.objects.filter(pk__in=project_ids)
    if request.method == 'POST':
        form = MultiApplicationForm(request.POST)
        if form.is_valid():
            for proj_id in project_ids:
                Application.objects.create(email=form.data['email'],
                                           project_id=proj_id,
                                           message=form.data['message'])
            return HttpResponseRedirect('/category/action-research-exchange/')
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
    # User must belong to an organization
    organization = require_organization(request)
    if isinstance(organization, HttpResponseRedirect):
        return organization
    initial = {'user': request.user}
    cat = Category.objects.filter(title='Action Research Exchange')
    if len(cat):
        initial['category'] = cat[0]
    form = ProjectForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect(form.instance.get_absolute_url())
    user = request.user
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arx_project_create.html', {}, context_instance=context)
