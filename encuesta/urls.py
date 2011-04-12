from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('mcas.encuesta.views',
    (r'^consultar/$', 'consultar'),
    (r'^indicadores/$', 'indicadores'),
    (r'^familia/jefe/$', 'familia_jefe'),
    (r'^familia/vivecon/$', 'familia_vivecon'),
    
    (r'^ajax/munis/$', 'get_munis'),
    (r'^ajax/comunies/$', 'get_comunies'),
#    (r'^indicadores/$', 'indicadores'),
#    (r'^lista/$', 'lista'),
#    (r'^lista/(?P<id>\d+)/$', 'lista'),
#    (r'^proyecto/(?P<id>\d+)/$', 'proyecto'),
#    (r'^organizacion/(?P<id>\d+)/$', 'organizacion'),
#    (r'^indicadores/(?P<vista>[-\w]+)/$', '_get_view'),
#    (r'^indicadores/meta/(?P<slug>[-\w]+)/$', 'meta'),
)


