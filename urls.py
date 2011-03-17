from django.conf.urls.defaults import *
from mcas.settings import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',    
    (r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns('',
                (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': PROJECT_DIR + '/files'}),
                )
