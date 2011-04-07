# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse 
from django.utils import simplejson
from mcas.lugar.models import Municipio, Departamento
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
            params['edad__range'] = (26, 45)
        else:
            params['edad__gt'] = 45

    if request.session['escolaridad']:
        params['escolaridad'] = request.session['escolaridad']

    if request.session['departamento'] and (not request.session['municipio']):
        municipios = Municipio.objects.filter(departamento__in=request.session['departamento'])
        print municipios
        params['municipio__in'] = municipios

    if request.session['municipio']:
        params['municipio__in'] = request.session['municipio']

    encuestas = Encuesta.objects.filter(**params)
    return encuestas

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

def get_munis(request):
    '''Metodo para obtener los municipios via Ajax segun los departamentos selectos'''
    ids = request.GET.get('ids', '')
    dicc = {}
    resultado = []
    if ids:
        lista = ids.split(',')    
    for id in lista:
        try:
            departamento = Departamento.objects.get(pk=id)
            municipios = Municipio.objects.filter(departamento__id=departamento.pk).order_by('nombre')
            lista1 = []
            for municipio in municipios:
                muni = {}
                muni['id'] = municipio.pk
                muni['nombre'] = municipio.nombre
                lista1.append(muni)
            dicc[departamento.nombre] = lista1
        except:
            pass
    resultado.append(dicc)    
    return HttpResponse(simplejson.dumps(resultado), mimetype='application/json')