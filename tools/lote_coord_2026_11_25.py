# -*- coding: utf-8 -*-
"""Sexto lote de coordinación (2026-11-25). Cubre la lectura K014 (Guía 34, 1.5 Más y mejores instancias de
participación: consejo directivo, consejo académico, rector, consejo de padres, PEI concertado) con cuatro ítems y
completa la lectura K011 (1.3 La autonomía escolar) con uno. Rota GAF (Fondo de Servicios Educativos), GDI (ruta
de mejoramiento, seguimiento y evaluación), GAC (acompañamiento con evaluación formativa, SIEE), GCO (protocolos de
convivencia, inclusión y convivencia) y PSI (compromiso social e institucional). Formatos: ingreso 2022 (3 opciones,
una correcta) y ascenso 2024 (cada opción es un nivel de desempeño; la correcta es la de nivel avanzado).
Genera data/lotes/coord-2026-11-25.json. Citas: texto literal de fuentes/."""
import json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
casos, items = [], []


def caso(id, titulo, texto):
    casos.append({"id": id, "titulo": titulo, "texto": texto})


def item(id, caso, familia, dif, enunciado, ops, clave, explicacion, fuente, consejo, citas, competencia, formato="ingreso 2022"):
    items.append({"id": id, "tipo": "caso", "caso": caso, "familia": familia, "dificultad": dif, "enunciado": enunciado,
                  "opciones": [{"l": l, "t": t, "j": j} for l, (t, j) in zip("ABC", ops)], "clave": clave,
                  "explicacion": explicacion, "fuente": fuente, "consejo": consejo,
                  "citas": [{"doc": d, "texto": t, "ubicacion": u} for d, t, u in citas], "competencia": competencia,
                  "cargo": "coordinador", "formato": formato})


G34, L715, L115, D1075 = "guia34_mineducacion_2008", "ley_715_2001", "ley_115_1994", "decreto_1075_2015"
R3842, D1965, D1421, GCNSC = "resolucion_3842_2022_ocr", "decreto_1965_2013", "decreto_1421_2017", "guia_orientacion_cnsc_2022"
K014 = "Guía 34, 1.5 Más y mejores instancias de participación"
K011 = "Guía 34, 1.3 La autonomía escolar"

# ------------------------------------------------------------ K014 · Guía 34, instancias de gobierno y participación
caso("CK52", "El orden de los contenidos de noveno",
     "En junio, los docentes de matemáticas y de ciencias naturales le muestran a usted como coordinador que la secuencia de contenidos de noveno no es "
     "coherente: en ciencias se necesitan funciones lineales dos periodos antes de que se enseñen en matemáticas. Proponen reorganizar las unidades de ambas "
     "áreas a partir del segundo semestre. Un padre de familia que integra el consejo directivo opina que cualquier cambio en el plan de estudios debe "
     "pasar primero por ese consejo, «porque es el que decide sobre el funcionamiento del colegio».")
item("CO084", "CK52", "GDI-GOB", 3,
     "La instancia a la que usted lleva la propuesta para revisarla y hacer los ajustes al plan de estudios es",
     [("el consejo directivo, porque le corresponde planear y evaluar el currículo y el plan de estudios y decidir sobre el funcionamiento institucional.",
       "Es incorrecta. Es el distractor más cercano: la Guía 34 sí le asigna al consejo directivo planear y evaluar el PEI, el currículo y el plan de estudios, pero la organización, la ejecución y los ajustes continuos del plan de estudios son del consejo académico."),
      ("el consejo académico, porque le corresponde la orientación pedagógica y el mejoramiento continuo del plan de estudios y los ajustes al currículo.",
       "Es correcta. La Guía 34 hace responsable al consejo académico de la organización, la orientación pedagógica, la ejecución y el mejoramiento continuo del plan de estudios, y de revisar y hacer ajustes al currículo; el Decreto 1075 le asigna introducir esas modificaciones y ajustes."),
      ("la comisión de evaluación y promoción de noveno, porque le corresponde analizar el desempeño del grado y recomendar actividades de refuerzo.",
       "Es incorrecta. Las comisiones de evaluación se ocupan del desempeño y la promoción de los estudiantes y de recomendar apoyos; reorganizar la secuencia de contenidos de dos áreas es una decisión curricular, no un asunto de promoción.")],
     "B",
     "Las palabras clave son «revisarla y hacer los ajustes». La Guía 34 distingue las funciones: el consejo directivo toma las decisiones sobre el funcionamiento institucional y planea y evalúa el PEI, el currículo y el plan de estudios; el consejo académico es responsable de la organización, la orientación pedagógica, la ejecución y el mejoramiento continuo del plan de estudios, y de revisar y ajustar el currículo. El Decreto 1075 (art. 2.3.3.1.5.7) lo confirma: el consejo académico estudia el currículo, introduce las modificaciones y ajustes y organiza el plan de estudios. El coordinador, que participa en ese consejo, lleva allí la propuesta de las áreas. La CNSC premia ubicar cada decisión en la instancia que la norma señala.",
     "Guía 34 MEN (2008), 1.5 Instancias de participación; Decreto 1075 de 2015, art. 2.3.3.1.5.7.",
     "Ajustes al plan de estudios durante el año: consejo académico. Planear y evaluar el PEI y adoptar el manual: consejo directivo.",
     [(G34, "El Consejo Académico, responsable de la organización, orientación pedagógica, ejecución y mejoramiento continuo del plan de estudios; así como de revisar y hacer ajustes al currículo", K014),
      (G34, "El Consejo Directivo, encargado de tomar las decisiones relacionadas con el funcionamiento institucional: planear y evaluar el PEI, el currículo y el plan de estudios", K014),
      (D1075, "b) Estudiar el currículo y propiciar su continuo mejoramiento, introduciendo las modificaciones y ajustes", "Decreto 1075, art. 2.3.3.1.5.7")],
     "Gobierno escolar")

caso("CK53", "Los resultados que nadie mostró",
     "Llegaron los resultados de la prueba Saber 11 y bajaron en lectura crítica. El rector los compartió solo con los docentes. La presidenta del consejo de "
     "padres le pide a usted que se los presente a ese consejo, porque «las familias también queremos saber qué pasó y ayudar». Algunos docentes le piden "
     "no hacerlo, porque temen que los padres usen los resultados para señalar a los profesores de lenguaje.")
item("CO085", "CK53", "GCO-COMUN", 2,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("proponer al rector una sesión con el consejo de padres para analizar los resultados y acordar su aporte a las acciones del plan de mejoramiento.",
       "Es correcta (nivel avanzado). Involucra al consejo de padres en lo que la norma le asigna: contribuir con el rector en el análisis, la difusión y el uso de los resultados y participar en el plan de mejoramiento. Además, al enfocarse en acciones, evita que el análisis se convierta en señalamiento."),
      ("enviar al consejo de padres el reporte de resultados con una explicación escrita de los puntajes, para que lo socialice con las demás familias del colegio.",
       "Es incorrecta (nivel mínimo). Cumple con la difusión, pero deja a los padres como receptores de un documento: no los involucra en el análisis ni en el uso de los resultados para mejorar, que es donde está su aporte."),
      ("reservar los resultados al equipo docente hasta tener listo el plan de mejoramiento, para evitar que se usen para señalar a los profesores.",
       "Es incorrecta (nivel inferior). Atiende el temor de los docentes, pero excluye a una instancia que por norma debe contribuir al análisis y uso de los resultados; ocultarlos debilita la confianza y la participación de las familias.")],
     "A",
     "La Guía 34 asigna al consejo de padres, entre sus principales funciones, involucrarse en la elaboración de los planes de mejoramiento y contribuir con el rector o director en el análisis, difusión y uso de los resultados de las pruebas SABER y el examen de Estado; el Decreto 1075 (art. 2.3.4.7) lo recoge en los mismos términos. En el formato de ascenso, el nivel avanzado no se queda en informar (mínimo) ni en proteger al equipo excluyendo a las familias (inferior): convierte los resultados en un insumo compartido para mejorar. El coordinador puede orientar la sesión hacia causas y acciones, no hacia culpables.",
     "Guía 34 MEN (2008), 1.5 Instancias de participación; Decreto 1075 de 2015, art. 2.3.4.7.",
     "Resultados Saber: el consejo de padres contribuye a su análisis, difusión y uso, y participa en el plan de mejoramiento.",
     [(G34, "contribuir con el rector o director en el análisis, difusión y uso de los resultados de las pruebas SABER y el examen de Estado", K014),
      (G34, "involucrarse en la elaboración de los planes de mejoramiento", K014),
      (D1075, "d) Participar en la elaboración de planes de mejoramiento y en el logro de los objetivos planteados;", "Decreto 1075, art. 2.3.4.7")],
     "Participación de las familias", "ascenso 2024")

caso("CK54", "Tres cupos para el diplomado",
     "La secretaría de educación ofrece a su institución tres cupos en un diplomado sobre evaluación formativa. Siete docentes se inscriben. Un jefe de área "
     "le pide a usted como coordinador que lo incluya directamente porque «usted es quien conoce el trabajo de cada uno», y en la reunión de docentes "
     "otro propone hacer un sorteo entre los interesados para que nadie se sienta excluido.")
item("CO086", "CK54", "GDI-ROL", 2,
     "Según la Guía 34 y la Ley 715, lo que corresponde para definir quiénes reciben los cupos es que",
     [("usted como coordinador seleccione a los docentes, porque lidera el trabajo académico del equipo y conoce de primera mano sus necesidades.",
       "Es incorrecta. El coordinador sí conoce las necesidades de formación y puede aportar ese análisis, pero la norma no le asigna la decisión: proponer a los docentes que recibirán capacitación es una función del rector."),
      ("la reunión de docentes decida por sorteo entre los interesados, para que la asignación de los cupos sea transparente e imparcial.",
       "Es incorrecta. El sorteo parece justo, pero desconoce que la formación debe responder a las necesidades institucionales y del plan de mejoramiento, y traslada a una reunión una función que la ley asigna al rector."),
      ("el rector proponga a los docentes que serán apoyados, y que usted le aporte criterios e información sobre las necesidades de cada área.",
       "Es correcta. La Ley 715 (art. 10.12) y la Guía 34 asignan al rector proponer a los docentes que recibirán capacitación; el coordinador, que acompaña el trabajo de los docentes, le aporta criterios e información para una decisión pertinente.")],
     "C",
     "La Guía 34 enumera las funciones del rector o director: además de dirigir el trabajo de los equipos de docentes y administrar los recursos humanos, debe proponer a los profesores que recibirán capacitación. La Ley 715 lo establece en el numeral 10.12: proponer a los docentes que serán apoyados para recibir capacitación. El coordinador no decide por su cuenta ni delega la decisión en un sorteo: su aporte es la información sobre las necesidades de formación de cada área, que ayuda al rector a proponer con criterio. En la CNSC, la opción correcta respeta quién decide y, a la vez, muestra cómo colabora el coordinador.",
     "Guía 34 MEN (2008), 1.5 Instancias de participación; Ley 715 de 2001, art. 10.12.",
     "Capacitación de docentes: la propone el rector (Ley 715, 10.12); el coordinador aporta criterios e información.",
     [(G34, "dirigir el trabajo de los equipos de docentes, proponer a los profesores que recibirán capacitación, administrar los recursos humanos de la institución", K014),
      (L715, "10.12. Proponer a los docentes que serán apoyados para recibir capacitación.", "Ley 715, art. 10.12")],
     "Funciones del rector y del coordinador")

caso("CK55", "Un nuevo énfasis para la media",
     "Su institución en Yopal decidió resignificar el PEI para ofrecer media técnica en agroindustria. Para ganar tiempo, el rector propone que el equipo "
     "directivo y los jefes de área redacten el nuevo horizonte institucional durante las vacaciones de diciembre y lo presenten en enero. Le pide a usted "
     "como coordinador organizar el trabajo.")
item("CO087", "CK55", "GDI-PEI", 3,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("organizar mesas de trabajo con docentes, estudiantes, familias, egresados y empresas agroindustriales de la región para concertar el nuevo énfasis.",
       "Es correcta (nivel avanzado). La Guía 34 busca que el PEI sea concertado por directivos, docentes, padres, estudiantes, egresados y representantes del sector productivo local; las mesas hacen que todos construyan el énfasis, no solo que lo conozcan."),
      ("redactar la propuesta con el equipo directivo y los jefes de área, y luego socializarla en una asamblea con las familias y los estudiantes.",
       "Es incorrecta (nivel mínimo). Informa a la comunidad, pero socializar un documento terminado no es concertarlo: las familias, los estudiantes, los egresados y el sector productivo quedan como receptores de una decisión ya tomada."),
      ("adoptar el énfasis que la secretaría de educación recomienda para los colegios técnicos del municipio, para quedar alineados con la política educativa local.",
       "Es incorrecta (nivel inferior). Renuncia a la autonomía institucional y a la participación: el énfasis del PEI no se adopta por recomendación externa, sino que se construye con la comunidad a partir del contexto de la institución.")],
     "A",
     "La Guía 34 explica que la ley creó el gobierno escolar para asegurar la participación organizada de la comunidad, y que con ello se busca que el PEI sea concertado por directivos, docentes, padres de familia, estudiantes, egresados y representantes del sector productivo local; también asigna al rector dirigir la resignificación del PEI con la participación de los distintos actores. La opción de redactar y luego socializar es el distractor cercano: parece participativa, pero solo informa. En un énfasis de media técnica, el sector productivo y los egresados aportan información decisiva. El nivel avanzado convierte la participación en construcción conjunta.",
     "Guía 34 MEN (2008), 1.5 Instancias de participación.",
     "PEI: se concerta con directivos, docentes, familias, estudiantes, egresados y sector productivo; socializar no es concertar.",
     [(G34, "Con lo anterior se busca que el PEI sea concertado por directivos, docentes, padres de familia, estudiantes, egresados y representantes del sector productivo local.", K014),
      (G34, "El Rector o Director, encargado de dirigir la resignificación del PEI con la participación de los distintos actores de la comunidad educativa", K014)],
     "PEI y participación", "ascenso 2024")

# ------------------------------------------------------------ K011 · Guía 34, autonomía escolar
caso("CK56", "Una asignatura de emprendimiento",
     "Con el nuevo énfasis agroindustrial del PEI, el consejo académico propone crear en décimo y once la asignatura optativa «Emprendimiento agropecuario» "
     "dentro del área de tecnología e informática. Un docente sugiere sacar las horas de la asignatura eliminando educación artística en la media, y un "
     "padre de familia afirma que ningún colegio puede crear asignaturas sin aprobación del Ministerio de Educación.")
item("CO088", "CK56", "GDI-AUTON", 3,
     "De acuerdo con la autonomía escolar, lo que usted como coordinador le explica al consejo académico es que",
     [("pueden crear la asignatura en lugar de educación artística, porque la autonomía permite ajustar el plan de estudios a las necesidades de la región.",
       "Es incorrecta. Mezcla una verdad con un error: la autonomía sí permite adaptar el plan a la región, pero el plan se organiza alrededor de las áreas fundamentales de cada nivel; la optativa se introduce dentro de las áreas, no en reemplazo de una de ellas."),
      ("pueden crear la asignatura dentro de las áreas de la ley, según el énfasis del PEI, y deben rendir cuentas a la comunidad sobre sus logros.",
       "Es correcta. La Guía 34 y la Ley 115 permiten introducir asignaturas optativas dentro de las áreas establecidas en la ley, en función del énfasis del PEI, y la Guía 34 añade que la autonomía se complementa con la rendición de cuentas sobre los logros."),
      ("deben presentar la asignatura al Ministerio de Educación para su aprobación, porque los cambios en el plan de estudios requieren aval nacional.",
       "Es incorrecta. El Ministerio fija lineamientos y estándares, pero la Ley General de Educación dio a cada establecimiento la autonomía para organizar su plan de estudios e introducir asignaturas optativas sin pedir aprobación previa.")],
     "B",
     "El caso tiene dos condiciones. Primera: la Guía 34 explica que la autonomía escolar permitió a cada establecimiento organizar su plan de estudios alrededor de las áreas fundamentales determinadas para cada nivel y de las asignaturas optativas en función del énfasis de su PEI; la Ley 115 (art. 77) precisa que las optativas se introducen dentro de las áreas establecidas en la ley, de modo que no reemplazan un área fundamental. Segunda: no se requiere aprobación del Ministerio, pero el ejercicio de la autonomía debe complementarse con una apropiada rendición de cuentas sobre los logros. Recuerde: autonomía con límites (áreas y lineamientos) y con rendición de cuentas.",
     "Guía 34 MEN (2008), 1.3 La autonomía escolar; Ley 115 de 1994, art. 77.",
     "Asignaturas optativas: dentro de las áreas de la ley y según el énfasis del PEI; la autonomía exige rendir cuentas.",
     [(G34, "les permitió organizar su plan de estudios alrededor de las áreas fundamentales determinadas para cada nivel, de las asignaturas optativas en función del énfasis de su PEI", K011),
      (G34, "Este ejercicio de autonomía debe ser complementado con una apropiada rendición de cuentas acerca de los logros obtenidos.", K011),
      (L115, "introducir asignaturas optativas dentro de las áreas establecidas en la ley", "Ley 115, art. 77")],
     "Autonomía escolar")

# ------------------------------------------------------------ GAF · Fondo de Servicios Educativos
caso("CK57", "Tres solicitudes para el fondo",
     "La sede rural de su institución desarrolla un proyecto pedagógico productivo de piscicultura con los estudiantes de la media. En la reunión de "
     "presupuesto llegan tres solicitudes para pagar con el Fondo de Servicios Educativos: 1) alevinos y concentrado para el proyecto de piscicultura; "
     "2) la matrícula de cuatro docentes en un diplomado sobre proyectos productivos; 3) los pasajes y viáticos de un docente que irá a un encuentro "
     "de experiencias en Bogotá. El rector le pide a usted revisar qué se puede financiar.")
item("CO089", "CK57", "GAF-FONDOS", 3,
     "Según el Decreto 1075, de las tres solicitudes se puede financiar con el Fondo de Servicios Educativos",
     [("la primera y la segunda, porque las dos guardan relación con el PEI, mientras que la tercera solo si el consejo directivo la aprueba.",
       "Es incorrecta. La relación con el PEI es condición necesaria, pero no suficiente: el decreto prohíbe expresamente financiar la capacitación de funcionarios, aunque el tema del diplomado esté ligado al proyecto productivo."),
      ("las tres, siempre que el consejo directivo las incluya en el presupuesto y guarden estricta relación con el Proyecto Educativo Institucional.",
       "Es incorrecta. La aprobación del consejo directivo no vuelve permitido un gasto prohibido: la capacitación de funcionarios y los viáticos y pasajes del personal están en la lista de prohibiciones del ordenador del gasto."),
      ("solo la primera, porque el sostenimiento de proyectos pedagógicos productivos es un gasto permitido y las otras dos están prohibidas.",
       "Es correcta. El artículo 2.3.1.6.3.11 permite sufragar el sostenimiento de semovientes y proyectos pedagógicos productivos; el 2.3.1.6.3.13 prohíbe financiar la capacitación de funcionarios y los gastos de personal como viáticos y pasajes.")],
     "C",
     "El ítem exige cruzar dos artículos del Decreto 1075. El 2.3.1.6.3.11 enumera en qué se pueden usar los recursos, siempre que guarden estricta relación con el PEI, e incluye el sostenimiento de semovientes y proyectos pedagógicos productivos. El 2.3.1.6.3.13 prohíbe al ordenador del gasto financiar la capacitación de funcionarios y reconocer gastos inherentes a la administración de personal, como viáticos, pasajes y gastos de viaje. Los gastos de viaje permitidos son los de los educandos, que pueden incluir al docente acompañante solo en las condiciones del numeral 9. Ni la relación con el PEI ni la aprobación del consejo directivo convierten en permitido un gasto prohibido.",
     "Decreto 1075 de 2015, arts. 2.3.1.6.3.11 y 2.3.1.6.3.13 (Decreto 4791 de 2008).",
     "Fondo: proyectos pedagógicos productivos sí; capacitación de funcionarios y viáticos del personal no, aunque el consejo los apruebe.",
     [(D1075, "10. Sufragar los costos destinados al sostenimiento de semovientes y proyectos pedagógicos productivos.", "Decreto 1075, art. 2.3.1.6.3.11"),
      (D1075, "6. Financiar fa capacitación de funcionarios.", "Decreto 1075, art. 2.3.1.6.3.13"),
      (D1075, "2. Reconocer o financiar gastos inherentes a la administración de personal, tales como viáticos, pasajes, gastos de viaje", "Decreto 1075, art. 2.3.1.6.3.13")],
     "Fondo de Servicios Educativos")

# ------------------------------------------------------------ GDI · seguimiento y evaluación del plan de mejoramiento
caso("CK58", "Tres momentos para mirar el plan",
     "El equipo de gestión que usted integra prepara el sistema de seguimiento del plan de mejoramiento de lectura. Propone tres momentos: 1) en mayo, "
     "mientras se ejecuta, revisar si las acciones son adecuadas para lograr los objetivos; 2) en noviembre, comparar lo logrado con lo propuesto al "
     "inicio; 3) dos años después, establecer si los estudiantes y el equipo gestor presentan cambios duraderos gracias al plan.")
item("CO090", "CK58", "GDI-MEJORA", 2,
     "Según la Guía 34, los momentos 1, 2 y 3 corresponden, respectivamente, a",
     [("el seguimiento o evaluación de proceso, la evaluación de resultados y la evaluación de impacto.",
       "Es correcta. La Guía 34 llama seguimiento o evaluación de proceso a la valoración durante la implementación; evaluación de resultados a comparar lo logrado con lo propuesto; y evaluación de impacto a establecer si hay cambios duraderos."),
      ("la evaluación de resultados, la evaluación de impacto y la autoevaluación institucional anual.",
       "Es incorrecta. Revisar en mayo si las acciones son adecuadas, mientras el plan se ejecuta, es seguimiento; además, la autoevaluación es la primera etapa de la ruta y no un tipo de evaluación del plan de mejoramiento."),
      ("el seguimiento o evaluación de proceso, la evaluación de impacto y la evaluación de resultados.",
       "Es incorrecta. Acierta en el primer momento, pero invierte los otros dos: comparar lo logrado con lo propuesto es evaluación de resultados, y buscar cambios duraderos en los beneficiarios es evaluación de impacto.")],
     "A",
     "La Guía 34 describe en la tercera etapa de la ruta tres tipos de evaluación del plan de mejoramiento. Cuando se valora durante la implementación se habla de seguimiento o evaluación de proceso, cuyo propósito es detectar a tiempo lo que facilita o limita el logro. La evaluación de resultados compara lo logrado con lo propuesto inicialmente, y la de impacto establece si los beneficiarios y el equipo gestor presentan cambios duraderos. Los tres arrojan información distinta y complementaria. La pista está en el momento y en la pregunta: durante, al final frente a lo planeado, y tiempo después frente a cambios duraderos.",
     "Guía 34 MEN (2008), 2.3 Tercera etapa: seguimiento y evaluación.",
     "Durante: seguimiento (proceso). Al final frente a lo propuesto: resultados. Cambios duraderos: impacto.",
     [(G34, "Cuando esta labor se realiza durante su implementación, se habla de seguimiento o evaluación de proceso.", "Guía 34, 2.3 Tercera etapa"),
      (G34, "la evaluación de resultados pretende comparar lo logrado en el desarrollo del plan con lo propuesto inicialmente; la de impacto busca establecer si, como consecuencia de la ejecución", "Guía 34, 2.3 Tercera etapa"),
      (G34, "los beneficiarios de un proyecto y el equipo gestor presentan cambios duraderos.", "Guía 34, 2.3 Tercera etapa")],
     "Ruta del mejoramiento")

# ------------------------------------------------------------ GAC · acompañamiento: evaluación formativa con docentes
caso("CK59", "Solo el examen final",
     "En sus visitas a las aulas de sexto y séptimo, usted encuentra que la mayoría de los docentes evalúa solo con un examen escrito al final de cada "
     "periodo; los estudiantes reciben la nota sin comentarios y no saben qué deben mejorar. El SIEE de la institución dice que la evaluación es "
     "formativa y continua. Varios docentes le dicen que «con 40 estudiantes no hay tiempo para otra cosa».")
item("CO091", "CK59", "GAC-ACOMP", 2,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("recordar por circular que el SIEE exige una evaluación formativa y advertir que su cumplimiento se revisará en la evaluación de desempeño.",
       "Es incorrecta (nivel inferior). Usa el control y la advertencia en lugar del acompañamiento: no ayuda a los docentes a resolver la dificultad práctica que plantean ni cambia lo que ocurre en el aula."),
      ("analizar sus instrumentos en jornadas pedagógicas y acordar con cada área prácticas de retroalimentación, con seguimiento en el aula.",
       "Es correcta (nivel avanzado). Usa las jornadas pedagógicas para revisar con los docentes sus prácticas, acuerda estrategias viables de retroalimentación y les hace seguimiento, como pide la Resolución 3842 para el coordinador."),
      ("compartir con los docentes una guía sobre evaluación formativa con ejemplos de rúbricas, para que cada uno la aplique en sus clases.",
       "Es incorrecta (nivel satisfactorio). Aporta un recurso útil, pero deja la aplicación a la iniciativa individual y no construye acuerdos de área ni hace seguimiento a si las prácticas de aula cambian.")],
     "B",
     "La Resolución 3842 asigna al coordinador participar en jornadas pedagógicas para promover, evaluar, hacer seguimiento y acompañar las buenas prácticas académicas, y coordinar el seguimiento a las actividades académicas de los docentes de manera que permita retroalimentar su desempeño profesional. A su vez, el mismo manual pide a los docentes realizar el seguimiento, la evaluación y la retroalimentación con un enfoque integral, flexible y formativo. En el formato de ascenso, el nivel avanzado acompaña: analiza con los docentes sus instrumentos, construye acuerdos viables para grupos numerosos y vuelve al aula a verificar. Informar (satisfactorio) o advertir (inferior) no transforma la práctica.",
     "Resolución 3842 de 2022, 1.3.1 Funciones del coordinador y 2.1.3 Funciones del docente.",
     "Acompañamiento: jornadas pedagógicas, acuerdos de área y seguimiento en el aula; no circulares ni advertencias.",
     [(R3842, "Participar en la organización y desarrollo de jornadas pedagógicas con los docentes y la comunidad educativa para promover, actualizar, evaluar, hacer seguimiento y acompañar las buenas prácticas sociales y académicas de la institución.", "Resolución 3842, 1.3.1 Funciones del coordinador"),
      (R3842, "Coordinar la implementación del proceso de seguimiento al cumplimiento de las asignaciones y actividades académicas de los docentes, que permita la retroalimentación del desempeño profesional de los docentes", "Resolución 3842, 1.3.1 Funciones del coordinador, num. 14"),
      (R3842, "Realizar el seguimiento, evaluación y retroalimentación teniendo en cuenta un enfoque integral, flexible y formativo.", "Resolución 3842, 2.1.3 Funciones del docente, num. 12")],
     "Acompañamiento pedagógico", "ascenso 2024")

# ------------------------------------------------------------ GCO · protocolos del manual de convivencia
caso("CK60", "La estudiante que contó",
     "Una estudiante de noveno le contó a su director de grupo que varios compañeros estaban compartiendo en redes una foto manipulada de otra compañera. "
     "Al día siguiente, todo el curso sabía quién había informado y la estudiante empezó a ser excluida; además, el director de grupo había comentado el "
     "caso, con nombres, en el chat de padres del curso. Al revisar el manual, el comité de convivencia encuentra que el protocolo solo dice: «el docente "
     "remite el caso a coordinación».")
item("CO092", "CK60", "GCO-CONV", 3,
     "A partir de lo que falló en este caso, lo que el protocolo del manual debe incluir como mínimo, según el Decreto 1965, es",
     [("un directorio con los teléfonos de la Policía de Infancia y Adolescencia y la Fiscalía, para remitirles los casos de ciberacoso.",
       "Es incorrecta. El directorio sí es un contenido mínimo del protocolo, pero no responde a lo que falló; además, un ciberacoso que no constituye delito es una situación tipo II que se atiende en el establecimiento, no se remite de inmediato a esas autoridades."),
      ("un formato único de queja que el estudiante deba radicar por escrito en coordinación, para que quede constancia antes de actuar.",
       "Es incorrecta. El decreto pide definir la forma de recepción y radicación de las quejas, pero exigir un formato escrito previo no corrige lo ocurrido y puede desestimular que los estudiantes informen."),
      ("mecanismos para garantizar la confidencialidad de la información y para proteger a quien informa de posibles acciones en su contra.",
       "Es correcta. El artículo 41 del Decreto 1965 exige que los protocolos definan mecanismos para garantizar la intimidad y la confidencialidad, y mecanismos que protejan a quien informa; justamente eso faltó en el caso.")],
     "C",
     "La clave es «lo que falló». El artículo 41 del Decreto 1965 fija los aspectos mínimos de los protocolos del establecimiento: la forma de recibir y radicar las quejas, los mecanismos para garantizar el derecho a la intimidad y a la confidencialidad, los mecanismos para proteger a quien informa de posibles acciones en su contra, las estrategias pedagógicas, las consecuencias proporcionales, el seguimiento y un directorio de entidades. En el caso se expusieron los nombres en un chat y se dejó sin protección a la estudiante que informó. Las otras opciones mencionan contenidos que también existen, pero no corrigen esas dos fallas.",
     "Decreto 1965 de 2013, art. 41 (compilado en el Decreto 1075 de 2015).",
     "Protocolos de convivencia: confidencialidad de la información y protección de quien informa son contenidos mínimos.",
     [(D1965, "2. Los mecanismos para garantizar el derecho a la intimidad y a la confidencialidad de los documentos en medio físico o electrónico", "Decreto 1965, art. 41"),
      (D1965, "3. Los mecanismos mediante los cuales se proteja a quien informe sobre la ocurrencia de situaciones que afecten la convivencia escolar", "Decreto 1965, art. 41")],
     "Protocolos de convivencia")

# ------------------------------------------------------------ GCO · inclusión y convivencia
caso("CK61", "Burlas en el descanso",
     "En cuarto grado estudia un niño con discapacidad intelectual que tiene su PIAR al día. En el descanso, varios compañeros lo imitan y se burlan de él, "
     "y en la reunión de padres algunas familias dijeron que «ese niño debería estar en un colegio especial». La docente de cuarto le pide a usted como "
     "coordinador que intervenga.")
item("CO093", "CK61", "GCO-INCL", 2,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("atender el caso con el comité de convivencia, ajustar la promoción y prevención del manual y hacer jornadas con las familias sobre inclusión.",
       "Es correcta (nivel avanzado). Atiende la situación con el comité y actúa sobre la causa en los dos frentes que señala el Decreto 1421: ajusta el manual con estrategias de promoción y prevención contra la exclusión y hace jornadas con las familias sobre el derecho a la educación de las personas con discapacidad."),
      ("organizarle al estudiante el descanso en un espacio aparte con un docente acompañante, mientras se calma la situación con el grupo.",
       "Es incorrecta (nivel inferior). Busca protegerlo, pero lo separa de sus compañeros y traslada la carga al niño discriminado: la medida termina reforzando la exclusión que se quería evitar."),
      ("hablar con el grupo de cuarto sobre el respeto a la diferencia y citar a los padres de los niños que se burlan para que firmen compromisos.",
       "Es incorrecta (nivel satisfactorio). Interviene en el caso concreto, pero no transforma las condiciones institucionales ni aborda las creencias de las familias que cuestionan el derecho del niño a estudiar en la institución.")],
     "A",
     "El Decreto 1421 asigna a los establecimientos, entre otras responsabilidades, ajustar los manuales de convivencia e incorporar estrategias en los componentes de promoción y prevención de la ruta de atención integral, para prevenir cualquier caso de exclusión o discriminación por discapacidad, y adelantar con las familias, en el marco de la escuela de familias, jornadas de concientización sobre el derecho a la educación de las personas con discapacidad. En el formato de ascenso, el nivel avanzado actúa sobre las causas y sobre toda la comunidad. Separar al niño es el error típico: parece protector, pero contradice el enfoque inclusivo.",
     "Decreto 1421 de 2017, art. 2.3.3.5.2.3.1, literal c), numerales 10 y 13.",
     "Discriminación por discapacidad: ajustar el manual (promoción y prevención) y trabajar con las familias; nunca separar al estudiante.",
     [(D1421, "10. Ajustar los manuales de convivencia escolar e incorporar estrategias en los componentes de promoción y prevención de la ruta de atención integral para la convivencia escolar, con miras a fomentar la convivencia y prevenir cualquier caso de exclusión o discriminación en razón a la discapacidad de los estudiantes.", "Decreto 1421, responsabilidades de los establecimientos, num. 10"),
      (D1421, "13. Adelantar con las familias o acudientes, en el marco de la escuela de familias, jornadas de concientización sobre el derecho a la educación de las personas con", "Decreto 1421, responsabilidades de los establecimientos, num. 13")],
     "Inclusión y convivencia", "ascenso 2024")

# ------------------------------------------------------------ GAC · contenido del SIEE
caso("CK62", "Boletines que no dicen nada",
     "El consejo académico revisa el SIEE con base en la encuesta de fin de año. Hay dos quejas principales: 1) las familias dicen que el boletín solo "
     "trae números y la palabra «Básico», sin explicar qué logró su hijo ni qué debe mejorar; 2) los estudiantes dicen que nunca se les pide valorar su "
     "propio trabajo ni el de su aprendizaje durante el periodo. Usted como coordinador orienta la revisión.")
item("CO094", "CK62", "GAC-SIEE", 3,
     "Según el Decreto 1075, los componentes del SIEE que deben ajustarse para atender las quejas 1 y 2 son, respectivamente,",
     [("la periodicidad de entrega de informes a los padres y las estrategias de valoración integral de los desempeños de los estudiantes.",
       "Es incorrecta. Entregar más seguido un boletín poco claro no resuelve la queja de las familias; y la valoración integral es responsabilidad del docente, mientras que la queja de los estudiantes es sobre valorarse a sí mismos."),
      ("la escala de valoración institucional y los mecanismos de participación de la comunidad en la construcción del sistema de evaluación.",
       "Es incorrecta. La escala define los niveles y su equivalencia con la nacional, no la claridad del informe; y la participación en construir el SIEE es distinta de que los estudiantes se autoevalúen en cada periodo."),
      ("la estructura de los informes de los estudiantes y los procesos de autoevaluación de los estudiantes, que el SIEE debe contener.",
       "Es correcta. El artículo 2.3.3.3.3.4 pide que el SIEE defina la estructura de los informes para que sean claros, comprensibles y den información integral, y los procesos de autoevaluación de los estudiantes.")],
     "C",
     "El artículo 2.3.3.3.3.4 del Decreto 1075 (Decreto 1290, art. 4) enumera once contenidos del SIEE. Dos responden exactamente a las quejas: la estructura de los informes de los estudiantes, para que sean claros, comprensibles y den información integral del avance en la formación (queja 1), y los procesos de autoevaluación de los estudiantes (queja 2). Los distractores usan otros numerales reales del mismo artículo —periodicidad, valoración integral, escala, participación— que suenan cercanos pero no corrigen lo que se reclama. Para este tipo de pregunta, relacione la palabra clave de la queja con la del numeral: «claros» con estructura, «valorar su propio trabajo» con autoevaluación.",
     "Decreto 1075 de 2015, art. 2.3.3.3.3.4 (Decreto 1290 de 2009, art. 4).",
     "SIEE: informes claros y comprensibles = estructura de los informes (num. 9); valorarse a sí mismo = autoevaluación (num. 5).",
     [(D1075, "9. La estructura de los informes de los estudiantes, para que sean claros, comprensibles y den información integral del avance en la formación.", "Decreto 1075, art. 2.3.3.3.3.4"),
      (D1075, "5. Los procesos de autoevaluación de los estudiantes.", "Decreto 1075, art. 2.3.3.3.3.4")],
     "SIEE")

# ------------------------------------------------------------ PSI · compromiso social e institucional
caso("CK63", "El informe del viernes",
     "La secretaría de educación pide a todas las instituciones, con plazo hasta el viernes, un informe de estudiantes que dejaron de asistir en el "
     "segundo semestre, para activar estrategias de permanencia. Es miércoles y faltan los datos de tres grupos. Un docente le sugiere a usted copiar las "
     "cifras del informe del año pasado, «porque igual nadie las revisa y así cumplimos».")
item("CO095", "CK63", "PSI-COMP", 2,
     "La actuación que mejor demuestra la competencia de compromiso social e institucional es",
     [("enviar el informe con las cifras del año anterior para cumplir el plazo y corregirlo después, cuando ya se tengan los datos reales de los grupos.",
       "Es incorrecta. Cumple el plazo, pero falta a la honestidad e integridad: entrega datos que no corresponden a la realidad y que la secretaría usará para decidir sobre estudiantes que pueden estar desertando."),
      ("consolidar con los directores de grupo los datos reales y entregar a tiempo el informe, señalando los datos que aún falten por verificar.",
       "Es correcta. Responde con oportunidad, eficiencia y calidad, y con honestidad: moviliza al equipo para obtener los datos reales, cumple el plazo y advierte con transparencia lo que falta, porque detrás del informe hay estudiantes en riesgo."),
      ("solicitar a la secretaría ampliar el plazo dos semanas y no enviar ningún dato hasta tener el informe completo y revisado.",
       "Es incorrecta. Cuida la calidad del dato, pero sacrifica la oportunidad: retrasa la activación de estrategias de permanencia para los estudiantes que ya dejaron de asistir, cuando era posible cumplir con la información disponible.")],
     "B",
     "La Guía de orientación de la CNSC define el compromiso social e institucional como la habilidad para asumir responsabilidades con ética y profesionalismo, anteponiendo los intereses institucionales a los personales, y le asocia conductas como demostrar honestidad e integridad en el ejercicio profesional y responder con oportunidad, eficiencia y calidad a las tareas asignadas. La opción correcta equilibra todas esas conductas: datos reales, entrega a tiempo y transparencia sobre lo pendiente. Copiar cifras sacrifica la honestidad y pedir más plazo sacrifica la oportunidad. En la prueba psicotécnica, la mejor respuesta suele cumplir la tarea sin renunciar a la ética.",
     "Guía de orientación al aspirante CNSC 2022, ejemplo 2 (Compromiso social e institucional).",
     "Compromiso social e institucional: honestidad + oportunidad + calidad; ni datos falsos ni demoras que afecten a los estudiantes.",
     [(GCNSC, "Habilidad para asumir responsabilidades con ética y profesionalismo, dentro y fuera del establecimiento, anteponiendo los intereses institucionales a los personales", "Guía de orientación CNSC 2022, ejemplo 2"),
      (GCNSC, "demuestra honestidad e integridad en su ejercicio profesional; reflexiona sistemáticamente sobre su responsabilidad social como educador; responde con oportunidad, eficiencia y calidad a las tareas que se le asignan", "Guía de orientación CNSC 2022, ejemplo 2")],
     "Compromiso social e institucional")

lote = {"id": "coord-2026-11-25", "fecha": "2026-11-25", "cargo": "coordinador",
        "nota": "Lectura K014 (Guía 34, 1.5 instancias de gobierno y participación) con cuatro ítems y K011 (autonomía escolar) con uno. Formatos ingreso 2022 y ascenso 2024 (la correcta es la de nivel avanzado).",
        "casos": casos, "fichas": [], "items": items}
json.dump(lote, open(os.path.join(RAIZ, "data", "lotes", "coord-2026-11-25.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(casos), "casos ·", len(items), "ítems")
