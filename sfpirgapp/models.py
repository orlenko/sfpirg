from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from mezzanine.core.models import Displayable
from mezzanine.core.models import Ownable
from mezzanine.core.models import RichText
from mezzanine.utils.models import AdminThumbMixin
from mezzanine.utils.models import upload_to
from mezzanine.core.fields import FileField
from mezzanine.pages.fields import MenusField


class LikePageMixin(models.Model, AdminThumbMixin):
    in_menus = MenusField(_("Show in menus"), blank=True, null=True)
    titles = models.CharField(editable=False, max_length=1000, null=True)
    content_model = models.CharField(editable=False, max_length=50, null=True)
    login_required = models.BooleanField(_("Login required"),
        default=True,
        help_text=_("If checked, only logged in users can view this page"))

    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("images", "images"),
        format="Image", max_length=255, null=True, blank=True)
    admin_thumb_field = "featured_image"

    class Meta:
        abstract = True



class Profile(LikePageMixin):
    user = models.OneToOneField(User)
    date_of_birth = models.DateField(null=True)
    title = models.CharField(null=True, max_length=255)
    bio = models.TextField(null=True)
    photo = FileField(verbose_name="Photo",
        upload_to=upload_to("sfpirgapp.Profile.photo", "photos"),
        format="Image", max_length=255, null=True, blank=True,
        help_text='User photo')
    admin_thumb_field = "photo"


class Testimonial(Displayable, Ownable, RichText, LikePageMixin):
    pass


class ActionGroup(Displayable, RichText, LikePageMixin):
    pass


class Category(Displayable, RichText, LikePageMixin):
    class Meta:
        verbose_name = u'Category'
        verbose_name_plural = u'Categories'
