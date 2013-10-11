from copy import deepcopy

from django.contrib import admin

from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from sfpirgapp.models import (
    Testimonial,
    Profile,
    Category,
)
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


common_fieldsets = deepcopy(PageAdmin.fieldsets)
common_fieldsets[0][1]['fields'].append('content')
common_fieldsets[0][1]['fields'].remove('in_menus')

testimonial_fieldsets = deepcopy(common_fieldsets)
testimonial_fieldsets[0][1]['fields'].append('user')
testimonial_fieldsets[0][1]['fields'].append('category')


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

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "sfpirgapp.Profile" in items:
                return True
        return False


action_group_fieldsets = deepcopy(common_fieldsets)
action_group_fieldsets[0][1]['fields'].append('category')


class ActionGroupAdmin(DisplayableAdmin, OwnableAdmin):
    fieldsets = action_group_fieldsets

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


admin.site.register(ActionGroup, ActionGroupAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Address)
admin.site.register(Organization)
admin.site.register(ProjectType)
admin.site.register(ProjectSubject)
admin.site.register(Project)
admin.site.register(Application)
admin.site.register(Liaison)