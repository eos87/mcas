# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import ConsultarForm
from models import Encuesta

def _query_set_filtrado(request):
    pass

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
    return render_to_response('encuesta/indicadores.html', RequestContext(request, locals()))