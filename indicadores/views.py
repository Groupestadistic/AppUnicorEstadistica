from email.mime import base
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# import pandas

# Create your views here.
def index(request):
    return render(request,'base/index.html',{})

@method_decorator(csrf_exempt)
def prueba(request):
    return render(request,'ajax/estudiantes/prueba.html', {})

@method_decorator(csrf_exempt)
def estudiantes_preg(request):
    return render(request,'ajax/estudiantes/estudiantes_preg.html', {})

@method_decorator(csrf_exempt)
def estudiantes_post(request):
    return render(request,'ajax/estudiantes/estudiantes_post.html', {})

@method_decorator(csrf_exempt)
def docentes(request):
    return render(request,'ajax/docentes/docentes.html', {})

@method_decorator(csrf_exempt)
def graduado(request):
    return render(request,'ajax/estudiantes/graduado.html', {})


@method_decorator(csrf_exempt)
def investigacion(request):
    return render(request,'ajax/investigacion_extencion/investigacion.html', {})

@method_decorator(csrf_exempt)
def bienestar(request):
    return render(request,'ajax/bienestar/bienestar.html', {})

@method_decorator(csrf_exempt)
def recurso_financiero(request):
    return render(request,'ajax/recursos_financieros/recursos_financieros.html', {})