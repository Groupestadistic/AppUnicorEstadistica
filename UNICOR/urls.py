"""UNICOR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:369369*
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from indicadores.views import *

urlpatterns = [
    path('accounts/', include('allauth.urls')),

    path('admin/', admin.site.urls),

    path('', index, name='index'), 
    path('estudiantes_preg/', estudiantes_preg, name='estudiantes_preg'),
    path('estudiantes_post/', estudiantes_post, name='estudiantes_post'),
    path('docentes/', docentes, name='docentes'),
    path('graduado/', graduado, name='graduado'),
    path('investigacion/', investigacion, name='investigacion'),
    path('bienestar/', bienestar, name='bienestar'),
    path('recurso_financiero/', recurso_financiero, name='recurso_financiero'),
    path('tasa_graduacion/', tasa_graduacion, name='tasa_graduacion'),

    path('zona_privada/',login_required(zona_privada), name='zona_privada'),
    path('zona_privada/num_grupos/',login_required(num_grupos), name='num_grupos'),
    path('zona_privada/cargue_notas/',login_required(cargue_notas), name='cargue_notas'),
    path('zona_privada/estimar_grupos/',login_required(estimar_grupos), name='estimar_grupos'),
    path('zona_privada/consulta_docente/',login_required(consulta_docente), name='consulta_docente')
]
