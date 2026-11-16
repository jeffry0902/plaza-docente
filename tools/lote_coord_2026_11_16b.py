# -*- coding: utf-8 -*-
"""Segundo lote de coordinación. Modela dos formatos de concursos pasados:
- Ingreso 2022 (Universidad Libre): caso + enunciado + 3 opciones, una correcta.
- Ascenso 2024 (Universidad de Antioquia, prueba pedagógica para coordinador): cada opción es un nivel de desempeño
  (avanzado, satisfactorio, mínimo, inferior); aquí se dejan 3 opciones y la correcta es la de nivel avanzado.
Genera data/lotes/coord-2026-11-16b.json. Las citas son texto literal de fuentes/."""
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
L1620, D1421 = "ley_1620_2013", "decreto_1421_2017"

# ------------------------------------------------------------ PEI y manual
caso("CK12", "Ajustes al PEI y al manual",
     "En febrero, la asociación de padres de familia le entrega a usted como coordinador una propuesta para modificar el horizonte institucional del PEI e incluir un énfasis en emprendimiento. "
     "Al mismo tiempo, el comité escolar de convivencia terminó de redactar un nuevo capítulo del manual de convivencia sobre el manejo de conflictos entre estudiantes. "
     "El rector le pide orientar los dos trámites para que queden en firme.")
item("CO029", "CK12", "GDI-PEI", 3,
     "Sobre la propuesta de la asociación de padres para modificar el PEI, el trámite que corresponde es",
     [("que usted la lleve al consejo académico para que la apruebe, porque el énfasis afecta el plan de estudios y la gestión académica.",
       "Es incorrecta. El consejo académico es consultado, pero no decide las modificaciones del PEI; además, la norma exige que la propuesta pase primero por la discusión de los demás estamentos."),
      ("que se presente al rector, que la someta a discusión de los estamentos y que el consejo directivo decida, consultado el académico.",
       "Es correcta. El artículo 2.3.3.1.4.2 del Decreto 1075 dice que las modificaciones se solicitan al rector, quien las somete a discusión de los demás estamentos; luego el consejo directivo decide, previa consulta al consejo académico."),
      ("que se someta a votación en una asamblea general de padres, porque fue ese estamento el que la propuso y la respalda mayoritariamente.",
       "Es incorrecta. Los estamentos participan en la discusión, pero ninguno decide por sí solo: la decisión sobre las modificaciones al PEI le corresponde al consejo directivo, previa consulta al consejo académico.")],
     "B",
     "El PEI se construye con participación, pero cada paso tiene un responsable. Según el artículo 2.3.3.1.4.2 del Decreto 1075 (Decreto 1860 de 1994, art. 15), cualquier estamento puede solicitar modificaciones al rector; el rector las somete a discusión de los demás estamentos y, concluida esa etapa, el consejo directivo decide sobre las propuestas, previa consulta al consejo académico. Por eso ni el consejo académico ni la asamblea de padres pueden aprobar el cambio. Como coordinador, usted debe coordinar y participar en la revisión del PEI (Resolución 3842), no decidirla.",
     "Decreto 1075 de 2015, art. 2.3.3.1.4.2, numeral 3.",
     "Modificar el PEI: solicitud al rector → discusión de estamentos → decide el consejo directivo con consulta al académico.",
     [(D1075, "Las modificaciones al proyecto educativo institucional podrán ser solicitadas al rector por cualquiera de los estamentos de la comunidad educativa.", "Decreto 1075, art. 2.3.3.1.4.2"),
      (D1075, "el consejo Directivo procederá a decidir sobre las propuestas, previa consulta con el Consejo Académico.", "Decreto 1075, art. 2.3.3.1.4.2")],
     "PEI y manual de convivencia")
item("CO030", "CK12", "GDI-PEI", 2,
     "Si la modificación se adopta, el rector deberá presentar al consejo directivo el plan operativo correspondiente",
     [("dentro de los tres meses siguientes a la adopción, con metas, estrategias, recursos y cronograma, y revisarlo por lo menos cada año.",
       "Es correcta. El numeral 5 del artículo 2.3.3.1.4.2 del Decreto 1075 fija ese plazo y ese contenido, y agrega que el plan operativo se revisa periódicamente, por lo menos cada año, como referencia de la evaluación institucional."),
      ("al finalizar el año escolar, junto con los resultados de la autoevaluación institucional, para incorporarlo al plan de mejoramiento.",
       "Es incorrecta. El plan operativo tiene un plazo propio, contado desde la adopción del PEI. La autoevaluación lo usa como referencia, pero no se presenta al cierre del año ni reemplaza su plazo."),
      ("dentro del mes siguiente a la adopción, para que la secretaría de educación lo apruebe antes de iniciar las actividades del proyecto.",
       "Es incorrecta. El plazo no es de un mes y la secretaría no aprueba el plan operativo. Sí presta asesoría a los establecimientos que la soliciten durante la elaboración y adopción del PEI.")],
     "A",
     "El Decreto 1075 (art. 2.3.3.1.4.2, numeral 5) establece que el rector presentará al consejo directivo, dentro de los tres meses siguientes a la adopción del PEI, el plan operativo con las metas, estrategias, recursos y cronograma necesarios para alcanzar sus objetivos. Ese plan se revisa por lo menos cada año y es punto de referencia para la evaluación institucional. Retenga tres datos: tres meses, rector ante consejo directivo y revisión anual; los distractores cambian el plazo o meten a la secretaría como instancia aprobadora.",
     "Decreto 1075 de 2015, art. 2.3.3.1.4.2, numeral 5.",
     "Plan operativo: el rector lo presenta al consejo directivo en 3 meses; se revisa al menos cada año.",
     [(D1075, "El rector presentará al Consejo Directivo, dentro de los tres meses siguientes a la adopción del proyecto educativo", "Decreto 1075, art. 2.3.3.1.4.2"),
      (D1075, "Periódicamente y por lo menos cada año, el plan operativo será revisado y constituirá un", "Decreto 1075, art. 2.3.3.1.4.2")],
     "PEI y manual de convivencia")
item("CO031", "CK12", "GDI-PEI", 2,
     "Para que el nuevo capítulo del manual de convivencia quede en firme y cumpla la norma, usted orienta que",
     [("el comité escolar de convivencia lo apruebe, porque es la instancia que lidera la convivencia, y lo divulgue a los estudiantes.",
       "Es incorrecta. El comité participa en la actualización del manual, pero adoptarlo es función del consejo directivo según el artículo 2.3.3.1.5.6 del Decreto 1075."),
      ("el rector lo expida por resolución, porque el manual hace parte del reglamento interno que él administra como ordenador.",
       "Es incorrecta. El rector orienta y ejecuta, pero la norma asigna la adopción del manual de convivencia y del reglamento de la institución al consejo directivo."),
      ("el consejo directivo lo adopte y que el capítulo incluya instancias de diálogo y de conciliación para resolver los conflictos.",
       "Es correcta. Adoptar el manual es función del consejo directivo, y el artículo 2.3.3.1.4.4 exige que los procedimientos para resolver conflictos incluyan instancias de diálogo y de conciliación.")],
     "C",
     "Dos normas del Decreto 1075 se combinan aquí. El artículo 2.3.3.1.5.6, literal c, asigna al consejo directivo adoptar el manual de convivencia y el reglamento de la institución. El artículo 2.3.3.1.4.4 dice qué debe contener el manual; entre otros, procedimientos para resolver con oportunidad y justicia los conflictos, que deben incluir instancias de diálogo y de conciliación. El comité de convivencia y el rector participan, pero no adoptan. En la prueba, verifique siempre quién adopta y qué contenido mínimo exige la norma.",
     "Decreto 1075 de 2015, arts. 2.3.3.1.4.4 y 2.3.3.1.5.6.",
     "Manual de convivencia: lo adopta el consejo directivo; resolución de conflictos con diálogo y conciliación.",
     [(D1075, "c) Adoptar el manual de convivencia y el reglamento de la institución;", "Decreto 1075, art. 2.3.3.1.5.6"),
      (D1075, "Deben incluir instancias de diálogo y de conciliación.", "Decreto 1075, art. 2.3.3.1.4.4")],
     "PEI y manual de convivencia")

# ------------------------------------------------------------ Gobierno escolar
caso("CK13", "Calendario de elecciones",
     "Las clases empezaron el 26 de enero. El rector le encarga a usted como coordinador organizar el calendario de participación estudiantil. "
     "Una estudiante de once quiere ser personera y, si gana, también representante de los estudiantes ante el consejo directivo. "
     "La sede de primaria tiene preescolar y los grados primero a quinto. Además, varias familias piden cupo para el segundo semestre y no hay criterios escritos para asignarlos.")
item("CO032", "CK13", "GDI-GOB", 3,
     "Sobre la elección del personero, usted organiza que",
     [("el consejo de estudiantes lo elija dentro del primer periodo, entre los candidatos de once, y que la estudiante asuma ambos cargos si gana.",
       "Es incorrecta. Al personero lo eligen todos los estudiantes matriculados, no el consejo de estudiantes, y los dos cargos que la estudiante quiere ocupar son incompatibles."),
      ("el rector convoque a todos los estudiantes antes del 25 de febrero, con voto secreto y mayoría simple, y que ella elija un solo cargo.",
       "Es correcta. El personero se elige dentro de los 30 días calendario siguientes al inicio de clases, por convocatoria del rector, con mayoría simple y voto secreto, y el cargo es incompatible con el de representante ante el consejo directivo."),
      ("el consejo directivo convoque la elección en las primeras ocho semanas, con voto secreto, y que ella combine ambos cargos.",
       "Es incorrecta. Quien convoca es el rector y el plazo es de 30 días calendario desde el inicio de clases. Además, la norma declara incompatibles el cargo de personero y el de representante de los estudiantes.")],
     "B",
     "El artículo 2.3.3.1.5.11 del Decreto 1075 fija las reglas: el personero es un estudiante del último grado; se elige dentro de los treinta días calendario siguientes a la iniciación de clases; el rector convoca a todos los estudiantes matriculados, y se elige por mayoría simple y voto secreto. También dice que el cargo de personero es incompatible con el de representante de los estudiantes ante el consejo directivo. Con clases desde el 26 de enero, el plazo vence el 25 de febrero. Las opciones incorrectas cambian quién convoca, quién elige o permiten acumular cargos.",
     "Decreto 1075 de 2015, art. 2.3.3.1.5.11.",
     "Personero: 30 días desde el inicio de clases, convoca el rector, mayoría simple y voto secreto; incompatible con el representante ante el consejo directivo.",
     [(D1075, "El personero de los estudiantes será elegido dentro de los treinta días calendario siguientes al de la iniciación de clases de un período lectivo", "Decreto 1075, art. 2.3.3.1.5.11"),
      (D1075, "El ejercicio del cargo de personero de los estudiantes es incompatible con el de representante de los estudiantes ante el Consejo Directivo.", "Decreto 1075, art. 2.3.3.1.5.11")],
     "Gobierno escolar")
item("CO033", "CK13", "GDI-GOB", 3,
     "Para elegir los voceros de la sede de primaria ante el consejo de estudiantes, usted organiza",
     [("una asamblea por cada grado, de preescolar a quinto, para que cada uno elija su vocero mediante votación secreta.",
       "Es incorrecta. Los grados cuarto y quinto sí eligen su propio vocero, pero preescolar y los tres primeros grados no votan por separado: la norma prevé para ellos una asamblea conjunta."),
      ("que los docentes de cada grado designen al vocero entre los estudiantes con mejor desempeño, por la edad de los niños.",
       "Es incorrecta. El vocero se elige por votación secreta en asamblea; la designación por parte de los docentes desconoce el carácter participativo del consejo de estudiantes."),
      ("una asamblea conjunta de preescolar a tercero que elija un vocero de tercer grado, y asambleas aparte para cuarto y quinto.",
       "Es correcta. El artículo 2.3.3.1.5.12 del Decreto 1075 dispone que los alumnos de preescolar y de los tres primeros grados se convoquen a una asamblea conjunta para elegir un vocero único entre los de tercer grado.")],
     "C",
     "El consejo de estudiantes tiene un vocero por cada grado, elegido por votación secreta en asambleas que convoca el consejo directivo dentro de las cuatro primeras semanas del calendario académico. La excepción que la CNSC suele preguntar está en el mismo artículo 2.3.3.1.5.12 del Decreto 1075: preescolar y los tres primeros grados de primaria van a una asamblea conjunta y eligen un vocero único entre los estudiantes de tercero. Cuarto y quinto eligen cada uno su vocero.",
     "Decreto 1075 de 2015, art. 2.3.3.1.5.12.",
     "Consejo de estudiantes: un vocero por grado; preescolar a tercero eligen uno solo, de tercer grado.",
     [(D1075, "Los alumnos del nivel preescolar y de los tres primeros grados del ciclo de primaria, serán convocados a una asamblea conjunta para elegir un", "Decreto 1075, art. 2.3.3.1.5.12")],
     "Gobierno escolar")
item("CO034", "CK13", "GDI-GOB", 2,
     "Sobre los criterios para asignar los cupos disponibles, usted le explica al rector que deben ser fijados por",
     [("el consejo directivo, que tiene entre sus funciones fijar los criterios para la asignación de cupos para nuevos alumnos.",
       "Es correcta. El literal d del artículo 2.3.3.1.5.6 del Decreto 1075 asigna al consejo directivo fijar los criterios para la asignación de cupos disponibles para la admisión de nuevos alumnos."),
      ("el consejo académico, porque los cupos dependen de la capacidad de cada grado y de la organización del plan de estudios.",
       "Es incorrecta. El consejo académico organiza el plan de estudios y la evaluación; la norma no le asigna fijar criterios de admisión, que son función del consejo directivo."),
      ("usted como coordinador, porque conoce la ocupación real de los grupos y atiende directamente a las familias que solicitan cupo.",
       "Es incorrecta. Conocer la ocupación de los grupos permite aportar información, pero fijar criterios de admisión es una decisión del consejo directivo, no una función del coordinador.")],
     "A",
     "El artículo 2.3.3.1.5.6 del Decreto 1075 enumera las funciones del consejo directivo; el literal d es fijar los criterios para la asignación de cupos disponibles para la admisión de nuevos alumnos. El coordinador puede aportar datos sobre la capacidad de los grupos, pero no decide los criterios. Esta función aparece con frecuencia junto a otras del consejo directivo que conviene memorizar: adoptar el manual de convivencia, aprobar el plan anual de actualización docente y participar en la evaluación de docentes y directivos.",
     "Decreto 1075 de 2015, art. 2.3.3.1.5.6, literal d.",
     "Criterios para asignar cupos: los fija el consejo directivo.",
     [(D1075, "d) Fijar los criterios para la asignación de cupos disponibles para la admisión de nuevos alumnos;", "Decreto 1075, art. 2.3.3.1.5.6")],
     "Gobierno escolar")

# ------------------------------------------------------------ Acompañamiento (estilo ascenso 2024)
caso("CK14", "Visita al aula de octavo",
     "Usted acompaña una clase de ciencias sociales de octavo. El docente expone durante toda la hora, los estudiantes copian y la evaluación del periodo es un único examen final; "
     "el PEI define un modelo pedagógico de aprendizaje activo con evaluación formativa. En las reuniones del área de sociales, cada docente trabaja contenidos distintos según su libro de texto. "
     "Dos docentes jóvenes le comentan que quieren proponer un proyecto de memoria histórica con la comunidad, pero no saben cómo presentarlo.")
item("CO035", "CK14", "GAC-ACOMP", 3,
     "Después de la clase, la acción que muestra un acompañamiento de nivel avanzado es",
     [("enviarle al docente un correo con recomendaciones sobre evaluación formativa y pedirle que ajuste su planeación para el siguiente periodo.",
       "Es incorrecta (nivel mínimo). Ofrece orientación, pero de manera unidireccional: no dialoga sobre lo observado, no construye acuerdos con el docente ni prevé seguimiento a los cambios."),
      ("conversar con el docente sobre lo observado frente al modelo del PEI, acordar con él ajustes en la evaluación y programar un seguimiento.",
       "Es correcta (nivel avanzado). Usa evidencias de la clase, retroalimenta frente al modelo pedagógico del PEI, construye acuerdos con el docente y define un seguimiento, como pide la función de orientar y acompañar el modelo."),
      ("registrar en el informe de seguimiento que el docente no aplica el modelo pedagógico y entregar el informe al rector para lo de su cargo.",
       "Es incorrecta (nivel inferior). Documentar es útil, pero limitarse a reportar convierte el acompañamiento en inspección y no ofrece al docente ninguna oportunidad de mejorar su práctica.")],
     "B",
     "La prueba de ascenso para coordinador (2024) no tiene opciones correctas o incorrectas: cada una corresponde a un nivel de desempeño. El nivel avanzado se reconoce porque usa evidencias, dialoga, construye acuerdos y hace seguimiento; el mínimo cumple pero de forma unidireccional, y el inferior se queda en reportar. En la prueba de ingreso, con una sola clave, la lógica es la misma. La Resolución 3842 le asigna al coordinador orientar y acompañar la implementación del modelo pedagógico del PEI, y la Guía 34 ubica la evaluación en el aula dentro del proceso de gestión de aula.",
     "Resolución 3842 de 2022, 1.3.1; Guía 34 MEN (2008), Cuadro No. 3, gestión de aula.",
     "Acompañar = evidencias + diálogo + acuerdos + seguimiento. Solo reportar es nivel inferior.",
     [(R3842, "Orientar y acompañar la implementación del modelo pedagógico, didáctico y curricular definido en el Proyecto Educativo Institucional", "Resolución 3842, 1.3.1"),
      (G34, "Relación y estilo pedagógico, planeación de clases y evaluación en el aula.", "Guía 34, Cuadro No. 3, Gestión de aula")],
     "Acompañamiento pedagógico", "ascenso 2024")
item("CO036", "CK14", "GAC-ACOMP", 2,
     "Frente a que cada docente del área trabaje contenidos distintos según su libro de texto, usted",
     [("pide a cada docente que entregue su plan de contenidos para que usted unifique uno solo y lo distribuya al inicio del periodo.",
       "Es incorrecta. Unificar desde coordinación deja por fuera la construcción colectiva del área y no garantiza que el plan responda a los referentes de calidad ni a las estrategias del PEI."),
      ("acuerda con el jefe de área que cada docente conserve su libro, siempre que cumpla las horas semanales asignadas a la asignatura.",
       "Es incorrecta. Cumplir la intensidad horaria no resuelve la falta de coherencia: la función del coordinador es articular el plan de estudios, no avalar que cada docente trabaje por separado."),
      ("orienta en la reunión de área la articulación del plan de estudios con los referentes de calidad del MEN y el PEI.",
       "Es correcta. La Resolución 3842 asigna al coordinador coordinar la articulación del plan de estudios con los referentes de calidad del MEN y el PEI, y orientar las reuniones de área para dar coherencia a las prácticas.")],
     "C",
     "Dos funciones del coordinador en la Resolución 3842 responden directamente a este caso: coordinar la articulación del plan de estudios de acuerdo con los referentes de calidad del Ministerio y las estrategias pedagógicas del PEI, y orientar las reuniones de área para promover la coherencia de las prácticas pedagógicas con los propósitos institucionales. La respuesta correcta usa el espacio colectivo del área; las incorrectas centralizan la decisión o se conforman con un cumplimiento formal.",
     "Resolución 3842 de 2022, 1.3.1 (funciones 7 y 10).",
     "Plan de estudios desarticulado → reunión de área + referentes de calidad del MEN + PEI.",
     [(R3842, "Coordinar la articulación del plan de estudios, de acuerdo con los referentes de calidad del Ministerio de Educación Nacional", "Resolución 3842, 1.3.1, función 7"),
      (R3842, "Orientar las reuniones de área, de ciclos y de otros equipos pedagógicos", "Resolución 3842, 1.3.1, función 10")],
     "Acompañamiento pedagógico", "ascenso 2024")
item("CO037", "CK14", "GAC-ACOMP", 3,
     "Con los dos docentes que quieren proponer el proyecto de memoria histórica, usted",
     [("los orienta para formularlo y los acompaña a sustentarlo ante el consejo académico, en articulación con los planes del PEI.",
       "Es correcta (nivel avanzado). La Resolución 3842 le asigna al coordinador sustentar ante el consejo académico proyectos que mejoren el aprendizaje y motivar la innovación pedagógica de los docentes."),
      ("les sugiere esperar a la próxima actualización del PEI, porque los proyectos nuevos deben quedar incluidos antes de ejecutarse.",
       "Es incorrecta (nivel inferior). Aplazar la iniciativa sin acompañarla desmotiva a los docentes; la norma prevé que los proyectos se sustenten ante el consejo académico y se articulen con los planes existentes."),
      ("les autoriza desarrollarlo con sus grupos de octavo como experiencia piloto y les pide un informe de resultados al final del año.",
       "Es incorrecta (nivel mínimo). Apoya la iniciativa, pero la deja aislada: no pasa por el consejo académico ni se articula con el PEI, por lo que difícilmente se vuelve un proyecto institucional.")],
     "A",
     "Entre las funciones del coordinador en la Resolución 3842 están sustentar ante el consejo académico proyectos que contribuyan al aprendizaje significativo y al mejoramiento de la calidad, y motivar e impulsar estrategias de innovación pedagógica por parte de los docentes. Por eso el nivel avanzado combina orientación a los docentes y paso por la instancia institucional. El piloto aislado es un apoyo de nivel mínimo y el aplazamiento es inferior. Esta lógica de niveles corresponde a la acción «toma decisiones que fortalecen la gestión pedagógica en coherencia con el PEI» de la prueba de ascenso.",
     "Resolución 3842 de 2022, 1.3.1 (funciones 2 y 9).",
     "Iniciativas de los docentes: acompañar y llevarlas al consejo académico, articuladas con el PEI.",
     [(R3842, "Sustentar ante el Consejo Académico proyectos que coadyuven al aprendizaje", "Resolución 3842, 1.3.1, función 2"),
      (R3842, "Motivar e impulsar estrategias de innovación pedagógica y planes de", "Resolución 3842, 1.3.1, función 9")],
     "Acompañamiento pedagógico", "ascenso 2024")

# ------------------------------------------------------------ Evaluaciones externas
caso("CK15", "Llegan los resultados Saber",
     "La institución recibió los resultados de las pruebas Saber 11 y Saber 3, 5 y 9. Varios docentes proponen publicar en la sala de profesores un listado con el promedio de los grupos de cada docente; "
     "otros dicen que esos resultados solo sirven para el ranking del colegio y que no tienen relación con el trabajo de aula.")
item("CO038", "CK15", "GAC-SEGUIM", 3,
     "Según la Guía 34, la forma de gestionar estos resultados que usted promueve como coordinador es",
     [("publicar los promedios por docente para que cada uno reconozca su responsabilidad y se generen compromisos individuales de mejora.",
       "Es incorrecta. Exponer los promedios por docente convierte los resultados en un instrumento de presión y no de análisis colectivo; la guía habla de un uso pedagógico de las evaluaciones externas."),
      ("analizar los resultados con las áreas y usarlos pedagógicamente en el seguimiento académico y en el plan de mejoramiento.",
       "Es correcta. La Guía 34 incluye el uso pedagógico de las evaluaciones externas como componente del seguimiento académico, en la gestión académica, y la ruta de mejoramiento usa esa información para priorizar acciones."),
      ("reservar los resultados para el rector y el consejo directivo, porque son insumos de rendición de cuentas y no de la práctica de aula.",
       "Es incorrecta. Restringir los resultados impide que los docentes los usen para ajustar sus prácticas, y contradice la Guía 34, que los ubica dentro del seguimiento académico de la institución.")],
     "B",
     "En el Cuadro No. 3 de la Guía 34, el proceso de seguimiento académico (gestión académica) tiene como componentes el seguimiento a los resultados académicos, a la asistencia y a los egresados, el uso pedagógico de las evaluaciones externas, las actividades de recuperación y los apoyos pedagógicos adicionales. Por eso los resultados Saber deben analizarse con las áreas para ajustar prácticas y alimentar el plan de mejoramiento, no para clasificar docentes ni para guardarse en la dirección. La CNSC premia el uso formativo de la información.",
     "Guía 34 MEN (2008), Cuadro No. 3, seguimiento académico.",
     "Pruebas Saber: uso pedagógico en el seguimiento académico, no ranking de docentes.",
     [(G34, "uso pedagógico de las evaluaciones externas", "Guía 34, Cuadro No. 3, Seguimiento académico")],
     "Seguimiento académico")

# ------------------------------------------------------------ Ruta de atención: componentes
caso("CK16", "Acciones del comité en el año",
     "Como integrante del comité escolar de convivencia, usted ayuda a organizar las acciones del año. Entre ellas están: un taller permanente con estudiantes de un sector con altos índices de violencia intrafamiliar, para disminuir el impacto de esas condiciones en su comportamiento; "
     "el registro del estado de los casos atendidos; y el caso de una estudiante en alto riesgo de vulneración de derechos que no se ha podido resolver con el manual de convivencia porque la familia no responde.")
item("CO039", "CK16", "GCO-CONV", 3,
     "El taller permanente con estudiantes del sector con violencia intrafamiliar corresponde al componente de la ruta de",
     [("promoción, porque desarrolla competencias ciudadanas y fortalece el ejercicio de los derechos de los estudiantes.",
       "Es incorrecta. La promoción se centra en desarrollar competencias y derechos y define los criterios de convivencia para toda la comunidad; este taller se dirige a disminuir el impacto de condiciones de riesgo específicas."),
      ("atención, porque asiste a estudiantes que ya viven situaciones de violencia en su familia y requieren respuesta inmediata.",
       "Es incorrecta. La atención responde de manera inmediata cuando se presenta un caso de violencia o acoso escolar; el taller es un proceso continuo que se anticipa a esos casos, no la respuesta a uno."),
      ("prevención, porque es un proceso continuo de formación para reducir el impacto del contexto familiar en la conducta.",
       "Es correcta. El artículo 30 de la Ley 1620 define la prevención como un proceso continuo de formación para disminuir el impacto de las condiciones del contexto económico, social, cultural y familiar.")],
     "C",
     "La Ley 1620 de 2013, artículo 30, define cuatro componentes de la Ruta de Atención Integral: promoción (desarrollo de competencias y derechos, clima escolar y criterios de convivencia), prevención (proceso continuo de formación para disminuir el impacto del contexto y que incide sobre las causas), atención (asistencia inmediata cuando se presenta un caso) y seguimiento (reporte al sistema de información). El dato clave del caso es que el taller es permanente y busca disminuir el impacto de condiciones familiares de riesgo: eso es prevención.",
     "Ley 1620 de 2013, art. 30.",
     "Promoción = competencias y derechos; prevención = formación continua frente a factores de riesgo; atención = respuesta inmediata al caso; seguimiento = reporte.",
     [(L1620, "El componente de prevención deberá ejecutarse a través de un proceso continuo de formación para el desarrollo integral del niño, niña y adolescente, con el propósito de disminuir en su comportamiento el impacto de las condiciones del contexto económico, social, cultural y familiar.", "Ley 1620 de 2013, art. 30")],
     "Comité de convivencia")
item("CO040", "CK16", "GCO-CONV", 2,
     "El registro del estado de los casos atendidos corresponde al componente de seguimiento, que según la Ley 1620 consiste en",
     [("reunir mensualmente al comité para revisar los compromisos firmados por los estudiantes y sus familias en cada caso.",
       "Es incorrecta. Revisar compromisos puede ser parte de la gestión del comité, pero la ley define el componente de seguimiento por el reporte de los casos al sistema de información unificado."),
      ("reportar de manera oportuna al Sistema de Información Unificado de Convivencia Escolar el estado de los casos atendidos.",
       "Es correcta. El artículo 30 de la Ley 1620 dice que el componente de seguimiento se centra en el reporte oportuno al Sistema de Información Unificado de Convivencia Escolar del estado de cada caso de atención reportado."),
      ("enviar a la secretaría de educación, al final de cada periodo, un informe con las estadísticas de convivencia de la institución.",
       "Es incorrecta. Un informe periódico a la secretaría no es lo que define la ley; el seguimiento se hace mediante el reporte oportuno del estado de cada caso al sistema de información unificado.")],
     "B",
     "La Ley 1620 de 2013, en su artículo 30, define el componente de seguimiento de manera muy concreta: se centra en el reporte oportuno de la información al Sistema de Información Unificado de Convivencia Escolar, del estado de cada uno de los casos de atención reportados. Las opciones incorrectas describen acciones razonables de gestión, pero no la definición legal. Ojo: en la prueba aparecen opciones «buenas prácticas» que no corresponden al concepto preguntado.",
     "Ley 1620 de 2013, art. 30.",
     "Seguimiento de la ruta = reporte oportuno al Sistema de Información Unificado de Convivencia Escolar.",
     [(L1620, "El componente de seguimiento se centrará en el reporte oportuno de la información al Sistema de Información Unificado de Convivencia Escolar, del estado de cada uno de los casos de atención reportados.", "Ley 1620 de 2013, art. 30")],
     "Comité de convivencia")
item("CO041", "CK16", "GCO-CONV", 3,
     "Sobre la estudiante en alto riesgo cuyo caso no se ha podido resolver con el manual de convivencia, lo que procede es que",
     [("el rector, conforme a la decisión del comité, traslade el caso al ICBF, la comisaría, la personería o la policía de infancia.",
       "Es correcta. El artículo 31 de la Ley 1620 dispone que las situaciones de alto riesgo que no puedan resolverse por las vías del manual sean trasladadas por el rector, de conformidad con las decisiones del comité, a esas entidades."),
      ("el comité cite nuevamente a la familia y, si no asiste, cierre el caso dejando constancia de que la familia no colaboró con el proceso.",
       "Es incorrecta. Cerrar el caso por falta de respuesta de la familia deja a la estudiante sin protección; la ley prevé trasladarlo a entidades externas cuando las vías del manual no son suficientes."),
      ("usted como coordinador haga la denuncia ante la policía de infancia en nombre de la institución, para no esperar la sesión del comité.",
       "Es incorrecta. Cualquier persona puede poner en conocimiento una situación, pero el traslado institucional del caso lo hace el rector de acuerdo con las decisiones del comité escolar de convivencia.")],
     "A",
     "El artículo 31 de la Ley 1620 de 2013 dice que, una vez agotada la instancia institucional, las situaciones de alto riesgo de violencia escolar o vulneración de derechos que no puedan ser resueltas por las vías del manual de convivencia serán trasladadas por el rector, de conformidad con las decisiones del comité, al ICBF, la comisaría de familia, la personería o la policía de infancia y adolescencia, según corresponda. La pregunta evalúa quién traslada y cuándo: el rector, con decisión del comité, cuando el manual no basta.",
     "Ley 1620 de 2013, art. 31.",
     "Alto riesgo que el manual no resuelve: el rector lo traslada a ICBF, comisaría, personería o policía de infancia según decida el comité.",
     [(L1620, "serán trasladadas por el rector de la institución, de conformidad con las decisiones del Comité Escolar de Convivencia, al ICBF, la Comisaria de Familia, la Personería Municipal o Distrital o a la Policía de Infancia y Adolescencia, según corresponda.", "Ley 1620 de 2013, art. 31")],
     "Comité de convivencia")

# ------------------------------------------------------------ Familias, entorno y riesgos
caso("CK17", "Las familias no llegan",
     "A la entrega de informes del primer periodo asistió solo el 35 % de las familias de la jornada de la tarde; muchas trabajan en turnos en el sector petrolero o viven en veredas lejanas. "
     "Además, una empresa de la zona propone un convenio para que los estudiantes de la media técnica hagan prácticas, y el cuerpo de bomberos ofrece apoyo para actualizar el plan escolar de gestión del riesgo ante inundaciones.")
item("CO042", "CK17", "GCO-COMUN", 3,
     "Frente a la baja asistencia de las familias, la acción de nivel avanzado que usted lidera es",
     [("enviar una circular recordando a las familias su deber de asistir a las reuniones y advirtiendo que se dejará constancia de la inasistencia.",
       "Es incorrecta (nivel inferior). Recordar deberes no indaga las causas de la inasistencia ni reconoce las condiciones de trabajo y distancia de las familias; refuerza la distancia entre ellas y la institución."),
      ("encontrarse con las familias para escuchar sus condiciones y concertar con ellas horarios, medios y formas de participación.",
       "Es correcta (nivel avanzado). Lidera encuentros con las familias para identificar sus necesidades y proponer estrategias que atiendan la diversidad de la comunidad, y articula los apoyos con docentes y familias."),
      ("programar una segunda entrega de informes un sábado para las familias que no asistieron, con la misma agenda del primer encuentro.",
       "Es incorrecta (nivel mínimo). Amplía la oportunidad de asistencia, pero decide sin escuchar a las familias y mantiene el mismo formato, sin buscar estrategias acordes con su realidad.")],
     "B",
     "La prueba de ascenso para coordinador valora como acción del criterio de contexto liderar encuentros con las familias para identificar y proponer estrategias que atiendan la diversidad de la comunidad. El nivel avanzado escucha y concierta; el mínimo amplía la oferta sin escuchar, y el inferior se limita a recordar deberes. La Resolución 3842 respalda esta lógica cuando pide al coordinador promover acciones pedagógicas colaborativas con docentes y familias. En el contexto de Yopal, turnos laborales y distancias son condiciones reales que la respuesta debe considerar.",
     "Resolución 3842 de 2022, 1.3.1 (función 11); Guía orientadora de la prueba de ascenso para coordinador (2024).",
     "Familias que no asisten: escuchar sus condiciones y concertar, no advertir ni repetir el mismo formato.",
     [(R3842, "que generen acciones pedagógicas colaborativas en favor de los estudiantes, donde participen docentes y familias.", "Resolución 3842, 1.3.1, función 11")],
     "Familias y entorno", "ascenso 2024")
item("CO043", "CK17", "GCO-COMUN", 2,
     "Según la Guía 34, el convenio de prácticas con la empresa y el apoyo de los bomberos al plan de riesgo se ubican, respectivamente, en",
     [("proyección a la comunidad, en la gestión de la comunidad, y en clima escolar, en la gestión directiva.",
       "Es incorrecta. La proyección a la comunidad son servicios que la institución ofrece a la comunidad, y el clima escolar trata del ambiente y la convivencia; ninguno de los dos corresponde a estas acciones."),
      ("apoyo a la gestión académica, en la gestión administrativa, y en planta física y recursos, en la misma área.",
       "Es incorrecta. Ninguna de las dos acciones es un trámite administrativo: una es una alianza con el sector productivo y la otra una estrategia para prevenir riesgos que afectan a la comunidad."),
      ("relaciones con el entorno, en la gestión directiva, y prevención de riesgos, en la de la comunidad.",
       "Es correcta. En la Guía 34, relaciones con el entorno incluye al sector productivo y está en la gestión directiva; prevención de riesgos, con los riesgos físicos y psicosociales y los programas de seguridad, está en la gestión de la comunidad.")],
     "C",
     "La Guía 34 ubica las alianzas con padres de familia, autoridades educativas, otras instituciones y el sector productivo en el proceso de relaciones con el entorno, dentro de la gestión directiva, porque buscan aunar esfuerzos para cumplir el PEI. La prevención de riesgos físicos y psicosociales y los programas de seguridad son componentes del proceso de prevención de riesgos, en la gestión de la comunidad. Recuerde la pregunta clave: ¿es una alianza para cumplir la misión (directiva) o una acción por el bienestar y la seguridad de la comunidad (comunidad)?",
     "Guía 34 MEN (2008), Cuadro No. 3.",
     "Sector productivo = relaciones con el entorno (directiva); riesgos físicos y psicosociales = prevención de riesgos (comunidad).",
     [(G34, "Padres de familia, autoridades educativas, otras instituciones, sector productivo.", "Guía 34, Cuadro No. 3, Relaciones con el entorno"),
      (G34, "Prevención de riesgos físicos y psicosociales, programas de seguridad.", "Guía 34, Cuadro No. 3, Prevención de riesgos")],
     "Familias y entorno")

# ------------------------------------------------------------ Clima e inclusión
caso("CK18", "Inicio de año en la sede",
     "Al iniciar el año llegan a la sede 60 estudiantes nuevos, varios de ellos migrantes. Uno de ellos tiene baja visión y en su institución anterior presentaba las evaluaciones con el mismo formato que sus compañeros. "
     "El rector le pide a usted organizar la bienvenida de los nuevos estudiantes y revisar cómo se están manejando los casos difíciles de convivencia.")
item("CO044", "CK18", "GDI-AREAS", 2,
     "Según la Guía 34, la inducción a los estudiantes nuevos y el manejo de casos difíciles hacen parte del proceso de",
     [("clima escolar, en la gestión directiva, cuyo propósito es generar un ambiente sano y agradable para el desarrollo de los estudiantes.",
       "Es correcta. La Guía 34 lista en el proceso de clima escolar componentes como la inducción a los nuevos estudiantes, el manual de convivencia, el bienestar de los alumnos y el manejo de conflictos y casos difíciles."),
      ("participación y convivencia, en la gestión de la comunidad, porque ambos aspectos tienen que ver con la integración de los estudiantes.",
       "Es incorrecta. Participación y convivencia trata de la participación de estudiantes y padres y sus instancias; la inducción y el manejo de casos difíciles están listados en el clima escolar."),
      ("inclusión, en la gestión de la comunidad, porque la llegada de estudiantes migrantes exige estrategias de atención a la diversidad.",
       "Es incorrecta. La inclusión atiende a poblaciones diversas y con necesidades particulares, pero los dos componentes por los que se pregunta están ubicados por la guía en el clima escolar.")],
     "A",
     "En el Cuadro No. 3 de la Guía 34, el proceso de clima escolar pertenece a la gestión directiva y se define como generar un ambiente sano y agradable que propicie el desarrollo de los estudiantes, el aprendizaje y la convivencia. Sus componentes incluyen pertenencia y participación, ambiente físico, inducción a los nuevos estudiantes, motivación hacia el aprendizaje, manual de convivencia, actividades extracurriculares, bienestar de los alumnos y manejo de conflictos y casos difíciles. Aunque el caso menciona migrantes, la pregunta es por la inducción y los casos difíciles.",
     "Guía 34 MEN (2008), Cuadro No. 3, clima escolar.",
     "Inducción de estudiantes nuevos y casos difíciles = clima escolar (gestión directiva).",
     [(G34, "ambiente físico, inducción a los nuevos estudiantes, motivación hacia el aprendizaje, manual de convivencia, actividades extracurriculares, bienestar de los alumnos, manejo de conflictos y casos difíciles.", "Guía 34, Cuadro No. 3, Clima escolar")],
     "Áreas de gestión")
item("CO045", "CK18", "GCO-INCL", 3,
     "Para el estudiante con baja visión, la acción que usted promueve es",
     [("aplicarle las mismas evaluaciones que a sus compañeros, como en la institución anterior, para no generar diferencias en el grupo.",
       "Es incorrecta. Dar el mismo formato a quien lo necesita adaptado no es igualdad sino una barrera; el Decreto 1421 obliga a los ajustes razonables basados en las necesidades específicas del estudiante."),
      ("eximirlo de las evaluaciones escritas y valorar su desempeño solo con la participación en clase, mientras se define su situación.",
       "Es incorrecta. Eximir al estudiante rebaja las exigencias en lugar de garantizar el acceso; los ajustes buscan que pueda demostrar sus aprendizajes en igualdad de condiciones, no excluirlo de la evaluación."),
      ("acordar con los docentes ajustes razonables en las evaluaciones, según sus necesidades, y registrarlos en el PIAR.",
       "Es correcta. El Decreto 1421 define los ajustes razonables como acciones, adaptaciones y apoyos basados en las necesidades específicas de cada estudiante, y el PIAR es la herramienta donde se planean y registran.")],
     "C",
     "El Decreto 1421 de 2017 define los ajustes razonables como las acciones, adaptaciones, estrategias, apoyos, recursos o modificaciones necesarias y adecuadas del sistema educativo y la gestión escolar, basadas en las necesidades específicas de cada estudiante. Para la baja visión, eso puede significar ampliar el formato, dar más tiempo o usar apoyos tecnológicos, y se planea en el PIAR. La prueba de ascenso valora como acción del coordinador promover y facilitar ajustes para los estudiantes que requieren apoyos específicos. Desconfíe de las opciones que igualan formatos o eximen al estudiante.",
     "Decreto 1421 de 2017, art. 2.3.3.5.1.4, numeral 4; Guía orientadora de la prueba de ascenso para coordinador (2024).",
     "Ajustes razonables: según las necesidades del estudiante y registrados en el PIAR; ni igualar formatos ni eximir.",
     [(D1421, "Ajustes razonables: son las acciones, adaptaciones, estrategias, apoyos,", "Decreto 1421 de 2017, art. 2.3.3.5.1.4"),
      (D1421, "basadas en necesidades específicas de cada estudiante", "Decreto 1421 de 2017, art. 2.3.3.5.1.4")],
     "Inclusión", "ascenso 2024")

# ------------------------------------------------------------ Psicotécnica (directivos), estilo ascenso: apoyo emocional y liderazgo
caso("CK19", "Una tarde difícil",
     "Al terminar la jornada, una docente llega a coordinación muy afectada: un padre de familia le gritó en la puerta del salón porque su hijo perdió dos asignaturas. Ella le dice a usted que se siente desautorizada y que está pensando en pedir traslado. "
     "Esa misma semana usted debe liderar la reunión de docentes de la jornada, en la que varios quieren cambiar las fechas de entrega de notas acordadas por el consejo académico.")
item("CO046", "CK19", "PSI-COMRI", 2,
     "Con la docente afectada, usted",
     [("le recomienda calmarse y no tomar decisiones apresuradas, y le recuerda que estos episodios son normales en el trabajo con familias.",
       "Es incorrecta. Aunque busca tranquilizarla, minimiza lo que siente y normaliza la agresión; no muestra escucha empática ni ofrece acciones institucionales frente a lo ocurrido."),
      ("la escucha con atención, reconoce cómo se siente y acuerda con ella citar al padre, con su acompañamiento, para tratar lo ocurrido.",
       "Es correcta. Escucha y comprende el punto de vista de la docente, maneja la situación con empatía y ofrece un mecanismo asertivo y acompañado para resolver el conflicto con el padre."),
      ("cita al padre al día siguiente para llamarle la atención por su comportamiento y le informa a la docente que el asunto ya quedó resuelto.",
       "Es incorrecta. Actúa con rapidez, pero sin escuchar a la docente ni involucrarla en la solución, y enfoca la respuesta en la sanción del padre más que en el diálogo para resolver el conflicto.")],
     "B",
     "La competencia de comunicación y relaciones interpersonales, tal como la describe la guía de la CNSC, incluye escuchar con atención, comprender los puntos de vista de los demás, manejar y expresar adecuadamente las emociones e identificar y comprender las de otros. La prueba de ascenso para coordinador también valora reconocer el apoyo emocional, la escucha y la empatía como base de la relación con la comunidad. La opción correcta combina escucha, reconocimiento de la emoción y una salida asertiva y acompañada; las demás minimizan o resuelven sin la docente.",
     "Guía de orientación al aspirante CNSC 2022 (competencia comunicación y relaciones interpersonales); Guía orientadora de la prueba de ascenso para coordinador (2024).",
     "Docente afectado: escuchar, reconocer la emoción y acompañar una salida asertiva.",
     [("guia_orientacion_cnsc_2022", "Habilidad para intercambiar con efectividad y empatía conceptos, criterios e ideas", "Guía de orientación CNSC 2022, ejemplo 5")],
     "Comunicación y relaciones interpersonales", "ascenso 2024")
item("CO047", "CK19", "PSI-LID", 3,
     "En la reunión de docentes que quieren cambiar las fechas de entrega de notas acordadas por el consejo académico, usted",
     [("acepta el cambio propuesto por la mayoría de la reunión y lo comunica a las familias, porque refleja el sentir de los docentes de la jornada.",
       "Es incorrecta. Valora la participación, pero desconoce una decisión del consejo académico, que es la instancia que la tomó; un directivo no puede revocarla con el voto de una reunión de jornada."),
      ("mantiene las fechas sin discusión y recuerda a los docentes que las decisiones del consejo académico son de obligatorio cumplimiento.",
       "Es incorrecta. Respeta la instancia, pero cierra el diálogo y no recoge las razones de los docentes, lo que debilita la confianza y el trabajo en equipo que debe promover un líder."),
      ("escucha los argumentos, recoge la propuesta por escrito y se compromete a llevarla al consejo académico, con fecha de respuesta.",
       "Es correcta. Ejerce liderazgo: escucha, canaliza la propuesta por la instancia que tomó la decisión y genera confianza al definir un camino claro, sin imponer ni desconocer al consejo académico.")],
     "C",
     "En la psicotécnica para directivos, el liderazgo se reconoce cuando el directivo orienta al equipo hacia las metas institucionales, escucha y canaliza las iniciativas por las instancias que corresponden. Las dos opciones incorrectas son extremos que la CNSC suele penalizar: ceder a la mayoría por encima de la instancia competente, o imponer la norma sin diálogo. La correcta escucha, canaliza al consejo académico y da claridad sobre el proceso, lo que fortalece la confianza del equipo.",
     "Guía de orientación al aspirante CNSC 2022 (lógica de las competencias comportamentales); Resolución 3842 de 2022.",
     "Liderazgo: ni ceder ni imponer; escuchar y canalizar por la instancia competente.",
     [], "Liderazgo")

lote = {"id": "coord-2026-11-16b", "fecha": "2026-11-16", "cargo": "coordinador",
        "nota": "Formatos de los concursos pasados: ingreso 2022 (3 opciones, una correcta) y ascenso 2024 (cada opción es un nivel de desempeño; aquí la correcta es la de nivel avanzado).",
        "casos": casos, "fichas": [], "items": items}
json.dump(lote, open(os.path.join(RAIZ, "data", "lotes", "coord-2026-11-16b.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(casos), "casos ·", len(items), "ítems")
