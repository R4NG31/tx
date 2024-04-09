from django.contrib import admin
from django.urls import path
from django import views
from . import views

urlpatterns = [
    path('cargarSitios/', views.cargarSitios, name='cargarSitios'),
    path('cargarFiltroSitios/', views.cargarFiltroSitios, name='cargarFiltroSitios'),
    path('listarSitios/', views.listarSitios, name='listarSitios'),
    path('crearSitios/', views.crearSitios, name='crearSitios'),
    path('editarSitios/<str:S_ATT_ID>', views.editarSitios, name='editarSitios'),
    
    path('cargarFO/', views.cargarFO, name='cargarFO'),
    path('cargarFiltroFO/', views.cargarFiltroFO, name='cargarFiltroFO'),
    path('listarFO/', views.listarFO, name='listarFO'),
    
    path('listarAGG/', views.listarAGG, name='listarAGG'),
    path('cargarAGG/', views.cargarAGG, name='cargarAGG'),
    path('cargarFiltroAGG/', views.cargarFiltroAGG, name='cargarFiltroAGG'),
   
    path('cargarProyeccion/', views.cargarProyeccion, name='cargarProyeccion'),
    path('cargarFiltroProyeccion/', views.cargarFiltroProyeccion, name='cargarFiltroProyeccion'),
    path('listarProyeccion/', views.listarProyeccion, name='listarProyeccion'),

    path('cargarMigracion/', views.cargarMigracion, name='cargarMigracion'),
    path('cargarMicroondas/', views.cargarMicroondas, name='cargarMicroondas'),
    # path('cargarMW/', views.cargarFiltroMicrondas, name='cargarMW'),
    path('cargarCarrier/', views.cargarCarrier, name='cargarCarrier'),
    path('cargarPon/', views.cargarPon, name='cargarPon'),
    path('cargarPanda/', views.cargarPanda, name='cargarPanda'),
    path('cargarTellus/', views.cargarTellus, name='cargarTellus'),
    path('cargarCapacidadManual/', views.cargarCapacidadManual, name='cargarCapacidadManual'),
    # path('cargarSemaforo/', views.cargarSemaforo, name='cargarSemaforo'),
    #path('cargarCapacidadManual/', views.cargarFiltroCapacidadManual, name='cargarCapacidadManual'),
    # path('cargarNOC/', views.cargarNOC, name='cargarNOC'),
    # path('cargarBaseSinTx/', views.cargarFiltroBaseSinTx, name='cargarBaseSinTx'),
]
#ver especificamente a que tipo de tx transporte
#ept = sitios al aire