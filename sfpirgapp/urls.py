
from django.conf.urls import patterns, include, url
from django.contrib import admin

from mezzanine.core.views import direct_to_template


admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^$', 'sfpirgapp.views.home.homepage', {}, name='home'),

    url(r'^testimonial/add/$', 'sfpirgapp.views.testimonial.add_testimonial', {}, name='add-testimonial'),
    url(r'^testimonial/random/$', 'sfpirgapp.views.testimonial.random_testimonial', {}, name='random-testimonial'),
    url(r'^testimonial/(?P<slug>.*)/$', 'sfpirgapp.views.testimonial.testimonial', {}, name='testimonial'),

    url(r'^news/(?P<news>.*)/$', 'sfpirgapp.views.newsposts.newspost', {}, name='news-post'),

    url(r'^events/(?P<event>.*)/$', 'sfpirgapp.views.events.event', {}, name='event'),

    url(r'^profile/organization/$', 'sfpirgapp.views.organization.organization', {}, name='organization'),
    url(r'^arx/project/toggle-selection/(?P<project>\d+)/$', 'sfpirgapp.views.arx.toggle_project_selection', {}, name='arx-toggle'),
    url(r'^arx/project/create/$', 'sfpirgapp.views.arx.create', {}, name='arx-project-create'),
    url(r'^arx/apply/$', 'sfpirgapp.views.arx.multi_apply', {}, name='arx-apply'),
    url(r'^arx/project/(?P<slug>[^/]*)/apply/$', 'sfpirgapp.views.arx.project_apply', {}, name='arx-project-apply'),
    url(r'^arx/project/(?P<slug>[^/]*)/$', 'sfpirgapp.views.arx.project', {}, name='arx-project'),

    url(r'^actiongroups/(?P<slug>.*)/$', 'sfpirgapp.views.actiongroups.actiongroup', {}, name='action-group'),
    url(r'^actiongroup/create/$', 'sfpirgapp.views.actiongroups.create', {}, name='action-group-create'),

    url(r'^category/(?P<slug>.*)/$', 'sfpirgapp.views.category.category', {}, name='category'),

    url(r'^add/(?P<model_name>.*)/$', 'sfpirgapp.views.add_new_model'),

    (r'^', include('mezzanine.urls')),

)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = 'mezzanine.core.views.page_not_found'
handler500 = 'mezzanine.core.views.server_error'
