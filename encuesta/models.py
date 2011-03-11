# -*- coding: UTF-8 -*-
from django.db import models
from mcas.lugar.models import *

class Organizacion(models.Model):
    nombre = models.CharField(max_length=250)
    nombre_corto = models.CharField(max_length=50, default='', verbose_name='Siglas/Nombre Corto')
#    direccion = models.CharField(max_length=200, blank=True, default='')
#    correo = models.EmailField(blank=True, default='')
#    website = models.URLField(blank=True, default='')
#    telefono = models.CharField(max_length=20, blank=True, default='')
#    contacto = models.CharField(max_length=150, blank=True, default='')
#    usuario = models.ForeignKey(User)
#    pais = models.ForeignKey(Pais)
#    departamento = models.ForeignKey(Departamento, verbose_name='Departamento')
#    municipio = models.ForeignKey(Municipio, verbose_name='Municipio')
#    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.nombre_corto

    class Meta:
        verbose_name = u'Organización'
        verbose_name_plural = u'Organizaciones'


class Encuestador(models.Model):
    nombre_completo = models.CharField(max_length=250, help_text='Un nombre y un Apellido')
#    telefono = models.CharField(max_length=20, blank=True, default='')

    def __unicode__(self):
        return u'%s' % self.nombre_completo

    class Meta:
        verbose_name_plural = u'Encuestadores'

AREA_RESIDE = ((1, 'Urbano'), (2, 'Rural'))
SEXO = ((1, 'Femenino'), (2, 'Masculino'))
NIVEL_EDUCATIVO = ((1, 'No sabe leer y escribir'),
                   (2, 'Alfabetizado'),
                   (3, 'Primaria Completa'),
                   (4, 'Primaria Incompleta'),
                   (5, 'Secundaria Completa'),
                   (6, 'Secundaria Incompleta'),
                   (7, 'Técnico'),
                   (8, 'Universitario'))
ESTADO_CIVIL = ((1, 'Soltero/a'), (2, 'Casado/a'), (3, 'Unión de hecho estable'), (4, 'Divorciada/o'), (5, 'Viuda/o'))
SI_NO = ((1, 'Si'), (2, 'No'))
IMPORTANCIA_RELIGION = ((1, 'Ninguna'), (2, 'Poca'), (3, 'Importante'), (4, 'Muy importante'))

class Encuesta(models.Model):
    organizacion = models.ForeignKey(Organizacion)
    recolector = models.ForeignKey(Encuestador)
    codigo = models.CharField(max_length=30)
    fecha = models.DateField()
    area_reside = models.IntegerField(verbose_name=u'En que área reside', choices=AREA_RESIDE)
    departamento = models.ForeignKey(Departamento)
    municipio = models.ForeignKey(Municipio)
    comunidad = models.ForeignKey(Comunidad, verbose_name=u'Comunidad/Barrio')
    sexo = models.IntegerField(choices=SEXO)
    edad = models.IntegerField()
    escolaridad = models.IntegerField(verbose_name=u'¿Qué nivel de escolaridad ha alcanzado', choices=NIVEL_EDUCATIVO)
    estado_civil = models.IntegerField(verbose_name=u'¿Cuál es su estado civil?', choices=ESTADO_CIVIL)
    no_hijas = models.IntegerField(default=0)
    no_hijos = models.IntegerField(default=0)
    iglesia = models.IntegerField(choices=SI_NO)
    que_iglesia = models.CharField(verbose_name='¿A que iglesia o congregación asiste?', default='', blank=True)
    importancia_religion = models.IntegerField(choices=IMPORTANCIA_RELIGION)

    class Meta:
        verbose_name_plural = u'Encuestas'

    def __unicode__(self):
        return u'Encuesta %s' % self.id

JEFE = ((1, 'Hombre'), (2, 'Mujer'))

class ViveCon(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        verbose_name = u'Persona con quien vive'
        verbose_name_plural = u'Personas con quien vive'

class Familia(models.Model):
    jefe = models.IntegerField(verbose_name=u'¿En casa quien es el jefe o jefa de familia?', choices=JEFE)
    vive_con = models.ManyToManyField(ViveCon, verbose_name=u'¿Con quien vive usted?')
    adultos = models.IntegerField(verbose_name=u'¿Número de personas adultas que viven en la vivienda?')
    uno_siete = models.IntegerField(verbose_name=u'¿Cuántas personas de 1-7 años viven en su casa?')
    ocho_diesciseis = models.IntegerField(verbose_name=u'¿Cuántas personas de 8-16 años viven en su casa?')
    encuesta = models.ForeignKey(Encuesta)

    def __unicode__(self):
        return u'Dato familia %s' % self.id

    class Meta:
        verbose_name = u'Dato familia'
        verbose_name_plural = u'Datos familia'

class Abuso(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        verbose_name_plural = u'Abusos'

class LugarAbuso(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        verbose_name_plural = u'Lugares de Abuso'

class Abusador(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        verbose_name_plural = u'Abusadores'

class QueHacer(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        verbose_name_plural = u'Que hacer para prevenir'

class DondeAprendio(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        verbose_name_plural = u'Donde aprendió'

class DondeInformarse(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        verbose_name_plural = u'Donde informarse'

class Conocimiento(models.Model):
    abuso = models.ManyToManyField(Abuso, verbose_name=u'¿Qué es para usted abuso sexual?')
    lugares = models.ManyToManyField(LugarAbuso, verbose_name=u'¿Sabe en que lugares puede ocurrir el abuso sexual?')
    quien_abusa = models.ManyToManyField(Abusador, verbose_name=u'¿Usted sabe quienes son los que abusan sexualmente de niñas, niños y adolescentes?')
    que_hacer = models.ManyToManyField(QueHacer, verbose_name=u'¿Sabe usted que se puede hacer para prevenir el abuso sexual?')
    conoce_ley = models.IntegerField(choices=SI_NO, verbose_name=u'¿Conoce sobre leyes que castigan a las personas que abusan sexualmente de los niños, niñas y adolescentes?')
    donde_aprendio = models.ManyToManyField(DondeAprendio, verbose_name=u'¿Dónde aprendió usted sobre abuso sexual?')
    donde_informarse = models.ManyToManyField(DondeInformarse, verbose_name=u'¿Dónde cree que podría informarse sobre el tema?')
    encuesta = models.ForeignKey(Encuesta)

    def __unicode__(self):
        return u'Conocimiento %s' % self.id

    class Meta:
        verbose_name_plural = u'Conocimientos'