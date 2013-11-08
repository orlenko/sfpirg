from ckeditor.widgets import CKEditor
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.forms.widgets import DateInput
from django.forms.widgets import HiddenInput
from django.utils.text import slugify
from mezzanine.conf import settings
from sfpirgapp.models import (Application, Liaison, Organization, Project,
    ActionGroup, Testimonial)
from sfpirgapp.models import Profile
from sfpirgapp.templatetags.sfpirg_tags import _category_by_model
from sfpirgapp.widgets import SelectWithPopUp, AdvancedFileInput
import logging
from sfpirgapp.models import ActionGroupRequest
from sfpirgapp.models import ProjectType
from sfpirgapp.models import ProjectSubject


log = logging.getLogger(__name__)


class ActionGroupRequestForm(ModelForm):
    class Meta:
        model = ActionGroupRequest
        exclude = ('is_processed',)


class ActionGroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActionGroupForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = 'Action Group Description'

    class Meta:
        model = ActionGroup
        exclude = ('keywords', 'in_menus', 'goals', 'timeline', 'oneliner', 'twoliner', 'potential_members', 'links')
        widgets = {
            'content': CKEditor(ckeditor_config='basic'),
            'announcements': CKEditor(ckeditor_config='basic'),
            'meetings': CKEditor(ckeditor_config='basic'),
            'links': CKEditor(ckeditor_config='basic'),
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
            'in_menus': HiddenInput(),
        }


class ProjectForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = (
            '(Please keep the title clear, short and descriptive. Keep in mind that the title should indicate '
            'what the project is actually about and it should be something that will attract a student\'s '
            'interest. Avoid acronyms).')
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
        exclude = ('slug', 'in_menus',)
        widgets = {
            'time_per_week': CKEditor(ckeditor_config='basic'),
            'support_method': CKEditor(ckeditor_config='basic'),
            'results_plan': CKEditor(ckeditor_config='basic'),
            'larger_goal': CKEditor(ckeditor_config='basic'),
            'researcher_qualities': CKEditor(ckeditor_config='basic'),
            'description_short': HiddenInput(),
            'size': HiddenInput(),
            'description_long': CKEditor(ckeditor_config='basic'),
            'liaison': SelectWithPopUp('Liaison'),
            'user': HiddenInput(),
            'category': HiddenInput(),
            'is_submitted': HiddenInput(),
            'is_approved': HiddenInput(),
            'is_underway': HiddenInput(),
            'is_finished': HiddenInput(),
            'is_completed_successfully': HiddenInput(),
            'date_start': DateInput(),
        }


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ('timestamp', )


class MultiApplicationForm(forms.Form):
    name = forms.CharField(label='Your Name')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea())


class OrganizationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Organization Name'

    class Meta:
        model = Organization
        widgets = {
            'slug': forms.HiddenInput(),
            'mandate': CKEditor(ckeditor_config='basic'),
            'communities': CKEditor(ckeditor_config='basic'),
            'sources_of_funding': CKEditor(ckeditor_config='basic'),
        }


class LiaisonForm(ModelForm):
    class Meta:
        model = Liaison


class TestimonialForm(ModelForm):
    class Meta:
        model = Testimonial
        exclude = ('keywords', 'in_menus',)
        widgets = {
            'content': CKEditor(ckeditor_config='basic'),
            'announcements': CKEditor(ckeditor_config='basic'),
            'meetings': CKEditor(ckeditor_config='basic'),
            'links': CKEditor(ckeditor_config='basic'),
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
            'in_menus': HiddenInput(),
        }


class ActionGroupFilterForm(forms.Form):
    pass


class ArxFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ArxFilterForm, self).__init__(*args, **kwargs)
        self.fields['project_type'].choices = [(rec.id, rec.title) for rec in ProjectType.objects.all()]
        self.fields['project_subject'].choices = [(rec.id, rec.title) for rec in ProjectSubject.objects.all()]

    project_type = forms.MultipleChoiceField(required=False)
    project_subject = forms.MultipleChoiceField(label='Project Issues', required=False)
