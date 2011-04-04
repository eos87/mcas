# -*- coding: UTF-8 -*-

from django import forms
from mcas.encuesta.models import *
from mcas.lugar.models import Departamento, Municipio

AREA_RESIDE = (('', 'Todos'), (1, 'Urbano'), (2, 'Rural'))
SEXO = (('', 'Ambos'), (1, 'Femenino'), (2, 'Masculino'))
EDAD_CHOICE = [('', 'Todas'), (1, '16-25'), (2, '25-45'), (3, '45-más')]
NIVEL_EDUCATIVO = (('', 'Todos'),
                 (1, 'No sabe leer y escribir'),
                 (2, 'Alfabetizado'),
                 (3, 'Primaria Completa'),
                 (4, 'Primaria Incompleta'),
                 (5, 'Secundaria Completa'),
                 (6, 'Secundaria Incompleta'),
                 (7, 'Técnico'),
                 (8, 'Universitario'))
ESTADO_CIVIL = (('', 'Todos'), (1, 'Soltero/a'), (2, 'Casado/a'), (3, 'Unión de hecho estable'), (4, 'Divorciada/o'), (5, 'Viuda/o'))
IGLESIA = (('', 'Todo'), (1, 'Si'), (2, 'No'))
IMPORTANCIA_RELIGION = (('', 'Todo'), (1, 'Ninguna'), (2, 'Poca'), (3, 'Importante'), (4, 'Muy importante'))

#mostrar solo los años donde hay informacion en BD
def get_anios():
    choices = []
    for en in Encuesta.objects.all().order_by('fecha'):
        choices.append((en.fecha.year, en.fecha.year))
    return choices

class ConsultarForm(forms.Form):
    anio = forms.ChoiceField(choices=get_anios(), label=u'Año')
    residencia = forms.ChoiceField(choices=AREA_RESIDE)
    sexo = forms.ChoiceField(choices=SEXO)
    edad = forms.ChoiceField(choices=EDAD_CHOICE)
    escolaridad = forms.ChoiceField(choices=NIVEL_EDUCATIVO)
    estado_civil = forms.ChoiceField(choices=ESTADO_CIVIL)
    departamento = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all())
    municipio = forms.ModelMultipleChoiceField(queryset=Municipio.objects.all())
    iglesia = forms.ChoiceField(choices=IGLESIA, required=False)
    importancia_religion = forms.ChoiceField(choices=IMPORTANCIA_RELIGION, required=False)

