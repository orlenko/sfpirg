from django.shortcuts import get_object_or_404
from sfpirgapp.models import Organization
from django.http.response import HttpResponseRedirect
from sfpirgapp.forms import OrganizationForm


def create(request):
    return ''



def edit(request, slug):
    organization = get_object_or_404(Organization, slug=slug)
    form = None
    if 'edit' in request.REQUEST:
        if request.method == 'POST':
            form = OrganizationForm(request.POST or None, instance=organization)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(organization.get_absolute_url())
        else:
            form = OrganizationForm(initial={'user': request.user,
                                        'liaison': organization.liason_set().first()},
                               instance=project)
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/arx_project.html', {}, context_instance=context)