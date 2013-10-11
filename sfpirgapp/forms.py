from sfpirgapp.models import Project
from django.forms.models import ModelForm
from sfpirgapp.models import Application
from sfpirgapp.models import Organization
from sfpirgapp.widgets import SelectWithPopUp
from sfpirgapp.models import Liaison
import logging
from django import forms
from django.forms.widgets import HiddenInput


log = logging.getLogger(__name__)


class ProjectForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        user = (self.instance.pk and self.instance.user) or kwargs.get('initial', {}).get('user')
        org = user and user.profile and user.profile.organization
        log.debug('Do we have an organization for this form? %s' % org)
        if org:
            qs = self.fields['liaison'].queryset
            self.fields['liaison'].queryset = qs.filter(organization=org)

    def set_parent_record(self, record):
        self.fields['user'].initial = record

    class Meta:
        model = Project
        exclude = ('slug',)
        widgets = {
            'liaison': SelectWithPopUp('Liaison'),
            'user': HiddenInput()
        }


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ('timestamp', )


class MultiApplicationForm(forms.Form):
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea())


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        widgets = {
            'mailing_address': SelectWithPopUp('Address'),
        }


class LiaisonForm(ModelForm):
    class Meta:
        model = Liaison