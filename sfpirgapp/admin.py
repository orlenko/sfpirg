from copy import deepcopy

from django.contrib import admin

from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from sfpirgapp.models import (
    Testimonial,
    Profile,
    Category,
    MyImageField,
    Settings,
    ActionGroupRequest)
from mezzanine.pages.admin import PageAdmin
from sfpirgapp.models import ActionGroup
from sfpirgapp import settings
from sfpirgapp.models import Address
from sfpirgapp.models import Organization
from sfpirgapp.models import ProjectType
from sfpirgapp.models import ProjectSubject
from sfpirgapp.models import Project
from django.contrib.admin.options import ModelAdmin
from sfpirgapp.models import Application
from sfpirgapp.models import Liaison
from sfpirgapp.widgets import AdvancedFileInput


common_fieldsets = deepcopy(PageAdmin.fieldsets)
common_fieldsets[0][1]['fields'].append('content')
common_fieldsets[0][1]['fields'].remove('in_menus')

testimonial_fieldsets = deepcopy(common_fieldsets)
testimonial_fieldsets[0][1]['fields'].append('user')
testimonial_fieldsets[0][1]['fields'].append('category')
testimonial_fieldsets[0][1]['fields'].append('author_full_name')
testimonial_fieldsets[0][1]['fields'].append('author_title')
testimonial_fieldsets[0][1]['fields'].append('author_email')


class TestimonialAdmin(DisplayableAdmin, OwnableAdmin):
    fieldsets = testimonial_fieldsets

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "sfpirgapp.Testimonial" in items:
                return True
        return False


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Profile',
         {'fields': ['user', 'date_of_birth', 'bio', 'photo']}),
    )
    list_display = ['user', 'date_of_birth']
    list_filter = []
    formfield_overrides = {
        MyImageField: {'widget': AdvancedFileInput},
    }

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "sfpirgapp.Profile" in items:
                return True
        return False


action_group_fieldsets = deepcopy(common_fieldsets)
action_group_fieldsets[0][1]['fields'].extend([
    'user',
    'category',
    'announcements',
    'meetings',
    'contact_email',
    'contact_phone',
    'links',
    'facebook_url',
    'twitter',
    'google_plus_url',
    'mailing_list_url',
    'is_approved',
    'in_menus',
])


class ActionGroupAdmin(DisplayableAdmin, OwnableAdmin):
    fieldsets = action_group_fieldsets

    list_display = ['title', 'user', 'is_approved']
    list_editable = ['is_approved']
    list_filter = ['is_approved']

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "sfpirgapp.ActionGroup" in items:
                return True
        return False


class CategoryAdmin(DisplayableAdmin, OwnableAdmin):
    fieldsets = common_fieldsets

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "sfpirgapp.Category" in items:
                return True
        return False


class AddressAdmin(ModelAdmin):
    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "sfpirgapp.Address" in items:
                return True
        return False


class ProjectAdmin(ModelAdmin):
    list_display = ['title', 'admin_thumb', 'user', 'organization_title', 'is_submitted', 'is_approved', 'is_underway', 'is_finished', 'is_completed_successfully']
    list_filter = ['user', 'is_submitted', 'is_approved', 'is_underway', 'is_finished', 'is_completed_successfully']
    list_editable = ['is_approved', 'is_underway', 'is_finished', 'is_completed_successfully']
    formfield_overrides = {
        MyImageField: {'widget': AdvancedFileInput},
    }


class SettingsAdmin(ModelAdmin):
    list_display = ['name', 'value']
    list_editable = ['value']


class ActionGroupRequestAdmin(ModelAdmin):
    list_display = ['title', 'contact_person', 'contact_email', 'is_processed']
    list_filter = ['is_processed']
    list_editable = ['is_processed']


admin.site.register(ActionGroup, ActionGroupAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Address)
admin.site.register(Organization)
admin.site.register(ProjectType)
admin.site.register(ProjectSubject)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Application)
admin.site.register(Liaison)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(ActionGroupRequest, ActionGroupRequestAdmin)
