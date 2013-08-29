from django.db import models
from django.contrib.auth.models import User
from mezzanine.core.models import Displayable
from mezzanine.core.models import Ownable
from mezzanine.core.models import RichText
from mezzanine.utils.models import AdminThumbMixin
from mezzanine.utils.models import upload_to
from mezzanine.core.fields import FileField


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


class Testimonial(Displayable, Ownable, RichText):

    @models.permalink
    def get_absolute_url(self):
        return ('testimonial', (), {"slug": self.slug})

