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


class ActionGroupCreateForm(forms.Form):
    def __init__(self, data, user):
        self.user = user
        self.initial = {}
        if user and not user.is_anonymous():
            self.initial = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'contact_name': user.get_full_name(),
                'contact_email': user.email,
            }
            if user.profile:
                self.initial['on_mailing_list'] = user.profile.on_mailing_list
        super(ActionGroupCreateForm, self).__init__(data, initial=self.initial)
        if user and not user.is_anonymous():
            self.fields['username'].widget = forms.HiddenInput()
            self.fields['first_name'].widget = forms.HiddenInput()
            self.fields['last_name'].widget = forms.HiddenInput()
            self.fields['email'].widget = forms.HiddenInput()
            self.fields['password1'].widget = forms.HiddenInput()
            self.fields['password1'].required = False
            self.fields['password2'].widget = forms.HiddenInput()
            self.fields['password2'].required = False
            if user.profile:
                self.fields['on_mailing_list'].widget = forms.HiddenInput()

    # User fields
    username = forms.CharField(label='Username',
                               max_length=30,
                               help_text='Required. 30 characters or fewer. Letters, numbers and '
                                         '@/./+/-/_ characters')
    first_name = forms.CharField(label='First Name', max_length=30, required=False)
    last_name = forms.CharField(label='Last Name', max_length=30, required=False)
    email = forms.EmailField(label='Email', max_length=75)
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="Password (again)",
                                widget=forms.PasswordInput(render_value=False))
    on_mailing_list = forms.BooleanField(label='Would you like to be added to our mailing list to receive periodic information about social and environmental justice happenings on and off campus?',
                                         required=False)

    # Account Group fields
    title = forms.CharField(label='Proposed Action Group Name')
    contact_name = forms.CharField(label='Main Contact Person', required=False)
    contact_email = forms.EmailField(label='Email', required=False)
    contact_phone = forms.CharField(label='Phone', required=False)
    group_email = forms.EmailField(label='Desired email address for Action Group', required=False)
    basis_of_unity = forms.CharField(widget=forms.TextInput(), label='General Basis of Unity / Objective', required=False)
    goals = forms.CharField(widget=forms.TextInput(), label='Main Goal(s)', required=False)
    timeline = forms.CharField(widget=forms.TextInput(), label='Plans and Timeline', required=False,
                               help_text='Specific Plans and timeline for the semester (please be as concrete as possible)')
    oneliner = forms.CharField(widget=forms.TextInput(),
                               label='One-liner for SFPIRG promotional materials',
                               required=False,
                               help_text='One-liner for SFPIRG promotional materials')
    twoliner = forms.CharField(widget=forms.TextInput(), label='One paragraph for SFPIRG website', required=False)
    potential_members = forms.CharField(widget=forms.TextInput(), label='Potential members of your group', required=False,
                                        help_text='Please include the members of your potential Action Group: (NAME, PHONE, EMAIL)')

    def clean_username(self):
        """
        Ensure the username doesn't exist or contain invalid chars.
        We limit it to slugifiable chars since it's used as the slug
        for the user's profile view.
        """
        username = self.cleaned_data.get("username")
        if username.lower() != slugify(username).lower():
            raise forms.ValidationError("Username can only contain letters, "
                                          "numbers, dashes or underscores.")
        lookup = {"username__iexact": username}
        try:
            User.objects.exclude(id=self.user.id).get(**lookup)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("This username is already registered")

    def clean_password2(self):
        """
        Ensure the password fields are equal, and match the minimum
        length defined by ``ACCOUNTS_MIN_PASSWORD_LENGTH``.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            errors = []
            if password1 != password2:
                errors.append("Passwords do not match")
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append("Password must be at least %s characters" %
                              settings.ACCOUNTS_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password1"] = self.error_class(errors)
        return password2

    def clean_email(self):
        """
        Ensure the email address is not already registered.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.exclude(id=self.user.id).filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError("This email is already registered")


    def save_user(self):
        if (not self.user) or self.user.is_anonymous():
            self.user = User.objects.create_user(username=self.cleaned_data['username'],
                                            first_name=self.cleaned_data['first_name'],
                                            last_name=self.cleaned_data['last_name'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password1'])
            self.user = authenticate(username=self.user.username,
                                    password=self.cleaned_data['password1'],
                                    is_active=True)
        if not self.user.profile:
            _profile = Profile.objects.create(user=self.user,
                        on_mailing_list=self.cleaned_data.get('on_mailing_list'))
        return self.user

    def save_action_group(self):
        return ActionGroup.objects.create(
            user=self.user,
            title=self.cleaned_data['title'],
            slug=slugify(self.cleaned_data['title']),
            category=_category_by_model(ActionGroup),
            contact_name=self.cleaned_data['contact_name'],
            contact_email=self.cleaned_data['contact_email'],
            contact_phone=self.cleaned_data['contact_phone'],
            group_email=self.cleaned_data['group_email'],
            basis_of_unity=self.cleaned_data['basis_of_unity'],
            goals=self.cleaned_data['goals'],
            timeline=self.cleaned_data['timeline'],
            oneliner=self.cleaned_data['oneliner'],
            twoliner=self.cleaned_data['twoliner'],
            potential_members=self.cleaned_data['potential_members'])

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
        exclude = ('slug', 'in_menus',)
        widgets = {
            'time_per_week': CKEditor(ckeditor_config='basic'),
            'support_method': CKEditor(ckeditor_config='basic'),
            'results_plan': CKEditor(ckeditor_config='basic'),
            'larger_goal': CKEditor(ckeditor_config='basic'),
            'researcher_qualities': CKEditor(ckeditor_config='basic'),
            'description_short': CKEditor(ckeditor_config='basic'),
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