from django.conf.urls.defaults import *

urlpatterns = patterns('mcas.encuesta.views',
    (r'^$', 'index'),
    (r'^consultar/$', 'consultar'),
    (r'^indicadores/$', 'indicadores'),
    (r'^generales/$', 'generales'),
    (r'^familia/(?P<vista>[-\w]+)/$', '_get_view'),
    (r'^conocimiento/(?P<vista>[-\w]+)/$', '_get_view'),
    (r'^actitud/(?P<vista>[-\w]+)/$', '_get_view'),
    (r'^practica/(?P<vista>[-\w]+)/$', '_get_view'),
    (r'^estado-actual/(?P<vista>[-\w]+)/$', '_get_view'),
    (r'^percepcion/(?P<vista>[-\w]+)/$', '_get_view'),
    
    (r'^ajax/organi/$', 'get_organi'),
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


