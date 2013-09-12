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


testimonial_fieldsets = deepcopy(PageAdmin.fieldsets)
testimonial_fieldsets[0][1]["fields"].append('user')
testimonial_fieldsets[0][1]["fields"].remove('in_menus')
testimonial_fieldsets[0][1]["fields"].append('content')


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


class ActionGroupAdmin(DisplayableAdmin, OwnableAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets)

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "sfpirgapp.ActionGroup" in items:
                return True
        return False


class CategoryAdmin(DisplayableAdmin, OwnableAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets)

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "sfpirgapp.Category" in items:
                return True
        return False


admin.site.register(ActionGroup, ActionGroupAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)