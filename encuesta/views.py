# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import ConsultarForm

def consultar(request):
    form = ConsultarForm()
    return render_to_response('encuesta/consultar.html', RequestContext(request, locals()))
