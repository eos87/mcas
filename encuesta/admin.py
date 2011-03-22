# -*- coding: UTF-8 -*-
from django.contrib import admin
from models import *

class FamiliaInline(admin.StackedInline):
    fields = ['jefe', 'vive_con', 'adultos', 'uno_siete', 'ocho_diesciseis']
    model = Familia
    max_num = 1

class ConocimientoInline(admin.StackedInline):
    fields = ['abuso', 'lugares', 'quien_abusa', 'que_hacer', 'conoce_ley', 'nombre_ley', 'donde_aprendio', 'donde_informarse', ]
    model = Conocimiento
    max_num = 1

class ActitudInline(admin.StackedInline):
    fields = ['porque_abuso', 'que_piensa', 'que_piensa_victimas', 'familia_ensena', 'escuela_ensena',]
    model = Actitud
    max_num = 1

class PracticaInline(admin.StackedInline):
    fields = ['que_haria', 'que_hago_prevenir', 'participa_prevenir', 'como',]
    model = Practica
    max_num = 1

class EstadoActualInline(admin.StackedInline):
    fields = ['problema_comunidad', 'problema_pais', 'personas_atienden', 'lugares', 'tipo_atencion', 'donde_van', ]
    model = EstadoActual
    max_num = 1

class PercepcionlInline(admin.StackedInline):
    fields = ['conoce_abusados', 'que_familia', 'quien_debe', 'mensaje', 'defender', 'rol_medios', 'rol_iglesia', 'rol_estado', 'rol_ongs', 'rol_empresas', ]
    model = Percepcion
    max_num = 1

admin.site.register(Organizacion)
admin.site.register(Encuestador)
admin.site.register(ViveCon)
admin.site.register(Abuso)
admin.site.register(LugarAbuso)
admin.site.register(Abusador)
admin.site.register(QueHacer)
admin.site.register(Ley)
admin.site.register(DondeAprendio)
admin.site.register(DondeInformarse)
admin.site.register(PorqueAbuso)
admin.site.register(QuePiensa)
admin.site.register(QuePiensaVictima)
admin.site.register(QueHaria)
admin.site.register(QueHacePrevenir)
admin.site.register(ComoParticipo)
admin.site.register(LugarAtencion)
admin.site.register(TipoAtencion)
admin.site.register(QueFamilia)
admin.site.register(QuienDebe)
admin.site.register(MensajeTransmiten)
admin.site.register(RolMedio)
admin.site.register(RolIglesia)
admin.site.register(RolEstado)
admin.site.register(RolOng)
admin.site.register(RolEmpresa)

class EncuestaAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("/files/css/especial.css", )
        }
    fields = ['organizacion', 'codigo', 'recolector', 'fecha', 'area_reside', 'municipio', 'comunidad', 'sexo', 'edad', 'escolaridad', 'estado_civil',
        'no_hijas', 'no_hijos', 'iglesia', 'que_iglesia', 'importancia_religion']
    inlines = [FamiliaInline, ConocimientoInline, ActitudInline, PracticaInline, EstadoActualInline, PercepcionlInline]

admin.site.register(Encuesta, EncuestaAdmin)