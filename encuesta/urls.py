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
    (r'^descarga/(?P<vista>[-\w]+)/$', '_get_view'),
    
    (r'^ajax/organi/$', 'get_organi'),
    (r'^ajax/munis/$', 'get_munis'),
    (r'^ajax/comunies/$', 'get_comunies'),
    #urls de descargas de word, pdf para familia
     (r'^vive.xls/$', 'vivencon_xls'),
     (r'^jefe.xls/$', 'familia_jefe_xls'),
     (r'^miembros.xls/$', 'familia_miembros_xls'),
     #conocimientos
     (r'^conocimiento_abuso.xls/$', 'conocimiento_abuso_xls'),
     (r'^conocimiento_lugar.xls/$', 'conocimiento_lugar_xls'),
     (r'^conocimiento_abusan_ninos.xls.xls/$', 'conocimiento_abusan_ninos_xls'),
     (r'^conocimiento_prevenir.xls/$', 'conocimiento_prevenir_xls'),
     (r'^conocimiento_leyes.xls/$', 'conocimiento_leyes_xls'),
     
#    (r'^indicadores/$', 'indicadores'),
#    (r'^lista/$', 'lista'),
#    (r'^lista/(?P<id>\d+)/$', 'lista'),
#    (r'^proyecto/(?P<id>\d+)/$', 'proyecto'),
#    (r'^organizacion/(?P<id>\d+)/$', 'organizacion'),
#    (r'^indicadores/(?P<vista>[-\w]+)/$', '_get_view'),
#    (r'^indicadores/meta/(?P<slug>[-\w]+)/$', 'meta'),
)


