from sfpirgapp.models import Project
from django.forms.models import ModelForm
from sfpirgapp.models import Application


class ProjectForm(ModelForm):
    class Meta:
        model = Project


class ApplicationForm(ModelForm):

    class Meta:
        model = Application
        exclude = ('timestamp', )