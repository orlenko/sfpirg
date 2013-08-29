from mezzanine.core.fields import RichTextField
from mezzanine.pages.models import Page
from mezzanine.core.fields import FileField
from mezzanine.utils.models import upload_to


class NewsPost(Page):
    content = RichTextField(blank=True)

    class Meta:
        verbose_name = u'News Post'
        verbose_name_plural = u'News Posts'
