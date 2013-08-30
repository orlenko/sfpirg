
from django.conf.urls import patterns, include, url
from django.contrib import admin

from mezzanine.core.views import direct_to_template


admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = patterns("",
    ("^admin/", include(admin.site.urls)),
    url("^$", "sfpirgapp.views.home.homepage", {}, name="home"),
    url('^testimonial/(?P<slug>.*)/$', 'sfpirgapp.views.testimonial.testimonial', {}, name='testimonial'),

    url('^news$', 'sfpirgapp.views.newsposts.newslist', {}, name='news-list'),
    url('^events$', 'sfpirgapp.views.events.eventslist', {}, name='events-list'),
    url('^arx$', 'sfpirgapp.views.arx.arxlist', {}, name='arx-list'),
    url('^action-groups$', 'sfpirgapp.views.actiongroups.aglist', {}, name='action-groups-list'),

    ("^", include("mezzanine.urls")),

)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
