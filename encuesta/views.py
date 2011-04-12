# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse 
from django.utils import simplejson
from mcas.lugar.models import Municipio, Departamento, Comunidad
from forms import ConsultarForm
from models import *
from mcas import grafos

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

    if request.session['estado_civil']:
        params['estado_civil'] = request.session['estado_civil']

    if request.session['departamento']:
        if not request.session['municipio']:
            municipios = Municipio.objects.filter(departamento__in=request.session['departamento'])
            params['municipio__in'] = municipios
        else:
            if request.session['comunidad']:
                params['comunidad__in'] = request.session['comunidad']
            else:
                params['municipio__in'] = request.session['municipio']

    if request.session['iglesia']:
        params['iglesia'] = request.session['iglesia']

    if request.session['importancia']:
        params['importancia_religion'] = request.session['importancia']

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
            request.session['estado_civil'] = form.cleaned_data['estado_civil']
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

def familia_jefe(request):
    encuestas = _query_set_filtrado(request)
    valores = []
    leyenda = []    
    for opcion in JEFE:
        suma = Familia.objects.filter(encuesta__in=encuestas, jefe=opcion[0]).count()
        valores.append(suma)
        leyenda.append(opcion[1])        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Quien es el jefe de familia?', type = grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/familia/jefe.html', RequestContext(request, locals()))

def familia_vivecon(request):
    encuestas = _query_set_filtrado(request)
    valores = []
    leyendas = []
    dicc = {}
    for quien in ViveCon.objects.all():        
        suma = Familia.objects.filter(encuesta__in=encuestas, vive_con=quien).count()        
        dicc[quien.nombre] = suma

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)

    return render_to_response('encuesta/familia/vivecon.html', RequestContext(request, locals()))

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

def get_comunies(request):
    ids = request.GET.get('ids', '')
    if ids:
        lista = ids.split(',')
    results = []
    comunies = Comunidad.objects.filter(municipio__pk__in=lista).order_by('nombre').values('id', 'nombre')

    return HttpResponse(simplejson.dumps(list(comunies)), mimetype='application/json')
