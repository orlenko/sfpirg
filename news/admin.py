from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import NewsPost


news_fieldsets = deepcopy(PageAdmin.fieldsets)


class NewsAdmin(PageAdmin):
    fieldsets = news_fieldsets


admin.site.register(NewsPost, NewsAdmin)
