from copy import deepcopy

from django.contrib import admin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin

from .models import Event, EventType, EventImage


event_fieldsets = deepcopy(PageAdmin.fieldsets)
event_fieldsets[0][1]['fields'].remove('in_menus')
event_fieldsets[0][1]['fields'].remove('login_required')
event_fieldsets[0][1]['fields'].remove('status')
event_fieldsets[0][1]['fields'].remove(('publish_date', 'expiry_date'))
event_fieldsets[1][1]['fields'].append('status')
event_fieldsets[1][1]['fields'].append(('publish_date', 'expiry_date'))
event_fieldsets[0][1]["fields"].extend([
    "content", "start", "end", "type", "zip_import", "in_menus", 'login_required'])


class EventImageInline(TabularDynamicInlineAdmin):
    model = EventImage


class EventAdmin(PageAdmin):
    inlines = (EventImageInline,)
    fieldsets = event_fieldsets

    def get_form(self, request, obj=None, **kwargs):
        """Don't require content even when status is published"""
        form = super(PageAdmin, self).get_form(request, obj, **kwargs)

        def clean_content(form):
            content = form.cleaned_data.get("content")
            return content

        form.clean_content = clean_content
        return form

admin.site.register(Event, EventAdmin)
admin.site.register(EventType)
