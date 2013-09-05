from mezzanine.conf import settings
from copy import deepcopy
from django.contrib import admin
from .models import NewsPost
from mezzanine.core.admin import DisplayableAdmin
from mezzanine.core.admin import OwnableAdmin


class NewsAdmin(DisplayableAdmin, OwnableAdmin):
    fieldsets = deepcopy(DisplayableAdmin.fieldsets)

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "news.NewsPost" in items:
                return True
        return False


admin.site.register(NewsPost, NewsAdmin)
