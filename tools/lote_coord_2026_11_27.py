# -*- coding: utf-8 -*-
"""Sexto lote de coordinación (2026-11-27). Cubre la lectura K014 (Guía 34, 1.5 Más y mejores instancias de
participación: consejo directivo, rector, consejo de padres, asociación de padres) con cuatro ítems y completa la
lectura K011 (Guía 34, 1.3 La autonomía escolar y 1.4 Las nuevas formas de trabajo) con dos más. Rota GAC (SIEE y
seguimiento académico), GAF (Fondo de Servicios Educativos), GCO (situaciones tipo I, familias e inclusión) y PSI
(compromiso social e institucional). Formatos: ingreso 2022 (3 opciones, una correcta) y ascenso 2024 (cada opción es
un nivel de desempeño; la correcta es la de nivel avanzado). Genera data/lotes/coord-2026-11-27.json.
Citas: texto literal de fuentes/."""
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


G34, L715, D1075, R3842 = "guia34_mineducacion_2008", "ley_715_2001", "decreto_1075_2015", "resolucion_3842_2022_ocr"
L115, D1965, D1421, CNSC = "ley_115_1994", "decreto_1965_2013", "decreto_1421_2017", "guia_orientacion_cnsc_2022"
K014 = "Guía 34, 1.5 Más y mejores instancias de participación"
K011 = "Guía 34, 1.3 La autonomía escolar y 1.4 Las nuevas formas de trabajo"

# ------------------------------------------------------------ K014 · Guía 34, instancias de gobierno y participación
caso("CK52", "El bazar del sábado",
     "La junta de acción comunal del barrio le escribe a usted como coordinador para pedir el polideportivo y cuatro salones de la institución un sábado de "
     "octubre: quieren hacer un bazar cultural con grupos de danza de los estudiantes y una feria de emprendimientos de las familias. Un docente le dice que "
     "eso lo decide el consejo académico porque hay estudiantes presentándose, y otro opina que basta con que el rector firme el permiso.")
item("CO084", "CK52", "GDI-GOB", 2,
     "Para responder a la junta, usted le explica al rector que la instancia a la que corresponde fijar el procedimiento para prestar las instalaciones es",
     [("el consejo académico, porque las presentaciones de los estudiantes hacen parte de los proyectos pedagógicos del plan de estudios.",
       "Es incorrecta. El consejo académico organiza, orienta y mejora el plan de estudios y revisa el currículo; que participen estudiantes no convierte el préstamo de las instalaciones en un asunto curricular."),
      ("el consejo directivo, que establece el procedimiento para permitir el uso de las instalaciones en actividades de la comunidad.",
       "Es correcta. El Decreto 1075 asigna al consejo directivo establecer el procedimiento para permitir el uso de las instalaciones en actividades educativas, culturales, recreativas, deportivas y sociales, y la Guía 34 lo repite al describir sus funciones."),
      ("el rector, porque como responsable de administrar los recursos de la institución puede autorizar el préstamo de la planta física.",
       "Es incorrecta. El rector ejecuta las decisiones y administra, pero el procedimiento para prestar las instalaciones lo define el consejo directivo; el rector lo aplicaría si ese procedimiento ya existiera.")],
     "B",
     "La palabra clave es «procedimiento para prestar las instalaciones». La Guía 34, al describir las instancias de gobierno escolar, ubica en el consejo directivo las decisiones sobre el funcionamiento institucional, entre ellas definir el uso de las instalaciones para actividades educativas, culturales, recreativas, deportivas y sociales. El Decreto 1075 (art. 2.3.3.1.5.6, literal l) lo dice como función: establecer el procedimiento para permitir ese uso. El coordinador orienta al rector para que la solicitud se tramite ante el consejo directivo o con el procedimiento que este ya haya fijado. La CNSC suele poner como distractores las otras dos instancias que sí existen pero tienen otras funciones.",
     "Guía 34 MEN (2008), 1.5; Decreto 1075 de 2015, art. 2.3.3.1.5.6, literal l.",
     "Uso de las instalaciones por la comunidad: el procedimiento lo establece el consejo directivo.",
     [(G34, "definir el uso de las instalaciones para la realización de actividades educativas, culturales, recreativas, deportivas y sociales", K014),
      (D1075, "Establecer el procedimiento para permitir el uso de las instalaciones en la realización de actividades educativas, culturales, recreativas, deportivas y sociales de la respectiva comunidad educativa", "Decreto 1075, art. 2.3.3.1.5.6, literal l")],
     "Gobierno escolar")

caso("CK53", "Los resultados Saber llegan a la reunión",
     "Llegaron los resultados de las pruebas Saber 11 y bajaron en lectura crítica por segundo año. El rector le pide a usted que proponga con qué instancia de "
     "padres de familia trabajar el análisis de los resultados y la manera de darlos a conocer a todas las familias. La presidenta de la asociación de padres se "
     "ofrece a encargarse, y un docente sugiere convocar a la asamblea general de padres para presentarlos allí.")
item("CO085", "CK53", "GCO-COMUN", 3,
     "La instancia que usted propone para analizar los resultados con el rector y definir cómo difundirlos es",
     [("la asociación de padres, porque entre sus finalidades está apoyar a las familias en las acciones para mejorar los resultados de aprendizaje.",
       "Es incorrecta. Es un distractor muy cercano: la asociación sí apoya acciones para mejorar resultados, pero la función de contribuir con el rector en el análisis, difusión y uso de los resultados de las pruebas es del consejo de padres."),
      ("la asamblea general de padres, porque al reunir a todos los padres del establecimiento garantiza que la información llegue a cada familia.",
       "Es incorrecta. La asamblea puede ser un espacio para comunicar, pero no es la instancia a la que la norma le asigna analizar con el rector los resultados ni decidir su uso; sería útil solo como escenario de difusión."),
      ("el consejo de padres, al que le corresponde contribuir con el rector en el análisis, la difusión y el uso de los resultados de las pruebas.",
       "Es correcta. El Decreto 1075 asigna al consejo de padres contribuir con el rector en el análisis, difusión y uso de los resultados de las pruebas de Estado, y la Guía 34 lo incluye entre sus principales funciones, junto con los planes de mejoramiento.")],
     "C",
     "La clave está en el verbo: analizar con el rector y difundir. La Guía 34 diferencia las instancias de padres: el consejo de padres contribuye con el rector o director en el análisis, difusión y uso de los resultados de las pruebas SABER y el examen de Estado; la asociación apoya la ejecución del PEI y del plan de mejoramiento y promueve la formación de los padres; la asamblea general reúne a todos los padres. El Decreto 1075 (art. 2.3.4.7, literal a) confirma la función del consejo de padres. Cuando dos instancias «ayudan a mejorar los resultados», busque cuál tiene la función exacta que pide el enunciado.",
     "Guía 34 MEN (2008), 1.5; Decreto 1075 de 2015, arts. 2.3.4.7 y 2.3.4.10.",
     "Análisis y difusión de resultados Saber con el rector: consejo de padres. Asociación: apoyar PEI, plan de mejoramiento y formación de padres.",
     [(G34, "contribuir con el rector o director en el análisis, difusión y uso de los resultados de las pruebas SABER y el examen de Estado", K014),
      (D1075, "Contribuir con el rector o director en el análisis, difusión y uso de los resultados de las evaluaciones periódicas de competencias y las pruebas de Estado", "Decreto 1075, art. 2.3.4.7, literal a"),
      (D1075, "Apoyar a las familias y a los estudiantes en el desarrollo de las acciones necesarias para mejorar sus resultados de aprendizaje", "Decreto 1075, art. 2.3.4.10, literal d")],
     "Participación de las familias")

caso("CK54", "Tres cupos para el diplomado",
     "La secretaría de educación ofrece a la institución tres cupos en un diplomado sobre diseño universal para el aprendizaje. Seis docentes se inscriben y "
     "le piden a usted, como coordinador que acompaña su trabajo pedagógico, que decida quiénes van. Uno de ellos sugiere que el consejo académico lo vote.")
item("CO086", "CK54", "GAF-TALENTO", 2,
     "De acuerdo con la Ley 715, a quien corresponde proponer a los docentes que recibirán la capacitación es",
     [("a usted como coordinador, porque acompaña el trabajo pedagógico de los docentes y conoce de primera mano sus necesidades de formación.",
       "Es incorrecta. El coordinador sí conoce las necesidades y puede aportar información y criterios, pero la ley no le asigna proponer a los docentes que recibirán capacitación; esa función es del rector."),
      ("al rector, a quien la ley le asigna esa función; usted le aporta la información sobre las necesidades de formación de cada docente.",
       "Es correcta. La Ley 715 (art. 10.12) asigna al rector proponer a los docentes que serán apoyados para recibir capacitación, y la Guía 34 lo repite entre sus funciones; el coordinador apoya con información pedagógica para decidir bien."),
      ("al consejo académico, porque la formación de los docentes hace parte de la orientación pedagógica y del mejoramiento del plan de estudios.",
       "Es incorrecta. El consejo académico orienta el plan de estudios y puede identificar necesidades de formación, pero proponer quiénes reciben capacitación es una función expresa del rector según la Ley 715.")],
     "B",
     "La palabra clave es «proponer». La Ley 715 de 2001 (art. 10.12) incluye entre las funciones del rector proponer a los docentes que serán apoyados para recibir capacitación, y la Guía 34, al describir al rector como instancia de gobierno escolar, señala que debe proponer a los profesores que recibirán capacitación, además de dirigir el trabajo de los equipos docentes y administrar el talento humano. El coordinador no decide ni lo somete a votación: aporta al rector la información de las necesidades de formación y del plan de mejoramiento para que la propuesta sea pertinente. En la prueba, desconfíe de opciones en las que el coordinador asume funciones que la ley asigna al rector.",
     "Ley 715 de 2001, art. 10.12; Guía 34 MEN (2008), 1.5.",
     "Capacitación docente: la propone el rector (Ley 715, art. 10.12); el coordinador aporta información.",
     [(G34, "proponer a los profesores que recibirán capacitación", K014),
      (L715, "Proponer a los docentes que serán apoyados para recibir capacitación.", "Ley 715, art. 10.12")],
     "Talento humano")

caso("CK55", "El PEI de vacaciones",
     "Durante las vacaciones de diciembre, el rector y los dos coordinadores reescribieron el horizonte institucional y el modelo pedagógico del PEI. El documento "
     "quedó bien redactado. En la primera semana de enero, el rector le pide a usted como coordinador que prepare su presentación para «arrancar el año con el "
     "PEI nuevo». Docentes, estudiantes, familias, egresados y empresas de la zona no han participado en la revisión.")
item("CO087", "CK55", "GDI-PEI", 3,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("presentar el documento en la primera jornada pedagógica para que todos los docentes lo conozcan y lo apliquen desde el inicio del año.",
       "Es incorrecta (nivel mínimo). Socializa el documento, pero los demás estamentos siguen como receptores de un PEI terminado; conocer un texto no equivale a concertarlo ni a compartir sus pautas."),
      ("proponer al rector mesas con docentes, estudiantes, familias, egresados y sector productivo para revisar el borrador antes de adoptarlo.",
       "Es correcta (nivel avanzado). Convierte el borrador en punto de partida de una construcción concertada con todos los estamentos, que es lo que la Guía 34 busca con el gobierno escolar y lo que la Resolución 3842 pide al coordinador."),
      ("radicar el documento ante el consejo directivo para que lo adopte cuanto antes, ya que el equipo directivo es el responsable de formularlo.",
       "Es incorrecta (nivel inferior). Usa el órgano formal para saltarse la participación: el consejo directivo adoptaría un PEI que la comunidad no conoce, y la responsabilidad de liderarlo no autoriza a construirlo sin ella.")],
     "B",
     "La Guía 34 explica que el gobierno escolar existe para que el PEI sea concertado por directivos, docentes, padres de familia, estudiantes, egresados y representantes del sector productivo local, y para que las pautas curriculares, de evaluación y de convivencia sean conocidas y compartidas, lo que fortalece la identidad institucional. La Resolución 3842 le asigna al coordinador coordinar y participar en la formulación, revisión y actualización del PEI. En la prueba de ascenso, el nivel avanzado usa el trabajo previo como insumo y abre la participación antes de la adopción; informar (mínimo) o adoptar sin consulta (inferior) no alcanzan la concertación que pide la norma.",
     "Guía 34 MEN (2008), 1.5; Resolución 3842 de 2022, 1.3.1.",
     "PEI: se concierta con todos los estamentos antes de adoptarlo; un borrador directivo es punto de partida, no producto final.",
     [(G34, "Con lo anterior se busca que el PEI sea concertado por directivos, docentes, padres de familia, estudiantes, egresados y representantes del sector productivo local.", K014),
      (R3842, "Coordinar y participar en la formulación, revisión y actualización del Proyecto", "Resolución 3842, 1.3.1 Funciones del coordinador")],
     "PEI concertado", "ascenso 2024")

# ------------------------------------------------------------ K011 · Guía 34, autonomía escolar y nuevas formas de trabajo
caso("CK56", "Un énfasis en sistemas",
     "El consejo académico quiere darle a la media un énfasis en desarrollo de software. Para conseguir horas, un grupo propone suprimir Educación Artística en "
     "la básica secundaria y pasar esas horas a programación; otro grupo prefiere esperar a que la secretaría de educación apruebe el énfasis. El rector le pide "
     "a usted orientar la discusión con base en la autonomía escolar.")
item("CO088", "CK56", "GDI-AUTON", 3,
     "La orientación que corresponde a un uso responsable de la autonomía escolar es",
     [("suprimir Artística en la básica secundaria y trasladar sus horas a programación, porque el énfasis del PEI le da prioridad sobre otras áreas.",
       "Es incorrecta. La autonomía permite organizar el plan de estudios, pero alrededor de las áreas fundamentales que la ley define para cada nivel; eliminar una de ellas excede los límites de la Ley 115."),
      ("mantener las áreas fundamentales, introducir asignaturas optativas acordes con el énfasis y rendir cuentas a la comunidad sobre sus logros.",
       "Es correcta. La Guía 34 dice que la autonomía permite organizar el plan de estudios alrededor de las áreas fundamentales y de asignaturas optativas según el énfasis del PEI, y que debe complementarse con rendición de cuentas."),
      ("solicitar a la secretaría de educación que apruebe el énfasis antes de ajustar el plan, porque a ella le corresponde diseñar el currículo.",
       "Es incorrecta. Según la Ley 115, las secretarías asesoran el diseño y desarrollo del currículo de las instituciones estatales, pero no lo diseñan ni aprueban el énfasis: esa decisión es parte de la autonomía institucional.")],
     "B",
     "El caso pide dos pasos. Primero, los límites: la Guía 34 explica que la autonomía escolar permite organizar el plan de estudios alrededor de las áreas fundamentales determinadas para cada nivel y de asignaturas optativas en función del énfasis del PEI; la Ley 115 (art. 77) la ejerce dentro de los límites de la ley, y deja a las secretarías la asesoría del currículo. Segundo, la responsabilidad: la Guía 34 agrega que la autonomía debe complementarse con una apropiada rendición de cuentas sobre los logros. Suprimir un área fundamental desborda la autonomía y esperar una aprobación la desconoce. La CNSC premia la opción que ejerce la autonomía dentro de la ley y con rendición de cuentas.",
     "Guía 34 MEN (2008), 1.3 La autonomía escolar; Ley 115 de 1994, art. 77.",
     "Autonomía: plan de estudios alrededor de las áreas fundamentales + optativas según el énfasis; siempre con rendición de cuentas.",
     [(G34, "organizar su plan de estudios alrededor de las áreas fundamentales determinadas para cada nivel, de las asignaturas optativas en función del énfasis de su PEI", K011),
      (G34, "Este ejercicio de autonomía debe ser complementado con una apropiada rendición de cuentas acerca de los logros obtenidos.", K011),
      (L115, "las instituciones de educación formal gozan de autonomía para organizar las áreas fundamentales de conocimientos definidas para cada nivel, introducir asignaturas optativas dentro de las áreas establecidas en la ley", "Ley 115, art. 77")],
     "Autonomía escolar")

caso("CK57", "Se enteraron por el grupo de WhatsApp",
     "El consejo académico aprobó mover la hora de lectura al inicio de la jornada, porque los registros muestran que la mayoría de los retardos se concentran en "
     "la primera hora. Los docentes de la jornada de la tarde se enteraron por un mensaje reenviado en un grupo de WhatsApp y le reclaman a usted como "
     "coordinador que «nadie les preguntó» y que el cambio les desordena las clases de la primera hora.")
item("CO089", "CK57", "GDI-ROL", 2,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("enviar una circular con la decisión, su fecha de inicio y sus razones, y pedir a los docentes que hagan llegar sus dudas por escrito.",
       "Es incorrecta (nivel mínimo). Ordena la información y la hace formal, pero la comunicación sigue en una sola dirección: no escucha las razones de los docentes ni construye con ellos el ajuste."),
      ("recordarles que la decisión fue aprobada por el consejo académico, que los representa, y que todos los docentes deben aplicarla.",
       "Es incorrecta (nivel inferior). Se apoya en la legalidad de la decisión y cierra el diálogo; desconoce que la comunicación implica escuchar de manera genuina y que el compromiso con una tarea depende de su legitimidad."),
      ("reunirse con los docentes de la tarde, escuchar sus objeciones, mostrar los datos de retardos y acordar con ellos los ajustes necesarios.",
       "Es correcta (nivel avanzado). Escucha de manera genuina, usa los datos como brújula para explicar la decisión y construye acuerdos, lo que da legitimidad al cambio y compromete a los docentes con su aplicación.")],
     "C",
     "La Guía 34 describe las nuevas formas de trabajo de los establecimientos: la comunicación no se limita a hablar, implica escuchar de manera genuina a los compañeros y transmitir las ideas de manera comprensible y oportuna; los consensos dan legitimidad a las decisiones y generan compromiso; y los datos e información pertinente funcionan como «brújulas» que orientan las decisiones. El nivel avanzado combina las tres cosas: escucha, muestra la evidencia de los retardos y acuerda ajustes. Informar por escrito (mínimo) o imponer la decisión (inferior) dejan intacto el problema de comunicación que el caso revela.",
     "Guía 34 MEN (2008), 1.4 Las nuevas formas de trabajo en los establecimientos educativos.",
     "Comunicación directiva: escuchar de verdad, explicar con datos y concertar; el consenso da legitimidad y compromiso.",
     [(G34, "Implica escuchar de manera genuina a los compañeros y a las personas a las que sirve el establecimiento educativo", K011),
      (G34, "Estos consensos, a su vez, darán mayor legitimidad a las decisiones y permitirán un alto nivel de compromiso con las tareas que cada persona desarrollará.", K011),
      (G34, "La comunicación y el trabajo en equipo se facilitan cuando se utilizan sistemáticamente datos e información pertinente", K011)],
     "Comunicación y trabajo en equipo", "ascenso 2024")

# ------------------------------------------------------------ GAC · SIEE y seguimiento académico
caso("CK58", "«Se los digo al final del periodo»",
     "A mitad del primer periodo, los estudiantes de décimo le cuentan a usted que la docente de química no les ha explicado cómo los va a evaluar: cuando "
     "preguntan, ella responde que «los criterios se los digo al final del periodo». Dos acudientes llaman a coordinación porque tampoco los conocen. El SIEE "
     "de la institución fue aprobado y publicado en enero.")
item("CO090", "CK58", "GAC-SIEE", 2,
     "Según el Decreto 1075, lo que usted orienta como coordinador es",
     [("respetar la libertad de cátedra de la docente para decidir cuándo informa los criterios, siempre que lo haga antes del cierre del periodo.",
       "Es incorrecta. La libertad para escoger métodos no incluye ocultar los criterios de evaluación: la norma reconoce a estudiantes y padres el derecho a conocerlos desde el inicio del año escolar."),
      ("pedir a la docente que dé a conocer ya a estudiantes y familias los criterios e instrumentos con que evaluará, conforme al SIEE.",
       "Es correcta. El Decreto 1075 reconoce a estudiantes y padres el derecho a conocer el SIEE —criterios, procedimientos e instrumentos de evaluación y promoción— desde el inicio del año; el coordinador debe garantizarlo ya."),
      ("remitir la queja al consejo directivo para que modifique el SIEE y fije una fecha obligatoria en la que se informen los criterios.",
       "Es incorrecta. El SIEE ya existe y fue publicado; el problema es que no se está aplicando. Modificarlo sería un trámite largo e innecesario que no resuelve a tiempo el derecho vulnerado.")],
     "B",
     "La palabra clave es «desde el inicio». El Decreto 1075 (arts. 2.3.3.3.3.12 y 2.3.3.3.3.14, que compilan el Decreto 1290) reconoce tanto al estudiante como a los padres de familia el derecho a conocer el sistema institucional de evaluación: criterios, procedimientos e instrumentos de evaluación y promoción desde el inicio del año escolar. Si un docente reserva los criterios para el final del periodo, vulnera ese derecho aunque el SIEE esté publicado. El coordinador, que hace seguimiento a las actividades académicas, interviene de inmediato con la docente; no necesita reformar el SIEE, sino hacerlo cumplir. Libertad de método no significa evaluación sin reglas conocidas.",
     "Decreto 1075 de 2015, arts. 2.3.3.3.3.12 y 2.3.3.3.3.14 (Decreto 1290 de 2009, arts. 12 y 14).",
     "Estudiantes y padres tienen derecho a conocer criterios, procedimientos e instrumentos de evaluación desde el inicio del año.",
     [(D1075, "Conocer el sistema institucional de evaluación de los estudiantes: criterios, procedimientos e instrumentos de evaluación y promoción desde el inicio de año escolar.", "Decreto 1075, arts. 2.3.3.3.3.12 y 2.3.3.3.3.14")],
     "SIEE: derechos de estudiantes y padres")

caso("CK59", "Noveno B en alerta",
     "Al cerrar el primer periodo, usted encuentra que en noveno B catorce estudiantes tienen desempeño bajo en tres o más áreas y que las inasistencias del "
     "grupo aumentaron en marzo. Los docentes del grado comentan en la sala de profesores que «es un grupo difícil», y varias familias no han vuelto a la "
     "institución desde la matrícula.")
item("CO091", "CK59", "GAC-SEGUIM", 2,
     "La propuesta del coordinador que corresponde al nivel avanzado es",
     [("reunir a los docentes del grado para analizar los casos y acordar, con ellos y con las familias, acciones pedagógicas comunes con seguimiento.",
       "Es correcta (nivel avanzado). Promueve el seguimiento al desempeño de los estudiantes con acciones pedagógicas colaborativas en las que participan docentes y familias, como pide la Resolución 3842, y deja previsto cómo revisar su efecto."),
      ("enviar a cada docente la lista de los estudiantes en riesgo y pedirle que diseñe actividades de refuerzo en su propia área durante el periodo.",
       "Es incorrecta (nivel satisfactorio). Activa el seguimiento y pide apoyos, pero cada docente actúa por separado y las familias quedan por fuera; la norma pide acciones colaborativas entre docentes y familias."),
      ("citar a los acudientes de los catorce estudiantes para informarles los resultados y hacerles firmar compromisos académicos individuales.",
       "Es incorrecta (nivel mínimo). Involucra a las familias, pero solo para informar y trasladarles la responsabilidad; no hay análisis con los docentes ni acciones pedagógicas de la institución.")],
     "A",
     "La Resolución 3842 asigna al coordinador promover acciones de seguimiento al desempeño académico y disciplinario de los estudiantes que generen acciones pedagógicas colaborativas en favor de los estudiantes, con participación de docentes y familias. En la prueba de ascenso, el nivel avanzado reúne esas tres condiciones: analiza los casos con el equipo del grado, acuerda acciones comunes (no cada docente por su lado) e integra a las familias, con un seguimiento previsto. Pedir refuerzos por área es un nivel intermedio y citar acudientes solo para firmar compromisos es un nivel mínimo, porque traslada el problema sin acción pedagógica institucional.",
     "Resolución 3842 de 2022, 1.3.1, función 11.",
     "Seguimiento académico avanzado: análisis con el equipo del grado + acciones colaborativas con docentes y familias + revisión.",
     [(R3842, "Promover acciones de seguimiento al desempeño académico y disciplinario de los estudiantes, que generen acciones pedagógicas colaborativas en favor de los estudiantes, donde participen docentes y familias.", "Resolución 3842, 1.3.1, función 11")],
     "Seguimiento académico", "ascenso 2024")

# ------------------------------------------------------------ GAF · Fondo de Servicios Educativos
caso("CK60", "Marzo sin audiencia",
     "Es 15 de marzo. En reunión del consejo de padres preguntan por los ingresos del bazar y por una donación en dinero que una empresa hizo a la institución. "
     "Usted revisa y encuentra que el rector aún no ha convocado la audiencia pública de rendición de cuentas y que la relación de contratos de la vigencia se "
     "publicó una sola vez, en diciembre. El rector le pide su opinión antes de responderles.")
item("CO092", "CK60", "GAF-FONDOS", 3,
     "De acuerdo con el Decreto 1075, lo que usted le advierte al rector es que",
     [("la audiencia pública con la comunidad debía hacerse a más tardar el último día de febrero, y la relación de contratos debe publicarse cada mes.",
       "Es correcta. El artículo 2.3.1.6.3.19 ordena publicar mensualmente la relación de contratos y celebrar, a más tardar el último día de febrero, audiencia pública con informe financiero que incluya ingresos por donaciones."),
      ("la rendición de cuentas se cumple con el informe semestral al consejo directivo, en el que basta con incluir los ingresos de la donación.",
       "Es incorrecta. El informe al consejo directivo existe (Ley 715, art. 10.15), pero no reemplaza la audiencia pública ante la comunidad educativa ni la publicación mensual de contratos que exige el Decreto 1075."),
      ("basta con publicar en la cartelera los estados contables al cierre de la vigencia, porque la audiencia pública es solo para sedes rurales.",
       "Es incorrecta. Publicar los estados contables es una de las obligaciones, no la única; además, la norma exige la audiencia pública a todos los rectores que manejan el Fondo, sin exceptuar a ninguna sede.")],
     "A",
     "El caso combina dos obligaciones del artículo 2.3.1.6.3.19 del Decreto 1075 (Decreto 4791 de 2008), que buscan la moralidad, publicidad y transparencia del Fondo de Servicios Educativos. Primera: publicar mensualmente, en lugar visible, la relación de contratos y convenios con contratista, objeto, valor, plazo y estado. Segunda: a más tardar el último día de febrero, y previa convocatoria a la comunidad educativa, celebrar audiencia pública para presentar el informe de gestión, incluidos los ingresos por donaciones. A 15 de marzo, ambas están incumplidas. El informe semestral al consejo directivo es otra obligación distinta, por eso es un distractor cercano.",
     "Decreto 1075 de 2015, art. 2.3.1.6.3.19 (Decreto 4791 de 2008, art. 19).",
     "FSE: contratos publicados cada mes; audiencia pública de rendición de cuentas a más tardar el último día de febrero.",
     [(D1075, "Publicar mensualmente en lugar visible y de fácil acceso la relación de los contratos y convenios celebrados durante el período transcurrido de la vigencia", "Decreto 1075, art. 2.3.1.6.3.19, num. 3"),
      (D1075, "A más tardar el último día de febrero de cada año y previa convocatoria a la comunidad educativa, celebrar audiencia pública para presentar informe de la gestión realizada con explicación de la información financiera correspondiente, incluyendo los ingresos obtenidos por convenios con particulares, premios, donaciones u otros", "Decreto 1075, art. 2.3.1.6.3.19, num. 4")],
     "Fondo de Servicios Educativos")

# ------------------------------------------------------------ GCO · convivencia e inclusión
caso("CK61", "Empujones en la fila del restaurante",
     "Dos estudiantes de sexto discuten por un puesto en la fila del restaurante escolar y se empujan; nadie resulta lastimado y es la primera vez que tienen un "
     "problema. El docente de turno quiere remitirlos al comité escolar de convivencia y pedir que los suspendan. La institución tiene estudiantes mediadores "
     "capacitados y el manual de convivencia prevé su participación.")
item("CO093", "CK61", "GCO-CONV", 3,
     "De acuerdo con el Decreto 1965, lo que usted como coordinador orienta es",
     [("remitir el caso al comité escolar de convivencia para que defina las medidas, porque todo empujón entre estudiantes es agresión escolar.",
       "Es incorrecta. Una agresión es tipo II si es repetida o causa daño; un conflicto esporádico sin daño es tipo I y lo atiende el establecimiento con mediación pedagógica, sin necesidad de llevarlo al comité."),
      ("informar de inmediato a los acudientes y remitir a ambos a valoración en salud, dejando constancia de cada una de las actuaciones.",
       "Es incorrecta. Aplica pasos del protocolo de las situaciones tipo II, previstos para casos con daño al cuerpo o a la salud; aquí no hubo lesiones y la situación es esporádica, es decir, tipo I."),
      ("reunir de inmediato a los dos estudiantes y mediar, con apoyo de los mediadores, para que acuerden cómo reparar, y hacer seguimiento.",
       "Es correcta. Es el protocolo tipo I del artículo 42: reunir inmediatamente a las partes, mediar de manera pedagógica, fijar la solución dejando constancia y hacer seguimiento; los mediadores capacitados pueden participar según el manual.")],
     "C",
     "Primero se clasifica: el Decreto 1965 (art. 40) define las situaciones tipo I como conflictos manejados inadecuadamente y situaciones esporádicas que en ningún caso generan daños al cuerpo o a la salud. Un empujón aislado, sin lesiones, encaja ahí. Luego se aplica el protocolo del artículo 42: reunir inmediatamente a las partes, mediar de manera pedagógica para buscar la reparación y la reconciliación, fijar la solución dejando constancia y hacer seguimiento a los compromisos. El parágrafo permite que participen estudiantes mediadores capacitados, según el manual. Remitir al comité o aplicar pasos del tipo II sobredimensiona la situación; la CNSC espera que clasifique antes de actuar.",
     "Decreto 1965 de 2013, arts. 40 y 42.",
     "Tipo I (esporádica, sin daño): reunir de inmediato, mediar pedagógicamente, dejar constancia y hacer seguimiento; pueden apoyar mediadores.",
     [(D1965, "Corresponden a este tipo los conflictos manejados inadecuadamente y aquellas situaciones esporádicas que inciden negativamente en el clima escolar, y que en ningún caso generan daños al cuerpo o a la salud.", "Decreto 1965, art. 40, num. 1"),
      (D1965, "Reunir inmediatamente a las partes involucradas en el conflicto y mediar de manera pedagógica para que éstas expongan sus puntos de vista y busquen la reparación de los daños causados", "Decreto 1965, art. 42, num. 1"),
      (D1965, "Los estudiantes que hayan sido capacitados como mediadores o conciliadores escolares podrán participar en el manejo de estos casos en los términos fijados en el Manual de Convivencia.", "Decreto 1965, art. 42, parágrafo")],
     "Situaciones tipo I")

caso("CK62", "Las familias que no vuelven",
     "La institución atiende a nueve estudiantes con discapacidad. Sus familias asistieron en febrero a firmar el PIAR y las actas de acuerdo, pero después casi "
     "no han regresado. Dos madres le cuentan a usted que en las reuniones de padres «nos miran raro» y que no saben a quién acudir cuando tienen dudas sobre "
     "los apoyos. La docente orientadora está dispuesta a trabajar con usted en una propuesta.")
item("CO094", "CK62", "GCO-INCL", 2,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("enviar una circular recordando a las familias que la norma las obliga a participar y a cumplir los compromisos firmados en el PIAR.",
       "Es incorrecta (nivel inferior). Las obligaciones de las familias existen, pero usarlas como reclamo ignora las barreras que las madres describen y no crea ninguna estrategia institucional de participación."),
      ("programar una reunión trimestral con estas familias para informarles los avances de sus hijos y darles recomendaciones para la casa.",
       "Es incorrecta (nivel satisfactorio). Abre un espacio de contacto periódico, pero las familias siguen como receptoras de información; no se reconocen sus saberes ni se promueve su incidencia en las decisiones."),
      ("crear con la orientadora una red de familias inclusivas, usar la escuela de familias y abrirles espacio en las instancias.",
       "Es correcta (nivel avanzado). Aplica las estrategias que el Decreto 1075 propone para promover la participación de las familias: redes de familias inclusivas, escuela de familias y participación en las instancias escolares para incidir en decisiones.")],
     "C",
     "El Decreto 1075 (art. 2.3.3.5.2.3.11, Decreto 1421) reconoce a las familias como corresponsables y ordena a los establecimientos valorar sus prácticas y saberes y desarrollar estrategias para promover su participación, entre ellas la conformación de redes de familias inclusivas, el aprovechamiento de la escuela de familias para una comunidad más incluyente y la participación en las instancias escolares para incidir en la toma de decisiones. El nivel avanzado responde a la barrera que describen las madres y construye participación real; informar cada trimestre es un nivel intermedio y recordarles sus obligaciones es un nivel inferior, porque pone el problema solo en las familias.",
     "Decreto 1075 de 2015, art. 2.3.3.5.2.3.11 (Decreto 1421 de 2017).",
     "Familias de estudiantes con discapacidad: redes de familias inclusivas, escuela de familias y participación en instancias escolares.",
     [(D1421, "la conformación de redes de familias inclusivas, ii) el aprovechamiento de la escuela de familias para fortalecer una comunidad educativa cada vez más incluyente", "Decreto 1421, art. 2.3.3.5.2.3.11"),
      (D1421, "la participación en los espacios e instancias escolares para incidir en la toma de decisiones.", "Decreto 1421, art. 2.3.3.5.2.3.11")],
     "Inclusión y familias", "ascenso 2024")

# ------------------------------------------------------------ PSI · compromiso social e institucional
caso("CK63", "Dos compromisos el mismo sábado",
     "Usted asumió desde hace un mes la organización de la jornada de matrícula extendida del sábado en la sede rural, pensada para las familias que entre "
     "semana trabajan en las fincas. El miércoles, un instituto privado le ofrece dictar ese mismo sábado un taller pagado, bien remunerado, para docentes de "
     "otros municipios. El instituto no puede cambiar la fecha.")
item("CO095", "CK63", "PSI-COMP", 2,
     "La actuación que mejor demuestra la competencia de compromiso social e institucional es",
     [("pedir al rector que traslade la jornada de matrícula a otro sábado, explicando que la nueva fecha también puede servir a las familias.",
       "Es incorrecta. Parece una salida negociada, pero acomoda una actividad institucional ya comprometida con las familias a su conveniencia personal, y puede dejar sin matrícula a quienes ya habían organizado su sábado."),
      ("delegar la jornada en un docente de la sede con las instrucciones por escrito y aceptar el taller, ya que se trata de un día no laboral.",
       "Es incorrecta. Que sea sábado no cambia la responsabilidad que asumió: delegar a última hora para atender un interés personal antepone este al institucional y arriesga la calidad de la atención a las familias."),
      ("cumplir con la jornada de matrícula que asumió y declinar el taller, aunque pierda el pago, explicándole al instituto el motivo.",
       "Es correcta. Asume con ética y profesionalismo la responsabilidad que adquirió y antepone el interés institucional y de las familias al beneficio personal, que es la definición de la competencia de compromiso social e institucional.")],
     "C",
     "La guía de orientación al aspirante de la CNSC define el compromiso social e institucional como la habilidad para asumir responsabilidades con ética y profesionalismo, dentro y fuera del establecimiento, anteponiendo los intereses institucionales a los personales e identificándose con los valores, principios y políticas institucionales. La Resolución 3842 la incluye entre las competencias comportamentales del directivo docente. En el caso, la jornada atiende a familias rurales que solo pueden ir ese día; cambiarla o delegarla para aceptar un ingreso personal invierte el orden de prioridades. En la prueba psicotécnica, la opción correcta suele ser la que honra el compromiso asumido aunque tenga un costo personal.",
     "Guía de orientación al aspirante CNSC (2022), prueba psicotécnica; Resolución 3842 de 2022, 1.1.3.",
     "Compromiso social e institucional: cumplir lo asumido y anteponer el interés institucional al personal.",
     [(CNSC, "Habilidad para asumir responsabilidades con ética y profesionalismo, dentro y fuera del establecimiento, anteponiendo los intereses institucionales a los personales e identificándose con los valores, principios y políticas institucionales", "Guía de orientación CNSC, prueba psicotécnica, ejemplo 2"),
      (R3842, "trabajo en equipo; negociación y mediación; compromiso social e institucional; iniciativa; y orientación al logro.", "Resolución 3842, 1.1.3 Competencias comportamentales")],
     "Compromiso social e institucional")

lote = {"id": "coord-2026-11-27", "fecha": "2026-11-27", "cargo": "coordinador",
        "nota": "Lectura K014 (Guía 34, 1.5 instancias de gobierno y participación) con cuatro ítems y dos más para K011 (autonomía escolar y nuevas formas de trabajo). Rota GAC, GAF, GCO y PSI-COMP. Formatos ingreso 2022 y ascenso 2024 (la correcta es la de nivel avanzado).",
        "casos": casos, "fichas": [], "items": items}
json.dump(lote, open(os.path.join(RAIZ, "data", "lotes", "coord-2026-11-27.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(casos), "casos ·", len(items), "ítems")
