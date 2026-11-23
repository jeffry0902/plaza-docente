# -*- coding: utf-8 -*-
"""Cuarto lote de coordinación (2026-11-20). Cubre la lectura K006 (Resolución 3842, funciones específicas 11 a 24 del
rector y requisitos del cargo de rector) y la K011 (Guía 34, establecimiento integrado y nuevas formas de trabajo), con un
ítem de la K013 (Fondo de Servicios Educativos, funciones del consejo directivo). Rota GAC, GAF, GCO y PSI (negociación y
mediación). Formatos: ingreso 2022 (3 opciones, una correcta) y ascenso 2024 (cada opción es un nivel de desempeño; la
correcta es la de nivel avanzado). Genera data/lotes/coord-2026-11-20.json. Citas: texto literal de fuentes/."""
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


R3842, D1075, D1965, D1421, G34 = "resolucion_3842_2022_ocr", "decreto_1075_2015", "decreto_1965_2013", "decreto_1421_2017", "guia34_mineducacion_2008"

# ------------------------------------------------------------ K006 · Resolución 3842, funciones 11 a 24 del rector
caso("CK30", "Sin informe desde enero",
     "Es septiembre. En una sesión del consejo directivo, la representante de los padres de familia le dice a usted, que asiste como coordinador invitado, "
     "que desde enero el consejo no ha recibido ningún informe de la gestión del establecimiento. "
     "El rector está de licencia por dos semanas y ella le pide a usted que prepare y presente «el informe que se debe dar cada año».")
item("CO060", "CK30", "GDI-ROL", 2,
     "Según la Resolución 3842, lo que usted le responde a la representante de los padres es que",
     [("rendir el informe al consejo directivo es función del rector y debe hacerse al menos cada seis meses, por lo que se le hará saber a él a su regreso.",
       "Es correcta. La función 13 del rector en la Resolución 3842 es rendir un informe al consejo directivo al menos cada seis meses. El coordinador puede apoyar con información, pero no asume una función del rector ni cambia su periodicidad."),
      ("rendir el informe al consejo directivo es función del coordinador mientras el rector esté ausente, y basta con presentarlo una vez al año.",
       "Es incorrecta. Mezcla dos errores: el informe al consejo directivo es una función específica del rector, no del coordinador, y la norma no habla de un informe anual sino de uno al menos cada seis meses."),
      ("rendir el informe al consejo directivo solo es obligatorio al cierre de cada vigencia fiscal, cuando se presentan al consejo los estados contables del Fondo.",
       "Es incorrecta. Confunde el informe de gestión con la presentación de los estados contables del Fondo de Servicios Educativos, que el consejo verifica aparte; el informe del rector se rinde al menos cada seis meses.")],
     "A",
     "La Resolución 3842 enumera las funciones específicas del rector o director rural. La número 13 es rendir un informe al consejo directivo del establecimiento educativo al menos cada seis meses. Dos ideas resuelven el caso: el informe es del rector (el coordinador puede apoyarlo, no reemplazarlo) y la periodicidad mínima es semestral, no anual. Si desde enero no hay informe en septiembre, el consejo tiene razón al pedirlo. La CNSC suele poner al coordinador ante funciones del rector para ver si distingue los dos cargos.",
     "Resolución 3842 de 2022, 1.2.1 Funciones específicas del rector, función 13.",
     "Informe al consejo directivo: lo rinde el rector, al menos cada seis meses.",
     [(R3842, "13. Rendir un informe al Consejo Directivo del establecimiento educativo, al menos cada seis (6) meses.", "Resolución 3842, 1.2.1, función 13")],
     "Funciones del rector y del coordinador")

caso("CK31", "Nuevo énfasis en la media",
     "Después de un año de trabajo, el consejo académico aprobó cambiar el énfasis de la media de la institución: pasará de académica a una media con profundización en desarrollo de software, "
     "lo que modifica la intensidad horaria de varias áreas y crea dos asignaturas nuevas. "
     "Un docente propone empezar a aplicarlo el próximo año «sin más trámites, porque la ley nos da autonomía curricular».")
item("CO061", "CK31", "GDI-ROL", 3,
     "Frente a un cambio de esta magnitud, lo que corresponde según la Resolución 3842 es que",
     [("el coordinador radique el cambio ante el Ministerio de Educación, porque es la entidad que fija los lineamientos curriculares del país.",
       "Es incorrecta. El Ministerio define lineamientos y referentes de calidad, pero la norma asigna la verificación de los cambios significativos en el currículo a la secretaría de educación, y quien los presenta es el rector, no el coordinador."),
      ("el rector presente el cambio a la secretaría de educación para que verifique el cumplimiento de los requisitos y adopte las medidas necesarias.",
       "Es correcta. La función 21 del rector en la Resolución 3842 es presentar a la secretaría de educación los cambios significativos en el currículo para que verifique el cumplimiento de los requisitos y adopte las medidas a que haya lugar."),
      ("el cambio se aplique con la aprobación del consejo académico, porque la autonomía escolar permite a cada institución organizar su plan de estudios.",
       "Es incorrecta. La autonomía escolar es real y permite organizar el plan de estudios, pero no elimina el control: un cambio significativo en el currículo debe presentarse a la secretaría de educación para que verifique los requisitos.")],
     "B",
     "La autonomía escolar permite a cada establecimiento organizar su plan de estudios, pero la Resolución 3842 asigna al rector una función de control externo: presentar a la secretaría de educación los cambios significativos en el currículo para que esta verifique el cumplimiento de los requisitos y adopte las medidas a que haya lugar (función 21). Cambiar el énfasis de la media y crear asignaturas es un cambio significativo. El distractor más fuerte es la autonomía: es una verdad a medias que la CNSC usa para que se olvide el trámite. Recuerde: quién presenta (rector) y ante quién (secretaría).",
     "Resolución 3842 de 2022, 1.2.1 Funciones específicas del rector, función 21; Guía 34, 1.3 La autonomía escolar.",
     "Cambio significativo en el currículo: el rector lo presenta a la secretaría de educación para que verifique requisitos.",
     [(R3842, "Presentar a la Secretaría de Educación respectiva, o a los organismos que hagan sus veces, los cambios significativos en el currículo para que ésta verifique el cumplimiento de los requisitos", "Resolución 3842, 1.2.1, función 21")],
     "Funciones del rector y del coordinador")

caso("CK32", "Llegan estudiantes a mitad de año",
     "Entre julio y agosto llegaron a la sede 23 estudiantes nuevos: familias que se trasladaron desde veredas de Paz de Ariporo y Hato Corozal y familias que vienen de otro país. "
     "En sexto grado, cuatro de los recién llegados ya dejaron de asistir. "
     "El rector le pide a usted que proponga cómo debe actuar la institución con los estudiantes que siguen llegando.")
item("CO062", "CK32", "GCO-COMUN", 2,
     "La propuesta del coordinador que corresponde al nivel avanzado es",
     [("organizar una jornada de inducción para los recién llegados en la que se les explique el manual de convivencia y el horario de clases.",
       "Es incorrecta (nivel satisfactorio). La inducción es útil para el ingreso, pero se queda en informar normas y horarios; no considera la situación de cada familia ni prevé acciones de bienestar y seguimiento para que los estudiantes permanezcan."),
      ("reportar a la secretaría de educación las inasistencias de los recién llegados para que ella defina si conservan o no el cupo asignado.",
       "Es incorrecta (nivel inferior). Traslada el problema a otra instancia y lo convierte en un asunto de cupos, cuando la acogida, el bienestar y la permanencia son procesos que el establecimiento debe promover en su propio contexto."),
      ("diseñar con orientación, docentes y familias un proceso de acogida al ingreso y un seguimiento a la permanencia ajustado a cada contexto.",
       "Es correcta (nivel avanzado). Cubre el ingreso y la permanencia, involucra a orientación, docentes y familias, y ajusta las acciones a la procedencia y la situación de cada estudiante, como pide la norma para estos procesos.")],
     "C",
     "La Resolución 3842 asigna al rector promover procesos de acogida, bienestar y permanencia, tanto para el ingreso de los estudiantes como para su permanencia, en correspondencia con los contextos y situaciones territoriales (función 20); el coordinador, a quien el rector le pide la propuesta, la concreta con los equipos. En la lógica de la prueba de ascenso, el nivel avanzado atiende los dos momentos (ingreso y permanencia), involucra a varios actores y se ajusta al contexto de cada estudiante. La inducción informativa es satisfactoria pero incompleta; remitir el caso a la secretaría es inferior.",
     "Resolución 3842 de 2022, 1.2.1, función 20; Guía orientadora de la prueba de ascenso para coordinador (2024).",
     "Acogida, bienestar y permanencia: se cuida el ingreso y también la permanencia, según el contexto de cada estudiante.",
     [(R3842, "Promover procesos de acogida, bienestar y permanencia en el establecimiento educativo, tanto para el ingreso de los estudiantes a esta, como para la permanencia en correspondencia a los contextos y situaciones territoriales.", "Resolución 3842, 1.2.1, función 20")],
     "Familias y entorno", "ascenso 2024")

caso("CK33", "¿Puede aspirar a rector?",
     "La coordinadora Marcela quiere inscribirse a un cargo de rector. Es licenciada en Educación y tiene esta experiencia: "
     "dos años como docente de tiempo completo en un colegio oficial, tres años como coordinadora en el mismo colegio y, antes de eso, un año como jefe de planeación de un colegio privado. "
     "Un compañero le dice que no le alcanza porque «se necesitan seis años en cargos de directivo docente».")
item("CO063", "CK33", "GAF-TALENTO", 3,
     "Según los requisitos del cargo de rector en la Resolución 3842, sobre la experiencia de Marcela se concluye que",
     [("sí la acredita, porque suma cinco años entre docente de tiempo completo y coordinadora, más un año en funciones de planeación.",
       "Es correcta. La segunda forma de acreditar la experiencia del rector es cinco años en cargos de directivo docente o de docente de tiempo completo y un año en cargos con funciones de administración de personal, finanzas o planeación. Marcela cumple exactamente esa combinación."),
      ("no la acredita, porque los seis años exigidos deben ser en cargos de directivo docente y ella solo suma tres años como coordinadora.",
       "Es incorrecta. Es lo que dice el compañero, pero la norma permite contar también los años como docente de tiempo completo y ofrece otras combinaciones; exigir seis años solo como directivo no es lo que dice el Manual."),
      ("sí la acredita, porque suma seis años de experiencia docente al contar el año de planeación del colegio privado como docencia.",
       "Es incorrecta. Llega a la conclusión correcta por una razón equivocada: el año de planeación no es experiencia docente; cuenta por aparte, como experiencia en funciones de planeación. Con solo cinco años de docencia y dirección no cumpliría la primera forma.")],
     "A",
     "La Resolución 3842 exige al rector seis años de experiencia profesional con reconocida trayectoria en materia educativa y ofrece tres formas de acreditarla: seis años como directivo docente o docente de tiempo completo; cinco años en esos cargos más un año en cargos con funciones de administración de personal, finanzas o planeación; o cuatro años más dos años en esas funciones. Marcela tiene cinco años (dos de docente y tres de coordinadora) y un año de planeación: cumple la segunda forma. Las trampas son exigir solo años de directivo o sumar la planeación como docencia.",
     "Resolución 3842 de 2022, 1.2.2.1 Requisitos del cargo de rector, b) Experiencia profesional mínima.",
     "Experiencia del rector: 6 años (directivo o docente de tiempo completo), o 5 + 1, o 4 + 2 en administración, finanzas o planeación.",
     [(R3842, "Cinco (5) años en cargos de directivo docente (Artículo 129 de la Ley 115 de", "Resolución 3842, 1.2.2.1 b), forma 2"),
      (R3842, "Un (1) año en otro tipo de cargos en los que haya cumplido funciones de administración de personal, finanzas o planeación de instituciones educativas, oficiales o privadas", "Resolución 3842, 1.2.2.1 b), forma 2"),
      (R3842, "en cargos de docente de tiempo completo en cualquier nivel educativo y tipo de institución oficial o privada, y,", "Resolución 3842, 1.2.2.1 b), forma 2")],
     "Talento humano y requisitos del cargo")

caso("CK34", "La tendencia que todos quieren adoptar",
     "Después de un foro regional, un grupo de docentes propone que desde el próximo año todas las áreas trabajen con herramientas de inteligencia artificial, "
     "«porque es la tendencia y no nos podemos quedar atrás». En la institución, solo la mitad de las sedes rurales tiene conectividad estable. "
     "El rector le encarga a usted preparar la ruta para decidir sobre la propuesta.")
item("CO064", "CK34", "GDI-PEI", 2,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("aprobar un piloto voluntario con los docentes interesados en las sedes con conectividad y evaluar sus resultados con ellos al terminar el año.",
       "Es incorrecta (nivel satisfactorio). Reconoce el contexto de conectividad y prevé una evaluación, pero la decisión queda en un grupo de docentes, sin la participación del gobierno escolar y sin articularla con el mejoramiento del PEI."),
      ("llevar la propuesta al gobierno escolar para analizarla según el contexto de las sedes y, si es pertinente, articularla al mejoramiento del PEI.",
       "Es correcta (nivel avanzado). La tendencia se identifica con la participación del gobierno escolar, se analiza a la luz del contexto institucional (sedes sin conectividad) y se articula con los procesos de mejoramiento del PEI."),
      ("adoptar la propuesta en todas las áreas desde enero, porque el plan de estudios debe actualizarse siempre con las nuevas tendencias de la educación.",
       "Es incorrecta (nivel inferior). Adopta la tendencia por moda, sin el gobierno escolar, sin revisar el contexto de las sedes rurales y sin articularla con el PEI; podría dejar por fuera a los estudiantes sin conectividad.")],
     "B",
     "La Resolución 3842 asigna al rector identificar, con la participación del gobierno escolar y de acuerdo con el contexto institucional, las tendencias educativas para articularlas con los procesos de mejoramiento del PEI (función 11). La frase tiene tres condiciones y el nivel avanzado cumple las tres: gobierno escolar, contexto y articulación con el PEI. El piloto voluntario es razonable y atiende el contexto, pero deja la decisión por fuera de las instancias (satisfactorio); adoptar la tendencia en todas las áreas sin análisis es inferior. En ascenso, busque la opción que cumple todas las condiciones de la norma.",
     "Resolución 3842 de 2022, 1.2.1, función 11; Guía orientadora de la prueba de ascenso para coordinador (2024).",
     "Tendencias educativas: se identifican con el gobierno escolar, según el contexto, y se articulan con el mejoramiento del PEI.",
     [(R3842, "Identificar con la participación del Gobierno Escolar, y de acuerdo con el contexto institucional, las tendencias educativas para articularlas con los procesos de mejoramiento del Proyecto Educativo Institucional", "Resolución 3842, 1.2.1, función 11")],
     "PEI y gestión estratégica", "ascenso 2024")

# ------------------------------------------------------------ K011 · Guía 34, establecimiento integrado
caso("CK35", "Dos sedes, dos proyectos",
     "Su institución integró hace tres años una escuela rural que tenía su propio PEI con énfasis agropecuario. "
     "En la autoevaluación institucional, los docentes de la sede rural dicen que «siguen trabajando con su PEI de siempre» y los de la sede principal afirman que la sede rural «no se ha querido integrar». "
     "El rector le pide a usted que proponga cómo abordar este hallazgo en el plan de mejoramiento.")
item("CO065", "CK35", "GDI-MEJORA", 2,
     "De acuerdo con la Guía 34, la propuesta que corresponde es",
     [("acordar que cada sede conserve su propio PEI, porque la autonomía escolar permite que cada una de ellas mantenga la identidad que construyó durante años.",
       "Es incorrecta. La autonomía la tiene el establecimiento educativo, no cada sede por separado; tras la integración, la Guía 34 plantea la unificación de los PEI alrededor de un proyecto común, no la coexistencia de varios."),
      ("pedir a la sede rural que adopte el PEI de la sede principal y programar jornadas para explicarles a sus docentes cómo deben aplicarlo.",
       "Es incorrecta. Busca un solo PEI, pero lo impone: la Guía 34 pide un proyecto común fruto de la concertación y el consenso, construido con un nuevo horizonte institucional, no la absorción de una sede por la otra."),
      ("incluir en el plan la construcción concertada de un proyecto común entre las sedes, con canales de comunicación y liderazgo del equipo directivo.",
       "Es correcta. La Guía 34 dice que la unificación de los PEI es un punto crucial del mejoramiento y que el liderazgo del rector y su equipo y los canales de comunicación apropiados son esenciales para lograr un proyecto común concertado.")],
     "C",
     "La Guía 34 explica que, después de la integración de establecimientos, el proceso más complejo fue la unificación de los Proyectos Educativos Institucionales, y que este es un punto crucial que debe ser abordado en el proceso de mejoramiento. Agrega que el liderazgo de los rectores y sus equipos, además de canales de comunicación apropiados, son esenciales para que todos trabajen en un proyecto común, fruto de la concertación y el consenso. Por eso no sirve mantener PEI separados ni imponer el de la sede principal. La palabra clave es «concertación».",
     "Guía 34 MEN (2008), 1.2 El establecimiento educativo integrado.",
     "Establecimiento integrado: un proyecto común entre sedes, construido por concertación, con liderazgo y buena comunicación.",
     [(G34, "Por lo tanto, este es un punto crucial que debe ser abordado en el proceso de mejoramiento.", "Guía 34, 1.2 El establecimiento educativo integrado"),
      (G34, "El liderazgo de los rectores o directores y sus equipos, además de la construcción de canales de comunicación apropiados, son esenciales para consolidar la identidad institucional", "Guía 34, 1.2 El establecimiento educativo integrado")],
     "Ruta de mejoramiento")

# ------------------------------------------------------------ K013 · Fondo de Servicios Educativos (consejo directivo)
caso("CK36", "Arreglo urgente de las baterías sanitarias",
     "En mayo se dañaron las baterías sanitarias de la sede de primaria. En el presupuesto del Fondo de Servicios Educativos hay recursos en el rubro de material didáctico que este año no se usarán completos. "
     "El rector le comenta a usted que, como es el ordenador del gasto, va a mover esos recursos al rubro de mantenimiento esta misma semana y que en la próxima sesión «le informa al consejo».")
item("CO066", "CK36", "GAF-FONDOS", 3,
     "Sobre el movimiento de recursos que plantea el rector, lo que corresponde según el Decreto 1075 es que",
     [("lo puede hacer por su cuenta y luego informarlo, porque el rector es el ordenador del gasto y ejerce la representación legal del Fondo.",
       "Es incorrecta. El rector sí es el ordenador del gasto, pero el decreto aclara que ese ejercicio no implica representación legal, y aprobar los traslados presupuestales que afecten el presupuesto vigente es función del consejo directivo."),
      ("debe solicitar la autorización de la secretaría de educación, porque los recursos del Fondo están bajo el control de las autoridades territoriales.",
       "Es incorrecta. Los recursos del Fondo sí están sometidos al control de autoridades administrativas y fiscales, pero la aprobación de los traslados presupuestales le corresponde al consejo directivo del establecimiento, no a la secretaría."),
      ("debe presentar el traslado al consejo directivo para su aprobación antes de ejecutarlo, porque esa instancia aprueba los traslados presupuestales.",
       "Es correcta. El numeral 3 del artículo 2.3.1.6.3.5 del Decreto 1075 dice que el consejo directivo aprueba las adiciones al presupuesto vigente y los traslados presupuestales que afecten el mismo; el rector propone y ejecuta, pero no lo aprueba solo.")],
     "C",
     "El Decreto 1075 reparte los papeles del Fondo de Servicios Educativos. El rector o director rural es el ordenador del gasto, pero su ejercicio no implica representación legal (art. 2.3.1.6.3.4). El consejo directivo aprueba el presupuesto y también las adiciones y los traslados presupuestales que afecten el presupuesto vigente (art. 2.3.1.6.3.5, numeral 3). Por eso, aunque la necesidad sea urgente y el rector tenga buena intención, el traslado se aprueba primero en el consejo directivo, que puede reunirse en sesión extraordinaria. Informar después invierte el orden que fija la norma.",
     "Decreto 1075 de 2015, arts. 2.3.1.6.3.4 y 2.3.1.6.3.5, numeral 3 (Decreto 4791 de 2008).",
     "Traslados y adiciones del presupuesto del Fondo: los aprueba el consejo directivo; el rector ordena el gasto, sin representación legal.",
     [(D1075, "3. Aprobar las adiciones al presupuesto vigente así como los traslados presupuestales que afecten el mismo.", "Decreto 1075, art. 2.3.1.6.3.5"),
      (D1075, "El rector o director rural es el ordenador del gasto del Fondo de Servicios Educativos y su ejercicio no implica representación legal.", "Decreto 1075, art. 2.3.1.6.3.4")],
     "Fondo de Servicios Educativos")

# ------------------------------------------------------------ GAC · SIEE (asistencia y promoción)
caso("CK37", "Las fallas de noveno",
     "En la comisión de evaluación y promoción de noveno se analiza el caso de un estudiante que aprobó todas las áreas pero acumuló muchas inasistencias por trabajar en la cosecha con su familia. "
     "Un docente afirma que «la ley dice que con el 25 % de fallas se pierde el año»; otro sostiene que «la asistencia no puede influir en la promoción, solo cuentan las notas». "
     "La comisión le pide a usted aclarar la norma.")
item("CO067", "CK37", "GAC-SIEE", 3,
     "La aclaración que corresponde según el Decreto 1075 es que",
     [("el porcentaje de asistencia que incide en la promoción lo define el propio establecimiento, por lo cual debe aplicarse lo que diga su SIEE.",
       "Es correcta. El artículo 2.3.3.3.3.6 del Decreto 1075 dice que el establecimiento educativo definirá el porcentaje de asistencia que incida en la promoción del estudiante, dentro de los criterios de promoción de su SIEE."),
      ("el porcentaje de asistencia que incide en la promoción está fijado por el decreto en el 25 %, por lo cual el estudiante no debe ser promovido.",
       "Es incorrecta. Acierta en que la asistencia puede incidir en la promoción, pero el decreto no fija ningún porcentaje: deja que cada establecimiento lo defina. Afirmar un 25 % es aplicar una regla que la norma vigente no contiene."),
      ("el porcentaje de asistencia no puede incidir en la promoción, porque la promoción depende solo de los desempeños alcanzados en las áreas.",
       "Es incorrecta. Es cierto que la promoción se basa en criterios del SIEE sobre los desempeños, pero el decreto permite expresamente que el establecimiento defina un porcentaje de asistencia que incida en la promoción.")],
     "A",
     "El artículo 2.3.3.3.3.6 del Decreto 1075 (Decreto 1290 de 2009) dice que cada establecimiento determina los criterios de promoción de acuerdo con su SIEE y que definirá el porcentaje de asistencia que incida en la promoción. Así, los dos docentes se equivocan: uno inventa un porcentaje nacional y el otro niega que la asistencia pueda contar. La comisión debe aplicar lo que el SIEE haya definido. Si al final no es promovido, el mismo artículo obliga a garantizarle el cupo. La CNSC suele usar cifras que «suenan» a norma: verifique siempre si el decreto las contiene.",
     "Decreto 1075 de 2015, art. 2.3.3.3.3.6 (Decreto 1290 de 2009, art. 6).",
     "Asistencia y promoción: el porcentaje lo define cada establecimiento en su SIEE; el decreto no fija ninguna cifra.",
     [(D1075, "Así mismo, el establecimiento educativo definirá el porcentaje de asistencia que incida en la promoción del estudiante.", "Decreto 1075, art. 2.3.3.3.3.6"),
      (D1075, "Cada establecimiento educativo determinará los criterios de promoción escolar de acuerdo con el sistema institucional de evaluación de los estudiantes.", "Decreto 1075, art. 2.3.3.3.3.6")],
     "SIEE y promoción")

# ------------------------------------------------------------ GAC · acompañamiento en evaluación formativa (ascenso 2024)
caso("CK38", "Una sola nota por periodo",
     "Al revisar las planillas del primer periodo, usted encuentra que un docente de ciencias naturales de séptimo registró una sola nota: la de un examen escrito al final del periodo. "
     "La mitad del grupo quedó en desempeño bajo y el docente dice que «los estudiantes ya saben lo que tienen que estudiar». "
     "Faltan siete semanas para cerrar el segundo periodo.")
item("CO068", "CK38", "GAC-ACOMP", 3,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("acordar con el docente varios momentos de valoración en el periodo y revisar con él cómo usar sus resultados para apoyar a quienes van bajos.",
       "Es correcta (nivel avanzado). Acompaña al docente en una evaluación que identifica avances y ritmos durante el periodo y que sirve para implementar estrategias de apoyo a quienes presentan debilidades, como señala el decreto."),
      ("pedirle al docente que agregue al menos tres notas más en el segundo periodo para que la valoración del grupo quede mejor sustentada.",
       "Es incorrecta (nivel mínimo). Aumenta el número de notas, pero se queda en lo formal: no revisa para qué sirve la evaluación ni cómo usar sus resultados para reorientar la enseñanza y apoyar a los estudiantes."),
      ("programar actividades de recuperación para los estudiantes con desempeño bajo al cierre del semestre y entregar sus resultados a las familias.",
       "Es incorrecta (nivel satisfactorio). Las estrategias de apoyo son necesarias, pero dejarlas para el cierre no cambia la práctica evaluativa del docente ni aprovecha la evaluación durante el periodo para reorientar el proceso.")],
     "A",
     "El artículo 2.3.3.3.3.3 del Decreto 1075 fija los propósitos de la evaluación en el ámbito institucional: identificar características, ritmos y estilos de aprendizaje para valorar avances; proporcionar información para consolidar o reorientar los procesos educativos, y suministrar información para implementar estrategias de apoyo. Un único examen final no cumple esos propósitos. En la prueba de ascenso, el nivel avanzado acompaña al docente para que la evaluación ocurra durante el proceso y se use para apoyar; agregar notas es mínimo y la recuperación al cierre es satisfactoria pero tardía.",
     "Decreto 1075 de 2015, art. 2.3.3.3.3.3 (Decreto 1290 de 2009, art. 3); Resolución 3842 de 2022, funciones del coordinador.",
     "Evaluación formativa: valorar durante el proceso y usar la información para reorientar y apoyar, no solo calificar al final.",
     [(D1075, "2. Proporcionar información básica para consolidar o reorientar los procesos educativos relacionados con el desarrollo integral del estudiante.", "Decreto 1075, art. 2.3.3.3.3.3"),
      (D1075, "3. Suministrar información que permita implementar estrategias pedagógicas para apoyar a los estudiantes que presenten debilidades y desempeños superiores en su proceso formativo.", "Decreto 1075, art. 2.3.3.3.3.3")],
     "Acompañamiento pedagógico", "ascenso 2024")

# ------------------------------------------------------------ GCO · comité escolar de convivencia (sesiones y quórum)
caso("CK39", "Sesión sin el personero",
     "El rector convocó una sesión extraordinaria del comité escolar de convivencia para analizar una situación tipo II que ya fue atendida. "
     "Asisten el rector, usted como coordinador, la docente orientadora, el docente que lidera procesos de convivencia, el presidente del consejo de padres y el presidente del consejo de estudiantes. "
     "El personero estudiantil avisó que no podrá llegar. El reglamento del comité fija como quórum la mitad más uno de sus integrantes.")
item("CO069", "CK39", "GCO-CONV", 3,
     "Sobre si el comité puede sesionar, lo que corresponde según el Decreto 1965 es que",
     [("sí puede sesionar, porque están presentes seis de sus siete integrantes y así se supera el quórum que fija el reglamento del comité.",
       "Es incorrecta. Es cierto que el quórum lo fija el reglamento, pero el decreto añade una condición que no depende de él: el comité no puede sesionar sin el personero estudiantil, aunque haya mayoría."),
      ("no puede sesionar, porque sin el personero estudiantil el comité no puede hacerlo, aunque se cumpla el quórum que fija su reglamento.",
       "Es correcta. El artículo 24 del Decreto 1965 dice que el quórum decisorio es el del reglamento, pero que en cualquier caso el comité no podrá sesionar sin la presencia del presidente, del personero estudiantil y del presidente del consejo de estudiantes."),
      ("sí puede sesionar, porque en una sesión extraordinaria basta con la presencia del presidente y de quien solicitó que se convocara.",
       "Es incorrecta. Las sesiones extraordinarias las convoca el presidente, también a solicitud de cualquier integrante, pero eso no cambia las presencias obligatorias: sin el personero estudiantil el comité no sesiona.")],
     "B",
     "El Decreto 1965 regula el funcionamiento del comité escolar de convivencia. El artículo 23 dice que sesiona como mínimo una vez cada dos meses y que las sesiones extraordinarias las convoca el presidente cuando las circunstancias lo exijan o por solicitud de cualquier integrante. El artículo 24 deja el quórum decisorio al reglamento, pero agrega que en cualquier caso el comité no podrá sesionar sin el presidente, el personero estudiantil y el presidente del consejo de estudiantes. La trampa es contar asistentes: aunque haya mayoría, la ausencia del personero impide sesionar.",
     "Decreto 1965 de 2013, arts. 23 y 24.",
     "Comité escolar de convivencia: sin presidente, personero o presidente del consejo de estudiantes no sesiona, haya o no quórum.",
     [(D1965, "En cualquier caso, este Comité no podrá sesionar sin la presencia del presidente, del personero estudiantil y del presidente del consejo de estudiantes.", "Decreto 1965, art. 24"),
      (D1965, "Las sesiones extraordinarias serán convocadas por el Presidente del Comité Escolar de Convivencia, cuando las circunstancias lo exijan o por solicitud de cualquiera de los integrantes del mismo.", "Decreto 1965, art. 23")],
     "Comité escolar de convivencia")

# ------------------------------------------------------------ GCO · inclusión, matrícula sin diagnóstico (ascenso 2024)
caso("CK40", "Matrícula sin diagnóstico",
     "En febrero llega una madre a matricular a su hijo de ocho años en segundo grado. Cuenta que en la escuela anterior le dijeron que el niño «podría tener una discapacidad», "
     "pero no tiene diagnóstico ni concepto médico porque la cita con el especialista no ha sido posible. "
     "La secretaria académica le pregunta a usted si debe recibirlo o pedirle a la madre que vuelva con el diagnóstico.")
item("CO070", "CK40", "GCO-INCL", 3,
     "La actuación del coordinador que corresponde al nivel avanzado es",
     [("matricular al niño y esperar a que la familia traiga el diagnóstico médico del especialista para iniciar la valoración pedagógica y la elaboración del PIAR.",
       "Es incorrecta (nivel satisfactorio). Respeta el derecho a la matrícula, pero detiene la respuesta pedagógica: el decreto no condiciona la valoración pedagógica ni el PIAR a que llegue el diagnóstico, y no gestiona el reporte a la secretaría."),
      ("aplazar la matrícula hasta que la familia presente el diagnóstico médico, para saber qué apoyos necesita el niño antes de asignarle un grupo.",
       "Es incorrecta (nivel inferior). Condiciona el ingreso al diagnóstico, cuando el decreto ordena matricular aunque no exista y prohíbe que la discapacidad sea causal de negación del cupo. Es una barrera de acceso, no una medida de apoyo."),
      ("matricularlo, registrar en el Simat las variables con la información de la familia, reportarlo a la secretaría e iniciar la acogida y la valoración.",
       "Es correcta (nivel avanzado). Sigue el proceso del decreto: matrícula y registro en el Simat con base en la información de la familia, reporte a la secretaría para el diagnóstico con el sector salud y, efectuada la matrícula, acogida, valoración pedagógica y PIAR.")],
     "C",
     "El artículo 2.3.3.5.2.3.1 del Decreto 1075 (Decreto 1421 de 2017) dice que, si el estudiante no cuenta con diagnóstico, se debe proceder con la matrícula y con el registro de las variables en el Simat con base en la información de la familia, y reportar a la secretaría de educación para que, con el sector salud, se establezca el diagnóstico en un plazo no mayor a tres meses. Efectuada la matrícula, se inicia la acogida, la valoración pedagógica y el PIAR. El nivel avanzado activa todo el proceso; el satisfactorio matricula pero espera, y el inferior pone una barrera.",
     "Decreto 1421 de 2017 (Decreto 1075, art. 2.3.3.5.2.3.1, numerales 1 y 2); Guía orientadora de la prueba de ascenso para coordinador (2024).",
     "Sin diagnóstico también se matricula: registro en el Simat con la información de la familia, reporte a la secretaría y PIAR.",
     [(D1421, "En caso de que el estudiante no cuente con dicho requisito, se deberá proceder con la matrícula y con el registro de las variables para la identificación de los estudiantes con discapacidad en el Simat, con base en la información de la familia", "Decreto 1421, art. 2.3.3.5.2.3.1, num. 1"),
      (D1421, "2. Efectuada la matrícula, se inicia el proceso de acogida incluido en la organización institucional con base en el diseño universal y se realiza la valoración pedagógica y la elaboración del PIAR.", "Decreto 1421, art. 2.3.3.5.2.3.1, num. 2")],
     "Inclusión y ajustes razonables", "ascenso 2024")

# ------------------------------------------------------------ PSI · negociación y mediación
caso("CK41", "La sala de informática del martes",
     "Dos docentes de la jornada de la mañana necesitan la sala de informática el martes de 8:00 a 10:00: la de matemáticas, para una práctica con hojas de cálculo que prepara con su grupo de noveno, "
     "y el de tecnología, para un proyecto de programación de décimo que entrega resultados en tres semanas. "
     "Los dos acuden a usted molestos y cada uno sostiene que su necesidad es la prioritaria.")
item("CO071", "CK41", "PSI-NEGM", 2,
     "La actuación que mejor demuestra la competencia de negociación y mediación es",
     [("asignar la franja al docente de tecnología, porque la sala está pensada sobre todo para su área y su proyecto tiene una fecha de entrega cercana.",
       "Es incorrecta. El criterio parece objetivo, pero el coordinador impone una decisión sin escuchar los intereses de ambos ni explorar alternativas; uno de los dos queda insatisfecho y el conflicto puede repetirse."),
      ("reunir a los dos docentes para que expongan qué necesita cada uno y construir con ellos un acuerdo sobre el uso de la sala en esas semanas.",
       "Es correcta. Facilita que las partes expongan sus intereses y busquen juntas una solución, por ejemplo alternar semanas o compartir franjas; un acuerdo construido así es más legítimo y genera compromiso, como señala la Guía 34."),
      ("llevar el caso a la próxima reunión de docentes para que el grupo decida por votación cuál de las dos actividades usa la sala el martes.",
       "Es incorrecta. Parece democrático, pero traslada a terceros un conflicto entre dos personas y lo resuelve por mayoría, sin que las partes negocien; quien pierde la votación no queda comprometido con la decisión.")],
     "B",
     "La Resolución 3842 incluye la negociación y la mediación entre las competencias comportamentales del directivo docente. La Guía 34 explica por qué importan: el trabajo en equipo desarrolla las capacidades de argumentación y negociación, que contribuyen a la consecución de acuerdos, y esos consensos dan mayor legitimidad a las decisiones y generan compromiso con las tareas. Mediar no es decidir por las partes ni pasar el conflicto a una votación: es facilitar que cada docente exponga su necesidad y que construyan juntos un acuerdo. En la prueba psicotécnica, descarte las opciones que imponen.",
     "Resolución 3842 de 2022, 1.1.3 Competencias comportamentales; Guía 34 MEN (2008), 1.4.",
     "Negociación y mediación: escuchar los intereses de las dos partes y construir con ellas el acuerdo; no imponerlo ni someterlo a votación.",
     [(R3842, "trabajo en equipo; negociación y mediación; compromiso social e institucional; iniciativa; y orientación al logro.", "Resolución 3842, 1.1.3 Competencias comportamentales"),
      (G34, "Igualmente, se desarrollan las capacidades de argumentación y negociación, lo que contribuye a la consecución de acuerdos sobre diferentes temas.", "Guía 34, 1.4 Las nuevas formas de trabajo")],
     "Negociación y mediación")

lote = {"id": "coord-2026-11-20", "fecha": "2026-11-20", "cargo": "coordinador",
        "nota": "Lecturas K006 (Resolución 3842, funciones 11 a 24 del rector y requisitos) y K011 (Guía 34, establecimiento integrado); un ítem de K013. Formatos ingreso 2022 y ascenso 2024 (la correcta es la de nivel avanzado).",
        "casos": casos, "fichas": [], "items": items}
json.dump(lote, open(os.path.join(RAIZ, "data", "lotes", "coord-2026-11-20.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(casos), "casos ·", len(items), "ítems")
