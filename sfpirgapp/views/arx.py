from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from sfpirgapp.models import Project
from sfpirgapp.forms import ProjectForm
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from sfpirgapp.forms import ApplicationForm
from django.contrib.auth.decorators import permission_required
import logging
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from sfpirgapp.models import Category


log = logging.getLogger(__name__)


def arxlist(request):
    arxlist = {}
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arxlist.html', {}, context_instance=context)


def require_organization(request):
    profile = request.user.profile
    log.debug('Profile: %s' % profile)
    if not profile:
        return HttpResponseRedirect('/account/update/?message=Please+update+your+profile&next=%s' % request.get_full_path())
    organization = profile.organization
    log.debug('Organization: %s' % organization)
    if not organization:
        return HttpResponseRedirect('/account/update/?message=Please+update+your+profile+and+organization&next=%s' % request.get_full_path())
    log.debug('Organization: %s' % organization)
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
            form = ProjectForm(request.POST or None, instance=project)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(project.get_absolute_url())
        else:
            form = ProjectForm(instance=project)
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arx_project.html', {}, context_instance=context)


@login_required
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
