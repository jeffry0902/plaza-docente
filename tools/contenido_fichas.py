# -*- coding: utf-8 -*-
"""Fichas de estudio (Estudia y responde) y preguntas de conocimiento del lote piloto.
Cada ficha: lectura propia + citas textuales verificables + 2 preguntas de comprensión.
Formato de opción: (texto, justificación). La primera justificación que empieza por
'Es correcta' indica la clave; el constructor asigna letras A/B/C en el orden escrito."""

G30 = "guia30_mineducacion_2008"
OCT = "orientaciones_tecnologia_2022"
D1075 = "decreto_1075_2015"
D1965 = "decreto_1965_2013"
L115 = "ley_115_1994"
D1278 = "decreto_1278_2002"
R3842 = "resolucion_3842_2022_ocr"
ANX = "anexo_tecnico_2026"
L1098 = "ley_1098_2006"
GCNSC = "guia_orientacion_cnsc_2022"

FICHAS = [
 dict(id="F01", familia="DIS-CONC", titulo="Artefactos, procesos y sistemas",
  lectura="La Guía 30 del MEN insiste en que la tecnología no es solo computadores. La organiza en tres tipos de productos: los artefactos (objetos que potencian la acción humana: un martillo, una licuadora, un celular), los procesos (secuencias de operaciones que transforman recursos: fabricar pan, reciclar plástico, potabilizar agua) y los sistemas (conjuntos de elementos relacionados que funcionan juntos para un objetivo: la red eléctrica, el transporte público, internet). Un mismo tema puede mirarse desde los tres: la bicicleta es un artefacto, su fabricación es un proceso y la ciclovía con señales, usuarios y normas es un sistema.",
  puntos=["Artefacto = objeto (lo puedo tocar y usar).", "Proceso = secuencia de pasos que transforma algo (tiene un antes y un después).", "Sistema = varios elementos relacionados que logran juntos un objetivo (si quito uno, el todo se afecta).", "Trampa CNSC: confundir el producto (artefacto) con la forma de producirlo (proceso)."],
  citas=[(G30, "Los artefactos: son dispositivos, herramientas, aparatos, instrumentos y máquinas que potencian la acción humana.", "Guía 30, p. 6"),
         (G30, "Los procesos: son fases sucesivas de operaciones que permiten la transformación de recursos", "Guía 30, p. 6"),
         (G30, "Los sistemas: son conjuntos o grupos de elementos ligados entre sí por relaciones estructurales o funcionales, diseñados para lograr colectivamente un objetivo.", "Guía 30, p. 7")],
  preguntas=[
   dict(enunciado="Según la Guía 30, la potabilización del agua en la planta del acueducto, entendida como la secuencia de captación, filtrado y desinfección, es un ejemplo de", opciones=[
     ("proceso, porque es una sucesión de operaciones que transforma un recurso para obtener un producto.", "Es correcta. La Guía 30 define los procesos como fases sucesivas de operaciones que transforman recursos."),
     ("artefacto, porque el agua tratada es un producto que la comunidad utiliza en la vida diaria.", "Es incorrecta. El artefacto es un dispositivo o herramienta; aquí se describe la secuencia de pasos, no un objeto."),
     ("sistema, porque cualquier actividad que se realiza en varias etapas constituye un sistema tecnológico.", "Es incorrecta. Un sistema son elementos relacionados que funcionan juntos; tener etapas es lo propio de un proceso.")],
    citas=[(G30, "Los procesos: son fases sucesivas de operaciones que permiten la transformación de recursos", "Guía 30, p. 6")]),
   dict(enunciado="De acuerdo con la Guía 30, un ejemplo de sistema tecnológico es", opciones=[
     ("un destornillador, porque es una herramienta que potencia la acción humana al ensamblar objetos.", "Es incorrecta. Una herramienta es un artefacto."),
     ("la red de generación y distribución de energía eléctrica, porque integra componentes, procesos y flujos de energía.", "Es correcta. La Guía 30 menciona la generación y distribución de la energía eléctrica como ejemplo de sistema tecnológico."),
     ("la elaboración de una mesa, porque implica cortar, lijar y ensamblar la madera en un orden determinado.", "Es incorrecta. Una secuencia de operaciones es un proceso.")],
    citas=[(G30, "La generación y distribución de la energía eléctrica, las redes de transporte, las tecnologías de la información y la comunicación, el suministro de alimentos y las organizaciones, son ejemplos de sistemas tecnológicos.", "Guía 30, p. 7")])]),

 dict(id="F02", familia="DIS-INNOV", titulo="Técnica, tecnología, ciencia; invención, innovación y descubrimiento",
  lectura="La Guía 30 diferencia conceptos que en la vida diaria usamos como sinónimos. La técnica es el saber hacer práctico (el artesano que sabe tejer un sombrero); la tecnología agrega el saber por qué se hace así, por eso está más ligada a la ciencia. La ciencia busca entender el mundo natural; la tecnología lo modifica para satisfacer necesidades. También distingue tres palabras clave: invención (algo que no existía: el primer teléfono), innovación (mejorar algo que ya existe y llevarlo al uso: un teléfono más rápido) y descubrimiento (hallar algo que ya existía pero no conocíamos: la penicilina).",
  puntos=["Técnica = saber hacer (empírico, artesanal). Tecnología = saber hacer + por qué.", "Ciencia = entender el mundo natural. Tecnología = transformarlo para satisfacer necesidades.", "Invención = nuevo, no existía. Innovación = mejora de lo existente. Descubrimiento = hallazgo de algo que ya estaba."],
  citas=[(G30, "De este origen se rescata la idea de la técnica como el saber-hacer, que surge en forma empírica o artesanal.", "Guía 30, p. 7"),
         (G30, "la ciencia busca entender el mundo natural y la tecnología modifica el mundo para satisfacer necesidades humanas.", "Guía 30, p. 7"),
         (G30, "La innovación implica introducir cambios para mejorar artefactos, procesos y sistemas existentes", "Guía 30, p. 8"),
         (G30, "La invención corresponde a un nuevo producto, sistema o proceso inexistente hasta el momento.", "Guía 30, p. 8"),
         (G30, "El descubrimiento es un hallazgo de un fenómeno que estaba oculto o era desconocido", "Guía 30, p. 8")],
  preguntas=[
   dict(enunciado="Un grupo de estudiantes adapta un molino de viento tradicional para que, además de bombear agua, cargue baterías con un pequeño generador. Según la Guía 30, esto es", opciones=[
     ("una invención, porque el molino resultante tiene una función que antes no cumplía.", "Es incorrecta. La invención es un producto inexistente hasta el momento; el molino ya existía."),
     ("un descubrimiento, porque los estudiantes hallaron una nueva forma de aprovechar el viento.", "Es incorrecta. El descubrimiento es el hallazgo de un fenómeno oculto o desconocido, como la gravedad."),
     ("una innovación, porque introduce cambios para mejorar un artefacto que ya existía.", "Es correcta. La innovación implica introducir cambios para mejorar artefactos, procesos y sistemas existentes.")],
    citas=[(G30, "La innovación implica introducir cambios para mejorar artefactos, procesos y sistemas existentes", "Guía 30, p. 8")]),
   dict(enunciado="Según la Guía 30, la diferencia entre ciencia y tecnología está en su propósito, porque", opciones=[
     ("la ciencia busca entender el mundo natural y la tecnología lo modifica para satisfacer necesidades humanas.", "Es correcta. Así lo plantea la Guía 30 citando al National Research Council."),
     ("la ciencia usa el método experimental y la tecnología se basa únicamente en la experiencia práctica.", "Es incorrecta. El saber empírico describe a la técnica, y la guía afirma que ciencia y tecnología comparten procesos de construcción de conocimiento."),
     ("la ciencia produce conocimientos teóricos y la tecnología produce exclusivamente aparatos electrónicos.", "Es incorrecta. La Guía 30 rechaza reducir la tecnología a dispositivos electrónicos.")],
    citas=[(G30, "la ciencia busca entender el mundo natural y la tecnología modifica el mundo para satisfacer necesidades humanas.", "Guía 30, p. 7")])]),

 dict(id="F03", familia="DIS-COMP", titulo="Los cuatro componentes del área",
  lectura="Todo el currículo de Tecnología e Informática en Colombia se organiza en cuatro componentes, desde la Guía 30 (2008) hasta las Orientaciones Curriculares (2022). 1) Naturaleza y evolución: qué es la tecnología, sus conceptos (sistema, proceso, función, innovación, algoritmo) y su historia. 2) Apropiación y uso (o uso y apropiación): utilizar la tecnología de forma adecuada, segura y crítica. 3) Solución de problemas: detectar fallas, diseñar, construir y evaluar soluciones. 4) Tecnología (informática) y sociedad: actitudes, valoración de impactos, ética y participación. Las tablas de la Guía 30 están organizadas por grupos de grados; en cada uno hay una competencia por componente y ejemplos de desempeños.",
  puntos=["Conceptos e historia → Naturaleza y evolución.", "Usar bien y con seguridad → Apropiación y uso.", "Detectar fallas, diseñar, construir → Solución de problemas.", "Impactos, ética, ambiente, participación → Tecnología y sociedad.", "Grupos de grados: 1°-3°, 4°-5°, 6°-7°, 8°-9°, 10°-11°."],
  citas=[(G30, "Se refiere a las características y objetivos de la tecnología, a sus conceptos fundamentales", "Guía 30, p. 14"),
         (G30, "Se trata de la utilización adecuada, pertinente y crítica de la tecnología", "Guía 30, p. 14"),
         (G30, "Se refiere al manejo de estrategias en y para la identificación, formulación y solución de problemas con tecnología", "Guía 30, p. 14"),
         (G30, "Las tablas están organizadas en cinco grupos de grados.", "Guía 30, p. 13")],
  preguntas=[
   dict(enunciado="El desempeño «Ensamblo y desarmo artefactos y dispositivos sencillos siguiendo instrucciones gráficas» pertenece, en la Guía 30, al componente de", opciones=[
     ("tecnología y sociedad, porque el trabajo con artefactos tiene efectos en la vida de la comunidad.", "Es incorrecta. Ese componente trata actitudes, valoración social y participación."),
     ("solución de problemas con tecnología, porque desarmar y ensamblar permite comprender cómo funcionan y detectar fallas.", "Es correcta. En la tabla de 1° a 3°, este desempeño aparece en la columna de solución de problemas con tecnología."),
     ("naturaleza y evolución de la tecnología, porque permite conocer los artefactos que se usaban en el pasado.", "Es incorrecta. Ese componente trata conceptos e historia, no la manipulación de artefactos.")],
    citas=[(G30, "Ensamblo y desarmo artefactos y dispositivos sencillos siguiendo instrucciones gráficas.", "Guía 30, p. 17")]),
   dict(enunciado="Según la Guía 30, el componente «Apropiación y uso de la tecnología» se refiere a", opciones=[
     ("la reflexión sobre los impactos sociales, ambientales y culturales de los productos tecnológicos.", "Es incorrecta. Esa es la descripción del componente Tecnología y sociedad."),
     ("la comprensión de los conceptos fundamentales de la tecnología y de su evolución en la historia.", "Es incorrecta. Esa es la descripción del componente Naturaleza y evolución."),
     ("la utilización adecuada, pertinente y crítica de artefactos, productos, procesos y sistemas tecnológicos.", "Es correcta. Así define la Guía 30 este componente.")],
    citas=[(G30, "Se trata de la utilización adecuada, pertinente y crítica de la tecnología", "Guía 30, p. 14")])]),

 dict(id="F04", familia="DIS-SIST", titulo="Sistemas y control por realimentación",
  lectura="Un sistema automático tiene un objetivo (mantener una temperatura, un nivel de agua, una velocidad). Para lograrlo necesita: un sensor que mide lo que pasa, un controlador que compara esa medida con un valor de referencia y decide, y un actuador que ejecuta la orden (motor, válvula, resistencia). Si la información de la salida vuelve al controlador para corregir, hay realimentación y el sistema es de lazo cerrado (la nevera con termostato). Si no vuelve, es de lazo abierto (una lavadora que gira 20 minutos aunque la ropa ya esté limpia). La Guía 30 pide en 6°-7° describir el rol de la realimentación, y en 10°-11° analizar sistemas de control basados en ella.",
  puntos=["Sensor → mide. Controlador → compara y decide. Actuador → ejecuta.", "Lazo cerrado = con realimentación (corrige solo).", "Lazo abierto = sin realimentación (hace lo programado sin verificar)."],
  citas=[(G30, "Describo el rol de la realimentación en el funcionamiento automático de algunos sistemas.", "Guía 30, 6° a 7°"),
         (G30, "Identifico artefactos que contienen sistemas de control con realimentación.", "Guía 30, 8° a 9°")],
  preguntas=[
   dict(enunciado="Una plancha de ropa se apaga sola cuando alcanza la temperatura elegida y se enciende de nuevo cuando se enfría. Para explicarlo en grado séptimo, el docente debe señalar que la plancha", opciones=[
     ("funciona en lazo abierto, porque el usuario elige la temperatura antes de empezar a planchar.", "Es incorrecta. Elegir un valor no define el tipo de lazo; lo define si la salida se mide y se usa para corregir."),
     ("funciona con realimentación, porque un elemento mide la temperatura y esa información se usa para encender o apagar la resistencia.", "Es correcta. La medida de la salida vuelve al control para corregir: es un sistema de control con realimentación."),
     ("no es un sistema, porque es un solo artefacto y los sistemas siempre están formados por varios artefactos.", "Es incorrecta. Un artefacto puede contener un sistema de control; la Guía 30 pide identificar artefactos que contienen sistemas de control con realimentación.")],
    citas=[(G30, "Identifico artefactos que contienen sistemas de control con realimentación.", "Guía 30, 8° a 9°")]),
   dict(enunciado="En un sistema de alumbrado que enciende las luces cuando un sensor detecta poca luz natural, el elemento que cumple la función de actuador es", opciones=[
     ("el sensor de luz, porque es el elemento que detecta cuándo oscurece.", "Es incorrecta. El sensor mide; no ejecuta la acción."),
     ("el interruptor automático que conecta las lámparas, porque ejecuta la orden de encender.", "Es correcta. El actuador es el elemento que ejecuta la acción ordenada por el controlador."),
     ("el valor mínimo de luz programado, porque determina el momento del encendido.", "Es incorrecta. Ese valor es la referencia con la que compara el controlador.")],
    citas=[(G30, "Describo el rol de la realimentación en el funcionamiento automático de algunos sistemas.", "Guía 30, 6° a 7°")])]),

 dict(id="F05", familia="DIS-DATOS", titulo="Informática, TIC y el sistema binario",
  lectura="Para la Guía 30, la informática es el conjunto de conocimientos que permiten acceder, buscar y manejar información con procesadores, y hace parte de un campo más amplio: las TIC (teléfono, radio, televisión, computadores, redes, internet). Los computadores representan todo con dos estados (0 y 1): eso es el sistema binario. Un bit tiene 2 estados; con n bits hay 2 elevado a la n combinaciones. Un byte son 8 bits, o sea 256 combinaciones, suficientes para codificar letras, números y signos. La guía pide en 8°-9° identificar artefactos de tecnología digital y describir el sistema binario.",
  puntos=["Informática ⊂ TIC.", "1 bit = 2 estados; 8 bits = 1 byte = 256 combinaciones.", "Para pasar a binario se usan potencias de 2: 1, 2, 4, 8, 16, 32, 64, 128.", "Ejemplo: 13 = 8 + 4 + 1 = 1101 en binario."],
  citas=[(G30, "La informática se refiere al conjunto de conocimientos científicos y tecnológicos que hacen posible el acceso, la búsqueda y el manejo de la información por medio de procesadores.", "Guía 30, p. 9"),
         (G30, "La informática hace parte de un campo más amplio denominado Tecnologías de la Información y la Comunicación (TIC)", "Guía 30, p. 9"),
         (G30, "Identifico artefactos basados en tecnología digital y describo el sistema binario utilizado en dicha tecnología.", "Guía 30, 8° a 9°")],
  preguntas=[
   dict(enunciado="Según la Guía 30, la relación entre la informática y las TIC es que", opciones=[
     ("la informática hace parte de un campo más amplio denominado Tecnologías de la Información y la Comunicación.", "Es correcta. Así lo establece la Guía 30."),
     ("las TIC son una rama de la informática dedicada exclusivamente a las redes y a internet.", "Es incorrecta. Es al revés: la informática hace parte de las TIC."),
     ("la informática y las TIC son sinónimos que se refieren al uso escolar de los computadores.", "Es incorrecta. La guía las distingue y advierte que los computadores no son sinónimo de tecnología.")],
    citas=[(G30, "La informática hace parte de un campo más amplio denominado Tecnologías de la Información y la Comunicación (TIC)", "Guía 30, p. 9")]),
   dict(enunciado="Al explicar el sistema binario en grado octavo, el número 13 se representa como", opciones=[
     ("1011, porque se suman las posiciones 8, 2 y 1 de derecha a izquierda.", "Es incorrecta. 1011 = 8 + 2 + 1 = 11."),
     ("1110, porque se suman las posiciones 8, 4 y 2 de derecha a izquierda.", "Es incorrecta. 1110 = 8 + 4 + 2 = 14."),
     ("1101, porque se suman las posiciones 8, 4 y 1 de derecha a izquierda.", "Es correcta. 8 + 4 + 1 = 13.")],
    citas=[(G30, "Identifico artefactos basados en tecnología digital y describo el sistema binario utilizado en dicha tecnología.", "Guía 30, 8° a 9°")])]),

 dict(id="F06", familia="DIS-DISENO", titulo="El diseño: especificaciones, restricciones y alternativas",
  lectura="Diseñar es resolver un problema con recursos limitados, dentro de condiciones y restricciones, para cumplir unas especificaciones. Especificaciones: lo que la solución debe lograr (cargar 2 kilos, funcionar sin electricidad). Restricciones: los límites (presupuesto, materiales, tamaño, tiempo). El proceso de diseño tiene momentos: identificar el problema, buscar información y generar ideas, elegir una alternativa, construirla, probarla y mejorarla. La Guía 30 insiste en que no hay soluciones perfectas: un mismo problema admite varias soluciones según los criterios que se prioricen.",
  puntos=["Especificación = qué debe lograr.", "Restricción = límites (costo, material, tiempo, tamaño).", "Momentos: problema → ideas → selección → prototipo → prueba → mejora.", "No hay soluciones perfectas: se comparan alternativas con criterios."],
  citas=[(G30, "Con tal fin se utilizan recursos limitados, en el marco de condiciones y restricciones, para dar respuesta a las especificaciones deseadas.", "Guía 30, p. 9"),
         (G30, "Reconozco que no hay soluciones perfectas, y que pueden existir varias soluciones a un mismo problema según los criterios utilizados y su ponderación.", "Guía 30, 8° a 9°")],
  preguntas=[
   dict(enunciado="Un docente pide diseñar un comedero automático para mascotas que entregue alimento dos veces al día, con un costo máximo de $40.000. En este planteamiento, «costo máximo de $40.000» es", opciones=[
     ("una especificación, porque describe lo que el comedero debe lograr para la mascota.", "Es incorrecta. Lo que el comedero debe lograr es entregar alimento dos veces al día."),
     ("una restricción, porque limita los recursos con los que se puede construir la solución.", "Es correcta. Según la Guía 30, el diseño trabaja con recursos limitados en el marco de condiciones y restricciones."),
     ("un criterio de evaluación, porque permite calificar qué tan bien quedó el prototipo.", "Es incorrecta. Es un límite del problema de diseño, no un criterio de calificación.")],
    citas=[(G30, "Con tal fin se utilizan recursos limitados, en el marco de condiciones y restricciones, para dar respuesta a las especificaciones deseadas.", "Guía 30, p. 9")]),
   dict(enunciado="Dos equipos presentan soluciones distintas para el mismo problema y discuten cuál es «la correcta». Según la Guía 30, el docente debe orientarlos a reconocer que", opciones=[
     ("la solución correcta es la que cumple el mayor número de especificaciones con el menor costo posible.", "Es incorrecta. Presenta un único criterio como absoluto; la guía dice que depende de los criterios y su ponderación."),
     ("pueden existir varias soluciones a un mismo problema, según los criterios utilizados y su ponderación.", "Es correcta. Es un desempeño explícito de la Guía 30 para 8° a 9°."),
     ("el docente debe definir cuál solución es correcta para evitar que la discusión afecte el trabajo.", "Es incorrecta. Quita a los estudiantes el análisis de criterios que la guía busca desarrollar.")],
    citas=[(G30, "Reconozco que no hay soluciones perfectas, y que pueden existir varias soluciones a un mismo problema según los criterios utilizados y su ponderación.", "Guía 30, 8° a 9°")])]),

 dict(id="F07", familia="DIS-FALLAS", titulo="Detección de fallas: prueba y descarte",
  lectura="Detectar fallas es una competencia del componente de solución de problemas que crece con los grados: en 1°-3° el niño detecta fallas simples y avisa a un adulto; en 6°-7° sigue procedimientos de prueba y descarte; en 10°-11° formula hipótesis sobre las fallas y propone cómo repararlas. Prueba y descarte significa probar cada parte por separado y eliminar las que funcionan hasta encontrar la que falla. El papel del docente es orientar ese procedimiento, no reparar por el estudiante.",
  puntos=["1°-3°: detecta fallas simples, actúa de forma segura e informa.", "6°-7°: prueba y descarte.", "10°-11°: hipótesis + prueba y descarte + estrategias de reparación.", "El docente orienta; el estudiante diagnostica."],
  citas=[(G30, "Detecto fallas simples en el funcionamiento de algunos artefactos sencillos, actúo de manera segura frente a ellos e informo a los adultos mis observaciones.", "Guía 30, 1° a 3°"),
         (G30, "Detecto fallas en artefactos, procesos y sistemas tecnológicos, siguiendo procedimientos de prueba y descarte, y propongo estrategias de solución.", "Guía 30, 6° a 7°")],
  preguntas=[
   dict(enunciado="Según la Guía 30, lo que se espera de un estudiante de grado segundo cuando un juguete eléctrico deja de funcionar es que", opciones=[
     ("lo desarme y cambie las piezas dañadas siguiendo un procedimiento de prueba y descarte.", "Es incorrecta. La prueba y descarte se espera desde 6°-7°."),
     ("formule hipótesis sobre la causa de la falla y proponga estrategias para repararlo.", "Es incorrecta. Formular hipótesis sobre fallas corresponde a 10°-11°."),
     ("detecte la falla simple, actúe de manera segura frente al artefacto e informe a un adulto lo que observó.", "Es correcta. Es el desempeño de 1° a 3° en solución de problemas.")],
    citas=[(G30, "Detecto fallas simples en el funcionamiento de algunos artefactos sencillos, actúo de manera segura frente a ellos e informo a los adultos mis observaciones.", "Guía 30, 1° a 3°")]),
   dict(enunciado="Un estudiante de grado séptimo no logra que funcione el circuito de su maqueta. La orientación coherente con la Guía 30 para ese grado es pedirle que", opciones=[
     ("pruebe por separado la pila, los cables y el bombillo, y descarte los que funcionan hasta encontrar el elemento que falla.", "Es correcta. Es el procedimiento de prueba y descarte que la Guía 30 propone para 6° a 7°."),
     ("reemplace todos los componentes del circuito por unos nuevos para asegurarse de que la maqueta funcione.", "Es incorrecta. Cambia todo sin diagnosticar; no desarrolla la competencia."),
     ("le entregue la maqueta al docente para que identifique el problema y le explique después la solución.", "Es incorrecta. El docente asume la tarea que debe desarrollar el estudiante.")],
    citas=[(G30, "Detecto fallas en artefactos, procesos y sistemas tecnológicos, siguiendo procedimientos de prueba y descarte, y propongo estrategias de solución.", "Guía 30, 6° a 7°")])]),

 dict(id="F08", familia="DIS-ALGO", titulo="Pensamiento computacional y programación",
  lectura="Las Orientaciones Curriculares (2022) proponen la programación como estrategia para desarrollar el pensamiento computacional: descomponer un problema, reconocer patrones, abstraer lo importante y escribir algoritmos (secuencias ordenadas de pasos). Herramientas como Scratch o Code.org permiten programar con bloques. Cuando no hay computadores, se puede trabajar el pensamiento computacional desconectado con juegos y retos basados en reglas. Conceptos básicos que debes dominar: secuencia (pasos en orden), condicional (si… entonces…), ciclo o bucle (repetir), variable (lugar donde se guarda un valor), contador y acumulador.",
  puntos=["Algoritmo = pasos ordenados y finitos para resolver un problema.", "Condicional: si pasa X, haz Y. Ciclo: repite N veces o mientras se cumpla algo.", "Contador suma de a 1; acumulador suma valores variables.", "Desconectado = sin computador, con juegos de reglas."],
  citas=[(OCT, "La programación es una forma de expresión y una estrategia que permite dar forma a las ideas", "Orientaciones Curriculares, 4.3.3"),
         (OCT, "Véase, por ejemplo, los usos pedagógicos de Scratch y Code.org.", "Orientaciones Curriculares, 4.3.3"),
         (OCT, "desarrollo del pensamiento computacional sin computadores es un enfoque didáctico que no requiere de equipos computacionales para su implementación", "Orientaciones Curriculares, 4.3.3")],
  preguntas=[
   dict(enunciado="En un programa de Scratch, el bloque «si temperatura > 30 entonces encender ventilador» es un ejemplo de", opciones=[
     ("un ciclo, porque el ventilador se encenderá cada vez que el programa se ejecute.", "Es incorrecta. Un ciclo repite instrucciones; aquí se toma una decisión."),
     ("un condicional, porque la acción se ejecuta solo cuando se cumple una condición.", "Es correcta. «Si… entonces…» es la estructura condicional."),
     ("una variable, porque la temperatura es un dato que cambia durante la ejecución.", "Es incorrecta. La temperatura sí es una variable, pero el bloque completo es un condicional.")],
    citas=[(OCT, "Véase, por ejemplo, los usos pedagógicos de Scratch y Code.org.", "Orientaciones Curriculares, 4.3.3")]),
   dict(enunciado="Según las Orientaciones Curriculares, el pensamiento computacional sin computadores", opciones=[
     ("reemplaza la formación con equipos en las instituciones que no tienen conectividad permanente.", "Es incorrecta. El documento aclara que no pretende sustituir el trabajo con equipos de cómputo."),
     ("es una estrategia exclusiva de preescolar, antes de que los niños usen dispositivos digitales.", "Es incorrecta. Se propone para niños y jóvenes, no solo para preescolar."),
     ("es un enfoque didáctico que no requiere equipos y usa recursos al alcance, como juegos basados en reglas.", "Es correcta. Así lo describen las Orientaciones Curriculares en el numeral 4.3.3.")],
    citas=[(OCT, "desarrollo del pensamiento computacional sin computadores es un enfoque didáctico que no requiere de equipos computacionales para su implementación", "Orientaciones Curriculares, 4.3.3")])]),

 dict(id="F09", familia="DIS-DIDAC", titulo="Estrategias didácticas propias del área",
  lectura="Las Orientaciones Curriculares (2022) describen estrategias didácticas específicas del área. Construcción-fabricación: pasar de las ideas a modelos, prototipos, simulaciones o programas. Diseño y rediseño: partir de un problema o de un producto existente para mejorarlo. Análisis de productos tecnológicos: partir de un producto terminado y descomponerlo en sus partes para entender sus decisiones de diseño. Enfoque CTS (ciencia, tecnología y sociedad): reflexión crítica sobre impactos. También mencionan estrategias emergentes: movimiento maker, STEM+ y la programación. Todas se integran en proyectos tecnológicos o Actividades Tecnológicas Escolares (ATE).",
  puntos=["Análisis de productos = desarmar y preguntarse por qué.", "Diseño y rediseño = crear o mejorar.", "Construcción-fabricación = materializar ideas.", "CTS = debatir impactos.", "STEM+ = integrar áreas en proyectos reales."],
  citas=[(OCT, "Se parte de un producto tecnológico terminado para descomponerlo en sus partes", "Orientaciones Curriculares, 4.2.3"),
         (OCT, "La construcción-fabricación como estrategia didáctica para la enseñanza y el aprendizaje de la tecnología y la informática centra su interés en el paso del mundo de las ideas y los diseños, al mundo de las realizaciones gráficas", "Orientaciones Curriculares, 4.2.1")],
  preguntas=[
   dict(enunciado="Una docente lleva una licuadora en desuso al aula para que los estudiantes la desarmen, identifiquen sus partes y discutan por qué se eligieron sus materiales. Según las Orientaciones Curriculares, está aplicando la estrategia de", opciones=[
     ("construcción-fabricación, porque los estudiantes manipulan físicamente un artefacto.", "Es incorrecta. Esa estrategia pasa de las ideas a realizaciones concretas; aquí se examina un producto existente."),
     ("análisis de productos tecnológicos, porque parte de un producto terminado y lo descompone en sus partes.", "Es correcta. Es la definición del numeral 4.2.3 de las Orientaciones Curriculares."),
     ("diseño y rediseño, porque los estudiantes reflexionan sobre las decisiones de diseño de la licuadora.", "Es incorrecta. El rediseño exige proponer mejoras al producto, y el enunciado no lo plantea.")],
    citas=[(OCT, "Se parte de un producto tecnológico terminado para descomponerlo en sus partes", "Orientaciones Curriculares, 4.2.3")]),
   dict(enunciado="La estrategia de construcción-fabricación, según las Orientaciones Curriculares, se centra en", opciones=[
     ("el paso del mundo de las ideas y los diseños al mundo de las realizaciones: modelos, prototipos, simulaciones o programas.", "Es correcta. Así la define el numeral 4.2.1."),
     ("la reflexión crítica sobre los efectos de la tecnología en el ambiente y en las comunidades.", "Es incorrecta. Eso corresponde al enfoque CTS."),
     ("el estudio de la historia de los artefactos para comprender su evolución a lo largo del tiempo.", "Es incorrecta. Eso corresponde al componente de naturaleza y evolución.")],
    citas=[(OCT, "La construcción-fabricación como estrategia didáctica para la enseñanza y el aprendizaje de la tecnología y la informática centra su interés en el paso del mundo de las ideas y los diseños, al mundo de las realizaciones gráficas", "Orientaciones Curriculares, 4.2.1")])]),

 dict(id="F10", familia="DIS-CTS", titulo="Tecnología, ética y sociedad",
  lectura="La Guía 30 dedica un apartado a la relación entre tecnología y ética: algunos desarrollos traen beneficios y, al mismo tiempo, dilemas (energía nuclear, contaminación, manipulación biomédica). Las TIC también generan discusiones éticas: privacidad, confidencialidad, derechos de propiedad de los programas, responsabilidad por su mal funcionamiento y acceso equitativo. El componente Tecnología y sociedad trata tres aspectos: las actitudes de los estudiantes hacia la tecnología, la valoración social que hacen de ella (impactos y sus causas) y su participación social (ética, responsabilidad, propuestas).",
  puntos=["Tres aspectos: actitudes, valoración social, participación social.", "Temas éticos de las TIC: privacidad, propiedad de programas, acceso equitativo.", "La tecnología trae beneficios y dilemas: se evalúan ambos."],
  citas=[(G30, "Algunos ejemplos de esta problemática tienen que ver con la privacidad y la confidencialidad, con los derechos de propiedad de los programas", "Guía 30, p. 10"),
         (G30, "La ética de la tecnología también se relaciona con el acceso equitativo a los productos y a los servicios tecnológicos que benefician a la humanidad", "Guía 30, p. 10")],
  preguntas=[
   dict(enunciado="Según la Guía 30, una de las discusiones éticas que generan las TIC se relaciona con", opciones=[
     ("la velocidad de procesamiento de los computadores frente a la de las calculadoras.", "Es incorrecta. Es un asunto técnico, no ético."),
     ("la cantidad de horas de clase que se dedican al área en cada grado.", "Es incorrecta. Es un asunto curricular, no una discusión ética de las TIC."),
     ("la privacidad y la confidencialidad, y los derechos de propiedad de los programas.", "Es correcta. La Guía 30 los menciona como ejemplos de la problemática ética de las TIC.")],
    citas=[(G30, "Algunos ejemplos de esta problemática tienen que ver con la privacidad y la confidencialidad, con los derechos de propiedad de los programas", "Guía 30, p. 10")]),
   dict(enunciado="Para la Guía 30, la ética de la tecnología también se relaciona con", opciones=[
     ("el acceso equitativo a los productos y servicios tecnológicos que benefician a la humanidad.", "Es correcta. Así lo plantea la Guía 30 en el apartado Tecnología y ética."),
     ("la prohibición de las tecnologías que tienen algún efecto negativo sobre el ambiente.", "Es incorrecta. La guía reconoce efectos negativos, pero también los problemas que la tecnología ha resuelto; no propone prohibir."),
     ("la obligación de enseñar programación a todos los estudiantes desde el preescolar.", "Es incorrecta. No es un planteamiento ético de la guía.")],
    citas=[(G30, "La ética de la tecnología también se relaciona con el acceso equitativo a los productos y a los servicios tecnológicos que benefician a la humanidad", "Guía 30, p. 10")])]),

 dict(id="F11", familia="DIS-SEG", titulo="Uso seguro y responsable de la tecnología",
  lectura="El componente de apropiación y uso incluye usar la tecnología de forma segura: normas de seguridad con herramientas y equipos, elementos de protección, mantenimiento adecuado y uso responsable y autónomo de las TIC. En 8°-9° la Guía 30 espera que el estudiante use las TIC de forma responsable y autónoma para aprender, investigar y comunicarse, y que haga mantenimiento a sus artefactos. En los casos de la CNSC, la respuesta correcta suele formar el criterio del estudiante en lugar de solo prohibir o controlar.",
  puntos=["Seguridad física: elementos de protección y normas al usar herramientas.", "Seguridad digital: contraseñas, datos personales, uso responsable.", "Formar el criterio > prohibir."],
  citas=[(G30, "Utilizo elementos de protección y normas de seguridad para la realización de actividades y manipulación de herramientas y equipos.", "Guía 30, 8° a 9°"),
         (G30, "Utilizo responsable y autónomamente las Tecnologías de la Información y la Comunicación (TIC) para aprender, investigar y comunicarme con otros en el mundo.", "Guía 30, 8° a 9°")],
  preguntas=[
   dict(enunciado="El desempeño «Utilizo elementos de protección y normas de seguridad para la realización de actividades y manipulación de herramientas y equipos» pertenece, en la Guía 30, al componente", opciones=[
     ("Apropiación y uso de la tecnología, porque trata de la utilización adecuada y segura de herramientas y equipos.", "Es correcta. En la tabla de 8° a 9° aparece en la columna de apropiación y uso."),
     ("Solución de problemas con tecnología, porque los elementos de protección resuelven el problema de los accidentes.", "Es incorrecta. Ese componente trata de identificar problemas, diseñar y detectar fallas."),
     ("Tecnología y sociedad, porque la seguridad en el trabajo es una responsabilidad social.", "Es incorrecta. Aunque tiene relación, la guía lo ubica en apropiación y uso.")],
    citas=[(G30, "Utilizo elementos de protección y normas de seguridad para la realización de actividades y manipulación de herramientas y equipos.", "Guía 30, 8° a 9°")]),
   dict(enunciado="Según la Guía 30, en grados octavo y noveno se espera que los estudiantes usen las TIC para", opciones=[
     ("entretenerse en su tiempo libre siempre que lo hagan bajo la supervisión de sus padres.", "Es incorrecta. No es el desempeño que plantea la guía."),
     ("aprender, investigar y comunicarse con otros en el mundo, de manera responsable y autónoma.", "Es correcta. Es el desempeño textual de la Guía 30 para 8° a 9°."),
     ("reemplazar los libros de texto y las clases presenciales por recursos digitales gratuitos.", "Es incorrecta. La guía no plantea reemplazar las clases.")],
    citas=[(G30, "Utilizo responsable y autónomamente las Tecnologías de la Información y la Comunicación (TIC) para aprender, investigar y comunicarme con otros en el mundo.", "Guía 30, 8° a 9°")])]),

 dict(id="F12", familia="PED-EVAL-NORM", titulo="El Sistema Institucional de Evaluación (Decreto 1290)",
  lectura="El Decreto 1290 de 2009, hoy compilado en el Decreto 1075 de 2015, ordena que cada institución tenga su Sistema Institucional de Evaluación de los Estudiantes (SIEE), que hace parte del PEI. Debe contener, entre otros: criterios de evaluación y promoción, escala institucional con su equivalencia a la escala nacional (Desempeño Superior, Alto, Básico y Bajo), acciones de seguimiento durante el año, estrategias de apoyo, periodicidad de informes, e instancias para atender reclamaciones. El SIEE lo aprueba el consejo directivo. El estudiante tiene derecho a conocerlo desde el inicio del año y a recibir acompañamiento para superar sus debilidades.",
  puntos=["Escala nacional: Superior, Alto, Básico, Bajo.", "El SIEE lo aprueba el consejo directivo y hace parte del PEI.", "Debe incluir apoyo durante el año y un procedimiento de reclamaciones.", "Derecho del estudiante: conocer criterios desde el inicio y recibir acompañamiento."],
  citas=[(D1075, "Desempeño Superior Desempeño Alto Desempeño Básico Desempeño Bajo", "Decreto 1075, art. 2.3.3.3.3.5"),
         (D1075, "Aprobar el sistema institucional de evaluación en sesión en el consejo directivo y consignación en el acta.", "Decreto 1075, art. 2.3.3.3.3.8"),
         (D1075, "Las acciones de seguimiento para el mejoramiento de los desempeños de los estudiantes durante el año escolar.", "Decreto 1075, art. 2.3.3.3.3.4")],
  preguntas=[
   dict(enunciado="De acuerdo con el Decreto 1290 de 2009, compilado en el Decreto 1075 de 2015, la escala de valoración nacional es", opciones=[
     ("Excelente, Sobresaliente, Aceptable, Insuficiente y Deficiente.", "Es incorrecta. Era una escala usada antes del Decreto 1290."),
     ("Desempeño Superior, Desempeño Alto, Desempeño Básico y Desempeño Bajo.", "Es correcta. Es la escala nacional del art. 2.3.3.3.3.5."),
     ("una escala numérica de 1 a 5 definida por cada secretaría de educación.", "Es incorrecta. Cada institución define su escala, pero debe tener equivalencia con la escala nacional cualitativa.")],
    citas=[(D1075, "Desempeño Superior Desempeño Alto Desempeño Básico Desempeño Bajo", "Decreto 1075, art. 2.3.3.3.3.5")]),
   dict(enunciado="Según el Decreto 1075 de 2015, el Sistema Institucional de Evaluación de los Estudiantes se aprueba", opciones=[
     ("por el consejo académico, en una reunión con los docentes de todas las áreas.", "Es incorrecta. El consejo académico participa, pero la aprobación es del consejo directivo."),
     ("por la secretaría de educación, después de revisar la propuesta del rector.", "Es incorrecta. Es una decisión institucional, no de la secretaría."),
     ("en sesión del consejo directivo, dejando constancia en el acta.", "Es correcta. Así lo exige el art. 2.3.3.3.3.8, numeral 3.")],
    citas=[(D1075, "Aprobar el sistema institucional de evaluación en sesión en el consejo directivo y consignación en el acta.", "Decreto 1075, art. 2.3.3.3.3.8")])]),

 dict(id="F13", familia="PED-EVAL", titulo="Evaluación formativa en Tecnología e Informática",
  lectura="La evaluación sirve para identificar ritmos y estilos de aprendizaje, reorientar los procesos y apoyar a quien lo necesita, no solo para calificar. Las Orientaciones Curriculares del área recomiendan evaluar el proceso y el progreso del estudiante con evidencias variadas (explicaciones orales y escritas, diagramas, mapas conceptuales, debates, productos tecnológicos) y recuerdan que no todo lo evaluado debe ser calificado. La Resolución 3842 de 2022 pide al docente hacer seguimiento, evaluación y retroalimentación con un enfoque integral, flexible y formativo.",
  puntos=["Evaluar ≠ calificar.", "Evidencias variadas: verbal, escrita, gráfica, productos.", "Retroalimentación oportuna durante el proceso.", "Rúbricas con criterios conocidos desde el inicio."],
  citas=[(OCT, "Tenga presente que no todo lo evaluado para emitir el juicio de valor debe ser calificado.", "Orientaciones Curriculares, 5.2.1"),
         (D1075, "Identificar las características personales, intereses, ritmos de desarrollo y estilos de aprendizaje del estudiante para valorar sus avances.", "Decreto 1075, art. 2.3.3.3.3.3")],
  preguntas=[
   dict(enunciado="Según las Orientaciones Curriculares del área, al evaluar las competencias en Tecnología e Informática el docente debe tener presente que", opciones=[
     ("toda actividad evaluada debe tener una nota para que el estudiante la tome en serio.", "Es incorrecta. Contradice lo que plantean las Orientaciones."),
     ("no todo lo evaluado para emitir el juicio de valor debe ser calificado.", "Es correcta. Es una recomendación textual del numeral 5.2.1."),
     ("la evaluación debe centrarse en el producto final, porque es la evidencia del aprendizaje.", "Es incorrecta. El documento pide considerar el proceso y el progreso.")],
    citas=[(OCT, "Tenga presente que no todo lo evaluado para emitir el juicio de valor debe ser calificado.", "Orientaciones Curriculares, 5.2.1")]),
   dict(enunciado="Uno de los propósitos de la evaluación institucional de los estudiantes, según el Decreto 1075 de 2015, es", opciones=[
     ("clasificar a los estudiantes por rendimiento para organizar los grupos del año siguiente.", "Es incorrecta. No es un propósito establecido por la norma."),
     ("identificar las características personales, intereses, ritmos de desarrollo y estilos de aprendizaje del estudiante para valorar sus avances.", "Es correcta. Es el primer propósito del art. 2.3.3.3.3.3."),
     ("certificar ante la secretaría de educación el cumplimiento de los planes de estudio.", "Es incorrecta. No aparece entre los propósitos de la evaluación de los estudiantes.")],
    citas=[(D1075, "Identificar las características personales, intereses, ritmos de desarrollo y estilos de aprendizaje del estudiante para valorar sus avances.", "Decreto 1075, art. 2.3.3.3.3.3")])]),

 dict(id="F14", familia="PED-INCL", titulo="PIAR, DUA y ajustes razonables (Decreto 1421)",
  lectura="El Decreto 1421 de 2017 (compilado en el Decreto 1075) reglamenta la atención educativa a la población con discapacidad. Primero se diseña para todos: el Diseño Universal del Aprendizaje (DUA) ofrece objetivos, métodos, materiales, apoyos y evaluaciones flexibles. Después, para cada estudiante con discapacidad se construye el PIAR (Plan Individual de Apoyos y Ajustes Razonables): lo lideran los docentes de aula con el docente de apoyo, la familia y el estudiante, se elabora en el primer trimestre y se actualiza cada año. Los ajustes razonables no dependen de un diagnóstico médico, sino de las barreras que enfrenta el estudiante. El currículo flexible mantiene los mismos objetivos generales y da diferentes caminos para alcanzarlos.",
  puntos=["DUA = para todo el grupo. PIAR = complemento individual.", "PIAR: lo lideran docentes de aula + docente de apoyo + familia + estudiante.", "Se elabora en el primer trimestre.", "Ajustes razonables: según barreras, no según diagnóstico."],
  citas=[(D1075, "Se deberá elaborar durante el primer trimestre del año escolar", "Decreto 1075, art. 2.3.3.5.2.3.5"),
         (D1075, "El diseño de los PIAR lo liderarán el o los docentes de aula con el docente de apoyo, la familia y el estudiante.", "Decreto 1075, art. 2.3.3.5.2.3.5"),
         (D1075, "su realización no depende de un diagnóstico médico de deficiencia, sino de las barreras visibles e invisibles", "Decreto 1421 de 2017, definiciones")],
  preguntas=[
   dict(enunciado="Según el Decreto 1075 de 2015 (Decreto 1421 de 2017), el PIAR de un estudiante con discapacidad debe elaborarse", opciones=[
     ("durante el primer trimestre del año escolar, y actualizarse anualmente.", "Es correcta. Así lo establece el art. 2.3.3.5.2.3.5."),
     ("al finalizar el primer periodo, cuando el docente ya conoce los resultados del estudiante.", "Es incorrecta. La norma fija el primer trimestre."),
     ("antes de la matrícula, como requisito para que el estudiante pueda ingresar a la institución.", "Es incorrecta. Ningún establecimiento puede condicionar la matrícula por la discapacidad.")],
    citas=[(D1075, "Se deberá elaborar durante el primer trimestre del año escolar", "Decreto 1075, art. 2.3.3.5.2.3.5")]),
   dict(enunciado="Según la definición del Decreto 1421 de 2017, los ajustes razonables", opciones=[
     ("se aplican solo cuando existe un diagnóstico médico que certifique la discapacidad del estudiante.", "Es incorrecta. Contradice la definición de la norma."),
     ("dependen de las barreras visibles e invisibles que impiden el goce del derecho a la educación.", "Es correcta. La norma establece que no dependen de un diagnóstico médico de deficiencia, sino de las barreras."),
     ("consisten en reducir los objetivos de aprendizaje del grado para el estudiante con discapacidad.", "Es incorrecta. El currículo flexible mantiene los mismos objetivos generales.")],
    citas=[(D1075, "su realización no depende de un diagnóstico médico de deficiencia, sino de las barreras visibles e invisibles", "Decreto 1421 de 2017, definiciones")])]),

 dict(id="F15", familia="PED-CURR", titulo="Currículo, plan de estudios, PEI y áreas obligatorias",
  lectura="La Ley 115 de 1994 establece nueve áreas obligatorias y fundamentales; Tecnología e Informática es la novena. Cada institución construye su Proyecto Educativo Institucional (PEI), que debe responder a las necesidades de los estudiantes y de la comunidad. El currículo es el conjunto de criterios, planes de estudio, programas, metodologías y procesos; el plan de estudios es su esquema estructurado por áreas. Las instituciones tienen autonomía para organizar las áreas dentro de los lineamientos del MEN. Los temas de enseñanza obligatoria del artículo 14 (ambiente, democracia, sexualidad, entre otros) no exigen asignatura propia: se incorporan transversalmente.",
  puntos=["Tecnología e informática: área obligatoria n.° 9 (art. 23).", "PEI: concreto, factible y evaluable (art. 73).", "Currículo (art. 76) ⊃ plan de estudios (art. 79).", "Autonomía escolar dentro de los lineamientos del MEN (art. 77)."],
  citas=[(L115, "Tecnología e informática.", "Ley 115, art. 23"),
         (L115, "Currículo es el conjunto de criterios, planes de estudio, programas, metodologías, y procesos", "Ley 115, art. 76"),
         (L115, "El Proyecto Educativo Institucional debe responder a situaciones y necesidades de los educandos, de la comunidad local, de la región y del país, ser concreto, factible y evaluable.", "Ley 115, art. 73")],
  preguntas=[
   dict(enunciado="Según la Ley 115 de 1994, el currículo se define como", opciones=[
     ("el conjunto de criterios, planes de estudio, programas, metodologías y procesos que contribuyen a la formación integral.", "Es correcta. Es la definición del art. 76."),
     ("el esquema de áreas obligatorias y optativas con sus asignaturas e intensidad horaria.", "Es incorrecta. Esa es la definición de plan de estudios (art. 79), que es solo una parte del currículo."),
     ("el listado de contenidos que el MEN establece para cada grado de la educación básica.", "Es incorrecta. El MEN da lineamientos; el currículo lo construye cada institución.")],
    citas=[(L115, "Currículo es el conjunto de criterios, planes de estudio, programas, metodologías, y procesos", "Ley 115, art. 76")]),
   dict(enunciado="Según el artículo 73 de la Ley 115 de 1994, el Proyecto Educativo Institucional debe", opciones=[
     ("ser igual en todas las instituciones de una entidad territorial para garantizar la equidad.", "Es incorrecta. Cada institución elabora el suyo de acuerdo con su contexto."),
     ("responder a las necesidades de los educandos y de la comunidad, y ser concreto, factible y evaluable.", "Es correcta. Es el texto del parágrafo del art. 73."),
     ("ser aprobado por el Ministerio de Educación Nacional antes de su aplicación.", "Es incorrecta. La ley no exige aprobación del MEN para el PEI.")],
    citas=[(L115, "El Proyecto Educativo Institucional debe responder a situaciones y necesidades de los educandos, de la comunidad local, de la región y del país, ser concreto, factible y evaluable.", "Ley 115, art. 73")])]),

 dict(id="F16", familia="PED-ENSENAR", titulo="Competencias del docente de aula (Resolución 3842 de 2022)",
  lectura="La Resolución 3842 de 2022 es el Manual de Funciones, Requisitos y Competencias, y es la base para diseñar las pruebas del concurso. Para el docente de aula define competencias funcionales en tres áreas de gestión. Gestión académica: dominio curricular, planeación y organización, competencias pedagógicas y didácticas, y evaluación del aprendizaje. Gestión administrativa: uso eficiente de recursos y participación en procesos institucionales. Gestión comunitaria: comunicación institucional e interacción con la comunidad. Define también siete competencias comportamentales: liderazgo, comunicación y relaciones interpersonales, trabajo en equipo, negociación y mediación, compromiso social e institucional, iniciativa y orientación al logro.",
  puntos=["Funcionales: académica (4), administrativa (2), comunitaria (2).", "Comportamentales: 7 (son las de la prueba psicotécnica y la entrevista).", "Funciones clave: planear según el contexto, ambientes de aprendizaje autónomo y cooperativo, evaluación formativa."],
  citas=[(R3842, "Dominio curricular y de contenidos de las áreas de conocimiento.", "Res. 3842 de 2022, 2.1.1.1"),
         (R3842, "liderazgo; comunicación y relaciones interpersonales; trabajo en equipo; negociación y mediación; compromiso social e institucional; iniciativa; y orientación al logro.", "Res. 3842 de 2022, 2.1.2")],
  preguntas=[
   dict(enunciado="Según la Resolución 3842 de 2022, las competencias funcionales del docente de aula se demuestran en", opciones=[
     ("tres áreas de la gestión institucional: académica, administrativa y comunitaria.", "Es correcta. Así lo establece el numeral 2.1.1."),
     ("cuatro áreas de gestión: directiva, académica, administrativa y comunitaria.", "Es incorrecta. La gestión directiva corresponde a los directivos docentes."),
     ("dos áreas: la pedagógica y la disciplinar del área de conocimiento.", "Es incorrecta. No es la organización que establece la resolución.")],
    citas=[(R3842, "competencias funcionales de los docentes se demuestran en tres (3) áreas de la", "Res. 3842 de 2022, 2.1.1")]),
   dict(enunciado="¿Cuál de las siguientes es una competencia comportamental del docente según la Resolución 3842 de 2022?", opciones=[
     ("Planeación y organización.", "Es incorrecta. Es una competencia funcional de la gestión académica."),
     ("Uso eficiente de recursos.", "Es incorrecta. Es una competencia funcional de la gestión administrativa."),
     ("Negociación y mediación.", "Es correcta. Hace parte de las siete competencias comportamentales.")],
    citas=[(R3842, "liderazgo; comunicación y relaciones interpersonales; trabajo en equipo; negociación y mediación; compromiso social e institucional; iniciativa; y orientación al logro.", "Res. 3842 de 2022, 2.1.2")])]),

 dict(id="F17", familia="NOR-CONV-TIPO", titulo="Situaciones tipo I, II y III (Decreto 1965)",
  lectura="El Decreto 1965 de 2013 reglamenta la Ley 1620 (convivencia escolar) y clasifica las situaciones que afectan la convivencia en tres tipos. Tipo I: conflictos manejados inadecuadamente y situaciones esporádicas que afectan el clima escolar, sin daño al cuerpo ni a la salud (un empujón aislado, una discusión). Tipo II: agresión, acoso o ciberacoso que no es delito, pero es repetido o sistemático, o causa daño al cuerpo o a la salud sin generar incapacidad. Tipo III: presuntos delitos, en especial contra la libertad, integridad y formación sexual, o cualquier otro delito de la ley penal. El decreto también define las formas de agresión: física, verbal, gestual, relacional y electrónica.",
  puntos=["Tipo I: esporádica, sin daño.", "Tipo II: repetida o sistemática, o con daño sin incapacidad; no es delito.", "Tipo III: presunto delito.", "Agresión: física, verbal, gestual, relacional, electrónica."],
  citas=[(D1965, "Corresponden a este tipo los conflictos manejados inadecuadamente y aquellas situaciones esporádicas que inciden negativamente en el clima escolar, y que en ningún caso generan daños al cuerpo o a la salud.", "Decreto 1965, art. 40"),
         (D1965, "situaciones de agresión escolar que sean constitutivas de presuntos delitos contra la libertad, integridad y formación sexual", "Decreto 1965, art. 40")],
  preguntas=[
   dict(enunciado="Dos estudiantes discuten a gritos por un balón en el descanso; es la primera vez y no hay golpes. Según el Decreto 1965 de 2013, es una situación", opciones=[
     ("tipo II, porque hubo agresión verbal entre dos estudiantes frente a sus compañeros.", "Es incorrecta. El tipo II exige repetición, sistematicidad o daño al cuerpo o a la salud."),
     ("tipo I, porque es un conflicto manejado inadecuadamente, esporádico y sin daño al cuerpo ni a la salud.", "Es correcta. Corresponde a la definición del art. 40, numeral 1."),
     ("tipo III, porque toda agresión entre estudiantes debe reportarse a la Policía de Infancia y Adolescencia.", "Es incorrecta. El tipo III se reserva para presuntos delitos.")],
    citas=[(D1965, "Corresponden a este tipo los conflictos manejados inadecuadamente y aquellas situaciones esporádicas que inciden negativamente en el clima escolar, y que en ningún caso generan daños al cuerpo o a la salud.", "Decreto 1965, art. 40")]),
   dict(enunciado="Excluir deliberadamente a un compañero de los grupos y difundir rumores para afectar su imagen es, según el Decreto 1965 de 2013, una agresión", opciones=[
     ("gestual, porque busca descalificar al otro sin necesidad de usar palabras.", "Es incorrecta. La agresión gestual se hace con gestos."),
     ("relacional, porque busca afectar negativamente las relaciones que el otro tiene.", "Es correcta. El art. 39 define así la agresión relacional e incluye excluir de grupos y difundir rumores."),
     ("verbal, porque los rumores se transmiten mediante palabras entre los compañeros.", "Es incorrecta. Aunque usa palabras, el decreto clasifica la exclusión y los rumores como agresión relacional.")],
    citas=[(D1965, "Es toda acción que busque afectar negativamente las relaciones que otros tienen. Incluye excluir de grupos, aislar deliberadamente y difundir rumores o secretos", "Decreto 1965, art. 39")])]),

 dict(id="F18", familia="NOR-CONV-RUTA", titulo="Protocolos de atención de la Ruta de Convivencia",
  lectura="Cada tipo de situación tiene su protocolo. Tipo I (art. 42): reunir de inmediato a las partes, mediar de forma pedagógica, fijar una solución imparcial y hacer seguimiento; los estudiantes mediadores pueden participar. Tipo II (art. 43): si hay daño, garantizar atención en salud; remitir si se requiere restablecer derechos; proteger a los involucrados; informar de inmediato a los padres; generar espacios para exponer lo ocurrido; definir acciones restaurativas; el comité escolar de convivencia hace seguimiento y reporta al sistema de información. Tipo III (art. 44): atención en salud, informar a los padres, el presidente del comité informa de inmediato a la Policía Nacional y se adoptan medidas de protección.",
  puntos=["Tipo I: mediación pedagógica inmediata.", "Tipo II: protección + padres + acciones restaurativas + comité.", "Tipo III: el presidente del comité informa a la Policía Nacional.", "Siempre se deja constancia."],
  citas=[(D1965, "Reunir inmediatamente a las partes involucradas en el conflicto y mediar de manera pedagógica", "Decreto 1965, art. 42"),
         (D1965, "Adoptar las medidas para proteger a los involucrados en la situación de posibles acciones en su contra", "Decreto 1965, art. 43"),
         (D1965, "pondrá la situación en conocimiento de la Policía Nacional", "Decreto 1965, art. 44")],
  preguntas=[
   dict(enunciado="Según el Decreto 1965 de 2013, en una situación tipo I el primer paso del protocolo es", opciones=[
     ("informar a la Policía de Infancia y Adolescencia para que verifique los hechos.", "Es incorrecta. Eso corresponde a situaciones tipo III."),
     ("reunir inmediatamente a las partes y mediar de manera pedagógica para que expongan sus puntos de vista.", "Es correcta. Es el numeral 1 del art. 42."),
     ("remitir el caso al comité escolar de convivencia para que defina la sanción.", "Es incorrecta. En tipo I la mediación es inmediata; el comité actúa en los tipos II y III.")],
    citas=[(D1965, "Reunir inmediatamente a las partes involucradas en el conflicto y mediar de manera pedagógica", "Decreto 1965, art. 42")]),
   dict(enunciado="En el protocolo para situaciones tipo III, el Decreto 1965 de 2013 establece que la situación se pone en conocimiento de la Policía Nacional por parte de", opciones=[
     ("el docente que conoció el caso, quien debe presentar la denuncia antes de informar a las directivas.", "Es incorrecta. La norma asigna esta acción al presidente del comité escolar de convivencia."),
     ("los padres de familia, porque son los representantes legales del estudiante afectado.", "Es incorrecta. La institución tiene el deber de informar."),
     ("el presidente del comité escolar de convivencia, de manera inmediata y por el medio más expedito.", "Es correcta. Así lo establece el art. 44, numeral 3.")],
    citas=[(D1965, "pondrá la situación en conocimiento de la Policía Nacional", "Decreto 1965, art. 44")])]),

 dict(id="F19", familia="NOR-DERECHOS", titulo="Interés superior y protección integral (Ley 1098)",
  lectura="El Código de la Infancia y la Adolescencia (Ley 1098 de 2006) se basa en la protección integral de niños, niñas y adolescentes. Principios clave: interés superior (garantizar todos sus derechos de forma integral y simultánea), prevalencia de sus derechos sobre los de los demás y corresponsabilidad (familia, sociedad y Estado). El Decreto 1965 retoma estos principios para la Ruta de Convivencia y agrega el derecho a no ser revictimizado y la protección de datos: la información de los casos es confidencial.",
  puntos=["Interés superior del menor.", "Prevalencia de sus derechos.", "Corresponsabilidad: familia, sociedad, Estado.", "No revictimización y confidencialidad."],
  citas=[(L1098, "Se entiende por interés superior del niño, niña y adolescente, el imperativo que obliga a todas las personas a garantizar la satisfacción integral y simultánea de todos sus Derechos Humanos", "Ley 1098, art. 8"),
         (D1965, "incluyendo el derecho a no ser revictimizado", "Decreto 1965, art. 35")],
  preguntas=[
   dict(enunciado="Según la Ley 1098 de 2006, el interés superior del niño, niña y adolescente es", opciones=[
     ("el imperativo que obliga a todas las personas a garantizar la satisfacción integral y simultánea de todos sus derechos humanos.", "Es correcta. Es la definición del art. 8."),
     ("la facultad de los padres para decidir sobre la educación de sus hijos menores de edad.", "Es incorrecta. No es la definición legal del principio."),
     ("la prioridad que tienen los menores en la asignación de cupos escolares en las instituciones oficiales.", "Es incorrecta. Confunde el principio con una medida administrativa.")],
    citas=[(L1098, "Se entiende por interés superior del niño, niña y adolescente, el imperativo que obliga a todas las personas a garantizar la satisfacción integral y simultánea de todos sus Derechos Humanos", "Ley 1098, art. 8")]),
   dict(enunciado="Según el Decreto 1965 de 2013, en todas las acciones de la Ruta de Atención Integral se debe garantizar, entre otros, el principio de", opciones=[
     ("publicidad, para que la comunidad educativa conozca los casos y aprenda de ellos.", "Es incorrecta. La ruta exige confidencialidad, no publicidad de los casos."),
     ("protección integral, incluido el derecho a no ser revictimizado.", "Es correcta. Así lo establece el art. 35."),
     ("celeridad, que obliga a cerrar cada caso en un plazo máximo de cinco días hábiles.", "Es incorrecta. El decreto no fija ese plazo.")],
    citas=[(D1965, "incluyendo el derecho a no ser revictimizado", "Decreto 1965, art. 35")])]),

 dict(id="F20", familia="NOR-ORG", titulo="El gobierno escolar (Ley 115)",
  lectura="En los establecimientos educativos del Estado, el gobierno escolar lo conforman el rector, el consejo directivo y el consejo académico (art. 142). El consejo directivo (art. 143-144) lo integran el rector, dos docentes, dos padres, un estudiante del último grado, un exalumno y un representante del sector productivo; adopta el reglamento, resuelve conflictos, aprueba el presupuesto de recursos propios y participa en el PEI. El consejo académico (art. 145) lo integran los directivos docentes y un docente por cada área o grado; se ocupa del currículo, el plan de estudios y la evaluación. Además existen el personero (estudiante del último grado) y el representante de los estudiantes.",
  puntos=["Gobierno escolar = rector + consejo directivo + consejo académico.", "Consejo académico → currículo y plan de estudios.", "Consejo directivo → reglamento, conflictos, presupuesto.", "Personero: estudiante del último grado."],
  citas=[(L115, "Cada establecimiento educativo del Estado tendrá un gobierno escolar conformado por el rector, el Consejo Directivo y el Consejo Académico.", "Ley 115, art. 142"),
         (L115, "El estudio, modificación y ajustes al currículo, de conformidad con lo establecido en la presente ley", "Ley 115, art. 145")],
  preguntas=[
   dict(enunciado="Según el artículo 142 de la Ley 115 de 1994, el gobierno escolar de un establecimiento educativo del Estado está conformado por", opciones=[
     ("el rector, el consejo directivo y el consejo académico.", "Es correcta. Es la conformación que fija el art. 142."),
     ("el rector, los coordinadores y la asociación de padres de familia.", "Es incorrecta. No es la conformación legal."),
     ("el consejo directivo, el personero y el comité escolar de convivencia.", "Es incorrecta. Mezcla órganos que no hacen parte del gobierno escolar según el art. 142.")],
    citas=[(L115, "Cada establecimiento educativo del Estado tendrá un gobierno escolar conformado por el rector, el Consejo Directivo y el Consejo Académico.", "Ley 115, art. 142")]),
   dict(enunciado="Un docente quiere proponer una nueva asignatura optativa dentro del área de Tecnología e Informática. Según la Ley 115, la instancia que estudia la organización del plan de estudios es", opciones=[
     ("el consejo directivo, porque toma las decisiones que afectan el funcionamiento de la institución.", "Es incorrecta. El plan de estudios es función del consejo académico."),
     ("la secretaría de educación, porque aprueba los cambios en las áreas obligatorias.", "Es incorrecta. No es la instancia que lo estudia dentro de la institución."),
     ("el consejo académico, al que le corresponde la organización del plan de estudio.", "Es correcta. Así lo dispone el art. 145, literal b.")],
    citas=[(L115, "La organización del plan de estudio", "Ley 115, art. 145")])]),

 dict(id="F21", familia="NOR-ESTATUTO", titulo="Periodo de prueba y la prueba eliminatoria",
  lectura="Quien gana el concurso es nombrado en periodo de prueba (Decreto 1278 de 2002, art. 31). Al terminar el año académico se le evalúa si sirvió al menos cuatro meses; si no, espera al año siguiente. Con 60 % o más en la evaluación de desempeño y competencias, se inscribe en el escalafón; con menos de 60 %, el docente es retirado del servicio. Antes de eso está el concurso: según el Anexo Técnico 2026, quien no supere 60 puntos en la Prueba de Aptitudes y Competencias Básicas (70 para directivos) no continúa en el proceso.",
  puntos=["Periodo de prueba: mínimo 4 meses en el año académico.", "60 % o más → escalafón. Menos de 60 % → retiro.", "Concurso: prueba eliminatoria de 60/100 para docentes (70 para directivos)."],
  citas=[(D1278, "Los docentes y directivos docentes que obtengan una calificación igual o superior al sesenta por ciento (60%)", "Decreto 1278, art. 31"),
         (D1278, "Los docentes que obtengan una calificación inferior al sesenta por ciento (60%) en la evaluación de desempeño o en competencias, serán retirados del servicio.", "Decreto 1278, art. 31"),
         (ANX, "Los aspirantes que no superen el mínimo aprobatorio (70.00 puntos) para Directivos Docentes y (60.00) para Docentes", "Anexo Técnico 2026, 2.2")],
  preguntas=[
   dict(enunciado="Según el Decreto 1278 de 2002, un docente que obtiene menos del 60 % en la evaluación del periodo de prueba", opciones=[
     ("repite el periodo de prueba al año siguiente en la misma institución.", "Es incorrecta. La norma no prevé repetir el periodo."),
     ("es retirado del servicio, porque no alcanzó el mínimo exigido para ser inscrito en el escalafón.", "Es correcta. Así lo establece el art. 31."),
     ("es reubicado en un cargo administrativo de la secretaría de educación.", "Es incorrecta. No existe esa figura en el art. 31.")],
    citas=[(D1278, "Los docentes que obtengan una calificación inferior al sesenta por ciento (60%) en la evaluación de desempeño o en competencias, serán retirados del servicio.", "Decreto 1278, art. 31")]),
   dict(enunciado="Según el Anexo Técnico del concurso 2026, el puntaje mínimo aprobatorio de la Prueba de Aptitudes y Competencias Básicas para docentes es", opciones=[
     ("70 puntos sobre 100, igual que para los directivos docentes.", "Es incorrecta. 70 es el mínimo para los directivos docentes."),
     ("55 puntos sobre 100, que corresponde al peso de la prueba en el puntaje total.", "Es incorrecta. 55 % es el peso de la prueba, no el mínimo aprobatorio."),
     ("60 puntos sobre 100; quien no lo alcance no continúa en el proceso.", "Es correcta. Así lo establece el numeral 2.2 del Anexo Técnico.")],
    citas=[(ANX, "Los aspirantes que no superen el mínimo aprobatorio (70.00 puntos) para Directivos Docentes y (60.00) para Docentes", "Anexo Técnico 2026, 2.2")])]),
]
