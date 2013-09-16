from django.db import models
from mezzanine.utils.models import AdminThumbMixin
from mezzanine.utils.models import upload_to
from mezzanine.core.fields import FileField
from django.contrib.auth.models import User
from mezzanine.core.models import Displayable, Orderable, RichText, Ownable
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.related import ForeignKey


class PageLike(Orderable, Displayable, RichText, AdminThumbMixin):
    titles = models.CharField(editable=False, max_length=1000, null=True)
    login_required = models.BooleanField(_("Login required"),
        default=False,
        help_text=_("If checked, only logged in users can view this page"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("images", "images"),
        format="Image", max_length=255, null=True, blank=True)
    admin_thumb_field = "featured_image"

    class Meta:
        abstract = True



class Profile(models.Model, AdminThumbMixin):
    user = models.OneToOneField(User)
    date_of_birth = models.DateField(null=True)
    title = models.CharField(null=True, max_length=255)
    bio = models.TextField(null=True)
    photo = FileField(verbose_name="Photo",
        upload_to=upload_to("sfpirgapp.Profile.photo", "photos"),
        format="Image", max_length=255, null=True, blank=True,
        help_text='User photo')
    admin_thumb_field = "photo"


class Testimonial(PageLike, Ownable):
    category = ForeignKey('Category', related_name='testimonials')

    @models.permalink
    def get_absolute_url(self):
        return ('testimonial', (), {'slug': self.slug})



class DummyTable(models.Model):
    pass


def DummyEmptyResultSet():
    return DummyTable.objects.filter(pk=-1)


class Category(PageLike, Ownable):
    class Meta:
        verbose_name = u'Category'
        verbose_name_plural = u'Categories'

    @models.permalink
    def get_absolute_url(self):
        return ('category', (), {'slug': self.slug})


class ActionGroup(PageLike, Ownable):
    parent = None # To make it compatible with the side_menu template
    children = DummyEmptyResultSet() # To make it compatible with the side_menu template

    category = ForeignKey(Category, related_name='action_groups')

    @models.permalink
    def get_absolute_url(self):
        return ('action-group', (), {'slug': self.slug})
