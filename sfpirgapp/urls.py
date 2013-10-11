
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

    url('^news/(?P<news>.*)/$', 'sfpirgapp.views.newsposts.newspost', {}, name='news-post'),

    url('^events/(?P<event>.*)/$', 'sfpirgapp.views.events.event', {}, name='event'),

    url(r'^arx/project/toggle-selection/(?P<project>\d+)/$', 'sfpirgapp.views.arx.toggle_project_selection', {}, name='arx-toggle'),
    url('^arx/project/create/$', 'sfpirgapp.views.arx.create', {}, name='arx-project-create'),
    url('^arx/apply/$', 'sfpirgapp.views.arx.multi_apply', {}, name='arx-apply'),
    url('^arx/project/(?P<slug>[^/]*)/apply/$', 'sfpirgapp.views.arx.project_apply', {}, name='arx-project-apply'),
    url('^arx/project/(?P<slug>[^/]*)/$', 'sfpirgapp.views.arx.project', {}, name='arx-project'),

    url('^actiongroups/(?P<slug>.*)/$', 'sfpirgapp.views.actiongroups.actiongroup', {}, name='action-group'),

    url('^category/(?P<slug>.*)/$', 'sfpirgapp.views.category.category', {}, name='category'),

    url('^add/(?P<model_name>.*)/$', 'sfpirgapp.views.add_new_model'),

    ("^", include("mezzanine.urls")),

)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
