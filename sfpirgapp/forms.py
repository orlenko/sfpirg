from sfpirgapp.models import Project
from django.forms.models import ModelForm
from sfpirgapp.models import Application
from sfpirgapp.models import Organization
from sfpirgapp.widgets import SelectWithPopUp
from sfpirgapp.models import Liaison
import logging
from django.forms.widgets import TextInput
from django.forms.widgets import Select


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

    class Meta:
        model = Project
        exclude = ('slug',)
        widgets = {
            'liaison': SelectWithPopUp('Liaison'),
            'user': Select(attrs={'readonly': 'readonly'})
        }


class ApplicationForm(ModelForm):

    class Meta:
        model = Application
        exclude = ('timestamp', )


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        widgets = {
            'contact': SelectWithPopUp('Contact'),
            'mailing_address': SelectWithPopUp('Address'),
        }


class LiaisonForm(ModelForm):
    class Meta:
        model = Liaison
        widgets = {
           'organization': SelectWithPopUp('Organization'),
        }