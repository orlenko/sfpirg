from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from sfpirgapp.models import Project
from sfpirgapp.forms import ProjectForm
from django.http.response import HttpResponseRedirect


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
            form = ProjectForm(instance=project)
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/project.html', {}, context_instance=context)


def create(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect(form.instance.get_absolute_url())
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/create_arx_project.html', {}, context_instance=context)