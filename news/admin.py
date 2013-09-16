from mezzanine.conf import settings
from copy import deepcopy
from django.contrib import admin
from .models import NewsPost
from mezzanine.core.admin import DisplayableAdmin
from mezzanine.pages.admin import PageAdmin


common_fieldsets = deepcopy(PageAdmin.fieldsets)
common_fieldsets[0][1]['fields'].append('content')
common_fieldsets[0][1]['fields'].remove('in_menus')
common_fieldsets[0][1]['fields'].append('category')

class NewsAdmin(DisplayableAdmin):
    fieldsets = common_fieldsets

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "news.NewsPost" in items:
                return True
        return False


admin.site.register(NewsPost, NewsAdmin)
