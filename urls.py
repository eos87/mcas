from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from mcas.settings import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'index1.html'}),
    (r'^index/$', direct_to_template, {'template': 'index.html'}),
    (r'^', include('mcas.encuesta.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns('',
                (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': PROJECT_DIR + '/files'}),
                )
