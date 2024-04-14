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
    path('cargarFiltroMigracion/', views.cargarFiltroMigracion, name='cargarFiltroMigracion'),
    path('listarMigracion/', views.listarMigracion, name='listarMigracion'),


    path('cargarMicroondas/', views.cargarMicroondas, name='cargarMicroondas'),
    path('cargarFiltroMicroondas/', views.cargarFiltroMicroondas, name='cargarFiltroMicroondas'),
    path('listarMicroondas/', views.listarMicroondas, name='listarMicroondas'),

    path('cargarCarrier/', views.cargarCarrier, name='cargarCarrier'),
    path('cargarFiltroCarrier/', views.cargarFiltroCarrier, name='cargarFiltroCarrier'),
    path('listarCarrier/', views.listarCarrier, name='listarCarrier'),


    path('cargarPon/', views.cargarPon, name='cargarPon'),
    path('listarPon/', views.listarPon, name='listarPon'),

    path('cargarPanda/', views.cargarPanda, name='cargarPanda'),
    path('listarPanda/', views.listarPanda, name='listarPanda'),

    path('cargarTellus/', views.cargarTellus, name='cargarTellus'),
    path('listarTellus/', views.listarTellus, name='listarTellus'),
    
    path('cargarCapacidadManual/', views.cargarCapacidadManual, name='cargarCapacidadManual'),

    
    path('cargarSemaforos/', views.cargarSemaforos, name='cargarSemaforos'),
    path('listarSemaforos/', views.listarSemaforos, name='listarSemaforos'),

    path('cargarCapacidadManual/', views.cargarCapacidadManual, name='cargarCapacidadManual'),
    path('cargarFiltroCapacidadManual/', views.cargarFiltroCapacidadManual, name='cargarFiltroCapacidadManual'),
    path('listarCapacidadManual/', views.listarCapacidadManual, name='listarCapacidadManual'),
    
    path('cargarBaseSinTx/', views.cargarBaseSinTx, name='cargarBaseSinTx'),
    path('cargarFiltroBaseSinTx/', views.cargarFiltroBaseSinTx, name='cargarFiltroBaseSinTx'),
    path('listarBaseSinTx/', views.listarBaseSinTx, name='listarBaseSinTx'),
]