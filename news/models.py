from mezzanine.core.fields import RichTextField
from mezzanine.pages.models import Page


class NewsPost(Page):
    content = RichTextField(blank=True)

    class Meta:
        verbose_name = u'News Post'
        verbose_name_plural = u'News Posts'
