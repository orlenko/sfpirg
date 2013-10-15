import random
from urllib import quote, unquote
from django.template import Context
from django.template.loader import get_template
from django.core.files.storage import default_storage
from mezzanine.conf import settings
from mezzanine import template
import logging

from sfpirgapp import models
from django.core.files.base import File
import os
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from django.template.base import Variable
from mezzanine.pages.models import Page
from sfpirgapp.models import (ActionGroup,  # @UnusedImport - actually used through globals()
    Testimonial, Project, Organization)  # @UnusedImport - actually used through globals()
from news.models import NewsPost  # @UnusedImport - actually used through globals()
from mezzanine.calendar.models import Event  # @UnusedImport - actually used through globals()

# Try to import PIL in either of the two ways it can end up installed.
try:
    from PIL import Image, ImageFile, ImageOps
except ImportError:
    import Image
    import ImageFile
    import ImageOps


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

register = template.Library()


@register.render_tag
def sfpirg_random_testimonial(context, token):
    log.debug('Creating a random testimonial block')
    all_testimonials = models.Testimonial.objects.filter(status=CONTENT_STATUS_PUBLISHED)
    count = len(all_testimonials)
    if count:
        index = random.randint(0, count-1)
        testimonial = all_testimonials[index]
        log.debug('Processing testimonial: %s' % testimonial)
        context['testimonial'] = testimonial
    else:
        context['testimonial'] = {
            'user': {
                'first_name': '',
                'last_name': '',
                'username': '',
                'get_full_name': '',
                'profile': {
                    'title': '',
                    'photo': ''
                }
            },
            'content': ''
        }
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
        print 'Both dimensions of %s are specified' % image_url
        if float(height) / width < float(image.size[1]) / image.size[0]:
            print 'Original image is tall and slim, will resize by width only'
            height = 0
        else:
            print 'Original image is wide and short, will resize by height only'
            print 'Because %s is less than %s' % (float(image.size[1]) / image.size[0],
                                                  float(height) / width)
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


@register.render_tag
def sfpirg_pagination(context, token):
    parts = token.split_contents()[1:]
    for part in parts:
        recordlist = Variable(part).resolve(context)
        break
    context['recordlist'] = recordlist
    t = get_template('include/pagination.html')
    return t.render(Context(context))


@register.render_tag
def action_group_slider(context, token):
    action_groups = models.ActionGroup.objects.all().order_by('title')[:200]
    sixes = []
    six = []
    for ag in action_groups:
        six.append(ag)
        if len(six) == 6:
            sixes.append(six)
            six = []
    if six:
        sixes.append(six)
    context['sixes'] = sixes
    t = get_template('sfpirg/action-group-slider.html')
    return t.render(Context(context))


@register.render_tag
def sfpirg_side_menu(context, token):
    links = []
    page = context.get('page')
    if page:
        if page.category:
            links.append((page.category.get_absolute_url(), page.category.title))
        elif page.parent:
            links.append((page.parent.get_absolute_url(), page.parent.title))
            for child in page.parent.children.all():
                links.append((child.get_absolute_url(), child.title))
        else:
            for child in page.children.all():
                links.append((child.get_absolute_url(), child.title))
    if not links:
        for page in Page.objects.published(for_user=context["request"].user).order_by('_order'):
            if page.in_menu_template('menus/side.html'):
                links.append((page.get_absolute_url(), page.title))
    context['links'] = links
    return get_template('sfpirg/side_menu.html').render(Context(context))


@register.render_tag
def projects_slider(context, token):
    pages = []
    for page in Page.objects.published(for_user=context["request"].user).order_by('_order'):
        if page.in_menu_template('menus/projects.html'):
            pages.append(page)
    context['pages'] = pages
    return get_template('sfpirg/projects_slider.html').render(Context(context))


@register.filter
def proj_lines_class(title):
    charcount = len(title)
    linelen = 6
    if charcount < 2 * linelen:
        return 'oneline'
    if charcount < 3 * linelen:
        return 'twoline'
    if charcount < 4 * linelen:
        return 'threeline'
    return 'fourline'


@register.filter
def category_slug(model_name):
    model = globals().get(model_name)
    if not model:
        return ''
    allrecs = model.objects.all()
    if not allrecs:
        return ''
    return allrecs[0].category.slug


@register.render_tag
def sfpirg_show_plus_field(context, token):
    parts = token.split_contents()[1:]
    form = None
    field = None
    for part in parts:
        if not field:
            field = Variable(part).resolve(context)
            continue
        if not form:
            form = Variable(part).resolve(context)
            break
    plusable = getattr(form.Meta, 'plusable', {}).get(field.name)
    if plusable:
        context['form'] = form
        context['field'] = field
        model_name = plusable['model']
        context['model_class'] = globals()[model_name]
        return get_template('sfpirg/plus_field.html').render(Context(context))
    return ''


@register.render_tag
def sfpirg_bottom_menu(context, token):
    published = Page.objects.published(for_user=context["request"].user)
    pages = []
    for page in published.order_by("_order"):
        if page.in_menu_template('menus/bottom.html'):
            pages.append(page)
    context['pages'] = pages
    return get_template('menus/bottom.html').render(Context(context))


@register.inclusion_tag('include/field.html', takes_context=True)
def sfpirg_field(context, field):
    log.debug('Field: %r' % field)
    context['field'] = field
    return context
