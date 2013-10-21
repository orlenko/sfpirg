from django.template.context import RequestContext
from django.shortcuts import render_to_response
from sfpirgapp.forms import OrganizationForm
from django.http.response import HttpResponseRedirect
import logging
from sfpirgapp.views.actiongroups import actiongroup
from mezzanine.utils.email import send_mail_template
from django.conf import settings
from sfpirgapp.models import Settings


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
        if not org:
            # This is a new organization!
            send_mail_template('Action Group Application Submitted: %s' % organization.title,
                   'sfpirg/email/arx_new_organization',
                   Settings.get_setting('SERVER_EMAIL'),
                   request.user.email,
                   context=locals(),
                   attachments=None,
                   fail_silently=settings.DEBUG,
                   addr_bcc=None)
        return HttpResponseRedirect(request.GET.get('next', '/'))
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/organization.html', {}, context_instance=context)
