from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.core.models import Displayable
from mezzanine.core.models import RichText
from mezzanine.core.fields import FileField
from django.db import models
from django.db.models.fields.related import ForeignKey
from mezzanine.pages.fields import MenusField
from django.conf import settings


class DummyTable(models.Model):
    pass


def DummyEmptyResultSet():
    return DummyTable.objects.filter(pk=-1)


class NewsPost(Displayable, RichText, AdminThumbMixin):
    featured_image = FileField(verbose_name="Featured Image",
        upload_to=upload_to("images", "images"),
        format="Image", max_length=255, null=True, blank=True)
    admin_thumb_field = "featured_image"
    login_required = models.BooleanField("Login required",
        default=False,
        help_text="If checked, only logged in users can view this page")
    parent = None # To make it compatible with the side_menu template
    children = DummyEmptyResultSet() # To make it compatible with the side_menu template
    category = ForeignKey('sfpirgapp.Category', related_name='news_posts')
    in_menus = MenusField("Show in menus", blank=True, null=True)

    @property
    def richtextpage(self):
        return self

    @models.permalink
    def get_absolute_url(self):
        return ('news-post', (), {'news': self.slug})

    def in_menu_template(self, template_name):
        if self.in_menus is not None:
            for i, l, t in settings.PAGE_MENU_TEMPLATES:
                if not unicode(i) in self.in_menus and t == template_name:
                    return False
        return True
