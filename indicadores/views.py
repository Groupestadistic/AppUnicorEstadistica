from email.mime import base
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


import pyodbc
import pymssql
import pandas as pd
import urllib.parse
from sqlalchemy import create_engine
import json

from indicadores.consultas_sql import consulta_result_materias

# TABLEAU
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

@method_decorator(csrf_exempt)
def tasa_graduacion(request):
    return render(request,'ajax/estudiantes/tasa_graduacion.html', {})




# ESTIMACION DE NUMERO DE GRUPOS

def zona_privada(request):
    return render(request,'base/zona_privada.html', {})


def conexion_sql():
    host = '10.0.4.20'
    nombre_bd = 'Campus'
    nombre_usuario = 'dbhz'
    password = 'Horarios.5822@'
    password = urllib.parse.quote_plus(password)
    conexion = create_engine("mssql+pymssql://"+nombre_usuario+":"+password+"@"+host+"/"+nombre_bd,deprecate_large_types=True)

    return conexion



@method_decorator(csrf_exempt)
def num_grupos(request):
    return render(request,'ajax/num_grupos/num_grupos.html', {})


@method_decorator(csrf_exempt)
def resumen(request):

    programa_current = request.POST['programa']
    periodo_consulta = request.POST['periodo']
    semestre_consulta = request.POST['semestre']
    print(periodo_consulta,semestre_consulta)

    conexion = conexion_sql()
    print('entro a hacer la consulta')
    resul_materias = pd.read_sql(consulta_result_materias,conexion, params=[periodo_consulta,semestre_consulta])
    print('salio de la consulta')
    

    if programa_current != "":
        resumen = resul_materias[(resul_materias['ProgramaEstudiante']==programa_current)]
    else:
        resumen = resul_materias

    resumen2 = resumen.groupby(['GRADE_ACTIVITY']).count().reset_index()[['GRADE_ACTIVITY','TipoDoc','GRADE_POINTS']]
    resumen2['porcentaje'] = round((resumen2['GRADE_POINTS']/resumen2['TipoDoc'])*100,2)
    resumen2.replace({'1Corte':'PRIMER CORTE','2Corte':'SEGUNDO CORTE','3Corte':'TERCER CORTE'}, inplace=True)
    resumen2 = resumen2.to_json(orient='records')
    data = json.loads(resumen2)

    cargue_docente = resumen.copy()
    cargue_docente['Nom_Docente'] = cargue_docente['Nom_Docente'].fillna('SIN DOCENTE ASIGNADO')
    cargue_docente['Nom_Docente']  = cargue_docente['Nom_Docente'].str.upper()
    cargados = pd.crosstab(cargue_docente.Nom_Docente, [cargue_docente.GRADE_ACTIVITY],margins = True, margins_name = "subtotal",aggfunc = ["count"], values = cargue_docente.GRADE_POINTS)
    a_cargar = pd.crosstab(cargue_docente.Nom_Docente, [cargue_docente.GRADE_ACTIVITY],margins = True, margins_name = "subtotal")
    result_docente = round((cargados/a_cargar)*100,0)
    result_docente.columns = result_docente.columns.droplevel(0)
    result_docente.reset_index(inplace=True)
    result_docente = result_docente.to_json(orient='records')
    result_docente = json.loads(result_docente)

    print(result_docente)

    return render(request,'ajax/num_grupos/resumen.html', {'datas':data, 'cargue_docente':result_docente})