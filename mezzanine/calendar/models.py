import os

from cStringIO import StringIO
from string import punctuation
from urllib import unquote
from zipfile import ZipFile

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import RichTextField, FileField
from mezzanine.core.models import SiteRelated, Orderable
from mezzanine.pages.models import Page
from mezzanine.utils.importing import import_dotted_path
from mezzanine.utils.models import upload_to

EVENTS_UPLOAD_DIR = "galleries"
if settings.PACKAGE_NAME_FILEBROWSER in settings.INSTALLED_APPS:
    fb_settings = "%s.settings" % settings.PACKAGE_NAME_FILEBROWSER
    try:
        EVENTS_UPLOAD_DIR = import_dotted_path(fb_settings).DIRECTORY
    except ImportError:
        pass


class Event(Page):
    content = RichTextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey('calendar.EventType', blank=True, null=True)
    zip_import = models.FileField(verbose_name=_("Zip import"),
                                  blank=True,
                                  null=True,
                    upload_to=upload_to("calendar.Event.zip_import", "events"),
                    help_text=_("Upload a zip file containing images, and "
                                  "they'll be imported into this event."))

    class Meta:
        verbose_name = u'Event'
        verbose_name_plural = u'Events'

    def save(self, delete_zip_import=True, *args, **kwargs):
        """
        If a zip file is uploaded, extract any images from it and add
        them to the gallery, before removing the zip file.
        """
        super(Event, self).save(*args, **kwargs)
        if self.zip_import:
            zip_file = ZipFile(self.zip_import)
            # import PIL in either of the two ways it can end up installed.
            try:
                from PIL import Image
            except ImportError:
                import Image
            for name in zip_file.namelist():
                data = zip_file.read(name)
                try:
                    image = Image.open(StringIO(data))
                    image.load()
                    image = Image.open(StringIO(data))
                    image.verify()
                except:
                    continue
                path = os.path.join(EVENTS_UPLOAD_DIR, self.slug,
                                    name.decode("utf-8"))
                try:
                    saved_path = default_storage.save(path, ContentFile(data))
                except UnicodeEncodeError:
                    from warnings import warn
                    warn("A file was saved that contains unicode "
                         "characters in its path, but somehow the current "
                         "locale does not support utf-8. You may need to set "
                         "'LC_ALL' to a correct value, eg: 'en_US.UTF-8'.")
                    path = os.path.join(EVENTS_UPLOAD_DIR, self.slug,
                                        unicode(name, errors="ignore"))
                    saved_path = default_storage.save(path, ContentFile(data))
                self.images.add(EventImage(file=saved_path))
            if delete_zip_import:
                zip_file.close()
                self.zip_import.delete(save=True)


class EventType(SiteRelated):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
        verbose_name = u'Event Type'
        verbose_name_plural = u'Event Types'

    def __unicode__(self):
        return self.name


class EventImage(Orderable):
    gallery = models.ForeignKey("calendar.Event", related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
                     upload_to=upload_to("calendar.EventImage.file", "events"))
    description = models.CharField(_("Description"), max_length=1000,
                                   blank=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.
        """
        if not self.id and not self.description:
            name = unquote(self.file.url).split("/")[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.description = name
        super(EventImage, self).save(*args, **kwargs)
