from mezzanine.conf import settings
from copy import deepcopy

from django.contrib import admin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin

from .models import Event, EventType, EventImage
from mezzanine.core.admin import DisplayableAdmin


event_fieldsets = deepcopy(PageAdmin.fieldsets)
event_fieldsets[0][1]['fields'].remove('login_required')
event_fieldsets[0][1]['fields'].remove('status')
event_fieldsets[0][1]['fields'].remove(('publish_date', 'expiry_date'))
event_fieldsets[1][1]['fields'].append('status')
event_fieldsets[1][1]['fields'].append(('publish_date', 'expiry_date'))
event_fieldsets[0][1]["fields"].extend([
    "content", "start", "end", "type", "category", "location", "link_url",
    ])


class EventImageInline(TabularDynamicInlineAdmin):
    model = EventImage


class EventAdmin(DisplayableAdmin):
    inlines = (EventImageInline,)
    fieldsets = event_fieldsets

    def get_form(self, request, obj=None, **kwargs):
        """Don't require content even when status is published"""
        form = super(EventAdmin, self).get_form(request, obj, **kwargs)

        def clean_content(form):
            content = form.cleaned_data.get("content")
            return content

        form.clean_content = clean_content
        return form

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "calendar.Event" in items:
                return True
        return False

admin.site.register(Event, EventAdmin)
admin.site.register(EventType)
