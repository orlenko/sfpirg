import os

ADMIN_MENU_ORDER = (
    ('SFPIRG', (
      'sfpirgapp.Category',
      'sfpirgapp.Testimonial',
      'news.NewsPost',
      'calendar.Event',
      'calendar.EventType',
      'sfpirgapp.Settings',
    )),
    ('Action Groups',(
      'sfpirgapp.ActionGroup',
      'sfpirgapp.ActionGroupRequest',
    )),
    ('Action Research Exchange', (
      'sfpirgapp.Project',
      'sfpirgapp.ProjectType',
      'sfpirgapp.ProjectSubject',
      'sfpirgapp.Organization',
      'sfpirgapp.Address',
      'sfpirgapp.Liaison',
      'sfpirgapp.Application',
    )),
    ('Content', (
      #'sfpirgapp.Testimonial',
      'pages.Page',
      #'blog.BlogPost',
      'generic.ThreadedComment',
      ('Media Library', 'fb_browse'),
    )),
    ('Site', ('sites.Site', 'redirects.Redirect', 'conf.Setting')),
    ('Users', ('auth.User', 'auth.Group',)),
)


PAGE_MENU_TEMPLATES = (
    (1, 'Top navigation bar', 'menus/top.html'),
    (2, 'Right-hand sidebar', 'menus/side.html'),
    (3, 'Footer', 'menus/bottom.html'),
    (4, 'Front-page Slideshow', 'menus/slideshow.html'),
    (5, 'Projects Carousel', 'sfpirg/projects_slider.html'),
)

INLINE_EDITING_ENABLED = True
USE_SOUTH = True
ADMINS = (
    ('SFPIRG Admin', 'sfpirg@bjola.ca'),
)
SERVER_EMAIL = 'noreply@sfpirg.ca'
ARX_ADMIN_EMAIL = 'arx@sfpirg.ca'
ACTION_GROUPS_ADMIN_EMAIL = 'actiongroups@sfpirg.ca'
MANAGERS = ADMINS
TIME_ZONE = None
USE_TZ = False
LANGUAGE_CODE = 'en'
DEBUG = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SITE_ID = 1
SITE_TITLE = 'SFPIRG - Simon Fraser Public Interest Research Group'
USE_I18N = False
SECRET_KEY = '%(SECRET_KEY)s'
INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

AUTHENTICATION_BACKENDS = ('mezzanine.core.auth_backends.MezzanineBackend',)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip('/'))
MEDIA_URL = STATIC_URL + 'media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip('/').split('/'))
ROOT_URLCONF = '%s.urls' % PROJECT_DIRNAME
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)
AUTH_PROFILE_MODULE = 'sfpirgapp.profile'
GRAPPELLI_ADMIN_TITLE = 'SFPIRG'
GRAPPELLI_ADMIN_HEADLINE = 'SFPIRG'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'ckeditor',
    'mezzanine.boot',
    'mezzanine.conf',
    'mezzanine.core',
    'mezzanine.generic',
    #'mezzanine.blog',
    'mezzanine.forms',
    'mezzanine.pages',
    'mezzanine.galleries',
    'mezzanine.twitter',
    'mezzanine.accounts',
    'mezzanine.calendar',
    'news',
    'sfpirgapp'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.tz',
    'mezzanine.conf.context_processors.settings',
)

MIDDLEWARE_CLASSES = (
    'mezzanine.core.middleware.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'mezzanine.core.request.CurrentRequestMiddleware',
    'mezzanine.core.middleware.RedirectFallbackMiddleware',
    'mezzanine.core.middleware.TemplateForDeviceMiddleware',
    'mezzanine.core.middleware.TemplateForHostMiddleware',
    'mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware',
    'mezzanine.core.middleware.SitePermissionMiddleware',
    # Uncomment the following if using any of the SSL settings:
    # 'mezzanine.core.middleware.SSLRedirectMiddleware',
    'mezzanine.pages.middleware.PageMiddleware',
    'mezzanine.core.middleware.FetchFromCacheMiddleware',
)

PACKAGE_NAME_FILEBROWSER = 'filebrowser_safe'
PACKAGE_NAME_GRAPPELLI = 'grappelli_safe'

OPTIONAL_APPS = (
    'debug_toolbar',
    'django_extensions',
    'compressor',
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}


CKEDITOR_CONFIGS = {
    'default': {
        'toolbarGroups':  [
            { 'name': 'clipboard',   'groups': [ 'clipboard', 'undo' ] },
            { 'name': 'editing',     'groups': [ 'find', 'selection', 'spellchecker' ] },
            { 'name': 'links' },
            { 'name': 'insert' },
            { 'name': 'forms' },
            { 'name': 'tools' },
            { 'name': 'document',       'groups': [ 'mode', 'document', 'doctools' ] },
            { 'name': 'others' },
            '/',
            { 'name': 'basicstyles', 'groups': [ 'basicstyles', 'cleanup' ] },
            { 'name': 'paragraph',   'groups': [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
            { 'name': 'styles' },
            { 'name': 'colors' },
            { 'name': 'about' }
        ],
        'width': 692,
        'height': 300,
        'allowedContent': True,
    },
    'basic': {
        'toolbar': 'Basic',
        'toolbarGroups': [
           # { 'name': 'clipboard',   'groups': [ 'clipboard', 'undo' ] },
           # { 'name': 'editing',     'groups': [ 'find', 'selection', 'spellchecker' ] },
            { 'name': 'links' },
           # { 'name': 'insert' },
           # { 'name': 'forms' },
           # { 'name': 'tools' },
           # { 'name': 'document',       'groups': [ 'mode', 'document', 'doctools' ] },
           # { 'name': 'others' },
           # '/',
            { 'name': 'basicstyles', 'groups': [ 'basicstyles', 'cleanup' ] },
           # { 'name': 'paragraph',   'groups': [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
           # { 'name': 'styles' },
           # { 'name': 'colors' },
           # { 'name': 'about' }
        ],
        'width': '100%',
        'height': 300,
        'allowedContent': True,
    }
}
RICHTEXT_WIDGET_CLASS = 'ckeditor.widgets.CKEditor'

try:
    from local_settings import *
except ImportError:
    pass

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
