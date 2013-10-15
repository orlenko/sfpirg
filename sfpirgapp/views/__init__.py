from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.utils.html import escape
from django.forms.models import modelform_factory
from django.db.models.loading import get_models, get_app, get_apps
from django import forms
from sfpirgapp import forms as sfpirg_forms


@login_required
def add_new_model(request, model_name):
    if (model_name.lower() == model_name):
        normal_model_name = model_name.capitalize()
    else:
        normal_model_name = model_name

    current_user = request.user
    current_profile = current_user.profile
    current_organization = current_profile and current_profile.organization

    auto_fields = {
        'organization': current_organization,
    }

    app_list = get_apps()
    for app in app_list:
        for model in get_models(app):
            if model.__name__ == normal_model_name:
                # Try to get a form based on model, if you can.
                form = getattr(sfpirg_forms, '%sForm' % normal_model_name, None) or modelform_factory(model)

                if request.method == 'POST':
                    form = form(request.POST)
                    if form.is_valid():
                        try:
                            new_obj = form.save()
                        except forms.ValidationError, error:
                            new_obj = None

                        if new_obj:
                            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                                (escape(new_obj._get_pk_val()), escape(new_obj)))

                else:
                    form = form()
                for fieldname, field in form.fields.items():
                    if fieldname in auto_fields:
                        field.initial = auto_fields[fieldname]
                        field.widget = forms.HiddenInput()

                page_context = {'form': form, 'field': normal_model_name}
                return render_to_response('popup.html', page_context, context_instance=RequestContext(request))