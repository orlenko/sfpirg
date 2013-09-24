from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from sfpirgapp.models import Project
from sfpirgapp.forms import ProjectForm
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from sfpirgapp.forms import ApplicationForm


def arxlist(request):
    arxlist = {}
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arxlist.html', {}, context_instance=context)


def project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    form = None
    if 'edit' in request.REQUEST:
        if request.method == 'POST':
            form = ProjectForm(request.POST or None, instance=project)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(project.get_absolute_url())
        else:
            form = ProjectForm(initial={'user': request.user}, instance=project)
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/project.html', {}, context_instance=context)


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
    return render_to_response('sfpirg/project_apply.html', {}, context_instance=context)


def create(request):
    form = ProjectForm(request.POST or None, initial={'user': request.user})
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect(form.instance.get_absolute_url())
    user = request.user
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/create_arx_project.html', {}, context_instance=context)