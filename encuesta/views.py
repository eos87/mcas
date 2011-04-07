# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import ConsultarForm
from models import Encuesta

def _query_set_filtrado(request):
    params = {}
    params['fecha__year'] = request.session['anio']
    if request.session['residencia']:
        params['area_reside'] = request.session['residencia']
    if request.session['sexo']:
        params['sexo'] = request.session['sexo']
    if request.session['edad']:
        edad = int(request.session['edad'])
        if edad == 1:
            params['edad__range'] = (16, 25)
        elif edad == 2:
            params['edad__range'] = (25, 45)
        else:
            params['edad__gt'] = 45

    encuestas = Encuesta.objects.filter(**params)
    return encuestas

@never_cache
def consultar(request):
    if request.method == 'POST':
        form = ConsultarForm(request.POST)
        if form.is_valid():
            request.session['anio'] = form.cleaned_data['anio']            
            request.session['residencia'] = form.cleaned_data['residencia']
            request.session['sexo'] = form.cleaned_data['sexo']
            request.session['edad'] = form.cleaned_data['edad']
            request.session['escolaridad'] = form.cleaned_data['escolaridad']
            request.session['departamento'] = form.cleaned_data['departamento']
            request.session['municipio'] = form.cleaned_data['municipio']
            request.session['comunidad'] = form.cleaned_data['comunidad']
            request.session['iglesia'] = form.cleaned_data['iglesia']
            request.session['importancia'] = form.cleaned_data['importancia_religion']
            request.session['centinel'] = 1
            return HttpResponseRedirect('/indicadores/')
    else:
        form = ConsultarForm()        
    return render_to_response('encuesta/consultar.html', RequestContext(request, locals()))

def indicadores(request):
    encuestas = _query_set_filtrado(request)
    return render_to_response('encuesta/indicadores.html', RequestContext(request, locals()))