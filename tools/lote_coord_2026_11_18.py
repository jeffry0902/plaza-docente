# -*- coding: utf-8 -*-
"""Tercer lote de coordinación (2026-11-18). Cubre la lectura K001 (Resolución 3842, presentación: función general y
competencias del directivo docente) y la K003 (Decreto 1075, comunidad educativa y órganos del gobierno escolar), y rota
GAC, GAF, GCO y PSI. Formatos: ingreso 2022 (3 opciones, una correcta) y ascenso 2024 (cada opción es un nivel de
desempeño; la correcta es la de nivel avanzado). Genera data/lotes/coord-2026-11-18.json. Citas: texto literal de fuentes/."""
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


R3842, D1278, D1075, L1620, D1421 = "resolucion_3842_2022_ocr", "decreto_1278_2002", "decreto_1075_2015", "ley_1620_2013", "decreto_1421_2017"
GCNSC = "guia_orientacion_cnsc_2022"

# ------------------------------------------------------------ K001 · Resolución 3842 (presentación)
caso("CK20", "Nombramiento en período de prueba",
     "Usted fue nombrado coordinador en período de prueba en una institución educativa oficial de Yopal y se posesionó en marzo. "
     "En la primera reunión, el rector le pide presentar su propuesta de trabajo para el año y le recuerda que, al terminar el año escolar, usted será evaluado. "
     "Un colega le comenta que esa evaluación «depende de los resultados Saber de la institución». Mientras tanto, usted empieza a anotar evidencias de su gestión para su autoevaluación.")
item("CO048", "CK20", "GAF-TALENTO", 2,
     "Sobre la evaluación que usted recibirá al terminar el año escolar, lo que corresponde según las normas es que",
     [("será una evaluación de desempeño laboral y de competencias, con base en las competencias funcionales y comportamentales del Manual.",
       "Es correcta. El artículo 12 del Decreto 1278 dice que al terminar el año el nombrado en período de prueba es sujeto de una evaluación de desempeño laboral y de competencias, y la Resolución 3842 dice que sus competencias son la base de esos protocolos."),
      ("será una valoración de los resultados de la institución en las pruebas Saber, porque esos resultados muestran el impacto del directivo.",
       "Es incorrecta. Los resultados Saber son un insumo de la autoevaluación institucional, pero la norma no los convierte en la base de la evaluación del período de prueba, que se hace sobre el desempeño y las competencias del cargo."),
      ("será una revisión de las metas del plan de mejoramiento que el rector le asigne al inicio, porque él es su superior inmediato.",
       "Es incorrecta. El rector es el superior inmediato del coordinador, pero la evaluación del período de prueba no es una revisión libre de metas fijadas por él: se rige por protocolos basados en las competencias funcionales y comportamentales del Manual.")],
     "A",
     "Dos normas se complementan. El artículo 12 del Decreto 1278 establece que, al terminar el año académico, quien fue nombrado en período de prueba es sujeto de una evaluación de desempeño laboral y de competencias; si la aprueba, adquiere derechos de carrera. La presentación de la Resolución 3842 agrega que las competencias funcionales y comportamentales del Manual son la base para el diseño de las pruebas del concurso y de los protocolos de evaluación de período de prueba. Por eso la palabra clave es «competencias»: ni los resultados Saber ni metas fijadas por el rector reemplazan ese referente.",
     "Decreto 1278 de 2002, art. 12; Resolución 3842 de 2022, 1.1.1 Competencias generales.",
     "Período de prueba: al cerrar el año, evaluación de desempeño laboral y de competencias (las del Manual de la Resolución 3842).",
     [(R3842, "para el diseño y adopción de los protocolos de evaluación de período de prueba y evaluación anual de desempeño laboral de los directivos docentes", "Resolución 3842, 1.1.1 Competencias generales"),
      (D1278, "Al terminar el año académico respectivo, la persona nombrada en periodo de prueba será sujeto de una evaluación de desempeño laboral y de competencias.", "Decreto 1278, art. 12")],
     "Talento humano y período de prueba")
item("CO049", "CK20", "GDI-ROL", 2,
     "Para preparar la propuesta de trabajo que le pidió el rector, la actuación que corresponde al nivel avanzado es",
     [("redactar usted mismo un plan detallado a partir de su experiencia y socializarlo con los docentes para que lo pongan en marcha en abril.",
       "Es incorrecta (nivel mínimo). Cumple con entregar un plan, pero lo construye de forma unidireccional: los docentes solo lo reciben. La función general del directivo pide liderar una construcción colectiva, no presentar un plan terminado."),
      ("esperar las directrices de la secretaría de educación antes de proponer acciones, para no contradecir las decisiones que lleguen después.",
       "Es incorrecta (nivel inferior). Las directrices de la secretaría sí son un marco, pero aplazar la planeación deja al establecimiento sin rumbo y desconoce que el directivo debe liderar el mejoramiento continuo en el marco del PEI."),
      ("construir el plan con los equipos docentes a partir del PEI y de las directrices de la secretaría, con metas y momentos de revisión.",
       "Es correcta (nivel avanzado). Lidera una construcción colectiva, la enmarca en el PEI y en las directrices de la secretaría, y prevé revisión para el mejoramiento continuo, que es exactamente la función general del directivo docente.")],
     "C",
     "La Resolución 3842 define la función general de los directivos docentes: desarrollan procesos de dirección, planeación, organización y evaluación, y son responsables de liderar y gestionar la construcción colectiva y el mejoramiento continuo de la organización escolar en el marco del PEI y de las directrices de la secretaría de educación y del MEN. En la lógica de la prueba de ascenso, el nivel avanzado reúne esos elementos: construye con otros, se enmarca en el PEI y prevé revisión. El plan hecho en solitario cumple a medias (mínimo) y esperar instrucciones es inferior.",
     "Resolución 3842 de 2022, 1.1 Función general; Guía orientadora de la prueba de ascenso para coordinador (2024).",
     "Función general del directivo: liderar la construcción colectiva y el mejoramiento continuo en el marco del PEI.",
     [(R3842, "son responsables de liderar y gestionar la construcción colectiva y mejoramiento continuo de la organización escolar en el marco del Proyecto Educativo Institucional (PEI), las directrices de la Secretaría de Educación", "Resolución 3842, 1.1 Función general")],
     "Rol del directivo docente", "ascenso 2024")
item("CO050", "CK20", "GDI-COMPET", 3,
     "Usted anota dos evidencias: 1) orientó a la comunidad educativa hacia el logro de las metas institucionales; 2) lideró el rediseño de un currículo que atiende la diversidad con perspectiva de inclusión. Según la Resolución 3842, esas evidencias corresponden, en su orden, a las áreas de gestión",
     [("comunitaria, la primera, porque involucra a la comunidad, y académica, la segunda, porque trata del currículo.",
       "Es incorrecta. Acierta en la segunda, pero la primera no es gestión comunitaria: guiar a la comunidad hacia las metas institucionales es la capacidad que la Resolución 3842 describe para la gestión directiva. La palabra «comunidad» es la trampa."),
      ("directiva, la primera, porque orienta hacia las metas, y académica, la segunda, porque trata del currículo.",
       "Es correcta. La Resolución 3842 dice que la gestión directiva involucra guiar a la comunidad educativa hacia el logro de las metas institucionales, y que la académica implica diseñar y evaluar un currículo que atienda la diversidad con perspectiva de inclusión."),
      ("directiva, la primera, porque orienta hacia las metas, y comunitaria, la segunda, porque trata de la inclusión.",
       "Es incorrecta. Acierta en la primera, pero la segunda es gestión académica: la Resolución 3842 ubica en esa área el diseño de un currículo que atienda la diversidad con una perspectiva de inclusión. La palabra «inclusión» lleva a confundirla con la comunitaria.")],
     "B",
     "La Resolución 3842 organiza las competencias funcionales del directivo en cuatro áreas de gestión. De la gestión directiva dice que involucra la capacidad para guiar a la comunidad educativa hacia el logro de las metas institucionales; de la académica, que implica diseñar, planear, implementar y evaluar un currículo que promueva el aprendizaje y atienda la diversidad con una perspectiva de inclusión. La CNSC suele poner palabras gancho, como «comunidad» o «inclusión», para que se clasifique por el tema y no por la descripción oficial del área. Clasifique siempre por lo que hace la acción.",
     "Resolución 3842 de 2022, 1.1.2 Competencias funcionales.",
     "Guiar a la comunidad hacia las metas = gestión directiva; currículo que atiende la diversidad = gestión académica.",
     [(R3842, "Involucra la capacidad para guiar a la comunidad educativa hacia el logro de las metas institucionales.", "Resolución 3842, 1.1.2 Gestión Directiva"),
      (R3842, "Implica la capacidad para diseñar, planear, implementar y evaluar un currículo que promueva el aprendizaje en las aulas y que atienda la diversidad con una perspectiva de inclusión.", "Resolución 3842, 1.1.2 Gestión Académica")],
     "Competencias funcionales del directivo")

caso("CK21", "Revisión del plan de estudios",
     "En la sede que usted coordina hay estudiantes con discapacidad, estudiantes que llegaron de otro país a mitad de año y un grupo de la zona rural que viaja más de una hora para llegar. "
     "En la revisión del plan de estudios, varios docentes afirman que el currículo «funciona bien para el estudiante promedio» y que los demás casos se pueden atender con talleres de nivelación por fuera de la clase.")
item("CO051", "CK21", "GAC-ACOMP", 3,
     "Como coordinador, la actuación que corresponde al nivel avanzado es",
     [("pedir a cada área que agregue a su plan un apartado de inclusión con talleres de nivelación y revisarlo con ellas al cierre del año.",
       "Es incorrecta (nivel satisfactorio). Reconoce la diversidad y hace seguimiento, pero la deja como un apartado aparte y por fuera de la clase; no transforma el diseño, la implementación ni la evaluación del currículo para todos."),
      ("remitir a los estudiantes con discapacidad y a los recién llegados al docente de apoyo para que les adapte el currículo vigente.",
       "Es incorrecta (nivel inferior). Delega la diversidad en una sola persona y mantiene intacto un currículo pensado para el promedio; además deja por fuera a los estudiantes rurales y no involucra a los docentes de aula."),
      ("liderar con las áreas la revisión del diseño, la implementación y la evaluación del currículo para que atienda esa diversidad.",
       "Es correcta (nivel avanzado). Orienta a los equipos de área para que todo el ciclo curricular, desde el diseño hasta la evaluación, promueva el aprendizaje en el aula y atienda la diversidad con perspectiva de inclusión, como describe la gestión académica.")],
     "C",
     "La Resolución 3842 dice que la gestión académica implica la capacidad para diseñar, planear, implementar y evaluar un currículo que promueva el aprendizaje en las aulas y que atienda la diversidad con una perspectiva de inclusión. La palabra clave es «en las aulas»: la diversidad no se atiende por fuera del currículo ni delegándola. En la prueba de ascenso, el nivel avanzado lidera con los equipos de área una revisión de todo el ciclo curricular; el satisfactorio agrega apartados sin cambiar la práctica, y el inferior remite a los estudiantes a otra persona.",
     "Resolución 3842 de 2022, 1.1.2 Gestión Académica; Guía orientadora de la prueba de ascenso para coordinador (2024).",
     "Inclusión en el currículo: se diseña, se enseña y se evalúa para todos en el aula; no se resuelve con talleres aparte.",
     [(R3842, "Implica la capacidad para diseñar, planear, implementar y evaluar un currículo que promueva el aprendizaje en las aulas y que atienda la diversidad con una perspectiva de inclusión.", "Resolución 3842, 1.1.2 Gestión Académica")],
     "Acompañamiento pedagógico", "ascenso 2024")

# ------------------------------------------------------------ K003 · Decreto 1075, gobierno escolar
caso("CK22", "Vacante en el consejo directivo",
     "En agosto, la docente que representa a los profesores en el consejo directivo es trasladada a otra institución. "
     "El rector le pide a usted organizar lo necesario para que el consejo vuelva a sesionar completo. "
     "En la reunión de docentes, algunos proponen elegir a alguien «por un año completo, para que alcance a hacer algo».")
item("CO052", "CK22", "GDI-GOB", 2,
     "Sobre la representación de los docentes en el consejo directivo, lo que corresponde según el Decreto 1075 es",
     [("elegir un nuevo representante por un período anual contado desde su elección, como proponen los docentes.",
       "Es incorrecta. Los representantes se eligen para períodos anuales, pero cuando hay vacancia el decreto no abre un período nuevo: el elegido solo completa el período que estaba en curso."),
      ("elegir un reemplazo para el resto del período, porque los representantes se eligen para períodos anuales.",
       "Es correcta. El artículo 2.3.3.1.5.3 del Decreto 1075 dice que los representantes de los órganos colegiados se eligen para períodos anuales y que, en caso de vacancia, se elige su reemplazo para el resto del período."),
      ("dejar la vacante hasta las elecciones del próximo año, porque el período anual ya está en curso.",
       "Es incorrecta. Dejar la silla vacía priva a los docentes de su representación en el consejo directivo durante meses; la norma prevé expresamente elegir un reemplazo en caso de vacancia.")],
     "B",
     "El artículo 2.3.3.1.5.3 del Decreto 1075 (Decreto 1860 de 1994, art. 20) define los órganos del gobierno escolar y fija una regla para los representantes de los órganos colegiados: se eligen para períodos anuales, continúan ejerciendo hasta ser reemplazados y, en caso de vacancia, se elige su reemplazo para el resto del período. La propuesta de los docentes suena razonable, pero cambiaría el calendario del gobierno escolar. Recuerde las tres reglas: período anual, continuidad hasta el reemplazo y reemplazo por el resto del período.",
     "Decreto 1075 de 2015, art. 2.3.3.1.5.3.",
     "Vacancia en un órgano colegiado: se elige reemplazo para el resto del período, no para un período nuevo.",
     [(D1075, "En caso de vacancia, se elegirá su reemplazo para el resto del período.", "Decreto 1075, art. 2.3.3.1.5.3"),
      (D1075, "Los representantes de los órganos colegiados serán elegidos para períodos anuales, pero continuarán ejerciendo sus funciones hasta cuando sean reemplazados.", "Decreto 1075, art. 2.3.3.1.5.3")],
     "Gobierno escolar")

caso("CK23", "Sesión antes de las elecciones",
     "Es 5 de febrero. Las clases empezaron hace una semana y todavía no se han elegido los nuevos representantes al consejo directivo. "
     "El rector convoca una sesión extraordinaria para estudiar un traslado presupuestal urgente. "
     "El representante de los egresados elegido el año anterior le pregunta a usted si todavía debe asistir.")
item("CO053", "CK23", "GDI-GOB", 2,
     "La respuesta que usted le da al representante de los egresados es:",
     [("Sí, porque los representantes siguen ejerciendo sus funciones hasta que sean reemplazados, aunque su período anual haya terminado.",
       "Es correcta. El artículo 2.3.3.1.5.3 del Decreto 1075 dice que los representantes de los órganos colegiados continúan ejerciendo sus funciones hasta cuando sean reemplazados, lo que evita que el consejo quede incompleto entre un año y otro."),
      ("No, porque su período anual terminó y la sesión debe esperar a que se elijan los nuevos representantes del consejo directivo.",
       "Es incorrecta. Es cierto que el período es anual, pero la norma prevé la continuidad hasta el reemplazo; aplazar la sesión no es necesario y podría afectar una decisión presupuestal urgente."),
      ("No, porque mientras no haya elecciones el rector puede designar un representante provisional de los egresados en el consejo.",
       "Es incorrecta. El rector no designa a los representantes de los estamentos: ellos participan por medio de sus representantes elegidos, y quien fue elegido el año anterior continúa hasta que sea reemplazado.")],
     "A",
     "El artículo 2.3.3.1.5.3 del Decreto 1075 resuelve este caso: los representantes de los órganos colegiados se eligen para períodos anuales, pero continúan ejerciendo sus funciones hasta cuando sean reemplazados. Además, el artículo 2.3.3.1.5.1 dice que los miembros de la comunidad educativa, incluidos los egresados organizados para participar, intervienen en la dirección por medio de sus representantes en los órganos del gobierno escolar. Por eso el rector no puede nombrar uno provisional ni hace falta aplazar la sesión. La palabra clave es «hasta cuando sean reemplazados».",
     "Decreto 1075 de 2015, arts. 2.3.3.1.5.1 y 2.3.3.1.5.3.",
     "Los representantes continúan en sus funciones hasta que sean reemplazados: no hay vacío entre un año y otro.",
     [(D1075, "Los representantes de los órganos colegiados serán elegidos para períodos anuales, pero continuarán ejerciendo sus funciones hasta cuando sean reemplazados.", "Decreto 1075, art. 2.3.3.1.5.3"),
      (D1075, "lo harán por medio de sus representantes en los órganos del gobierno escolar", "Decreto 1075, art. 2.3.3.1.5.1")],
     "Gobierno escolar")

# ------------------------------------------------------------ GAC · SIEE y seguimiento
caso("CK24", "Reclamación por la no promoción",
     "Al cierre del año, la comisión de evaluación y promoción determinó que un estudiante de noveno no es promovido. "
     "La familia presentó la reclamación primero ante el docente y luego ante la comisión, como lo indica el sistema institucional de evaluación (SIEE), y las dos instancias mantuvieron la decisión. "
     "Ahora la familia acude a usted y pide que el caso pase a «la última instancia del colegio».")
item("CO054", "CK24", "GAC-SIEE", 3,
     "Según el Decreto 1075, la instancia del establecimiento que decide esta reclamación es",
     [("el consejo académico, porque es la instancia superior que participa en la orientación pedagógica del establecimiento.",
       "Es incorrecta. El consejo académico sí es la instancia superior en lo pedagógico y aprueba el SIEE, pero la norma no le asigna decidir las reclamaciones de evaluación o promoción: esa función es del consejo directivo."),
      ("el consejo directivo, porque la norma le asigna servir de instancia para decidir reclamaciones de evaluación o promoción.",
       "Es correcta. El artículo 2.3.3.3.3.11, numeral 7, del Decreto 1075 dice que el establecimiento, a través del consejo directivo, sirve de instancia para decidir sobre las reclamaciones de estudiantes o padres sobre evaluación o promoción."),
      ("la secretaría de educación, porque las dos instancias internas previstas en el SIEE ya mantuvieron la decisión.",
       "Es incorrecta. La secretaría tiene otras responsabilidades frente a la evaluación, pero antes de ella hay una instancia interna que el decreto señala de forma expresa para decidir estas reclamaciones: el consejo directivo.")],
     "B",
     "El SIEE debe definir las instancias, procedimientos y mecanismos de atención y resolución de reclamaciones (art. 2.3.3.3.3.4, numeral 10), y la familia ya los siguió. Pero el artículo 2.3.3.3.3.11, numeral 7, del Decreto 1075 fija que el establecimiento, a través del consejo directivo, sirve de instancia para decidir sobre las reclamaciones de estudiantes o padres sobre evaluación o promoción. El distractor más fuerte es el consejo académico, porque es la instancia pedagógica superior; la CNSC pregunta justamente por esa diferencia. Recuerde: el académico orienta y aprueba el SIEE; el directivo decide las reclamaciones.",
     "Decreto 1075 de 2015, arts. 2.3.3.3.3.4 (num. 10) y 2.3.3.3.3.11 (num. 7).",
     "Reclamaciones sobre evaluación o promoción: después de las instancias del SIEE, decide el consejo directivo.",
     [(D1075, "7. A través de consejo directivo servir de instancia para decidir sobre reclamaciones que presenten los estudiantes o sus padres de familia en relación con la evaluación o promoción.", "Decreto 1075, art. 2.3.3.3.3.11"),
      (D1075, "10. Las instancias, procedimientos y mecanismos de atención y resolución de reclamaciones de padres de familia y estudiantes sobre la evaluación y promoción.", "Decreto 1075, art. 2.3.3.3.3.4")],
     "SIEE y promoción")

caso("CK25", "Informes del primer periodo",
     "Al cerrar el primer periodo, el 38 % de los estudiantes de séptimo tiene desempeño bajo en matemáticas, frente al 12 % en los demás grados de la básica secundaria. "
     "Los docentes de séptimo atribuyen el resultado a la «falta de interés» de los estudiantes y proponen esperar al segundo periodo.")
item("CO055", "CK25", "GAC-SEGUIM", 2,
     "De acuerdo con las responsabilidades del establecimiento frente a la evaluación, la acción que usted orienta primero es",
     [("analizar los informes con los docentes de séptimo para identificar prácticas escolares que puedan estar afectando el desempeño y ajustarlas.",
       "Es correcta. El numeral 8 del artículo 2.3.3.3.3.11 del Decreto 1075 pide analizar periódicamente los informes de evaluación para identificar prácticas escolares que puedan afectar el desempeño e introducir las modificaciones necesarias."),
      ("citar a las familias de séptimo para que firmen compromisos académicos, porque el bajo interés de los estudiantes depende sobre todo del hogar.",
       "Es incorrecta. La interlocución con las familias y los compromisos son responsabilidades válidas, pero empezar por ahí acepta sin análisis la explicación de los docentes y deja de lado las prácticas escolares, que es lo que la norma pide revisar."),
      ("programar actividades de recuperación al final del año escolar, para que los estudiantes superen el desempeño bajo antes de la promoción.",
       "Es incorrecta. Las actividades de apoyo hacen parte del SIEE, pero dejarlas para el cierre del año contradice el seguimiento periódico; con una diferencia tan marcada entre grados, primero hay que analizar qué está pasando en el aula.")],
     "A",
     "El artículo 2.3.3.3.3.11 del Decreto 1075 enumera las responsabilidades del establecimiento frente a la evaluación. El numeral 8 pide analizar periódicamente los informes de evaluación con el fin de identificar prácticas escolares que puedan estar afectando el desempeño de los estudiantes e introducir las modificaciones necesarias. Una diferencia de 38 % frente a 12 % entre grados es una alerta institucional, no solo un problema de interés individual. Las otras opciones son acciones válidas en otro momento, pero no responden a lo que pide el enunciado: la acción que va primero.",
     "Decreto 1075 de 2015, art. 2.3.3.3.3.11, numerales 3, 4 y 8.",
     "Con resultados atípicos, primero se analizan los informes para revisar las prácticas escolares; después vienen compromisos y apoyos.",
     [(D1075, "8. Analizar periódicamente los informes de evaluación con el fin de identificar prácticas escolares que puedan estar afectando el desempeño de los estudiantes, e introducir las modificaciones que sean necesarias para mejorar.", "Decreto 1075, art. 2.3.3.3.3.11")],
     "Seguimiento académico")

# ------------------------------------------------------------ GAF · Fondo de Servicios Educativos
caso("CK26", "Propuestas para el presupuesto",
     "En la preparación del presupuesto del Fondo de Servicios Educativos, el consejo académico le entrega a usted tres propuestas para que las presente al rector: "
     "un curso preparatorio para las pruebas Saber 11 dictado por una empresa externa; la contratación del servicio de aseo de la sede, porque la persona de planta se pensionó; "
     "y la inscripción de un equipo de estudiantes en las olimpiadas regionales de robótica.")
item("CO056", "CK26", "GAF-FONDOS", 3,
     "Con base en las normas del Fondo de Servicios Educativos, usted le informa al consejo académico que puede financiarse",
     [("el curso preparatorio Saber 11, siempre que guarde relación con el PEI y lo apruebe el consejo directivo.",
       "Es incorrecta. Aunque guarde relación con el PEI y lo apruebe el consejo directivo, el decreto prohíbe de forma expresa al ordenador del gasto financiar cursos preparatorios del examen del ICFES con recursos del Fondo."),
      ("la contratación del aseo, porque el Fondo puede cubrir elementos de aseo para el funcionamiento de la sede.",
       "Es incorrecta. El Fondo sí puede comprar elementos de aseo como bienes de consumo final, pero contratar el servicio de aseo y vigilancia del establecimiento está prohibido; la trampa es confundir los insumos con el servicio."),
      ("la inscripción en las olimpiadas, previa aprobación del consejo directivo, porque es una competencia científica.",
       "Es correcta. El numeral 13 del artículo 2.3.1.6.3.11 permite financiar la inscripción y participación de los educandos en competencias científicas de orden regional, previa aprobación del consejo directivo.")],
     "C",
     "Los recursos del Fondo de Servicios Educativos solo pueden usarse en los conceptos del artículo 2.3.1.6.3.11 del Decreto 1075, que guarden estricta relación con el PEI; el numeral 13 incluye la inscripción y participación de los educandos en competencias científicas regionales, previa aprobación del consejo directivo. El artículo 2.3.1.6.3.13 prohíbe al ordenador del gasto contratar servicios de aseo y vigilancia y financiar cursos preparatorios del examen del ICFES. Las dos trampas son cercanas: el aseo (se compran elementos, no se contrata el servicio) y el preicfes (la aprobación del consejo no levanta una prohibición).",
     "Decreto 1075 de 2015, arts. 2.3.1.6.3.11 (num. 4 y 13) y 2.3.1.6.3.13 (num. 3 y 5).",
     "FSE: sí competencias de estudiantes con aprobación del consejo directivo; no preicfes ni contrato de aseo y vigilancia.",
     [(D1075, "13. Inscripción y participación de los educandos en competencias deportivas, culturales, pedagógicas y científicas de orden local, regional, nacional o internacional, previa aprobación del consejo directivo.", "Decreto 1075, art. 2.3.1.6.3.11"),
      (D1075, "3. Contratar servicios de aseo y vigilancia del establecimiento educativo.", "Decreto 1075, art. 2.3.1.6.3.13"),
      (D1075, "5. Financiar cursos preparatorios del examen del ICFES, entre otros que defina el Ministerio de Educación Nacional.", "Decreto 1075, art. 2.3.1.6.3.13")],
     "Fondo de Servicios Educativos")

# ------------------------------------------------------------ GCO · familias e inclusión (estilo ascenso 2024)
caso("CK27", "El manual se ajusta sin las familias",
     "El comité escolar de convivencia está revisando el manual de convivencia. En la sede de primaria, a las dos reuniones convocadas asistieron menos de diez familias; "
     "muchas trabajan por turnos en fincas y en el comercio. Algunos docentes proponen terminar el ajuste sin ellas «porque ya se les invitó dos veces».")
item("CO057", "CK27", "GCO-COMUN", 2,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("enviar el borrador del manual por los grupos de mensajería de cada curso y dar una semana para que las familias manden comentarios.",
       "Es incorrecta (nivel satisfactorio). Abre un canal más y da un plazo, pero se queda en una consulta escrita que muchas familias no podrán leer ni discutir, y no pasa por las instancias de participación definidas en el PEI."),
      ("terminar el ajuste con el comité y los docentes y luego citar a las familias para explicarles las obligaciones que asumen con el manual.",
       "Es incorrecta (nivel inferior). Las familias deben cumplir el manual, pero la Ley 1620 también les asigna participar en su revisión y ajuste; informarles al final las convierte en receptoras y no en participantes."),
      ("acordar con el consejo de padres encuentros por sede en horarios accesibles para recoger aportes y contarles cómo se incorporaron.",
       "Es correcta (nivel avanzado). Usa una instancia de participación del PEI, adapta horarios y lugares a la realidad de las familias y devuelve información sobre cómo se tuvieron en cuenta sus aportes.")],
     "C",
     "El artículo 22 de la Ley 1620 dice que la familia deberá participar en la revisión y ajuste del manual de convivencia a través de las instancias de participación definidas en el PEI. Si las familias no llegan, el reto del coordinador es crear condiciones para que participen. En la prueba de ascenso, el nivel avanzado reconoce el contexto (turnos de trabajo, sedes alejadas), usa las instancias del PEI y cierra el ciclo contando cómo se incorporaron los aportes. Consultar por mensajes es satisfactorio; informar al final es inferior.",
     "Ley 1620 de 2013, art. 22, numeral 4; Guía orientadora de la prueba de ascenso para coordinador (2024).",
     "Manual de convivencia: las familias participan en su revisión por las instancias del PEI; el coordinador crea las condiciones.",
     [(L1620, "4. Participar en la revisión y ajuste del manual de convivencia a través de las instancias de participación definidas en el proyecto educativo institucional del establecimiento educativo.", "Ley 1620, art. 22")],
     "Familias y entorno", "ascenso 2024")

caso("CK28", "Informe de fin de año",
     "Termina el año escolar. Una estudiante de quinto grado con discapacidad intelectual tiene en su PIAR ajustes particulares en la evaluación de los aprendizajes. "
     "La docente de aula le pregunta a usted qué debe entregar a la familia, y el docente de apoyo propone redactar él solo un informe aparte «para no mezclarlo con el boletín».")
item("CO058", "CK28", "GCO-INCL", 3,
     "La orientación del coordinador que corresponde al nivel avanzado es",
     [("que la estudiante reciba el mismo boletín que sus compañeros, sin anexos, para darle un trato igual y evitar así cualquier forma de discriminación.",
       "Es incorrecta (nivel mínimo). Es cierto que recibe los mismos informes que todos, pero como su PIAR tiene ajustes en la evaluación, la norma exige además un anexo con el informe anual de competencias; omitirlo afecta la continuidad de sus apoyos."),
      ("que la docente de aula, con el docente de apoyo, elabore el informe anual de competencias como anexo del boletín final y de su historia escolar.",
       "Es correcta (nivel avanzado). Así lo dispone el artículo 2.3.3.5.2.3.7: el anexo lo elabora el docente de aula en coordinación con el docente de apoyo, hace parte del boletín final y de la historia escolar y sirve para el PIAR del año siguiente."),
      ("que el docente de apoyo redacte el informe aparte y lo entregue solo a la familia, porque la información de la estudiante es confidencial.",
       "Es incorrecta (nivel inferior). La historia escolar sí es confidencial, pero el informe no es un documento aparte del docente de apoyo: lo elabora el docente de aula con él y debe quedar en el boletín y en la historia escolar.")],
     "B",
     "El artículo 2.3.3.5.2.3.7 del Decreto 1075 (Decreto 1421 de 2017) dice que los estudiantes con discapacidad reciben los mismos informes que todos y que, si su PIAR tiene ajustes particulares en la evaluación, al finalizar el año se anexa un informe anual de competencias (en básica y media). Lo elabora el docente de aula en coordinación con el docente de apoyo, hace parte del boletín final y de la historia escolar, y se usa en la entrega pedagógica y para el PIAR siguiente. Las opciones incorrectas toman una verdad a medias: el trato igual o la confidencialidad.",
     "Decreto 1421 de 2017 (Decreto 1075, art. 2.3.3.5.2.3.7).",
     "PIAR con ajustes en la evaluación → informe anual de competencias anexo al boletín, hecho por el docente de aula con el de apoyo.",
     [(D1421, "Este anexo será elaborado por el docente de aula en coordinación con el docente de apoyo y demás docentes intervinientes y hará parte del boletín final de cada estudiante y de su historia escolar.", "Decreto 1421, art. 2.3.3.5.2.3.7"),
      (D1421, "Los estudiantes con discapacidad recibirán los mismos informes de seguimiento y retroalimentación que el establecimiento educativo fije en el sistema institucional de evaluación de todos los estudiantes.", "Decreto 1421, art. 2.3.3.5.2.3.7")],
     "Inclusión y ajustes razonables", "ascenso 2024")

# ------------------------------------------------------------ PSI · iniciativa
caso("CK29", "Ausencias intermitentes",
     "Al revisar los registros de asistencia, usted nota que cinco estudiantes de décimo de la jornada de la tarde han faltado de forma intermitente durante tres semanas. "
     "Ningún docente lo ha reportado, no hay situaciones de convivencia registradas y el periodo académico cierra en un mes.")
item("CO059", "CK29", "PSI-INIC", 2,
     "La actuación que mejor demuestra la competencia de iniciativa es",
     [("esperar el cierre del periodo para que la comisión de evaluación revise el caso con los informes de desempeño de los cinco estudiantes.",
       "Es incorrecta. La comisión es una instancia válida, pero esperar un mes deja crecer el problema; la iniciativa consiste en anticiparse antes de que las ausencias se conviertan en pérdida del periodo o en deserción."),
      ("proponer con los directores de grupo un contacto temprano con las familias para conocer las causas y acordar acciones antes del cierre.",
       "Es correcta. Se anticipa al problema, actúa con autonomía sin esperar un reporte y propone una alternativa concreta con los directores de grupo y las familias, que es como la guía de la CNSC define la iniciativa."),
      ("enviar una circular a todas las familias de la jornada que recuerde las normas de asistencia y las consecuencias previstas en el manual.",
       "Es incorrecta. Recordar la norma no es un error, pero es una respuesta general y reactiva: no averigua las causas de estos cinco casos ni propone una solución para ellos.")],
     "B",
     "La guía de orientación de la CNSC define la iniciativa como anticiparse a los problemas proponiendo alternativas de solución, y trabajar de forma proactiva y con autonomía frente a las responsabilidades. En el caso no hay un reporte ni una instancia que lo exija todavía, y por eso la opción correcta es la que actúa antes del cierre, busca las causas con los directores de grupo y propone acciones con las familias. Esperar a la comisión es reactivo, y la circular general cumple la forma pero no resuelve. En la prueba, busque la opción que anticipa y propone.",
     "Guía de orientación al aspirante CNSC 2022 (competencia Iniciativa); Resolución 3842 de 2022, 1.1.3.",
     "Iniciativa: anticiparse y proponer una solución concreta, sin esperar a que alguien reporte el problema.",
     [(GCNSC, "Anticiparse a los problemas proponiendo alternativas de solución.", "Guía de orientación CNSC 2022, competencia Iniciativa")],
     "Iniciativa")

lote = {"id": "coord-2026-11-18", "fecha": "2026-11-18", "cargo": "coordinador",
        "nota": "Lecturas K001 (Resolución 3842, presentación) y K003 (Decreto 1075, gobierno escolar). Formatos ingreso 2022 y ascenso 2024 (la correcta es la de nivel avanzado).",
        "casos": casos, "fichas": [], "items": items}
json.dump(lote, open(os.path.join(RAIZ, "data", "lotes", "coord-2026-11-18.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(casos), "casos ·", len(items), "ítems")
