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
     (r'^conocimiento_aprendio.xls/$', 'conocimiento_aprendio_xls'),
     (r'^conocimiento_informarse.xls/$', 'conocimiento_informarse_xls'),
     #Actitud
     (r'^actitud_abuso.xls/$', 'actitud_abuso_xls'),
     (r'^actitud_piensa.xls/$', 'actitud_piensa_xls'),
     (r'^actitud_victima.xls/$', 'actitud_victimas_xls'),
     (r'^actitud_familia.xls/$', 'actitud_familia_xls'),
     (r'^actitud_escuela.xls/$', 'actitud_escuela_xls'),
     #practica
     (r'^practica_situacion.xls/$', 'practica_situacion_xls'),
     (r'^practica_prevenir.xls/$', 'practica_prevenir_xls'),
     (r'^practica_participa_prevenir.xls/$', 'practica_participa_prevenir_xls'),
     (r'^practica_como.xls/$', 'practica_como_xls'),
     #estado actual
     (r'^estado_problema.xls/$', 'estado_problema_xls'),
     (r'^estado_problema_pais.xls/$', 'estado_problema_pais_xls'),
     (r'^estado_atencion.xls/$', 'estado_atencion_xls'),
     (r'^estado_lugares.xls/$', 'estado_lugares_xls'),
     (r'^estado_tipo_atencion.xls/$', 'estado_tipo_atencion_xls'),
     (r'^estado_donde.xls/$', 'estado_donde_xls'),
     #percepcion
     
     
     
#    (r'^indicadores/$', 'indicadores'),
#    (r'^lista/$', 'lista'),
#    (r'^lista/(?P<id>\d+)/$', 'lista'),
#    (r'^proyecto/(?P<id>\d+)/$', 'proyecto'),
#    (r'^organizacion/(?P<id>\d+)/$', 'organizacion'),
#    (r'^indicadores/(?P<vista>[-\w]+)/$', '_get_view'),
#    (r'^indicadores/meta/(?P<slug>[-\w]+)/$', 'meta'),
)


