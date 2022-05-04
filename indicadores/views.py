from email.mime import base
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def index(request):
    return render(request,'base/index.html',{})

@method_decorator(csrf_exempt)
def estudiantes_preg(request):
    return render(request,'ajax/estudiantes/estudiantes_preg.html', {})

@method_decorator(csrf_exempt)
def docentes(request):
    return render(request,'ajax/docentes/docentes.html', {})