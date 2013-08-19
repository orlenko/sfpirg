import random
from urllib import quote, unquote
from django.template import Context, TemplateSyntaxError, Variable
from django.template.loader import get_template
from django.core.files.storage import default_storage
from mezzanine.conf import settings
from mezzanine import template
import logging
import traceback

from sfpirgapp import models
from django.core.files.base import File
import os

# Try to import PIL in either of the two ways it can end up installed.
try:
    from PIL import Image, ImageFile, ImageOps
except ImportError:
    import Image
    import ImageFile
    import ImageOps


log = logging.getLogger(__name__)

register = template.Library()


@register.render_tag
def sfpirg_random_testimonial(context, token):
    all_testimonials = models.Testimonial.objects.all()
    count = len(all_testimonials)
    if count:
        index = random.randint(0, count-1)
        testimonial = all_testimonials[index]
        log.debug('Processing testimonial: %s' % testimonial)
        context['testimonial'] = testimonial
    else:
        context['testimonial'] = {}
    t = get_template('sfpirg/testimonial_block.html')
    return t.render(Context(context))


@register.simple_tag
def sfpirg_thumbnail(image_url, width, height, quality=95):
    """
    Given the URL to an image, resizes the image using the given width and
    height on the first time it is requested, and returns the URL to the new
    resized image.

    Aspect ratio is always preserved - so, if width/height do not match original aspect ratio,
    the image will be resized so that one side is equal to the target dimention, and the other will be larger.

    This is useful for cases when we need to fill a rectangle with a resized image,
    and the source images have unpredictable aspect ratio.
    """
    if not image_url:
        return ""

    image_url = unquote(unicode(image_url))
    if image_url.startswith(settings.MEDIA_URL):
        image_url = image_url.replace(settings.MEDIA_URL, "", 1)
    image_dir, image_name = os.path.split(image_url)
    image_prefix, image_ext = os.path.splitext(image_name)
    filetype = {".png": "PNG", ".gif": "GIF"}.get(image_ext, "JPEG")
    thumb_name = "%s-ar-%sx%s%s" % (image_prefix, width, height, image_ext)
    thumb_dir = os.path.join(settings.MEDIA_ROOT, image_dir,
                             settings.THUMBNAILS_DIR_NAME)
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    thumb_path = os.path.join(thumb_dir, thumb_name)
    thumb_url = "%s/%s" % (settings.THUMBNAILS_DIR_NAME,
                           quote(thumb_name.encode("utf-8")))
    image_url_path = os.path.dirname(image_url)
    if image_url_path:
        thumb_url = "%s/%s" % (image_url_path, thumb_url)

    try:
        thumb_exists = os.path.exists(thumb_path)
    except UnicodeEncodeError:
        # The image that was saved to a filesystem with utf-8 support,
        # but somehow the locale has changed and the filesystem does not
        # support utf-8.
        from mezzanine.core.exceptions import FileSystemEncodingChanged
        raise FileSystemEncodingChanged()
    if thumb_exists:
        # Thumbnail exists, don't generate it.
        return thumb_url
    elif not default_storage.exists(image_url):
        # Requested image does not exist, just return its URL.
        return image_url

    f = default_storage.open(image_url)
    try:
        image = Image.open(f)
    except:
        # Invalid image format
        return image_url

    image_info = image.info
    width = int(width)
    height = int(height)

    # If already right size, don't do anything.
    if width == image.size[0] or height == image.size[1]:
        return image_url
    # Set dimensions.
    if width and height:
        #print 'Both dimensions of %s are specified' % image_url
        if float(height) / width < float(image.size[1]) / image.size[0]:
            #print 'Original image is tall and slim, will resize by width only'
            height = 0
        else:
            #print 'Original image is wide and short, will resize by height only'
            #print 'Because %s is less than %s' % (float(image.size[1]) / image.size[0],
            #    float(height) / width)
            width = 0
    if not width:
        width = int(round(float(image.size[0]) * height / image.size[1]))
    elif not height:
        height = int(round(float(image.size[1]) * width / image.size[0]))

    if image.mode not in ("P", "L", "RGBA"):
        image = image.convert("RGBA")
    # Required for progressive jpgs.
    ImageFile.MAXBLOCK = image.size[0] * image.size[1]
    try:
        image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
        image = image.save(thumb_path, filetype, quality=quality, **image_info)
        # Push a remote copy of the thumbnail if MEDIA_URL is
        # absolute.
        if "://" in settings.MEDIA_URL:
            with open(thumb_path, "r") as f:
                default_storage.save(thumb_url, File(f))
    except Exception:
        # If an error occurred, a corrupted image may have been saved,
        # so remove it, otherwise the check for it existing will just
        # return the corrupted image next time it's requested.
        #print 'Failed to convert image! Error: %s' %  traceback.format_exc()
        try:
            os.remove(thumb_path)
        except Exception:
            #print 'Failed to remove thumbnail! Error: %s' %  traceback.format_exc()
            pass
        return image_url
    return thumb_url