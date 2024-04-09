
from django.contrib import admin
from django.urls import path, include
from apps.sitios.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home.as_view(), name='index'),
    path('sitios/', include('apps.sitios.urls')),

] 
