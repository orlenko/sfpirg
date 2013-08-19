from copy import deepcopy

from django.contrib import admin

from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from sfpirgapp.models import (
    Testimonial,
    Profile
)


testimonial_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
testimonial_fieldsets[0][1]["fields"].extend(["user", "content", ])
testimonial_list_display = ["title", "user", "status", "admin_link"]
testimonial_fieldsets = list(testimonial_fieldsets)
resource_list_filter = deepcopy(DisplayableAdmin.list_filter)


class TestimonialAdmin(DisplayableAdmin, OwnableAdmin):
    fieldsets = testimonial_fieldsets
    list_display = testimonial_list_display
    list_filter = resource_list_filter

#     class Media:
#         css = {
#              'all': ('/static/css/admin.css',)
#         }

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Profile',
         {'fields': ['user', 'date_of_birth', 'bio', 'photo']}),
    )
    list_display = ['user', 'date_of_birth']
    list_filter = []


admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Profile, ProfileAdmin)