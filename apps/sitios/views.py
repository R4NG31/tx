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

#----------------------  SITIOS   ---------------------------#
def listarSitios(request):
    busqueda = request.POST.get("buscar")
    sitios = SitiosTotales.objects.all()
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

    return render(request, "sitios/listarSitios.html",data)

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
    fo = FibraOptica.objects.all()
    # if busqueda:
    #     fo = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(fo,15)
        fo = paginator.page(page)
    except:
        raise Http404
    data = {'entity':fo,'paginator': paginator }

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
    agredaor = AGG.objects.all()
    # if busqueda:
    #     agredaor = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(agredaor,15)
        agredaor = paginator.page(page)
    except:
        raise Http404
    data = {'entity':agredaor,'paginator': paginator }

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

def listarProyeccion(request):
    busqueda = request.POST.get("buscar")
    sitios = Proyeccion.objects.all()
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

    return render(request, "sitios/listarProyeccion.html",data)

#---------------------- MIGRACION   ---------------------------#
def cargarMigracion(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,'-')
        df.rename(columns=nomColsMigracion,inplace=True)
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        
        engine = create_engine(conexion(),echo=False)
        df.to_sql(Migracion._meta.db_table, if_exists='replace',con=engine,index=False)

    return render(request, "sitios/cargarMigracion.html")

def cargarFiltroMigracion(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
            
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,'-')
        df.rename(columns=nomColsMigracion,inplace=True)
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        control = df['CONTROL'] != 'BAJA'
        df = df[control]
        engine = create_engine(conexion(),echo=False)
        df.to_sql(FiltroMigracion._meta.db_table, if_exists='replace',con=engine,index=False)

    return render(request, "sitios/cargarFiltroMigracion.html")

def listarMigracion(request):
    busqueda = request.POST.get("buscar")
    migracion = Migracion.objects.all()
    # if busqueda:
    #     migracion = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(migracion,15)
        migracion = paginator.page(page)
    except:
        raise Http404
    data = {'entity':migracion,'paginator': paginator }

    return render(request, "sitios/listarMigracion.html",data)


#---------------------- MICROONDAS   ---------------------------#

def cargarMicroondas(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,'-')
        df.rename(columns=nomColsMW,inplace=True)   
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        engine = create_engine(conexion(),echo=False)
        df.to_sql(MW._meta.db_table, if_exists='replace', con=engine,index=False)

    return render(request, "sitios/cargarMicroondas.html")

def cargarFiltroMicroondas(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
            
        df = pd.read_excel(upload_file, engine='openpyxl',header=1)
        df = df.replace(np.nan,' ')
        df.rename(columns=nomColsMW,inplace=True)   
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        control_b = df['CONTROL'] != 'BAJA'
        control_r = df['CONTROL'] != 'REVISAR'
        df = df[control_b & control_r]

        engine = create_engine(conexion(),echo=False)
        df.to_sql(MW._meta.db_table, if_exists='replace', con=engine,index=False)

    return render(request, "sitios/cargarFiltroMicroondas.html")

def listarMicroondas(request):
    busqueda = request.POST.get("buscar")
    mw = MW.objects.all()
    # if busqueda:
    #     mw = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(mw,15)
        mw = paginator.page(page)
    except:
        raise Http404
    data = {'entity':mw,'paginator': paginator }

    return render(request, "sitios/listarMicroondas.html",data)

#---------------------- CARRIER   ---------------------------#
def cargarCarrier(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,' ')
        df.rename(columns=nomColsCarrier,inplace=True)
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        engine = create_engine(conexion(),echo=False)
        df.to_sql(Carrier._meta.db_table, if_exists='replace', con=engine,index=False)

    return render(request, "sitios/cargarCarrier.html")



def cargarFiltroCarrier(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
            
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,' ')
        df.rename(columns=nomColsCarrier,inplace=True)
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        control = df['CONTROL'] != 'BAJA'
        df = df[control]
        engine = create_engine(conexion(),echo=False)
        df.to_sql(FiltroCarrier._meta.db_table, if_exists='replace', con=engine,index=False)

    return render(request, "sitios/cargarFiltroCarrier.html")

def listarCarrier(request):
    busqueda = request.POST.get("buscar")
    pon = Carrier.objects.all()
    # if busqueda:
    #     pon = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(pon,15)
        pon = paginator.page(page)
    except:
        raise Http404
    data = {'entity':pon,'paginator': paginator }

    return render(request, "sitios/listarCarrier.html",data)

#---------------------- PON   ---------------------------#

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

def listarPon(request):
    busqueda = request.POST.get("buscar")
    pon = Pon.objects.all()
    # if busqueda:
    #     pon = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(pon,15)
        pon = paginator.page(page)
    except:
        raise Http404
    data = {'entity':pon,'paginator': paginator }

    return render(request, "sitios/listarPon.html",data)

#--------------------------------- PANDA ---------------------------------#
def cargarPanda(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,' ')
        df.rename(columns=nomColsPanda,inplace=True)
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        engine = create_engine(conexion(),echo=False)
        df.to_sql(Panda._meta.db_table,if_exists='replace',con=engine,index=False)

    return render(request, "sitios/cargarPanda.html")

def listarPanda(request):
    busqueda = request.POST.get("buscar")
    panda = Panda.objects.all()
    # if busqueda:
    #     panda = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(panda,15)
        panda = paginator.page(page)
    except:
        raise Http404
    data = {'entity':panda,'paginator': paginator }

    return render(request, "sitios/listarPanda.html",data)
   
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

def listarTellus(request):
    busqueda = request.POST.get("buscar")
    tellus = Tellus.objects.all()
    # if busqueda:
    #     tellus = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(tellus,15)
        tellus = paginator.page(page)
    except:
        raise Http404
    data = {'entity':tellus,'paginator': paginator }

    return render(request, "sitios/listarTellus.html",data)

def cargarSemaforos(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
            
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan,' ')
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        df.rename(columns=nomColsSemaforo,inplace=True)
                        
        engine = create_engine(conexion(),echo=False)
        df.to_sql(Semaforos._meta.db_table,if_exists='replace',con=engine,index=False)
    return render(request, "sitios/cargarSemaforos.html")
 
def listarSemaforos(request):
    busqueda = request.POST.get("buscar")
    semaforos = Semaforos.objects.all()
    # if busqueda:
    #     semaforos = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(semaforos,15)
        semaforos = paginator.page(page)
    except:
        raise Http404
    data = {'entity':semaforos,'paginator': paginator }

    return render(request, "sitios/listarSemaforos.html",data)
 
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

def cargarFiltroCapacidadManual(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
            
        df = pd.read_excel(upload_file, engine='openpyxl',header=0)
        df = df.replace(np.nan, ' ')
        for name in df.columns:
            df[name] = df[name].apply(lambda value:" ".join(str(value).strip().split()))
            df[name] = df[name].str.upper()
        df.rename(columns=nomColsCapacidadManual,inplace=True)
        control = df['CONTROL'] != 'BAJA'
        df = df[control]
        engine = create_engine(conexion(),echo=False)
        df.to_sql(FiltroCapacidadManual._meta.db_table,if_exists='replace',con=engine,index=False)
    return render(request, "sitios/cargarFiltroCapacidadManual.html")

def listarCapacidadManual(request):
    busqueda = request.POST.get("buscar")
    semaforos = CapacidadManual.objects.all()
    # if busqueda:
    #     semaforos = FibraOptica.objects.filter(
    #         Q(ATTID__icontains = busqueda) | Q(ESTADO__icontains = busqueda)).distinct()

    page = request.GET.get('page',1)
    try:
        paginator = Paginator(semaforos,15)
        semaforos = paginator.page(page)
    except:
        raise Http404
    data = {'entity':semaforos,'paginator': paginator }

    return render(request, "sitios/listarCapacidadManual.html",data)
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






