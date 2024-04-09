from django.shortcuts import render,redirect
from apps.sitios.forms import *
from apps.sitios.models import *
from  apps.sitios.conexion import conexion
import pandas as pd
from  sqlalchemy import create_engine
import openpyxl
import numpy as np
from django.views.generic import TemplateView,ListView
from django.core.paginator import Paginator
from django.http import Http404
from apps.sitios.dicColumns import *

class Home(TemplateView):
    template_name= 'index.html'

def listarSitios(request):
    sitios = SitiosTotales.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(sitios,15)
        sitios = paginator.page(page)
    except:
        raise Http404
    
    data = {'entity': sitios,'paginator': paginator }
    return render(request, "sitios/listarSitios.html", data)

def crearSitios(request):
    if request.method == 'POST':
        sitios_form = SitiosTotalesForm(request.POST)
        if sitios_form.is_valid():
            sitios_form.save()
        return redirect('listarSitios')     
    else:
        sitios_form = SitiosTotalesForm()
    data = {'sitios_form':sitios_form}    
    return render(request, "sitios/crearSitio.html", data)    
    
def editarSitios(request, S_ATT_ID):
    sitios = SitiosTotales.objects.get(S_ATT_ID = S_ATT_ID)
    if request.method == 'GET':
        sitios_form = SitiosTotalesForm(instance= sitios)
    else:
        sitios_form = SitiosTotalesForm(request.POST, instance=sitios)
        if sitios_form.is_valid():
            sitios_form.save()
        return redirect('listarSitios')   
    data = {'sitios_form':sitios_form}
    return render(request, 'sitios/crearSitio.html', data)     
     
def cargarSitios(request):
    engine = create_engine(conexion(),echo=False)
    if request.method == "POST":
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl', header=1)
        df = df.replace('-',' ')
        df.columns = df.columns.str.strip()
        df.rename(columns=nomColsSitios,inplace=True)
        for name in df.columns:
             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
             df[name] = df[name].str.upper()
        df.to_sql(SitiosTotales._meta.db_table, if_exists='replace', con=engine,index=False)   
    return render(request, "sitios/cargarSitios.html")

def cargarFiltroSitios(request):
    cols = [0,1,2,7,8,9,10,11,12,13,14,18,19]
    engine = create_engine(conexion(),echo=False)
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl', usecols=cols, header=0)
        df = df.replace('-',' ')
        df.columns = df.columns.str.strip()
        df.rename(columns=nomColsFiltroSitios, inplace=True)
        for name in df.columns:
             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
             df[name] = df[name].str.upper()
        df_filtro_c = df['CLASIFICACION'] != 'Alpha'
        df_filtro_t = df['TECNOLOGIA'] != '-'
        df= df[df_filtro_c & df_filtro_t]
        
        df.to_sql(FiltroSitiosTotales._meta.db_table, if_exists='replace', con=engine,index=False)
    return render(request, "sitios/cargarSitios.html")

def cargarFO(request):
    engine = create_engine(conexion(),echo=False)
    if request.method == "POST":
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl', header=1)
        df = df.replace(np.nan,' ')
        df.columns = df.columns.str.strip()
        df.rename(columns=nomColsFO, inplace=True)
        for name in df.columns:
             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
             df[name] = df[name].str.upper()
        df.to_sql(FibraOptica._meta.db_table, if_exists='replace', con=engine,index=False)           
    return render(request, "sitios/cargarFO.html")

def cargarFiltroFO(request):
    engine = create_engine(conexion(),echo=False)
    cols = [0,1,2,3,4,5,6,7,16,19,20,21,22,23]
 
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl', usecols=cols, header=1)
        df.columns = df.columns.str.strip()
        df = df.replace(np.nan,' ')
        df.rename(columns=nomColsFO,inplace=True)
        for name in df.columns:
             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
             df[name] = df[name].str.upper()
        df_alta_activo = df['CONTROL'] !='BAJA'
        df_vacio_id = df['ID_ATT_F'] = ' '
        df = df[df_alta_activo]
        df.to_sql(FiltroFibraOptica._meta.db_table, if_exists='replace', con=engine,index=False)    
    return render(request, "sitios/cargarFiltroFO.html")

def listarFO(request):
    busqueda = request.POST.get("buscar")
    sitios = FibraOptica.objects.all()
    # if busqueda:
    #     sitios = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(sitios,15)
        sitios = paginator.page(page)
    except:
        raise Http404
    data = {'entity':sitios,'paginator': paginator }

    return render(request, "sitios/listarFO.html",data)

def cargarAGG(request):
    engine = create_engine(conexion(),echo=False)
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=1)
        df = df.replace(np.nan,' ')
        df.columns = df.columns.str.strip() 
        df.rename(columns=nomColsAgg, inplace=True)
        for name in df.columns:
             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
             df[name] = df[name].str.upper()
        df.to_sql(AGG._meta.db_table, if_exists='replace', con=engine,index=False)

    return render(request, "sitios/cargarAGG.html")

def cargarFiltroAGG(request):
    cols = [0,1,2,3,4,5,6,7,16,18,19,20,21,22,23]

    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',usecols=cols,header=1)
        df = df.replace(np.nan,' ')

        df.rename(columns=nomColsFiltroAgg, inplace=True)
        for name in df.columns:
             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
             df[name] = df[name].str.upper()
        
        control = df['CONTROL'] != 'BAJA'
        proyecto = df['PROYECTO'] != '-'
        df = df[control & proyecto]
        engine = create_engine(conexion(),echo=False)
        df.to_sql(Filtro_AGG._meta.db_table, if_exists='replace', con=engine,index=False)

    return render(request, "sitios/cargarFiltroAGG.html")

def listarAGG(request):
    busqueda = request.POST.get("buscar")
    sitios = FibraOptica.objects.all()
    # if busqueda:
    #     sitios = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(sitios,15)
        sitios = paginator.page(page)
    except:
        raise Http404
    data = {'entity':sitios,'paginator': paginator }

    return render(request, "sitios/listarAGG.html",data)

#----------------------  PROYECCION   ---------------------------#
def cargarProyeccion(request):
    engine = create_engine(conexion(),echo=False)
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=1)
        df = df.replace(np.nan,' ')
        df.rename(columns=nomColsProyeccion,inplace=True)
        for name in df.columns:
             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
             df[name] = df[name].str.upper()
        df.to_sql(Proyeccion._meta.db_table, if_exists='replace', con=engine,index=False)

    return render(request, "sitios/cargarProyeccion.html")

#---------------------- FILTRO PROYECCION   ---------------------------#
def cargarFiltroProyeccion(request):
    cols = [0,1,2,3,4,5,6,7,8,17,20,21,22,24]   
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',usecols=cols,header=1)
        df = df.replace(np.nan,' ')
        df.rename(columns=nomColsProyeccion,inplace=True)
        for name in df.columns:
             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
             df[name] = df[name].str.upper()
        control_p = df['CONTROL'] != 'BAJA'
        df = df[control_p]
        engine = create_engine(conexion(),echo=False)
        df.to_sql(FiltroProyeccion._meta.db_table, if_exists='replace', con=engine,index=False)

    return render(request, "sitios/cargarFiltroProyeccion.html")

def cargarMigracion(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,'-')
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        engine = create_engine(conexion(),echo=False)
        df.rename(columns=nomColsMigracion,inplace=True)
        
        df.to_sql(Migracion._meta.db_table, if_exists='replace',con=engine,index=False)

    return render(request, "sitios/cargarMigracion.html")

# def cargarFiltroMigracion(request):
#     if request.method == 'POST':
#         upload_file = request.FILES['file']
            
#         df = pd.read_excel(upload_file, engine='openpyxl',header=0)
#         df = df.replace(np.nan,'-')
#         for name in df.columns:
#             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
#             df[name] = df[name].str.upper()
#         engine = create_engine(conexion(),echo=False)
#         df.rename(
#             columns={'ID ATT':'ID_ATT_M','Origen TX':'ORIGEN_TX','TX Grupos':'TX_GRUPOS','TX Detalle':'TX_DETALLE','Control':'CONTROL',	
#                     'Fecha':'FECHA','POC':'POC','Observaciones':'OBSERVACIONES','ID Panda':'ID_PANDA','ID_ATT':'ID_ATT',	
#                     'Site Name':'SITE_NAME','MARKET':'MARKET','Proyecto':'PROYECTO','Real Migracion':'REAL_MIGRACION',	
#                     'Scope':'SCOPE','Panda':'PANDA','Status':'STATUS','TX TYPE':'TX_TYPE','AT&T ID':'ATT_ID','Latitud':'LATITUD',	
#                     'Longitud':'LONGITUD','Estado':'ESTADO','Municipio':'MUNICIPIO','Mercado':'MERCADO','Region_Celular':'REGION_CELULAR',	
#                     'Clasificacion':'CLASIFICACION','Control de cambios RAN':'CONTROL_DE_CAMBIOS_RAN'},inplace=True)
#         control = df['CONTROL'] != 'BAJA'
#         df = df[control]
#         df.to_sql(Migracion._meta.db_table, if_exists='replace',con=engine,index=False)

#     return render(request, "sitios/cargarProyeccion.html")

def cargarMicroondas(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,'-')
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        df.rename(columns=nomColsMW,inplace=True)   
        engine = create_engine(conexion(),echo=False)
        df.to_sql(MW._meta.db_table, if_exists='replace', con=engine,index=False)

    return render(request, "sitios/cargarMicroondas.html")

# def cargarFiltroMicrondas(request):
#     if request.method == 'POST':
#         upload_file = request.FILES['file']
            
#         df = pd.read_excel(upload_file, engine='openpyxl',header=1)
#         df = df.replace(np.nan,' ')
#         for name in df.columns:
#             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
#             df[name] = df[name].str.upper()
#         df.rename(
#             columns={'ATTID ':'ATT_ID_MW','TX MW':'TX_MW','TX Grupos MW':'TX_GRUPOS_MW','TX Detalle MW':'TX_DETALLE_MW','Control':'CONTROL', 
#                     'Fecha':'FECHA','POC':'POC','Observaciones':'OBSERVACIONES','Nombre':'NOMBRE','Latitud':'LATITUD','Longitud':'LONGITUD',
#                     'Estado':'ESTADO','Municipio':'MUNICIPIO','Mercado':'MERCADO','Region_Celular':'REGION_CELULAR',
#                     'Control de cambios RAN':'CONTROL_DE_CAMBIOS_RAN','Proyecto Migrados':'PROYECTO_MIGRADOS','Real Migracion':'REAL_MIGRACION',
#                     'TX Origen':'TX_ORIGEN','Medio TX \nGrupos':'MEDIO_TX_GRUPOS','TX Detalle':'TX_DETALLE','Panda':'PANDA','Status':'STATUS',	
#                     'TX TYPE':'TX_TYPE','Capacidad 1G':'CAPACIDAD_1G','Sitio A ':'SITIO_A','Sitio B':'SITIO_B','Enlace':'ENLACE',
#                     'Tecnologia':'TECNOLOGIA','Agregador Grupo':'AGREGADOR_GRUPO','Agregador Detalle':'AGREGADOR_DETALLE',
#                     'Agregador':'AGREGADOR_1','Tracker':'TRACKER','ATTID':'ATT_ID', 'Sitio A':'SITE_A','Sitio B.1':'SITE_B','Link':'LINK',
#                     'Agregador.1':'AGREGADOR_2','Site 1':'SITE_1','Site 2':'SITE_2','Site 3':'SITE_3','Site 4':'SITE_4','Site 5':'SITE_5',
#                     'Site 6':'SITE_6','Site 7':'SITE_7','Site 8':'SITE_8','Site 9':'SITE_9','Site 10':'SITE_10','Sitios Carga':'SITIOS_CARGA',
#                     'Tipo':'TIPO','ATTID.1':'ATTID','TECNOLOGIA ACTUAL':'TECNOLOGIA_ACTUAL','Capacidad (Mbps)':'CAPACIDAD_MBPS',
#                     'Utilización (Mbps)':'UTILIZACIÓN_MBPS','Flag H':'FLAG_H','Numero_de_Certificado':'NUMERO_DE_CERTIFICADO',
#                     'Numero_de_Link':'NUMERO_DE_LINK','Identificador_Certificado':'IDENTIFICADOR_CERTIFICADO','Concesionario':'CONCESIONARIO',
#                     'Responsable_Cons':'RESPONSABLE_CONS','Dirección_Cons':'DIRECCION_CONS','Teléfono_Cons':'TELEFONO_CONS',	
#                     'E-mail_Cons':'E_MAIL_CONS','Usuaruo_Final':'USUARIO_FINAL','Responsable_Us':'RESPONSABLE_US','Dirección_Us':'DIRECCION_US',	
#                     'Teléfono_Us':'TELEFONO_US','E-mail_Us':'E_MAIL_US','Fecha_solicitud':'FECHA_SOLICITUD','Fecha _Constancia':'FECHA_CONSTANCIA',	
#                     'Fecha de cancelación':'FECHA_DE_CANCELACION','Motivo':'MOTIVO','Nombre_A':'NOMBRE_A','Domicilio_A':'DOMICILIO_A',	
#                     'Ciudad_A':'CIUDAD_A','Clave Estado A':'CLAVE_ESTADO_A','Latitud_grad_A':'LATITUD_GRAD_A','Latitud_min_A':'LATITUD_MIN_A',	
#                     'Latitud_seg_A':'LATITUD_SEG_A','Longitud_grad_A':'LONGITUD_GRAD_A','Longitud_min_A':'LONGITUD_MIN_A',
#                     'Longitud_seg_A':'LONGITUD_SEG_A','ASNM_A':'ASNM_A','Azimut_A':'AZIMUT_A','Nombre_B':'NOMBRE_B','Domicilio_B':'DOMICILIO_B',	
#                     'Ciudad_B':'CIUDAD_B','Clave Estado B':'CLAVE_ESTADO_B','Latitud_grad_B':'LATITUD_GRAD_B','Latitud_min_B':'LATITUD_MIN_B',	
#                     'Latitud_seg_B':'LATITUD_SEG_B','Longitud_grad_B':'LONGITUD_GRAD_B','Longitud_min_B':'LONGITUD_MIN_B',
#                     'Longitud_seg_B':'LONGITUD_SEG_B','ASNM_B':'ASNM_B','Azimut_B':'AZIMUT_B','Longitud_Enlace':'LONGITUD_ENLACE',
#                     'Banda_Frecuencia':'BANDA_FRECUENCIA','Frecuencia_Tx':'FRECUENCIA_TX','Frecuencia_Rx':'FRECUENCIA_RX',	
#                     'Marca_Radio':'MARCA_RADIO','Modelo_Radio':'MODELO_RADIO','Modulación':'MODULACION','Emisión':'EMISION',	
#                     'Ancho_Banda':'ANCHO_BANDA','TX_Planned':'TX_PLANNED','Separación_canal':'SEPARACION_CANAL',	
#                     'Sub_Banda_Op':'SUB_BANDA_OP','Separación_Duplex':'SEPARACION_DUPLEX','Umbra_Recepción':'UMBRA_RECEPCION',	
#                     'Tasa de Bits Umbral':'TASA_DE_BITS_UMBRAL','PIRE':'PIRE','PIRE_A':'PIRE_A','PIRE_B':'PIRE_B','Velocidad_Tx':'VELOCIDAD_TX',
#                     'Capacidad_Canales':'CAPACIDAD_CANALES','Homologación_Equipo':'HOMOLOGACION_EQUIPO',	
#                     'Configuración_Enlace':'CONFIGURACION_ENLACE','Antena_Tipo_A':'ANTENA_TIPO_A','Antena_Marca_A':'ANTENA_MARCA_A',
#                     'Antena_Modelo_A':'ANTENA_MODELO_A','Antena_Diámetro_A':'ANTENA_DIAMETRO_A','Antena_Ganancia_A':'ANTENA_GANANCIA_A',	
#                     'Antena_Polarización_A':'ANTENA_POLARIZACION_A','Antena_Angulo_abertura_A':'ANTENA_ANGULO_ABERTURA_A',	
#                     'Antena_Angulo_elevación_A':'ANTENA_ANGULO_ELEVACION_A','Modelo_Radio_B':'MODELO_RADIO_B','Antena_Tipo_B':'ANTENA_TIPO_B',	
#                     'Antena_Marca_B':'ANTENA_MARCA_B','Antena_Modelo_B':'ANTENA_MODELO_B','Antena_Diámetro_B':'ANTENA_DIAMETRO_B',
#                     'Antena_Ganancia_B':'ANTENA_GANANCIA_B','Antena_Polarización_B':'ANTENA_POLARIZACION_B',	
#                     'Antena_Angulo_abertura_B':'ANTENA_ANGULO_ABERTURA_B','Antena_Angulo_elevación_B':'ANTENA_ANGULO_ELEVACION_B',	
#                     'Línea_Marca_A':'LINEA_MARCA_A','Línea_tipo_A':'LINEA_TIPO_A','Línea_Longitud_A':'LINEA_LONGITUD_A',
#                     'Línea_atenuación_A':'LINEA_ATENUACION_A','Otras Pérdidas Tx A':'OTRAS_PERDIDAS_TX_A',
#                     'Otras Pérdidas Rx A':'OTRAS_PERDIDAS_RX_A','Línea_Marca_B':'LINEA_MARCA_B','Línea_tipo_B':'LINEA_TIPO_B',	
#                     'Línea_Longitud_B':'LINEA_LONGITUD_B','Línea_atenuación_B':'LINEA_ATENUACION_B','Otras Pérdidas Tx B':'OTRAS_PERDIDAS_TX_B',	
#                     'Otras Pérdidas Rx B':'OTRAS_PERDIDAS_RX_B','Edificio_Altura_A':'EDIFICIO_ALTURA_A',
#                     'Torre_Altura_A':'TORRE_ALTURA_A','Torre_Antena_Altura_A':'TORRE_ANTENA_ALTURA_A','Torre_Tipo_A':'TORRE_TIPO_A',
#                     'Edificio_Altura _B':'EDIFICIO_ALTURA_B','Torre_Altura_B':'TORRE_ALTURA_B','Torre_Antena_Altura_B':'TORRE_ANTENA_ALTURA_B',	
#                     'Torre_Tipo_B':'TORRE_TIPO_B','Pot Tx A':'POT_TX_A','Rx_Planned_A':'RX_PLANNED_A','Pote Tx B':'POTE_TX_B','Rx_Planned_B':'RX_PLANNED_B',	
#                     'No_Channel':'NO_CHANNEL','Channel ID  A':'CHANNEL_ID_A','Channel ID  B':'CHANNEL_ID_B','Observaciones Configuracion':'OBSERVACIONES_CONFIGURACION', 
#                     'Proyecto':'PROYECTO','Solicitud':'SOLICITUD','Ellipse':'ELLIPSE','Google':'GOOGLE','Orden de Trabajp':'ORDEN_DE_TRABAJO',	
#                     'Contratista':'CONTRATISTA','Protocolo de Recepcion':'PROTOCOLO_DE_RECEPCION','Rx med A':'RX_MED_A','Rx Med B':'RX_MED_B',
#                     'Gestion':'GESTION','IPLocal':'IPLOCAL','IP Remoto':'IP_REMOTO','No Serie IDU Local':'NO_SERIE_IDU_LOCAL',
#                     'No Serie ODU Local':'NO_SERIE_ODU_LOCAL','No Serie IDU Remoto':'NO_SERIE_IDU_REMOTO','No Serie ODU Remoto':'NO_SERIE_ODU_REMOTO',
#                     'Observaciones Ingenieria':'OBSERVACIONES_INGENIERIA','Desmontajes':'DESMONTAJES','Fecha.1':'FECHA_2','Responsabe':'RESPONSABLE',			
#                          },inplace=True)   
#         control_b = df['CONTROL'] != 'BAJA'
#         control_r = df['CONTROL'] != 'REVISAR'
#         df = df[control_b & control_r]
#         engine = create_engine(conexion(),echo=False)

#         df.to_sql(MW._meta.db_table, if_exists='replace', con=engine,index=False)

#     return render(request, "sitios/cargarMW.html")

def cargarCarrier(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,' ')
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        df.rename(columns=nomColsCarrier,inplace=True)
        engine = create_engine(conexion(),echo=False)
        df.to_sql(Carrier._meta.db_table, if_exists='replace', con=engine,index=False)

    return render(request, "sitios/cargarCarrier.html")

# def cargarFiltroCarrier(request):
#     if request.method == 'POST':
#         upload_file = request.FILES['file']
            
#         df = pd.read_excel(upload_file, engine='openpyxl',header=0)
#         df = df.replace(np.nan,' ')
#         df.rename(columns={
#                     'ID_ATT':'ID_ATT_C','TX':'TX','TX Grupos':'TX_GRUPOS','TX Detalle':'TX_DETALLE','Control':'CONTROL',
#                     'Fecha de Alta o Baja':'FECHA_ALTA_BAJA','POC':'POC','Observaciones':'OBSERVACIONES','TX Carrier':'TX_CARRIER',	
#                     'Proyecto F.O  ':'PROYECTO_FO','Segundo Puerto Habilitado':'SEGUNDO_PUERTO_HABILITADO','CID Carrier':'CID_CARRIER',
#                     'Región':'REGION','Mercado':'MERCADO','Punta A Naming Convention':'PUNTA_A_NAMING_CONVECTION',	
#                     'Punta A ID Sitio':'PUNTA_A_ID_SITIO','Punta A Nombre Sitio':'PUNTA_A_NOMBRE_SITIO',	
#                     'Lat. Punta A':'LATITUD_PUNTA_A','Long. Punta A':'LONGITUD_PUNTA_A','Punta B Naming Convention':'PUNTA_B_NAMING_CONVECTION',	
#                     'Punta B ID Sitio':'PUNTA_B_ID_SITIO','Punta B Nombre Sitio':'PUNTA_B_NOMBRE_SITIO',	
#                     'Lat. Punta B':'LATITUD_PUNTA_B','Long. Punta B':'LONGITUD_PUNTA_B',	
#                     'Carrier':'CARRIER','Tipo Enlace':'TIPO_ENLACE','Proyecto Principal':'PROYECTO_PRINCIPAL',	
#                     'Fase ':'FASE','Capacidad (Mbps)':'CAPACIDAD_MBPS','Estatus':'ESTATUS','TRACKER':'TRACKER',	
#                     'AT&T ID 2':'ATT_ID','Nombre':'NOMBRE','Control de cambios RAN':'CONTROL_DE_CAMBIOS_RAN',	
#                     'Base Origen \nTX':'BASE_ORIGEN_TX','Grupos \nMedio TX ':'GRUPOS_MEDIO_TX',	
#                     'TX Detalle2':'TX_DETALLE_2','Base Origen Proyeccion':'BASE_ORIGEN_PROYECCION' },inplace=True)
#         for name in df.columns:
#             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
#             df[name] = df[name].str.upper()
#         control = df['CONTROL'] != 'BAJA'
#         df = df[control]
#         engine = create_engine(conexion(),echo=False)
#         df.to_sql(Carrier._meta.db_table, if_exists='replace', con=engine,index=False)

#     return render(request, "sitios/cargarCarrier.html")

def cargarPon(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,' ')
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        df.rename(columns=nomColsPon,inplace=True)
        engine = create_engine(conexion(),echo=False)
        df.to_sql(Pon._meta.db_table,if_exists='replace',con=engine,index=False)

    return render(request, "sitios/cargarPon.html")


def cargarPanda(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,' ')
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        df.rename(columns=nomColsPanda,inplace=True)
        engine = create_engine(conexion(),echo=False)
        df.to_sql(Panda._meta.db_table,if_exists='replace',con=engine,index=False)

    return render(request, "sitios/cargarPanda.html")

   
def cargarTellus(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,' ')
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        df.rename(columns=nomColsTellus,inplace=True)
        engine = create_engine(conexion(),echo=False)
        df.to_sql(Tellus._meta.db_table,if_exists='replace',con=engine,index=False)

    return render(request, "sitios/cargarTellus.html")

# def cargarSemaforo(request):
#     if request.method == 'POST':
#         upload_file = request.FILES['file']
            
#         df = pd.read_excel(upload_file, engine='openpyxl',header=0)
#         df = df.replace(np.nan,' ')
#         for name in df.columns:
#             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
#             df[name] = df[name].str.upper()
#         df.rename(columns={
#                     'Aggregator':'AGGREGATOR',	
#                     'Site 1':'SITE_1',	
#                     'Site 2':'SITE_2',	
#                     'Site 3':'SITE_3',	
#                     'Site 4':'SITE_4',	
#                     'Site 5':'SITE_5',	
#                     'Site 6':'SITE_6',	
#                     'Site 7':'SITE_7',	
#                     'Site 8':'SITE_8',	
#                     'Site 9':'SITE_9',	
#                     'Site 10':'SITE_10',
#                     'Site ID':'SITE_ID',	
#                     'ATTID':'ATTID',	
#                     'LINK':'LINK',	
#                     'Tx  Actual':'TX_ACTUAL',	
#                     'SITIOS QUE CARGA':'SITIOS_QUE_CARGA',	
#                     'TECNOLOGIA ACTUAL':'TECNOLOGIA_ACTUAL',	
#                     'Capacidad (Mbps)':'CAPACIDAD_MBPS',	
#                     'Configuración':'CONFIGURACION',	
#                     'Ancho de Banda':'ANCHO_DE_BANDA',	
#                     'TX A':'TX_A',	
#                     'TX B':'TX_B',	
#                     'Utilización (Mbps)':'UTILIZACION_MBPS_1',	
#                     'Porcentaje de Utilización Picos Maximos(%)':'PORCENTAJE_UTILIZACION_PICOS_MAXIMOS',	
#                     'Flag H':'FLAG_H',
#                     'Utilización (Mbps) ':'UTILIZACION_MBPS_2', 	
#                     'Porcentaje de Utilización Picos Maximos(%) ':'PORCENTAJE_UTILIZACION_PICOS_MAXIMOS_2', 	
#                     'Flag V':'FLAG_V',	
#                     'Sitios':'SITIOS',	 
#                     ' Site Floating Mercado':'SITE_FLOATING_MERCADO',	 
#                     ' LINK FLOATING 2023 (Mbps)':'LINK_FLOATING_2023_MBPS',	 
#                     ' FLAG FLOATING 2023 (Mbps)':'FLAG_FLOATING_2023_MBPS',	 
#                     ' PRIORIDAD TAC FLOATING 2023 (Mbps)':'PRIORIDAD_TAC_FLOATING_2023_MBPS',	 
#                     ' SALUD FLOATING 2023 (Mbps)':'SALUD_FLOATING_2023_MBPS',	
#                     'PUNTO DE AFECTACION FLOATING 2023 (Mbps)':'PUNTO_AFECTACION_FLOATING_2023_MBPS',	 
#                     ' Site Floating Municipio':'SITE_FLOATING_MUNICIPIO',	 
#                     ' LINK FLOATING 2024 (Mbps)':'LINK_FLOATING_2024_MBPS',	 
#                     ' FLAG FLOATING 2024 (Mbps)':'FLAG_FLOATING_2024_MBPS',	 
#                     ' PRIORIDAD TAC FLOATING 2024 (Mbps)':'PRIORIDAD_TAC_FLOATING_2024_MBPS',	 
#                     ' SALUD FLOATING 2024 (Mbps)':'SALUD_FLOATING_2024_MBPS',	
#                     'PUNTO DE AFECTACION FLOATING 2024 (Mbps)':'PUNTO_DE_AFECTACION_FLOATING_2024_MBPS',},inplace=True)
                        
#         engine = create_engine(conexion(),echo=False)
#         df.to_sql(Semaforos._meta.db_table,if_exists='replace',con=engine,index=False)
#     return render(request, "sitios/cargarSemaforo.html")
 
def cargarCapacidadManual(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,' ')
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        df.rename(columns=nomColsCapacidadManual,inplace=True)
        engine = create_engine(conexion(),echo=False)
        df.to_sql(CapacidadManual._meta.db_table,if_exists='replace',con=engine,index=False)
    return render(request, "sitios/cargarCapacidadManual.html")

# def cargarFiltroCapacidadManual(request):
#     if request.method == 'POST':
#         upload_file = request.FILES['file']
            
#         df = pd.read_excel(upload_file, engine='openpyxl',header=0)
#         df = df.replace(np.nan, ' ')
#         for name in df.columns:
#             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
#             df[name] = df[name].str.upper()
#         df.rename(columns={
#                         'ID_ATT':'ID_ATT',	
#                         'TX':'TX',	
#                         'TX Grupos Manual':'TX_GRUPOS_MANUAL',	
#                         'TX Detalle Manual':'TX_DETALLE_MANUAL',	
#                         'Control':'CONTROL',	
#                         'Fecha':'FECHA',	
#                         'POC':'POC',	
#                         'Observaciones':'OBSERVACIONES',	
#                         'TRACKER':'TRACKER',	
#                         'AT&T ID':'ATT_ID',	
#                         'Nombre':'NOMBRE',	
#                         'Latitud':'LATITUD',	
#                         'Longitud':'LONGITUD',	
#                         'Estado':'ESTADO',	
#                         'Municipio':'MUNICIPIO',	
#                         'Mercado':'MERCADO',	
#                         'Region_Celular':'REGION_CELULAR',	
#                         'Region':'REGION',	
#                         'Vendor':'VENDOR',	
#                         'Cobertura':'COBERTURA',	
#                         'Tipo':'TIPO',	
#                         'Proyecto':'PROYECTO',	
#                         'Clasificacion':'CLASIFICACION',	
#                         'Control de cambios RAN':'CONTROL_CAMBIOS_RAN',	
#                         'Base Origen TX':'BASE_ORIGEN_TX',	
#                         "Grupos \nMedio TX ":'GRUPOS_MEDIO_TX',	
#                         'TX Detalle':'TX_DETALLE',	
#                         'Capacidad':'CAPACIDAD',	
#                         'Control':'CONTROL'},inplace=True)
#         control = df['CONTROL'] != 'BAJA'
#         df = df[control]
#         engine = create_engine(conexion(),echo=False)
#         df.to_sql(CapacidadManual._meta.db_table,if_exists='replace',con=engine,index=False)
#     return render(request, "sitios/cargarCapacidadManual.html")

# def cargarBaseSinTx(request):
#     if request.method == 'POST':
#         upload_file = request.FILES['file']
            
#         df = pd.read_excel(upload_file, engine='openpyxl',header=0)
#         df = df.replace(np.nan,' ')

#         for name in df.columns:
#             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
#             df[name] = df[name].str.upper()
#         df.rename(
#             columns={
#                     'ID_ATT':'ID_ATT',	
#                     'TX':'TX',	
#                     'TX Grupos Manual':'TX_GRUPOS_MANUAL',	
#                     'TX Detalle Manual':'TX_DETALLE_MANUAL',	
#                     'Control':'CONTROL',	
#                     'Fecha':'FECHA',	
#                     'POC':'POC',	
#                     'Observaciones':'OBSERVACIONES',	
#                     'ID':'TRACKER',	
#                     'AT&T ID':'ATT_ID',	
#                     'Nombre':'NOMBRE',	
#                     'Latitud':'LATITUD',	
#                     'Longitud':'LONGITUD',	
#                     'Estado':'ESTADO',	
#                     'Municipio':'MUNICIPIO',	
#                     'Mercado':'MERCADO',	
#                     'Region_Celular':'REGION_CELULAR',	
#                     'Region':'REGION',	
#                     'Vendor':'VENDOR',	
#                     'Cobertura':'COBERTURA',	
#                     'Tipo':'TIPO',	
#                     'Proyecto':'PROYECTO',	
#                     'Clasificacion':'CLASIFICACION',	
#                     'Control de cambios RAN':'CONTROL_CAMBIOS_RAN',	
#                     'Base Origen \nTX':'BASE_ORIGEN_TX',	
#                     'Grupos \nMedio TX ':'GRUPOS_MEDIO_TX',	
#                     'TX Detalle':'TX_DETALLE',	
#                     'Base Origen \nTX.1':'BASE_ORIGEN_TX_1',	
#                     'Grupos \nMedio TX .1':'GRUPOS_MEDIO_TX_1',	
#                     'TX Detalle.1':'TX_DETALLE_1',	
#                     'Capacidad':'CAPACIDAD',	
#                     'Control.1':'CONTROL_1',	
#                     'Control de cambios RAN.1':'CONTROL_CAMBIOS_RAN_1',	
#                     'Base Origen \nTX.2':'BASE_ORIGEN_TX_2',	
#                     'Grupos \nMedio TX .2':'GRUPOS_MEDIO_TX_2',	
#                     'TX Detalle.2':'TX_DETALLE_2',	
#                     'Panda':'PANDA',	
#                     'Status':'STATUS',	
#                     'TX TYPE':'TX_TYPE',	
#                     'Real Migracion':'REAL_MIGRACION',	
#                     '#':'NUMERO'} ,inplace=True)
    
#         control_b = df['CONTROL'] != 'BAJA'
#         control_r = df['CONTROL'] != 'REVISAR'
#         df = df[control_b & control_r]
#         engine = create_engine(conexion(),echo=False)
#         df.to_sql(BaseSinTX._meta.db_table,if_exists='replace',con=engine,index=False)
#     return render(request, "sitios/cargarBaseSinTx.html")

# def cargarFiltroBaseSinTx(request):
#     cols = [0,1,2,3,4,5,6,7]
    
#     if request.method == 'POST':
#         upload_file = request.FILES['file']
            
#         df = pd.read_excel(upload_file, engine='openpyxl', usecols= cols,header=0)
#         df = df.replace(np.nan,' ')

#         for name in df.columns:
#             df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
#             df[name] = df[name].str.upper()
#         df.rename(
#             columns={
#                     'ID_ATT':'ID_ATT',	
#                     'TX':'TX',	
#                     'TX Grupos Manual':'TX_GRUPOS_MANUAL',	
#                     'TX Detalle Manual':'TX_DETALLE_MANUAL',	
#                     'Control':'CONTROL',	
#                     'Fecha':'FECHA',	
#                     'POC':'POC',	
#                     'Observaciones':'OBSERVACIONES',	
#                     } ,inplace=True)
    
#         control_b = df['CONTROL'] != 'BAJA'
#         control_r = df['CONTROL'] != 'REVISAR'
#         df = df[control_b & control_r]
#         engine = create_engine(conexion(),echo=False)
        
#         df.to_sql(BaseFiltroSinTX._meta.db_table,if_exists='replace',con=engine,index=False)
#     return render(request, "sitios/cargarBaseSinTx.html")



# def listarFO(request):
#     busqueda = request.POST.get("buscar")
#     sitios = Origen_FO.objects.all()
#     if busqueda:
#         sitios = Origen_FO.objects.filter(
#             Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

#     page = request.GET.get('page',1)
#     try:
#         paginator = Paginator(sitios,5)
#         sitios = paginator.page(page)
#     except:
#         raise Http404
#     data = {'entity':sitios,'paginator': paginator }

#     return render(request, "sitios/listarFO.html",data)






