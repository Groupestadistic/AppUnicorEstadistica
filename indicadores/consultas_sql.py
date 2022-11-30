consulta_prerequisitos = """
Select PlEs.MATRIC_YEAR+' - '+PlEs.MATRIC_TERM Version, Prog.LONG_DESC ProgramaNombre, (CASE WHEN Seme.DISCIPLINE = '01SEMESTRE' THEN '1' 
				 ELSE (CASE WHEN Seme.DISCIPLINE = '02SEMESTRE' THEN '2' 
				 ELSE (CASE WHEN Seme.DISCIPLINE = '03SEMESTRE' THEN '3' 
				 ELSE (CASE WHEN Seme.DISCIPLINE = '04SEMESTRE' THEN '4' 
				 ELSE (CASE WHEN Seme.DISCIPLINE = '05SEMESTRE' THEN '5' 
				 ELSE (CASE WHEN Seme.DISCIPLINE = '06SEMESTRE' THEN '6' 
				 ELSE (CASE WHEN Seme.DISCIPLINE = '07SEMESTRE' THEN '7' 
				 ELSE (CASE WHEN Seme.DISCIPLINE = '08SEMESTRE' THEN '8' 
				 ELSE (CASE WHEN Seme.DISCIPLINE = '09SEMESTRE' THEN '9' 
				 ELSE (CASE WHEN Seme.DISCIPLINE = '10SEMESTRE' THEN '10' 
				 END) END) END) END) END) END) END) END) END) END) AS SEMESTRE, TiCl.LONG_DESC Clasificacion, ClMa.ENROLLED_SEQ MateriaSeq, ClMa.EVENT_ID MateriaCodigo, Mate.EVENT_LONG_NAME MateriaNombre, 
       Mate.CREDITS MateriaCreditos, 
       case when ClMa.LOGICAL_OPERATOR='A' then 'Y'
            when ClMa.LOGICAL_OPERATOR='O' then 'Ó'			
            when ClMa.LOGICAL_OPERATOR='N' then ''								
       end MateriaLogica, 
	   case when ClMa.INCLUDE_DEGREE_GPA ='Y' then 'SI'
		else 'NO'
	   end MateriaSeIncluyeEnPga, Prer.OPEN_PARENS PrerrequisitoParentecisAbrir, PrCu.PREREQ_EVENT_ID PrerrequisitoCodigo, MaPr.EVENT_LONG_NAME PrerrequisitoNombre, 
	   case when Prer.LOGICAL_OPERATOR='A' then 'Y' 
		else Prer.LOGICAL_OPERATOR 
	   end PrerrequisitoOperadorLogico, Prer.CLOSE_PARENS PrerrequisitoParentecisCerrar, PrCu.MINIMUM_CREDITS PrerrequisitoCredito, (CASE WHEN DE.DISCIPLINE = '01SEMESTRE' THEN '1' 
				 ELSE (CASE WHEN DE.DISCIPLINE = '02SEMESTRE' THEN '2' 
				 ELSE (CASE WHEN DE.DISCIPLINE = '03SEMESTRE' THEN '3' 
				 ELSE (CASE WHEN DE.DISCIPLINE = '04SEMESTRE' THEN '4' 
				 ELSE (CASE WHEN DE.DISCIPLINE = '05SEMESTRE' THEN '5' 
				 ELSE (CASE WHEN DE.DISCIPLINE = '06SEMESTRE' THEN '6' 
				 ELSE (CASE WHEN DE.DISCIPLINE = '07SEMESTRE' THEN '7' 
				 ELSE (CASE WHEN DE.DISCIPLINE = '08SEMESTRE' THEN '8' 
				 ELSE (CASE WHEN DE.DISCIPLINE = '09SEMESTRE' THEN '9' 
				 ELSE (CASE WHEN DE.DISCIPLINE = '10SEMESTRE' THEN '10' 
				 END) END) END) END) END) END) END) END) END) END) AS SEMESTRE, PlEs.DEGREE, PlEs.curriculum
	  
	  
	
From   DEGREQ PlEs
		inner join
		CODE_CURRICULUM Prog on PlEs.CURRICULUM=Prog.CODE_VALUE_KEY
		inner join
		DEGREQDISC Seme on PlEs.MATRIC_YEAR=Seme.MATRIC_YEAR
						and PlEs.MATRIC_TERM = Seme.MATRIC_TERM
						and PlEs.PROGRAM = Seme.PROGRAM
						and PlEs.DEGREE = Seme.DEGREE
						and PlEs.CURRICULUM = Seme.CURRICULUM
		LEFT outer join
		CODE_DISCIPLINE Nive on Seme.DISCIPLINE=Nive.CODE_VALUE_KEY
		inner join
		DEGREQCLASS Clas on Seme.MATRIC_YEAR = Clas.MATRIC_YEAR
						and Seme.MATRIC_TERM = Clas.MATRIC_TERM
						and Seme.PROGRAM = Clas.PROGRAM
						and Seme.DEGREE = Clas.DEGREE
						and Seme.CURRICULUM = Clas.CURRICULUM
						and Seme.DISCIPLINE = Clas.DISCIPLINE
		inner join
		CODE_EVENTCLASS TiCl on Clas.EVENT_CLASS=Ticl.CODE_VALUE_KEY
		inner join
		DEGREQEVENT ClMa on Clas.MATRIC_YEAR = ClMa.MATRIC_YEAR
						and Clas.MATRIC_TERM = ClMa.MATRIC_TERM
						and Clas.PROGRAM = ClMa.PROGRAM
						and Clas.DEGREE = ClMa.DEGREE
						and Clas.CURRICULUM = ClMa.CURRICULUM
						and Clas.DISCIPLINE = ClMa.DISCIPLINE
						and Clas.EVENT_CLASS = ClMa.EVENT_CLASS
		left outer join
		EVENT Mate on ClMa.EVENT_ID=Mate.EVENT_ID
		left join
		EVENTPREREQUISITE Prer on Mate.EVENT_ID=Prer.EVENT_ID
		left join
		EVENTPREREQCOURSE PrCu on Prer.PREREQ_ID=PrCu.PREREQ_ID
		left join
		EVENT MaPr on PrCu.PREREQ_EVENT_ID=MaPr.EVENT_ID
		left join 
		DEGREQEVENT DE on PrCu.PREREQ_EVENT_ID = de.EVENT_ID

		 

where PlEs.MATRIC_YEAR+PlEs.MATRIC_TERM+PlEs.CURRICULUM IN (SELECT MATRIC_YEAR+MATRIC_TERM+CURRICULUM
															FROM ACADEMIC A
															WHERE A.ACADEMIC_YEAR = '2022'
															AND A.ACADEMIC_TERM = 'SEM2'
															AND A.ACADEMIC_SESSION = 'PREG01'
															AND A.ACADEMIC_FLAG = 'Y'
															AND A.ENROLL_SEPARATION IN ('5','12')
															AND A.PEOPLE_CODE_ID IN (SELECT PEOPLE_CODE_ID
																					 FROM TRANSCRIPTDETAIL TD
																					 WHERE TD.ACADEMIC_YEAR = A.ACADEMIC_YEAR
																					  AND TD.ACADEMIC_TERM = A.ACADEMIC_TERM
																					  AND TD.ACADEMIC_SESSION = A.ACADEMIC_SESSION
																					  AND TD.ADD_DROP_WAIT = 'A'))
																
order by ProgramaNombre, Version,Seme.DISCIPLINE, Clas.EVENT_CLASS, ClMa.ENROLLED_SEQ, Mate.EVENT_ID, Prer.SEQUENCE_NUMBER


"""

consulta_result_materias = """
--declare @periodo_consulta varchar(4),
--	@semestre_consulta varchar(4)

Select
	p.SUFFIX as TipoDoc,
	p.NICKNAME as Identificacion,
	p.people_code_id,
	p.FIRST_NAME + ' ' + p.MIDDLE_NAME + ' ' + p.LAST_NAME as Nombres,
	org.org_name_1 as sede,
	cu.LONG_DESC as ProgramaEstudiante,
	fac.long_desc as Facultad,
	cu.STATUS as EstadoAlumnoPrograma,
	Ac.CLASS_LEVEL Semestre,
	TaDe.ACADEMIC_YEAR as año,
	TaDe.ACADEMIC_TERM as Periodo,
	TaDe.ACADEMIC_SESSION as Sesion,
	-- Tade.REVISION_DATE FechaMatricula,
	Secc.CodigoMateria,
	SeCc.NombreMateria,
	Secc.Seccion,
	tg.GRADE_ACTIVITY,
	tg.GRADE_POINTS,
	tade.FINAL_GRADE,
	Secc.ProgramaMateria,
	--tade.FINAL_GRADE,
	(
		select
			ev.long_desc
		from
			CODE_EVENTSUBTYPE ev
		where
			ev.code_value_key = secc.EVENT_SUB_TYPE
	) as TipoMateri,
(
		select
			top 1 dir.address_line_1 + ' ' + dir.city
		from
			Addressschedule dir
		where
			P.People_code_Id = dir.People_Org_Code_Id
			and Address_type = 'FAMI'
	) DIRECCION,
	(
		select
			top 1 ciu.long_desc
		from
			Addressschedule dir,
			code_county ciu
		where
			ciu.code_value_key = dir.county
			and P.People_code_Id = dir.People_Org_Code_Id
			and Address_type = 'FAMI'
	) CIUDAD,
	(
		select
			top 1 dep.long_desc
		from
			Addressschedule dir,
			code_state dep
		where
			dep.code_value_key = dir.state
			and P.People_code_Id = dir.People_Org_Code_Id
			and Address_type = 'FAMI'
	) DEPARTAMENTO,
(
		select
			top 1 Ppf.PhoneNumber
		from
			PersonPhone as Ppf
		where
			Ppf.PersonId = P.PersonId
			and ppf.PhoneType = 'FAMILIAR'
	) TelFijo,
(
		select
			top 1 Ppc.PhoneNumber
		from
			PersonPhone as Ppc
		where
			Ppc.PersonId = P.PersonId
			and ppc.PhoneType = 'CELULAR'
	) TelMovil,
(
		select
			top 1 dir.EMAIL_ADDRESS
		from
			Addressschedule dir
		where
			P.People_code_Id = dir.People_Org_Code_Id
			and Address_type = 'FAMI'
	) EMAIL,
	dm.GENDER as Genero,
(
		select
			top 1 DISCIPLINE
		from
			DEGREQEVENT as de
		where
			tade.EVENT_ID = de.EVENT_ID
			and ac.CURRICULUM = de.CURRICULUM
	) seme,
	p1.PEOPLE_CODE_ID as Cog_Docente,
	p1.nickname Identificacion4,
	p1.LAST_NAME + ' ' + p1.FIRST_NAME + ' ' + p1.MIDDLE_NAME as Nom_Docente,
	(
		select
			TOP 1 d.Tipo_de_vinculacion
		from
			[DB-HZ].dbo.USUARIOS u
			inner join [DB-HZ].dbo.DOCENTES d on d.Id_USUARIO = u.Id
		where
			CONVERT(VARCHAR, u.CEDULA) = p1.nickname
	) Vinculación_Docente,
	(
		select
			TOP 1 NOMBRE_DEPARTAMENTO
		from
			[DB-HZ].dbo.USUARIOS u
			inner join [DB-HZ].dbo.DOCENTES d on d.Id_USUARIO = u.Id
			inner join [DB-HZ].dbo.DEPARTAMENTOS dp on d.Departamento = dp.Id
		where
			CONVERT(VARCHAR, u.CEDULA) = p1.nickname
	) DEPARTAMENTO,
	case
		when ac.CLASS_LEVEL in ('SE01') then '1'
		when ac.CLASS_LEVEL in ('SE02') then '2'
		when ac.CLASS_LEVEL in ('SE03') then '3'
		when ac.CLASS_LEVEL in ('SE04') then '4'
		when ac.CLASS_LEVEL in ('SE05') then '5'
		when ac.CLASS_LEVEL in ('SE06') then '6'
		when ac.CLASS_LEVEL in ('SE07') then '7'
		when ac.CLASS_LEVEL in ('SE08') then '8'
		when ac.CLASS_LEVEL in ('SE09') then '9'
		when ac.CLASS_LEVEL in ('SE10') then '10'
		when ac.CLASS_LEVEL in ('NULL') then '0'
		when ac.CLASS_LEVEL in ('') then '0'
	end as SemNumero ------------------
,
	isnull(
		convert(numeric(9, 1), round(tg.grade_points, 2, 1)),
		0
	) Nota1 ----------
,
	case
		when tg.GRADE_POINTS >= '3' then '1'
		when tg.GRADE_POINTS < '3' then '0'
	end as Gano ----------------
	--tener en cuenta los null en el excel para las perdidas o ganadas (1 o 0)
	----------------
,
	case
		when tg.GRADE_POINTS < '3' then '1'
		when tg.GRADE_POINTS >= '3' then '0'
	end as Perdio --- convertir los null manual---
,
	case
		when tg.GRADE_POINTS = '0' then '0. Cero'
		when (
			tg.GRADE_POINTS > '0'
			and tg.GRADE_POINTS < '2'
		) then '1. Muy Baja'
		when (
			tg.GRADE_POINTS >= '2'
			and tg.GRADE_POINTS < '3'
		) then '2. Baja'
		when (
			tg.GRADE_POINTS >= '3'
			and tg.GRADE_POINTS < '4'
		) then '3. Media'
		when (
			tg.GRADE_POINTS >= '4'
			and tg.GRADE_POINTS < '4.5'
		) then '4. Alta'
		when (
			tg.GRADE_POINTS >= '4.5'
			and tg.GRADE_POINTS <= '5'
		) then '5. Muy Alta'
	end as Rango -------------------
,
(
		select
			top 1 case
				when de.DISCIPLINE = '01SEMESTRE' then '1'
				when de.DISCIPLINE = '02SEMESTRE' then '2'
				when de.DISCIPLINE = '03SEMESTRE' then '3'
				when de.DISCIPLINE = '04SEMESTRE' then '4'
				when de.DISCIPLINE = '05SEMESTRE' then '5'
				when de.DISCIPLINE = '06SEMESTRE' then '6'
				when de.DISCIPLINE = '07SEMESTRE' then '7'
				when de.DISCIPLINE = '08SEMESTRE' then '8'
				when de.DISCIPLINE = '09SEMESTRE' then '9'
				when de.DISCIPLINE = '10SEMESTRE' then '10'
				when de.DISCIPLINE = 'NULL' then '0'
				when de.DISCIPLINE = ' ' then '0'
			end
		from
			DEGREQEVENT as de
		where
			tade.EVENT_ID = de.EVENT_ID
			and ac.CURRICULUM = de.CURRICULUM
	) SemMateriaNum,
(3.2 - GRADE_POINTS * 1 / 3) * 3 / 2 as ProxNotaMin,
	secc.Creditos, ac.curriculum
From
	PEOPLE p
	inner join ACADEMIC ac on p.PEOPLE_CODE_ID = ac.PEOPLE_CODE_ID
	inner join CODE_CURRICULUM cu on ac.CURRICULUM = cu.CODE_VALUE_KEY
	inner join TRANSCRIPTDETAIL TaDe on p.PEOPLE_CODE_ID = TaDe.PEOPLE_CODE_ID
	and ac.ACADEMIC_YEAR = Tade.ACADEMIC_YEAR
	and ac.ACADEMIC_TERM = TaDe.ACADEMIC_TERM
	and ac.ACADEMIC_SESSION = TaDe.ACADEMIC_SESSION
	and ac.transcript_seq = tade.transcript_seq
	inner join (
		Select
			sec.SECTION as Seccion,
			Eve.EVENT_ID as CodigoMateria,
			sec.EVENT_SUB_TYPE,
			Eve.EVENT_LONG_NAME as NombreMateria,
			Cur.LONG_DESC as ProgramaMateria,
			sec.EVENT_STATUS as EstadoSeccion,
			Sec.ACADEMIC_YEAR as Año,
			Sec.ACADEMIC_TERM as Periodo,
			Sec.ACADEMIC_SESSION as Sesion,
			sec.CREDITS as Creditos
		From
			SECTIONS Sec
			left outer join CODE_CURRICULUM Cur on Sec.CURRICULUM = Cur.CODE_VALUE_KEY
			inner join EVENT Eve on Sec.EVENT_ID = Eve.EVENT_ID
	) SeCc on TaDe.SECTION = Secc.Seccion
	and TaDe.EVENT_ID = secc.CodigoMateria
	and TaDe.ACADEMIC_YEAR = Secc.Año
	and TaDe.ACADEMIC_TERM = Secc.Periodo
	and TaDe.ACADEMIC_SESSION = secc.Sesion
	and tade.EVENT_SUB_TYPE = secc.EVENT_SUB_TYPE
	left outer join TRANSCRIPTGRADING tg on tg.PEOPLE_CODE_ID = p.PEOPLE_CODE_ID
	and tg.PEOPLE_CODE_ID = tade.PEOPLE_CODE_ID
	and tg.ACADEMIC_YEAR = tade.ACADEMIC_YEAR
	and tg.ACADEMIC_TERM = tade.ACADEMIC_TERM
	and tg.ACADEMIC_SESSION = tade.ACADEMIC_SESSION
	and tg.EVENT_ID = tade.EVENT_ID
	and tg.EVENT_SUB_TYPE = tade.EVENT_SUB_TYPE
	and tg.SECTION = tade.SECTION
	left outer join code_college as fac on ac.COLLEGE = fac.CODE_VALUE_KEY
	left outer join demographics as dm on ac.people_code_id = dm.people_code_id
	and ac.ACADEMIC_YEAR = dm.ACADEMIC_YEAR
	and ac.ACADEMIC_TERM = dm.ACADEMIC_TERM
	and ac.ACADEMIC_SESSION = dm.ACADEMIC_SESSION
	left outer join organization as org on org.org_code_id = ac.org_code_id
	left outer join SECTIONPER sp on TaDe.ACADEMIC_YEAR = sp.ACADEMIC_YEAR
	and TaDe.ACADEMIC_TERM = sp.ACADEMIC_TERM
	and TaDe.ACADEMIC_SESSION = sp.ACADEMIC_SESSION
	and TaDe.EVENT_ID = sp.EVENT_ID
	and TaDe.SECTION = sp.SECTION
	left outer join PEOPLE p1 on p1.PEOPLE_CODE_ID = sp.PERSON_CODE_ID
where
	ac.ACADEMIC_YEAR = %s
	and ac.ACADEMIC_TERM = %s
	and ac.ACADEMIC_SESSION = 'Preg01'
	and ac.academic_flag = 'Y'
	and tade.ADD_DROP_WAIT = 'A'
	and secc.EstadoSeccion in ('A','P')
order by
	fac.long_desc,
	cu.LONG_DESC,
	p.PEOPLE_CODE_ID

"""

consulta_cancelaciones = """

SELECT DISTINCT P.PEOPLE_CODE_ID ID_SISTEMA, P.SUFFIX TIPO_DOCUMENTO, P.NICKNAME NUM_DOCUMENTO, (p.LAST_NAME+' '+p.FIRST_NAME+' '+p.MIDDLE_NAME) ESTUDIANTE,(A.ACADEMIC_YEAR+' - '+A.ACADEMIC_TERM+' - '+A.ACADEMIC_SESSION) PERIODO_ACADEMICO, CCF.LONG_DESC FACULTAD, CCD.LONG_DESC DEPARTAMENTO,
       CC.LONG_DESC PROGRAMA, A.CLASS_LEVEL SEMESTRE_ESTUDIANTE,O.ORG_NAME_1 LUGAR_DE_DESARROLLO, TM.EVENT_ID ID_ASIGNATURA_CANCELADA, E.EVENT_LONG_NAME NOMBRE_ASIGNATURA, TM.SECTION GRUPO, TM.DROP_REASON ESTADO, DE.EVENT_CLASS TIPO_ASIGNATURA,
       DE.DISCIPLINE, A.curriculum
FROM ACADEMIC A
INNER JOIN 
PEOPLE P ON P.PEOPLE_CODE_ID = A.PEOPLE_CODE_ID 
INNER JOIN 
CODE_COLLEGE CCF ON CCF.CODE_VALUE_KEY = A.COLLEGE
INNER JOIN 
CODE_DEPARTMENT CCD ON CCD.CODE_VALUE_KEY = A.DEPARTMENT
INNER JOIN 
CODE_CURRICULUM CC ON CC.CODE_VALUE_KEY = A.CURRICULUM
INNER JOIN ORGANIZATION O ON O.ORG_CODE_ID = A.ORG_CODE_ID
INNER JOIN 
TRANSCRIPTMARKETING TM ON TM.PEOPLE_CODE_ID = A.PEOPLE_CODE_ID 
AND A.ACADEMIC_YEAR = TM.ACADEMIC_YEAR
AND A.ACADEMIC_TERM = TM.ACADEMIC_TERM
AND A.ACADEMIC_SESSION = TM.ACADEMIC_SESSION
AND DROP_REASON  = 'CancMateri' -- in ('CancMateri',''CancSemest)
INNER JOIN 
EVENT E ON E.EVENT_ID = TM.EVENT_ID
INNER JOIN 
DEGREQEVENT DE ON DE.EVENT_ID = E.EVENT_ID
AND DE.MATRIC_YEAR = A.MATRIC_YEAR
AND DE.MATRIC_TERM = A.MATRIC_TERM
AND DE.CURRICULUM = A.CURRICULUM


WHERE A.ACADEMIC_YEAR = %s
AND A.ACADEMIC_TERM = %s
AND A.ACADEMIC_SESSION = 'PREG01'
AND A.ACADEMIC_FLAG = 'Y'
AND A.ENROLL_SEPARATION IN ('5','12')

/* Sacar Laboratorios */
AND A.PEOPLE_CODE_ID NOT IN (SELECT PEOPLE_CODE_ID 
                             FROM TRANSCRIPTDETAIL
                             WHERE ACADEMIC_YEAR = A.ACADEMIC_YEAR
								AND ACADEMIC_TERM = A.ACADEMIC_TERM
								AND ACADEMIC_SESSION = A.ACADEMIC_SESSION
								AND EVENT_ID = TM.EVENT_ID
								AND SECTION = TM.SECTION
								AND (SECTION LIKE 'L%' AND CREDIT = 0))
ORDER BY PROGRAMA,ID_SISTEMA, TM.EVENT_ID

"""

consulta_hist_academic = """
select PEOPLE_CODE_ID, (MATRIC_YEAR+' - '+MATRIC_TERM) VERSION , PROGRAM, DEGREE, CURRICULUM, DISCIPLINE, EVENT_CLASS, EVENT_ID, ENROLLED_SEQ, TAKEN_EVENT_ID, STATUS, TAKEN_YEAR, TAKEN_TERM
from STDDEGREQEVENT
where TAKEN_YEAR >= '2014'
AND STATUS = 'C'
"""

