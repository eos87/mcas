# -*- coding: UTF-8 -*-
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
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
            return HttpResponseRedirect('/indicadores/')
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
    escolaridad = []
    for escuela in NIVEL_EDUCATIVO:
        conteo = encuestas.filter(escolaridad=escuela[0]).aggregate(conteo=Count('escolaridad'))['conteo']
        porcentaje = round(saca_porcentajes(conteo,numero),2)
        escolaridad.append([escuela[1],conteo,porcentaje])
        
    civil = []
    for estado in ESTADO_CIVIL:
        conteo = encuestas.filter(estado_civil=estado[0]).aggregate(conteo=Count('estado_civil'))['conteo']
        porcentaje = round(saca_porcentajes(conteo,numero),2)
        civil.append([estado[1],conteo,porcentaje])
         
    religion = []
    for re in IMPORTANCIA_RELIGION:
        conteo = encuestas.filter(importancia_religion=re[0]).aggregate(conteo=Count('importancia_religion'))['conteo']
        porcentaje = round(saca_porcentajes(conteo,numero),2)
        religion.append([re[1],conteo,porcentaje])
        
    depart = []   
    for depar in Departamento.objects.all():
        conteo = encuestas.filter(municipio__departamento=depar).aggregate(conteo=Count('municipio__departamento'))['conteo']
        porcentaje = round(saca_porcentajes(conteo,numero),2)
        if conteo != 0:
            depart.append([depar.nombre,conteo,porcentaje])       
    
    munis = []
    for mun in Municipio.objects.all():
        conteo = encuestas.filter(municipio=mun).aggregate(conteo=Count('municipio'))['conteo']
        porcentaje = round(saca_porcentajes(conteo,numero),2)
        if conteo != 0:
            munis.append([mun.nombre,conteo,porcentaje])
    
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
    return write_xls('encuesta/familia/jefe_xls.html', dict, 'jefe.xls')  
#-------------------------------------------------------------------------------
def familia_vivecon(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyendas = []
    dicc = {}
    for quien in ViveCon.objects.all()[:8]:        
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
    for quien in ViveCon.objects.all()[:8]:        
        suma = Familia.objects.filter(encuesta__in=encuestas, vive_con=quien).count()
        tabla = round(saca_porcentajes(suma,numero),1)        
        dicc[quien.nombre] = (suma,tabla)

    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    dict = {'dicc2':dicc2}
    return dict
    
def vivencon_xls(request):
    dict = __vivencon_xls__(request)
    print dict
    return write_xls('encuesta/familia/vivecon_xls.html', dict, 'vive_con_quien.xls')
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
    
def __familia_miembros(request):
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
    return write_xls('encuesta/familia/miembros_xls.html', dict, 'miembros.xls')
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
    return write_xls('encuesta/conocimiento/abuso_xls.html', dict, 'conocimiento.xls')
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
    

def conocimiento_leyes(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []    
    for opcion in SI_NO:
        suma = Conocimiento.objects.filter(encuesta__in=encuestas, conoce_ley=opcion[0]).count()
        valores.append(suma)
        leyenda.append(opcion[1])        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Conoce sobre las leyes que castigan a las personas que abusan?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/conocimiento/leyes.html', RequestContext(request, locals()))
    
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
    
def actitud_familia(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []    
    for opcion in SI_NO:
        suma = Actitud.objects.filter(encuesta__in=encuestas, familia_ensena=opcion[0]).count()
        valores.append(suma)
        leyenda.append(opcion[1])        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Estaría usted de acuerdo que en la Familia se enseñe a los niños, niñas y adolescentes a prevenir el abuso sexual?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/actitud/familia.html', RequestContext(request, locals()))  
    
def actitud_escuela(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []    
    for opcion in SI_NO:
        suma = Actitud.objects.filter(encuesta__in=encuestas, escuela_ensena=opcion[0]).count()
        valores.append(suma)
        leyenda.append(opcion[1])        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Estaría usted de acuerdo que en la Escuela se enseñe a los niños, niñas y adolescentes a prevenir el abuso sexual?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/actitud/escuela.html', RequestContext(request, locals()))
    
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
    
def practica_participa_prevenir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []    
    for opcion in SI_NO:
        suma = Practica.objects.filter(encuesta__in=encuestas, participa_prevenir=opcion[0]).count()
        valores.append(suma)
        leyenda.append(opcion[1])        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Usted participa o ha participado en algún tipo de organización que previene el abuso sexual?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/practica/participa_prevenir.html', RequestContext(request, locals()))
    
def practica_como(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()    
    dicc = {}
    for hacer in ComoParticipo.objects.all():
        suma = Practica.objects.filter(encuesta__in=encuestas, como=hacer).count()
        tabla = round(saca_porcentajes(suma,numero),1)
        dicc[hacer.nombre] = (suma,tabla)
    
    dicc2 = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    
    return render_to_response('encuesta/practica/como.html', RequestContext(request, locals())) 
    
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
    
def estado_problema_pais(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []    
    for opcion in PROBLEMA:
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, problema_pais=opcion[0]).count()
        valores.append(suma)
        leyenda.append(opcion[1])        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Usted considera que el abuso sexual es un problema en el país?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/estado/problema_pais.html', RequestContext(request, locals()))
    
def estado_atencion(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []    
    for opcion in SI_NO:
        suma = EstadoActual.objects.filter(encuesta__in=encuestas, personas_atienden=opcion[0]).count()
        valores.append(suma)
        leyenda.append(opcion[1])        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Sabe si hay lugares o personas en esta comunidad que atienden a niños/as, adolescentes que vivieron abuso sexual?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/estado/atencion.html', RequestContext(request, locals()))
    
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
    
def percepcion_reducir(request):
    encuestas = _query_set_filtrado(request)
    numero = encuestas.count()
    valores = []
    leyenda = []    
    for opcion in SI_NO_SABE:
        suma = Percepcion.objects.filter(encuesta__in=encuestas, defender=opcion[0]).count()
        valores.append(suma)
        leyenda.append(opcion[1])        

    grafo_url = grafos.make_graph(valores, leyenda, '¿Cree usted que si la población se organizará para defender los derechos humanos, de niños/as y adolescentes, el abuso se disminuiría?', type=grafos.PIE_CHART_3D, pie_labels=True)

    return render_to_response('encuesta/percepcion/reducir.html', RequestContext(request, locals())) 
    
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
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Charset']='UTF-8'
    return response
