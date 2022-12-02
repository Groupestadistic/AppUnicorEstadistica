from email.mime import base
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


import pyodbc
import pymssql
import pandas as pd
import urllib.parse
from sqlalchemy import create_engine
import json

from indicadores.consultas_sql import consulta_result_materias, consulta_prerequisitos, consulta_cancelaciones

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
def cargue_notas(request):

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
    cargados = pd.crosstab(cargue_docente.Nom_Docente, [cargue_docente.GRADE_ACTIVITY],aggfunc = ["count"], values = cargue_docente.GRADE_POINTS)
    a_cargar = pd.crosstab(cargue_docente.Nom_Docente, [cargue_docente.GRADE_ACTIVITY])
    result_docente = round((cargados/a_cargar)*100,0)
    result_docente.columns = result_docente.columns.droplevel(0)
    result_docente.reset_index(inplace=True)

    result_docente = result_docente.to_json(orient='records')
    result_docente = json.loads(result_docente)

    print(result_docente)

    return render(request,'ajax/num_grupos/resumen.html', {'datas':data, 'cargue_docente':result_docente})



@method_decorator(csrf_exempt)
def estimar_grupos(request):
    programa_current = request.POST['programa']
    periodo_consulta = request.POST['periodo']
    semestre_consulta = request.POST['semestre']
    est_nuevo_ingreso = request.POST['est_nuevo_ingreso']
    cap_grupo = int(request.POST['cap_grupo'])
    clasific_materia = 'OBLIGATORIA'

    print(periodo_consulta,semestre_consulta)

    conexion = conexion_sql()
    print('entro a hacer la consulta')
    prerequisitos = pd.read_sql(consulta_prerequisitos,conexion)
    resul_materias = pd.read_sql(consulta_result_materias,conexion, params=[periodo_consulta,semestre_consulta])
    cancelaciones = pd.read_sql(consulta_cancelaciones,conexion, params = [periodo_consulta,semestre_consulta])
    print('salio de la consulta')

    if programa_current != "":
        prerequisitos = prerequisitos[prerequisitos['ProgramaNombre']==programa_current]
        resul_materias = resul_materias[(resul_materias['ProgramaEstudiante']==programa_current)]
        cancelaciones = cancelaciones[cancelaciones['PROGRAMA']==programa_current]
    
    prerequisitos.columns = ['Version', 'ProgramaNombre', 'Sem_materia', 'Clasificacion', 'MateriaSeq',
       'MateriaCodigo', 'MateriaNombre', 'MateriaCreditos', 'MateriaLogica',
       'MateriaSeIncluyeEnPga', 'PrerrequisitoParentecisAbrir',
       'PrerrequisitoCodigo', 'PrerrequisitoNombre',
       'PrerrequisitoOperadorLogico', 'PrerrequisitoParentecisCerrar',
       'PrerrequisitoCredito', 'Sem_prerequisito', 'Preg_post','CodigoPrograma']

    resul_materias['GRADE_POINTS'] = resul_materias['GRADE_POINTS'].fillna(0)

    programas = prerequisitos[prerequisitos['Preg_post']=='PREG']['ProgramaNombre'].unique()
    lista_gral = []
    
    for programa_current in programas:
        print('pograma: ',programa_current )
        # programa_current = 'Ingeniería Industrial'
        pensum_programa = prerequisitos[(prerequisitos['ProgramaNombre']==programa_current) & (prerequisitos['Clasificacion'] == clasific_materia)]
        versiones = sorted(pensum_programa['Version'].unique())

        semestres = pensum_programa['Sem_materia'].unique()

        for versi in versiones:
            for semestre in semestres:
                print('numero de semestre : ', semestre)
                materias = pensum_programa[(pensum_programa['Sem_materia']== semestre) & (pensum_programa['Version'] == versi)]
                
                for materia in materias['MateriaCodigo'].unique():

                    # hallar cantidad de estudiantes que cancelaron
                    cant_cancelaciones = cancelaciones[(cancelaciones['PROGRAMA']==programa_current) & (cancelaciones['ID_ASIGNATURA_CANCELADA']==materia)]['ESTUDIANTE'].count()
                    
                    # listado de estudiantes que perdieron materia [1 si perdio ; 0 si gano]
                    prom_materias = resul_materias[(resul_materias['ProgramaEstudiante']==programa_current) & (resul_materias['CodigoMateria']==materia) & ((resul_materias['GRADE_ACTIVITY']=='1Corte')|(resul_materias['GRADE_ACTIVITY']=='2Corte')|(resul_materias['GRADE_ACTIVITY']=='3Corte'))].groupby('people_code_id')['GRADE_POINTS'].mean().apply(lambda x: 0 if x>=3 else 1)
                    
                    # hallar cantidad de estudiantes que van perdidos hasta este momento
                    cant_mat_perdidas= sum(prom_materias)


                    #hallar los prerequisitos de cada materia
                    pre_requi = materias[materias['MateriaCodigo']==materia]
                    pre_requisitos_materia = pre_requi.groupby('PrerrequisitoCodigo')['Sem_materia'].count().index.values
                    condicion_prere = pre_requi['PrerrequisitoOperadorLogico'].unique()

                    name_materia = pre_requi['MateriaNombre'].unique()[0]

                    lista_prere = []
                    for pre_materia in pre_requisitos_materia:

                        prom_materias_pre = resul_materias[(resul_materias['ProgramaEstudiante']==programa_current) & (resul_materias['CodigoMateria']==pre_materia) & ((resul_materias['GRADE_ACTIVITY']=='1Corte')|(resul_materias['GRADE_ACTIVITY']=='2Corte')|(resul_materias['GRADE_ACTIVITY']=='3Corte'))].groupby('people_code_id')['GRADE_POINTS'].mean()

                        # list_ganaron = list(filter(lambda x: prom_materias_pre[x]>=3,prom_materias_pre.index.values))
                        list_ganaron = set([id for id in prom_materias_pre.index.values if prom_materias_pre[id] >= 3])
                        lista_prere.append(list_ganaron)

                    
                    if semestre == '1' and len(prom_materias)==0:
                        cont_estudi_ganan_pre = 0
                    elif semestre == '1' and len(prom_materias)!=0:
                        cont_estudi_ganan_pre = est_nuevo_ingreso
                    else:
                        if len(lista_prere)==0:
                            cont_estudi_ganan_pre = 0
                        elif len(lista_prere)==1:
                            estudi_ganan_pre = lista_prere[0]
                            cont_estudi_ganan_pre = len(estudi_ganan_pre)
                        else:
                            estudi_ganan_pre = lista_prere[0]

                            if 'O' in condicion_prere:
                                for i in range(1, len(lista_prere)):
                                    estudi_ganan_pre = estudi_ganan_pre | lista_prere[i]
                            else:
                                for i in range(1, len(lista_prere)):
                                    estudi_ganan_pre = estudi_ganan_pre & lista_prere[i]
                            
                            cont_estudi_ganan_pre = len(estudi_ganan_pre)
                    print(cant_cancelaciones,cant_mat_perdidas, cont_estudi_ganan_pre)
                    tot = int(cant_cancelaciones) + int(cant_mat_perdidas) + int(cont_estudi_ganan_pre)
                    lista_gral.append([programa_current,versi, semestre, materia, name_materia, len(lista_prere),cant_cancelaciones,cant_mat_perdidas,cont_estudi_ganan_pre,len(prom_materias), tot, tot/cap_grupo,])
                    # mostrar resultado
                    # print(str(semestre) +' '+ str(materia) +' '+ str(cant_cancelaciones) + ' ' + str(cant_mat_perdidas) + ' ' +  str(cont_estudi_ganan_pre)  + ' ' +  str(len(prom_materias)))

    results = pd.DataFrame(lista_gral)
    results.columns=['Programa','Version','semestre','cod_materia','Name_materia','Cantidad_Prerequisitos','cancelaciones','perdidas','ganadores_prerequisitos','matriculados', 'Estudi_para_nuevo_grupos','Num_Grupos']
    # dta.to_excel('data_pre_industrial.xlsx')


    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename=filename.csv'
    # results.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=False,decimal=",")
    # return response

    results = results.to_json(orient='records')
    results = json.loads(results)
    return render(request,'ajax/num_grupos/result_num_grupos.html', {'result_num_grupos':results})