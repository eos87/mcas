# -*- coding: UTF-8 -*-
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from forms import ConsultarForm
from mcas import grafos
from mcas.lugar.models import Comunidad
from mcas.lugar.models import Departamento
from mcas.lugar.models import Municipio
from models import *

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
            params['edad__range'] = (18, 24)
        elif edad == 2:
            params['edad__range'] = (25, 44)
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
                
    if request.session['organizacion']:
        params['organizacion__in'] = request.session['organizacion']

    if request.session['iglesia']:
        params['iglesia'] = request.session['iglesia']

    if request.session['importancia']:
        params['importancia_religion'] = request.session['importancia']

    encuestas = Encuesta.objects.filter( ** params)
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
            request.session['organizacion'] = form.cleaned_data['organizacion']
            request.session['municipio'] = form.cleaned_data['municipio']
            request.session['comunidad'] = form.cleaned_data['comunidad']
            request.session['iglesia'] = form.cleaned_data['iglesia']
            request.session['importancia'] = form.cleaned_data['importancia_religion']
            request.session['centinel'] = 1
            encuestas = _query_set_filtrado(request).count()
            if encuestas != 0:
                return HttpResponseRedirect('/indicadores/')
            else:
                nono = 2
    else:
        form = ConsultarForm()       
    return render_to_response('encuesta/consultar.html', RequestContext(request, locals()))

def index(request):
    total_encuesta = Encuesta.objects.all().count()
    total_organizacion = Organizacion.objects.all().count()
    return render_to_response('index.html',RequestContext(request, locals()))

def indicadores(request):
    encuestas = _query_set_filtrado(request)
    return render_to_response('encuesta/indicadores.html', RequestContext(request, locals()))
    

def generales(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    #-----------------------------------------------
    urbano = encuestas.filter(area_reside=1).count()
    por_urbano = round(saca_porcentajes(urbano,numero),2)
    rural = encuestas.filter(area_reside=2).count()
    por_rural = round(saca_porcentajes(rural,numero),2)
    hombre = encuestas.filter(sexo=2).count()
    por_hombre = round(saca_porcentajes(hombre,numero),2)
    mujer = encuestas.filter(sexo=1).count()
    por_mujer = round(saca_porcentajes(mujer,numero),2)
    iglesia_si = encuestas.filter(iglesia=1).count()
    iglesia_no = encuestas.filter(iglesia=2).count()
    
    #de los entrevistados cuantos tiene nivel de escolaridad
    escolaridad = {}
    for escuela in NIVEL_EDUCATIVO:
        conteo = encuestas.filter(escolaridad=escuela[0]).aggregate(conteo=Count('escolaridad'))['conteo']
        porcentaje = round(saca_porcentajes(conteo,numero),2)
        escolaridad[escuela[1]] = (conteo,porcentaje)        
    dicc2 = sorted(escolaridad.items(), key=lambda x: x[1], reverse=True)
        #escolaridad.append([escuela[1],conteo,porcentaje])
        
    civil = {}
    for estado in ESTADO_CIVIL:
        conteo = encuestas.filter(estado_civil=estado[0]).aggregate(conteo=Count('estado_civil'))['conteo']
        porcentaje = round(saca_porcentajes(conteo,numero),2)
        civil[estado[1]] = (conteo,porcentaje)
    dicc3 = sorted(civil.items(), key=lambda x: x[1], reverse=True)

         
    religion = []
    for re in IMPORTANCIA_RELIGION:
        conteo = encuestas.filter(importancia_religion=re[0]).aggregate(conteo=Count('importancia_religion'))['conteo']
        porcentaje = round(saca_porcentajes(conteo,numero),2)
        religion.append([re[1],conteo,porcentaje])
        
    depart = {}   
    for depar in Departamento.objects.all():
        conteo = encuestas.filter(municipio__departamento=depar).aggregate(conteo=Count('municipio__departamento'))['conteo']
        porcentaje = round(saca_porcentajes(conteo,numero),2)
        if conteo != 0:
            depart[depar.nombre] = (conteo,porcentaje)
    dicc4 = sorted(depart.items(), key=lambda x: x[1], reverse=True)      
       
    munis = []
    for mun in Municipio.objects.all():
        conteo = encuestas.filter(municipio=mun).aggregate(conteo=Count('municipio'))['conteo']
        porcentaje = round(saca_porcentajes(conteo,numero),2)
        if conteo != 0:
            munis.append([mun.departamento.nombre,mun.nombre,conteo,porcentaje])
            sorted(munis, key=lambda muni: muni[3])
    return render_to_response('encuesta/generales.html', RequestContext(request, locals()))

#SALIDAS DE FAMILIAS

def familia_jefe(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in JEFE:
        suma = Familia.objects.filter(encuesta__in=encuestas, jefe=opcion[0]).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[opcion[1]] = (suma,tabla)
        valores.append(suma)
        leyenda.append(opcion[1])        

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)  
    
    grafo_url = grafos.make_graph(valores, leyenda, '¿Quién es el jefe de familia?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/familia/jefe.html', RequestContext(request, locals()))

def __familia_jefe(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in JEFE:
        suma = Familia.objects.filter(encuesta__in=encuestas, jefe=opcion[0]).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[opcion[1]] = (suma,tabla)
        valores.append(suma)
        leyenda.append(opcion[1])        

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def familia_jefe_xls(request):
    dict = __familia_jefe(request)
    print dict
    return write_xls('encuesta/familia/jefe_xls.html', dict, 'jefe.doc')
    
def familia_jefe_pdf(request):
    dict = __familia_jefe(request)
    return write_pdf('encuesta/familia/jefe_xls.html', dict)  
#-------------------------------------------------------------------------------
def familia_vivecon(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyendas = []
    dicc = {}
    for quien in ViveCon.objects.all()[:10]:        
        suma = Familia.objects.filter(encuesta__in=encuestas, vive_con=quien).count()
        tabla = round(saca_porcentajes(suma,numero),1)        
        dicc[quien.nombre] = (suma,tabla)

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/familia/vivecon.html', locals(),
                               RequestContext(request))
    
def __vivencon_xls__(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for quien in ViveCon.objects.all()[:10]:        
        suma = Familia.objects.filter(encuesta__in=encuestas, vive_con=quien).count()
        tabla = round(saca_porcentajes(suma,numero),1)        
        dicc[quien.nombre] = (suma,tabla)

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def vivencon_xls(request):
    dict = __vivencon_xls__(request)
    return write_xls('encuesta/familia/vivecon_xls.html', dict, 'vive_con_quien.doc')
    
def vivencon_pdf(request):
    dict = __vivencon_xls__(request)
    return write_pdf('encuesta/familia/vivecon_xls.html', dict)
#-------------------------------------------------------------------------------    

def familia_miembros(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()

    #adultos mayores
    adultos1 = Familia.objects.filter(encuesta__in=encuestas, adultos__range=(0,2)).count()
    adultos2 = Familia.objects.filter(encuesta__in=encuestas, adultos__range=(3,5)).count()
    adultos3 = Familia.objects.filter(encuesta__in=encuestas, adultos__gt=6).count()
    #uno a siete años
    uno_siete1 = Familia.objects.filter(encuesta__in=encuestas, uno_siete__range=(0,2)).count()
    uno_siete2 = Familia.objects.filter(encuesta__in=encuestas, uno_siete__range=(3,5)).count()
    uno_siete3 = Familia.objects.filter(encuesta__in=encuestas, uno_siete__gt=6).count()
    #ocho a diesciseis
    ocho_1 = Familia.objects.filter(encuesta__in=encuestas, ocho_diesciseis__range=(0,2)).count()
    ocho_2 = Familia.objects.filter(encuesta__in=encuestas, ocho_diesciseis__range=(3,5)).count()
    ocho_3 = Familia.objects.filter(encuesta__in=encuestas, ocho_diesciseis__gt=6).count()
    
    valores = []
    leyenda = ['Adultos', 'De 1-7 años', 'De 8 a 16 años']     
    #dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)    

    grafo_url = grafos.make_graph(valores, leyenda, '¿Miembros de la familia?', type=grafos.PIE_CHART_3D, size=(958, 313), pie_labels=True)
    return render_to_response('encuesta/familia/miembros.html', RequestContext(request, locals()))
    
def __familia_miembros_xls(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()

    #adultos mayores
    adultos1 = Familia.objects.filter(encuesta__in=encuestas, adultos__range=(0,2)).count()
    adultos2 = Familia.objects.filter(encuesta__in=encuestas, adultos__range=(3,5)).count()
    adultos3 = Familia.objects.filter(encuesta__in=encuestas, adultos__gt=6).count()
    #uno a siete años
    uno_siete1 = Familia.objects.filter(encuesta__in=encuestas, uno_siete__range=(0,2)).count()
    uno_siete2 = Familia.objects.filter(encuesta__in=encuestas, uno_siete__range=(3,5)).count()
    uno_siete3 = Familia.objects.filter(encuesta__in=encuestas, uno_siete__gt=6).count()
    #ocho a diesciseis
    ocho_1 = Familia.objects.filter(encuesta__in=encuestas, ocho_diesciseis__range=(0,2)).count()
    ocho_2 = Familia.objects.filter(encuesta__in=encuestas, ocho_diesciseis__range=(3,5)).count()
    ocho_3 = Familia.objects.filter(encuesta__in=encuestas, ocho_diesciseis__gt=6).count()
    
    valores = []
    leyenda = ['Adultos', 'De 1-7 años', 'De 8 a 16 años']     
    dict = {'adultos1':adultos1, 'adultos2':adultos2, 'adultos3':adultos3, 'uno_siete1':uno_siete1,
             'uno_siete2':uno_siete2, 'uno_siete3':uno_siete3, 'ocho_1':ocho_1, 'ocho_2':ocho_2,
             'uno_siete3':uno_siete3} 
             
    return dict

def familia_miembros_xls(request):
    dict = __familia_miembros_xls(request)
    return write_xls('encuesta/familia/miembros_xls.html', dict, 'miembros.doc')
    
def familia_miembros_pdf(request):
    dict = __familia_miembros_xls(request)
    return write_pdf('encuesta/familia/miembros_xls.html', dict)
#-------------------------------------------------------------------------------        

#SALIDAS DE CONOCIMIENTOS

def conocimiento_abuso(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for abuso in Abuso.objects.all():
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, abuso=abuso).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[abuso.nombre] = (suma,tabla)
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/conocimiento/abuso.html', RequestContext(request, locals()))
    
    
def __conocimiento_abuso(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for abuso in Abuso.objects.all():
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, abuso=abuso).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[abuso.nombre] = (suma,tabla)
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    
    return dict
    
def conocimiento_abuso_xls(request):
    dict = __conocimiento_abuso(request)
    return write_xls('encuesta/conocimiento/abuso_xls.html', dict, 'conocimiento.doc')
    
def conocimiento_abuso_pdf(request):
    dict = __conocimiento_abuso(request)
    return write_pdf('encuesta/conocimiento/abuso_xls.html', dict)
#-------------------------------------------------------------------------------
def conocimiento_lugar(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for lugar in LugarAbuso.objects.all()[:12]:
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, lugares=lugar).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[lugar.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/conocimiento/lugar.html', RequestContext(request, locals()))
    
def __conocimiento_lugar(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for lugar in LugarAbuso.objects.all()[:12]:
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, lugares=lugar).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[lugar.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def conocimiento_lugar_xls(request):
    dict = __conocimiento_lugar(request)
    return write_xls('encuesta/conocimiento/lugar_xls.html', dict, 'lugar.doc')
    
def conocimiento_lugar_pdf(request):
    dict = __conocimiento_lugar(request)
    return write_pdf('encuesta/conocimiento/lugar_xls.html', dict)
#-------------------------------------------------------------------------------

def conocimiento_abusan_ninos(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for abuso in Abusador.objects.all():
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, quien_abusa=abuso).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[abuso.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/conocimiento/abusan_ninos.html', RequestContext(request, locals()))

def __conocimiento_abusan_ninos(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for abuso in Abusador.objects.all():
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, quien_abusa=abuso).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[abuso.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def conocimiento_abusan_ninos_xls(request):
    dict = __conocimiento_abusan_ninos(request)
    return write_xls('encuesta/conocimiento/abusan_ninos_xls.html', dict, 'abusan_ninos.doc')
    
def conocimiento_abusan_ninos_pdf(request):
    dict = __conocimiento_abusan_ninos(request)
    return write_pdf('encuesta/conocimiento/abusan_ninos_xls.html', dict)
#-------------------------------------------------------------------------------
    
def conocimiento_prevenir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for hacer in QueHacer.objects.all():
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, que_hacer=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/conocimiento/prevenir.html', RequestContext(request, locals()))

def __conocimiento_prevenir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for hacer in QueHacer.objects.all():
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, que_hacer=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def conocimiento_prevenir_xls(request):
    dict = __conocimiento_prevenir(request)
    return write_xls('encuesta/conocimiento/prevenir_xls.html', dict, 'prevenir.doc')
    
def conocimiento_prevenir_pdf(request):
    dict = __conocimiento_prevenir(request)
    return write_pdf('encuesta/conocimiento/prevenir_xls.html', dict)
#-------------------------------------------------------------------------------    

def conocimiento_leyes(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in SI_NO:
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, conoce_ley=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),1)
        valores.append(suma)
        leyenda.append(opcion[1])
        dicc[opcion[1]] = (suma,porcentaje)
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)               

    grafo_url = grafos.make_graph(valores, leyenda, '¿Conoce sobre las leyes que castigan a las personas que abusan?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/conocimiento/leyes.html', RequestContext(request, locals()))

def __conocimiento_leyes(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}   
    for opcion in SI_NO:
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, conoce_ley=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),1)
        dicc[opcion[1]] = (suma,porcentaje)
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
        
def conocimiento_leyes_xls(request):
    dict = __conocimiento_leyes(request)
    return write_xls('encuesta/conocimiento/leyes_xls.html', dict, 'leyes.doc')
    
def conocimiento_leyes_pdf(request):
    dict = __conocimiento_leyes(request)
    return write_pdf('encuesta/conocimiento/leyes_xls.html', dict)
#-------------------------------------------------------------------------------
    
def conocimiento_aprendio(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for aprender in DondeAprendio.objects.all():
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, donde_aprendio=aprender).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[aprender.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/conocimiento/aprendio.html', RequestContext(request, locals()))   

def __conocimiento_aprendio(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for aprender in DondeAprendio.objects.all():
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, donde_aprendio=aprender).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[aprender.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def conocimiento_aprendio_xls(request):
    dict = __conocimiento_aprendio(request)
    return write_xls('encuesta/conocimiento/aprendio_xls.html', dict, 'aprendio.doc')
    
def conocimiento_aprendio_pdf(request):
    dict = __conocimiento_aprendio(request)
    return write_pdf('encuesta/conocimiento/aprendio_xls.html', dict)
#-------------------------------------------------------------------------------
    
def conocimiento_informarse(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for informar in DondeInformarse.objects.all():
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, donde_informarse=informar).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[informar.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/conocimiento/informarse.html', RequestContext(request, locals()))     

def __conocimiento_informarse(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for informar in DondeInformarse.objects.all():
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, donde_informarse=informar).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[informar.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def conocimiento_informarse_xls(request):
    dict = __conocimiento_informarse(request)
    return write_xls('encuesta/conocimiento/informarse_xls.html', dict, 'informarse.doc')
    
def conocimiento_informarse_pdf(request):
    dict = __conocimiento_informarse(request)
    return write_pdf('encuesta/conocimiento/informarse_xls.html', dict)
#-------------------------------------------------------------------------------

#SALIDAS DE ACTITUD

def actitud_abuso(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for abuso in PorqueAbuso.objects.all():
        suma = Actitud.objects.filter(encuesta__in=encuestas, porque_abuso=abuso).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[abuso.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/actitud/abuso.html', RequestContext(request, locals()))   

def __actitud_abuso(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for abuso in PorqueAbuso.objects.all():
        suma = Actitud.objects.filter(encuesta__in=encuestas, porque_abuso=abuso).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[abuso.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict

def actitud_abuso_xls(request):
    dict = __actitud_abuso(request)
    return write_xls('encuesta/actitud/abuso_xls.html', dict, 'abuso.doc')
    
def actitud_abuso_pdf(request):
    dict = __actitud_abuso(request)
    return write_pdf('encuesta/actitud/abuso_xls.html', dict)
#-------------------------------------------------------------------------------    

def actitud_piensa(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for pensar in QuePiensa.objects.all():
        suma = Actitud.objects.filter(encuesta__in=encuestas, que_piensa=pensar).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[pensar.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/actitud/piensa.html', RequestContext(request, locals()))
    
def __actitud_piensa(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for pensar in QuePiensa.objects.all():
        suma = Actitud.objects.filter(encuesta__in=encuestas, que_piensa=pensar).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[pensar.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def actitud_piensa_xls(request):
    dict = __actitud_piensa(request)
    return write_xls('encuesta/actitud/piensa_xls.html', dict, 'piensa.doc')
    
def actitud_piensa_pdf(request):
    dict = __actitud_piensa(request)
    return write_pdf('encuesta/actitud/piensa_xls.html', dict)
#------------------------------------------------------------------------------- 
  
def actitud_victimas(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for victima in QuePiensaVictima.objects.all():
        suma = Actitud.objects.filter(encuesta__in=encuestas, que_piensa_victimas=victima).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[victima.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/actitud/victima.html', RequestContext(request, locals()))

def __actitud_victimas(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}
    for victima in QuePiensaVictima.objects.all():
        suma = Actitud.objects.filter(encuesta__in=encuestas, que_piensa_victimas=victima).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[victima.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def actitud_victimas_xls(request):
    dict = __actitud_victimas(request)
    return write_xls('encuesta/actitud/victima_xls.html', dict, 'victima.doc')
    
def actitud_victimas_pdf(request):
    dict = __actitud_victimas(request)
    return write_pdf('encuesta/actitud/victima_xls.html', dict)
#-------------------------------------------------------------------------------     
def actitud_familia(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in SI_NO:
        suma = Actitud.objects.filter(encuesta__in=encuestas, familia_ensena=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)
        valores.append(suma)
        leyenda.append(opcion[1])
        dicc[opcion[1]] = (suma,porcentaje)

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)       

    grafo_url = grafos.make_graph(valores, leyenda, '¿Estaría usted de acuerdo que en la Familia se enseñe a los niños, niñas y adolescentes a prevenir el abuso sexual?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/actitud/familia.html', RequestContext(request, locals()))  

def __actitud_familia(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}    
    for opcion in SI_NO:
        suma = Actitud.objects.filter(encuesta__in=encuestas, familia_ensena=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)
        dicc[opcion[1]] = (suma,porcentaje)

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def actitud_familia_xls(request):
    dict = __actitud_familia(request)
    return write_xls('encuesta/actitud/familia_xls.html', dict, 'familia.doc')
    
def actitud_familia_pdf(request):
    dict = __actitud_familia(request)
    return write_pdf('encuesta/actitud/familia_xls.html', dict)
#-------------------------------------------------------------------------------       
def actitud_escuela(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in SI_NO:
        suma = Actitud.objects.filter(encuesta__in=encuestas, escuela_ensena=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)
        valores.append(suma)
        leyenda.append(opcion[1])
        dicc[opcion[1]] = (suma,porcentaje)
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Estaría usted de acuerdo que en la Escuela se enseñe a los niños, niñas y adolescentes a prevenir el abuso sexual?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/actitud/escuela.html', RequestContext(request, locals()))

def __actitud_escuela(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}    
    for opcion in SI_NO:
        suma = Actitud.objects.filter(encuesta__in=encuestas, escuela_ensena=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)
        dicc[opcion[1]] = (suma,porcentaje)
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
def actitud_escuela_xls(request):
    dict = __actitud_escuela(request)
    return write_xls('encuesta/actitud/escuela_xls.html', dict, 'escuela.doc')
    
def actitud_escuela_pdf(request):
    dict = __actitud_escuela(request)
    return write_pdf('encuesta/actitud/escuela_xls.html', dict)
#-------------------------------------------------------------------------------    
    
#PRACTICA

def practica_situacion(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in QueHaria.objects.all():
        suma = Practica.objects.filter(encuesta__in=encuestas, que_haria=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/practica/situacion.html', RequestContext(request, locals()))  

def __practica_situacion(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in QueHaria.objects.all():
        suma = Practica.objects.filter(encuesta__in=encuestas, que_haria=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict

def practica_situacion_xls(request):
    dict = __practica_situacion(request)
    return write_xls('encuesta/practica/situacion_xls.html', dict, 'situacion.doc')
    
def practica_situacion_pdf(request):
    dict = __practica_situacion(request)
    return write_pdf('encuesta/practica/situacion_xls.html', dict)
#-------------------------------------------------------------------------------    
   
def practica_prevenir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in QueHacePrevenir.objects.all():
        suma = Practica.objects.filter(encuesta__in=encuestas, que_hago_prevenir=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/practica/prevenir.html', RequestContext(request, locals()))
    
def __practica_prevenir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in QueHacePrevenir.objects.all():
        suma = Practica.objects.filter(encuesta__in=encuestas, que_hago_prevenir=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def practica_prevenir_xls(request):
    dict = __practica_prevenir(request)
    return write_xls('encuesta/practica/prevenir_xls.html', dict, 'prevenir.doc')
    
def practica_prevenir_pdf(request):
    dict = __practica_prevenir(request)
    return write_pdf('encuesta/practica/prevenir_xls.html', dict)
#-------------------------------------------------------------------------------  
    
def practica_participa_prevenir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in SI_NO:
        suma = Practica.objects.filter(encuesta__in=encuestas, participa_prevenir=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)
        valores.append(suma)
        leyenda.append(opcion[1])
        dicc[opcion[1]] = (suma,porcentaje)
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)                

    grafo_url = grafos.make_graph(valores, leyenda, '¿Usted participa o ha participado en algún tipo de organización que previene el abuso sexual?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/practica/participa_prevenir.html', RequestContext(request, locals()))

def __practica_participa_prevenir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}    
    for opcion in SI_NO:
        suma = Practica.objects.filter(encuesta__in=encuestas, participa_prevenir=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)
        dicc[opcion[1]] = (suma,porcentaje)
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def practica_participa_prevenir_xls(request):
    dict = __practica_participa_prevenir(request)
    return write_xls('encuesta/practica/participa_prevenir_xls.html', dict, 'participa_prevenir.doc')
    
def practica_participa_prevenir_pdf(request):
    dict = __practica_participa_prevenir(request)
    return write_pdf('encuesta/practica/participa_prevenir_xls.html', dict)
#-------------------------------------------------------------------------------     
    
def practica_como(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    practica_si = Practica.objects.filter(encuesta__in=encuestas, participa_prevenir=1)
    
    primer = encuestas.filter(practica__participa_prevenir=1,practica__como=10).count()
    por_primer = round(saca_porcentajes(primer,practica_si.count()),1)
    print por_primer    
    dicc = {}
    segundo=0
    for hacer in ComoParticipo.objects.all().exclude(id=10):
        suma = practica_si.filter(como=hacer).count()
        segundo += suma
        tabla = round(saca_porcentajes(suma, practica_si.count()), 1)
        dicc[hacer.nombre] = (suma, tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    por_segundo = round(saca_porcentajes(segundo,practica_si.count()),1)
    
    print por_segundo
    
    return render_to_response('encuesta/practica/como.html', RequestContext(request, locals())) 

def __practica_como(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in ComoParticipo.objects.all():
        suma = Practica.objects.filter(encuesta__in=encuestas, como=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def practica_como_xls(request):
    dict = __practica_como(request)
    return write_xls('encuesta/practica/como_xls.html', dict, 'como.doc')
    
def practica_como_pdf(request):
    dict = __practica_como(request)
    return write_pdf('encuesta/practica/como_xls.html', dict)
#-------------------------------------------------------------------------------       
#SALIDAS DE ESTADO ACTUAL

def estado_problema(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in PROBLEMA:
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, problema_comunidad=hacer[0]).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer[1]] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/estado/problema_comunidad.html', RequestContext(request, locals())) 
    
def __estado_problema(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in PROBLEMA:
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, problema_comunidad=hacer[0]).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer[1]] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def estado_problema_xls(request):
    dict = __estado_problema(request)
    return write_xls('encuesta/estado/problema_comunidad_xls.html', dict, 'problema_comunidad.doc')
    
def estado_problema_pdf(request):
    dict = __estado_problema(request)
    return write_pdf('encuesta/estado/problema_comunidad_xls.html', dict)
#-------------------------------------------------------------------------------
    
def estado_problema_pais(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in PROBLEMA:
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, problema_pais=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)
        valores.append(suma)
        leyenda.append(opcion[1])
        dicc[opcion[1]] = (suma,porcentaje)
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Usted considera que el abuso sexual es un problema en el país?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/estado/problema_pais.html', RequestContext(request, locals()))

def __estado_problema_pais(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}    
    for opcion in PROBLEMA:
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, problema_pais=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)
        dicc[opcion[1]] = (suma,porcentaje)
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True) 
    dict = {'dicc2':dicc2}
    return dict
    
def estado_problema_pais_xls(request):
    dict = __estado_problema_pais(request)
    return write_xls('encuesta/estado/problema_pais_xls.html', dict, 'problema_pais.doc')
    
def estado_problema_pais_pdf(request):
    dict = __estado_problema_pais(request)
    return write_pdf('encuesta/estado/problema_pais_xls.html', dict)
#------------------------------------------------------------------------------- 
    
def estado_atencion(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in SI_NO:
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, personas_atienden=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)        
        valores.append(suma)
        leyenda.append(opcion[1])        
        dicc[opcion[1]]= (suma,porcentaje)
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)

    grafo_url = grafos.make_graph(valores, leyenda, '¿Sabe si hay lugares o personas en esta comunidad que atienden a niños/as, adolescentes que vivieron abuso sexual?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/estado/atencion.html', RequestContext(request, locals()))

def __estado_atencion(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}    
    for opcion in SI_NO:
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, personas_atienden=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)              
        dicc[opcion[1]]= (suma,porcentaje)
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict

def estado_atencion_xls(request):
    dict = __estado_atencion(request)
    return write_xls('encuesta/estado/atencion_xls.html', dict, 'atencion.doc')
    
def estado_atencion_pdf(request):
    dict = __estado_atencion(request)
    return write_pdf('encuesta/estado/atencion_xls.html', dict)
#-------------------------------------------------------------------------------     
    
def estado_lugares(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in LugarAtencion.objects.all():
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, lugares=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/estado/lugares.html', RequestContext(request, locals())) 

def __estado_lugares(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in LugarAtencion.objects.all():
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, lugares=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict

def estado_lugares_xls(request):
    dict = __estado_lugares(request)
    return write_xls('encuesta/estado/lugares_xls.html', dict, 'lugares.doc')
    
def estado_lugares_pdf(request):
    dict = __estado_lugares(request)
    return write_pdf('encuesta/estado/lugares_xls.html', dict)
#-------------------------------------------------------------------------------    
    
def estado_tipo_atencion(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in TipoAtencion.objects.all():
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, tipo_atencion=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/estado/tipo_atencion.html', RequestContext(request, locals())) 

def __estado_tipo_atencion(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in TipoAtencion.objects.all():
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, tipo_atencion=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def estado_tipo_atencion_xls(request):
    dict = __estado_tipo_atencion(request)
    return write_xls('encuesta/estado/tipo_atencion_xls.html', dict, 'tipo_atencion.doc')
    
def estado_tipo_atencion_pdf(request):
    dict = __estado_tipo_atencion(request)
    return write_pdf('encuesta/estado/tipo_atencion_xls.html', dict)
#------------------------------------------------------------------------------- 
    
def estado_donde(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in DONDE_VAN:
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, donde_van=hacer[0]).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer[1]] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/estado/donde.html', RequestContext(request, locals())) 

def __estado_donde(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in DONDE_VAN:
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, donde_van=hacer[0]).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer[1]] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict

def estado_donde_xls(request):
    dict = __estado_donde(request)
    return write_xls('encuesta/estado/donde_xls.html', dict, 'donde.doc')
    
def estado_donde_pdf(request):
    dict = __estado_donde(request)
    return write_pdf('encuesta/estado/donde_xls.html', dict)
#-------------------------------------------------------------------------------    
    
# SALIDAS DE PERCEPCION

def percepcion_ninos_abusados(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in SI_NO:
        suma = Percepcion.objects.filter(encuesta__in=encuestas, conoce_abusados=opcion[0]).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[opcion[1]] = (suma,tabla)
        valores.append(suma)
        leyenda.append(opcion[1])

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Ha conocido de niños, niñas o adolescentes que hayan sido abusados sexualmente?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/percepcion/ninos_abusados.html', RequestContext(request, locals()))
    
def __percepcion_ninos_abusados(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}    
    for opcion in SI_NO:
        suma = Percepcion.objects.filter(encuesta__in=encuestas, conoce_abusados=opcion[0]).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[opcion[1]] = (suma,tabla)

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True) 
    dict = {'dicc2':dicc2}
    return dict
    
def percepcion_ninos_xls(request):
    dict = __percepcion_ninos_abusados(request)
    return write_xls('encuesta/percepcion/ninos_abusados_xls.html', dict, 'ninos_abusados.doc')
    
def percepcion_ninos_pdf(request):
    dict = __percepcion_ninos_abusados(request)
    return write_pdf('encuesta/percepcion/ninos_abusados_xls.html', dict)
#-------------------------------------------------------------------------------  
    
def percepcion_familia(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in QueFamilia.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, que_familia=opcion).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[opcion.nombre] = (suma,tabla)
        valores.append(suma)
        leyenda.append(opcion.nombre)  
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)

    return render_to_response('encuesta/percepcion/familia_abuso.html', RequestContext(request, locals())) 

def __percepcion_familia(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}    
    for opcion in QueFamilia.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, que_familia=opcion).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[opcion.nombre] = (suma,tabla)
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def percepcion_familia_xls(request):
    dict = __percepcion_familia(request)
    return write_xls('encuesta/percepcion/familia_abuso_xls.html', dict, 'familia_abuso.doc')
    
def percepcion_familia_pdf(request):
    dict = __percepcion_familia(request)
    return write_pdf('encuesta/percepcion/familia_abuso_xls.html', dict)
#-------------------------------------------------------------------------------      
def percepcion_prevenir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in QuienDebe.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, quien_debe=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/percepcion/encargado_prevenir.html', RequestContext(request, locals())) 

def __percepcion_prevenir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in QuienDebe.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, quien_debe=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def percepcion_prevenir_xls(request):
    dict = __percepcion_prevenir(request)
    return write_xls('encuesta/percepcion/encargado_prevenir_xls.html', dict, 'encargado_prevenir.doc')
    
def percepcion_prevenir_pdf(request):
    dict = __percepcion_prevenir(request)
    return write_pdf('encuesta/percepcion/encargado_prevenir_xls.html', dict)
#-------------------------------------------------------------------------------     
def percepcion_mensajes(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in MensajeTransmiten.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, mensaje=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/percepcion/mensajes.html', RequestContext(request, locals()))

def __percepcion_mensajes(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in MensajeTransmiten.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, mensaje=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def percepcion_mensajes_xls(request):
    dict = __percepcion_mensajes(request)
    return write_xls('encuesta/percepcion/mensajes_xls.html', dict, 'mensajes.doc')
    
def percepcion_mensajes_pdf(request):
    dict = __percepcion_mensajes(request)
    return write_pdf('encuesta/percepcion/mensajes_xls.html', dict)
#------------------------------------------------------------------------------- 
    
def percepcion_reducir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []
    dicc = {}    
    for opcion in SI_NO_SABE:
        suma = Percepcion.objects.filter(encuesta__in=encuestas, defender=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)        
        valores.append(suma)
        leyenda.append(opcion[1])        
        dicc[opcion[1]] = (suma,porcentaje)
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)

    grafo_url = grafos.make_graph(valores, leyenda, '¿Cree usted que si la población se organizará para defender los derechos humanos, de niños/as y adolescentes, el abuso se disminuiría?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/percepcion/reducir.html', RequestContext(request, locals())) 

def __percepcion_reducir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}    
    for opcion in SI_NO_SABE:
        suma = Percepcion.objects.filter(encuesta__in=encuestas, defender=opcion[0]).count()
        porcentaje = round(saca_porcentajes(suma,numero),2)               
        dicc[opcion[1]] = (suma,porcentaje)
        
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict

def percepcion_reducir_xls(request):
    dict = __percepcion_reducir(request)
    return write_xls('encuesta/percepcion/reducir_xls.html', dict, 'reducir.doc')
    
def percepcion_reducir_pdf(request):
    dict = __percepcion_reducir(request)
    return write_pdf('encuesta/percepcion/reducir_xls.html', dict)
#-------------------------------------------------------------------------------     
       
def percepcion_iglesia(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in RolIglesia.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, rol_iglesia=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/percepcion/iglesia.html', RequestContext(request, locals())) 

def __percepcion_iglesia(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in RolIglesia.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, rol_iglesia=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict

def percepcion_iglesia_xls(request):
    dict = __percepcion_iglesia(request)
    return write_xls('encuesta/percepcion/iglesia_xls.html', dict, 'iglesia.doc')
    
def percepcion_iglesia_pdf(request):
    dict = __percepcion_iglesia(request)
    return write_pdf('encuesta/percepcion/iglesia_xls.html', dict)
#-------------------------------------------------------------------------------         
def percepcion_medios(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}  
    for opcion in RolMedio.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, rol_medios=opcion).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[opcion.nombre] = (suma,tabla)         

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)    

    return render_to_response('encuesta/percepcion/medios.html', RequestContext(request, locals())) 

def __percepcion_medios(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    dicc = {}  
    for opcion in RolMedio.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, rol_medios=opcion).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[opcion.nombre] = (suma,tabla)         

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict

def percepcion_medios_xls(request):
    dict = __percepcion_medios(request)
    return write_xls('encuesta/percepcion/medios_xls.html', dict, 'medios.doc')

def percepcion_medios_pdf(request):
    dict = __percepcion_medios(request)
    return write_pdf('encuesta/percepcion/medios_xls.html', dict)
#-------------------------------------------------------------------------------     
def percepcion_estado(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in RolEstado.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, rol_estado=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/percepcion/estado.html', RequestContext(request, locals()))

def __percepcion_estado(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in RolEstado.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, rol_estado=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def percepcion_estado_xls(request):
    dict = __percepcion_estado(request)
    return write_xls('encuesta/percepcion/estado_xls.html', dict, 'estado.doc')
    
def percepcion_estado_pdf(request):
    dict = __percepcion_estado(request)
    return write_pdf('encuesta/percepcion/estado_xls.html', dict)
#-------------------------------------------------------------------------------     
def percepcion_ong(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in RolOng.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, rol_ongs=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/percepcion/ongs.html', RequestContext(request, locals()))

def __percepcion_ong(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in RolOng.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, rol_ongs=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def percepcion_ong_xls(request):
    dict = __percepcion_ong(request)
    return write_xls('encuesta/percepcion/ong_xls.html', dict, 'ong.doc')
    
def percepcion_ong_pdf(request):
    dict = __percepcion_ong(request)
    return write_pdf('encuesta/percepcion/ong_xls.html', dict)
#-------------------------------------------------------------------------------     
def percepcion_empresa(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in RolEmpresa.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, rol_empresas=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/percepcion/empresas.html', RequestContext(request, locals()))     

def __percepcion_empresa(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in RolEmpresa.objects.all():
        suma = Percepcion.objects.filter(encuesta__in=encuestas, rol_empresas=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def percepcion_empresa_xls(request):
    dict = __percepcion_empresa(request)
    return write_xls('encuesta/percepcion/empresa_xls.html', dict, 'empresas.doc')
    
def percepcion_empresa_pdf(request):
    dict = __percepcion_empresa(request)
    return write_pdf('encuesta/percepcion/empresa_xls.html', dict)
#-------------------------------------------------------------------------------     
#FUNCIONES UTILITARIAS

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
    
    #filtrar segun la organizacion seleccionada
    org_ids = request.GET.get('org_ids', '')
    if org_ids:
        lista = org_ids.split(',')    
        municipios = [encuesta.municipio for encuesta in Encuesta.objects.filter(organizacion__id__in=lista)]
        #crear los keys en el dicc para evitar KeyError
        for municipio in municipios:
            dicc[municipio.departamento.nombre] = []
        
        #agrupar municipios por departamento padre                
        for municipio in municipios:
            muni = {'id': municipio.id, 'nombre': municipio.nombre}
            if not muni in dicc[municipio.departamento.nombre]:
                dicc[municipio.departamento.nombre].append(muni)            
    
    resultado.append(dicc)
        
    return HttpResponse(simplejson.dumps(resultado), mimetype='application/json')

def get_comunies(request):
    ids = request.GET.get('ids', '')
    if ids:
        lista = ids.split(',')
    results = []
    comunies = Comunidad.objects.filter(municipio__pk__in=lista).order_by('nombre').values('id', 'nombre')

    return HttpResponse(simplejson.dumps(list(comunies)), mimetype='application/json')
    
def get_organi(request):
    ids = request.GET.get('ids', '')
    if ids:
        lista = ids.split(',')    
    municipios = Municipio.objects.filter(departamento__pk__in=lista)
    orgs_id_list = [encuesta.organizacion.pk for encuesta in Encuesta.objects.filter(municipio__in=municipios)]    
    organizaciones = Organizacion.objects.filter(pk__in=orgs_id_list).order_by('nombre').values('id', 'nombre_corto')
    
    return HttpResponse(simplejson.dumps(list(organizaciones)), mimetype='application/json')

#obtener la vista adecuada para los indicadores
def _get_view(request, vista):
    if vista in VALID_VIEWS:
        return VALID_VIEWS[vista](request)
    else:
        raise ViewDoesNotExist("Tried %s in module %s Error: View not define in VALID_VIEWS." % (vista, 'encuesta.views'))

VALID_VIEWS = {
    'jefe': familia_jefe,
    'vivecon': familia_vivecon,
    'miembros': familia_miembros,
    #vistas para conocimiento
    'que-es-abuso': conocimiento_abuso,
    'en-que-lugar': conocimiento_lugar,
    'quines-abusan': conocimiento_abusan_ninos,
    'como-prevenir': conocimiento_prevenir,
    'leyes': conocimiento_leyes,
    'donde-aprendio': conocimiento_aprendio,
    'donde-informarse': conocimiento_informarse,
    #vistas para actitud
    'porque-abuso': actitud_abuso,
    'abusadores': actitud_piensa,
    'victimas': actitud_victimas,
    'familia-ensena-ninos': actitud_familia,
    'escuela-ensena': actitud_escuela,
    #vistas para prácticas
    'que-haria-en-caso': practica_situacion,
    'para-prevenir': practica_prevenir,
    'participacion': practica_participa_prevenir,
    'como-participacion': practica_como,
    #vistas para estado actual
    'problema-comunidad': estado_problema,
    'problema-pais': estado_problema_pais,
    'atencion': estado_atencion,
    'lugares-atencion': estado_lugares,
    'tipo-atencion': estado_tipo_atencion,
    'donde-ir': estado_donde,
    #vistas para percepcion
    'ninos-abusados': percepcion_ninos_abusados,
    'donde-se-da':  percepcion_familia,
    'encargados-prevenir': percepcion_prevenir,
    'mensajes-ninos': percepcion_mensajes,
    'poblacion-organizada': percepcion_reducir,
    'rol-medios': percepcion_medios,
    'rol-iglesia': percepcion_iglesia,
    'rol-estado': percepcion_estado,
    'rol-ong': percepcion_ong,
    'rol-emp': percepcion_empresa,
    #vista de datos generales
    'general': generales,
    #vistas para las descargas familia en xls
    'vivecon_xls': vivencon_xls,
    'jefe_xls': familia_jefe_xls,
    'miembros_xls': familia_miembros_xls,
    #descargas conocimiento xls
    'conocimiento_abuso_xls':conocimiento_abuso_xls,    
    }

def get_prom(total, cantidad):
    """Funcion para sacar promerio"""
    if total == None or cantidad == None or total == 0:
        x = 0
    else:
        x = (cantidad * 100) / float(total)
    return x
    
def saca_porcentajes(values):
    """sumamos los valores y devolvemos una lista con su porcentaje"""
    total = sum(values)
    valores_cero = [] #lista para anotar los indices en los que da cero el porcentaje
    for i in range(len(values)):
        porcentaje = (float(values[i])/total)*100
        values[i] = "%.2f" % porcentaje + '%' 
    return values

def saca_porcentajes(dato, total, formato=True):
    '''Si formato es true devuelve float caso contrario es cadena'''
    if dato != None:
        try:
            porcentaje = (dato/float(total)) * 100 if total != None or total != 0 else 0
        except:
            return 0
        if formato:
            return porcentaje
        else:
            return '%.2f' % porcentaje
    else: 
        return 0
        
def write_xls(template_src, context_dict, filename):
    response = render_to_response(template_src, context_dict)
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-word'
    response['Charset']='UTF-8'
    return response
    
def write_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
    html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al procesar pdf %s' % cgi.escape(html))
