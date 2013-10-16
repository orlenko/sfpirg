import logging

from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput

from sfpirgapp.models import (Application, Liaison, Organization, Project,
    ActionGroup)
from sfpirgapp.widgets import SelectWithPopUp, AdvancedFileInput


log = logging.getLogger(__name__)


class ActionGroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActionGroupForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = 'Action Group Description'

    def save(self, *args, **kwargs):
        self.data['status'] = self.data['is_approved'] == 'True' and 2 or 1
        return super(ActionGroupForm, self).save(*args, **kwargs)

    class Meta:
        model = ActionGroup
        exclude = ('keywords',)
        widgets = {
            'status': HiddenInput(),
            'user': HiddenInput(),
            'category': HiddenInput(),
            'featured_image': AdvancedFileInput(),
            'is_approved': HiddenInput(),
            'slug': HiddenInput(),
            '_meta_title': HiddenInput(),
            'description': HiddenInput(),
            'gen_description': HiddenInput(),
            'keywords': HiddenInput(),
            'short_url': HiddenInput(),
            'publish_date': HiddenInput(),
            'expiry_date': HiddenInput(),
            'in_sitemap': HiddenInput(),
            'theme_color': HiddenInput(),
            '_order': HiddenInput(),
            'login_required': HiddenInput(),
        }


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
            'user': HiddenInput(),
            'category': HiddenInput(),
            'is_draft': HiddenInput(),
            'is_approved': HiddenInput(),
        }


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ('timestamp', )


class MultiApplicationForm(forms.Form):
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea())


class OrganizationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Organization Name'

    class Meta:
        model = Organization
        widgets = {
            'slug': forms.HiddenInput(),
        }


class LiaisonForm(ModelForm):
    class Meta:
        model = Liaison