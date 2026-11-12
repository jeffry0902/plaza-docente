# Generador diario del banco · Plaza Docente

Reglas que sigue la tarea programada que agrega preguntas cada día. Si algo de esto no se cumple, el lote **no se publica**.

## 0. Plan de lectura (lo que ella lee antes de responder)
- `python3 tools/fragmentar.py` parte los documentos en ~235 lecturas cortas (3-4 min) y las ordena: 50 % Guía 30 y Orientaciones Curriculares (prioridad 1), 30 % Ley 1620 + Decreto 1965 y Decreto 1421 (prioridad 2), 20 % el resto (Decreto 1290/1075, Ley 115, Decreto 1278, Res. 3842, Ley 1098).
- El reto diario abre con la siguiente lectura del plan y luego hace las preguntas cuyas citas están en ese texto. Cada pregunta tipo caso muestra antes "Antes de responder, lee esto" (el pasaje exacto) y después la cita.
- Por eso, **cada día se escriben preguntas para las próximas lecturas de su plan**: lee `estado.datos.lecturas` de la cuenta 'Aspirante' en Supabase, identifica las siguientes 5 lecturas sin leer en `data/lecturas/indice.json` y garantiza que cada una tenga al menos 4 ítems con citas textuales tomadas de ese mismo texto.
- Después de agregar el lote, vuelve a correr `python3 tools/fragmentar.py` (actualiza `data/contextos.json`).

## 1. Qué se genera cada día (~50 ítems)
- **3 fichas nuevas** (Estudia y responde) con 2 preguntas de conocimiento cada una → 6 ítems.
- **~44 ítems tipo caso** (formato CNSC de juicio situacional: caso + enunciado + 3 opciones A/B/C, justificación por opción), repartidos así:
  - 40 % DIS (Tecnología e Informática: los 4 componentes + didáctica del área), basados sobre todo en la Guía 30 y las Orientaciones Curriculares
  - 25 % PED (evaluar, enseñar, inclusión: Decreto 1421, DUA, PIAR, ajustes razonables tienen prioridad)
  - 15 % NOR (prioridad: Ley 1620, Decreto 1965, Ruta de Atención y solución de conflictos; luego organización escolar y estatuto)
  - 10 % LC + RC, 5 % CB, 5 % PSI
- Prioridad: familias con menos de 4 ítems y familias que la aspirante falla más (tabla `intentos` de Supabase).

## 2. Modelo Basado en Evidencias (ICFES)
Componente → afirmación → evidencia (= familia) → tareas. Cada ítem nuevo pertenece a una familia de `data/marco.json`.
Una familia debe tener **varias tareas con contextos distintos** (otro grado, otra área, otro artefacto, otra situación de convivencia) que evalúen exactamente la misma evidencia. Así funciona el repaso: si falla, vuelve la misma evidencia en otro contexto.

## 3. Fuentes permitidas (carpeta `fuentes/`)
Solo documentos oficiales: Guía 30 MEN, Ley 1620 de 2013 (texto vigente traído de la Secretaría del Senado por el workflow `traer-fuentes`), Orientaciones Curriculares de Tecnología e Informática (2022), Ley 115, Decreto 1075 (incluye 1290 y 1421), Decreto 1278, Ley 1098, Ley 1620, Decreto 1965, Resolución 3842 de 2022, Anexo Técnico CNSC 2026, Acuerdo 314 de 2026, Guía de orientación CNSC. Cuadernillos de terceros: solo como referencia de estilo, nunca como fuente de un dato.

## 4. Reglas de calidad (obligatorias)
1. Todo ítem DIS, PED o NOR lleva al menos una **cita textual** (`citas: [{doc, texto, ubicacion}]`) copiada del documento. El validador comprueba que el texto exista literalmente.
2. La clave debe desprenderse de la cita: alguien que no sea experto debe poder leer la cita y confirmar la respuesta.
3. Nunca se inventan números de artículo, plazos, porcentajes ni conformaciones de órganos que no estén en la cita.
4. Opciones de longitud parecida, sin "todas las anteriores", sin absolutos obvios. Las incorrectas son errores típicos reales.
5. Justificación por opción: la correcta empieza por "Es correcta."; las demás por "Es incorrecta." y dicen por qué.

## 5. Proceso
1. Redactar el lote en `data/lotes/AAAA-MM-DD.json` (ids nuevos únicos).
2. `python3 tools/validar.py --fuentes fuentes` → debe decir `RESULTADO: OK`.
3. **Verificación ciega**: un agente independiente responde cada ítem sin ver la clave, solo con el caso y las citas. Si su respuesta no coincide con la clave, o si dice que hay dos respuestas defendibles, el ítem va a cuarentena (`data/cuarentena/`) y no se publica.
4. Revisar la tabla `reportes` de Supabase: cada reporte se contrasta con la norma; si hay error se corrige el ítem o se agrega su id a `retirados` en `data/indice.json`; se marca el reporte como resuelto.
5. Agregar el lote a `data/indice.json`, subir el número de caché en `sw.js`, commit y push a `main` (GitHub Pages publica solo).

## 6. Qué puede revisar alguien que no es experto
Abrir la pregunta en la app: el recuadro verde "Lo que dice el documento oficial" debe decir lo mismo que la opción marcada como correcta. Si no coincide, tocar "Repórtala".
