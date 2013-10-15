from django.template.context import RequestContext
from django.shortcuts import render_to_response
from sfpirgapp.forms import OrganizationForm
from django.http.response import HttpResponseRedirect
import logging


log = logging.getLogger(__name__)


def get_org(request):
    if not request.user or request.user.is_anonymous:
        return None
    if not request.user.profile:
        return None
    return request.user.profile.organization


def organization(request):
    user = request.user
    org = get_org(request)
    form = OrganizationForm(request.POST or None,
                            instance=org,
                            initial={
                                'contact_name': user.get_full_name(),
                                'contact_email': user.email
                            })
    if request.method == 'POST' and form.is_valid():
        form.save()
        user.profile.organization = form.instance
        user.profile.save()
        return HttpResponseRedirect(request.GET.get('next'))
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/organization.html', {}, context_instance=context)
