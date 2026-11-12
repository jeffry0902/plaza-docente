# Plaza Docente

Tu dosis diaria para la plaza docente: entrenamiento diario para la prueba escrita del concurso docente CNSC 2026 (Tecnología e Informática).

- **Formato fiel a la CNSC:** casos con enunciado y 3 opciones (Prueba de Juicio Situacional), con la justificación de cada opción y la fuente normativa.
- **Estructura del Anexo Técnico 2026:** Aptitudes y Competencias Básicas (lectura crítica, razonamiento cuantitativo, competencias blandas, conocimientos disciplinares y pedagógicos) + Psicotécnica.
- **Repaso inteligente:** cada error guarda la competencia en el cofre y vuelve con otro caso a 1, 3, 7, 14 y 30 días.
- **Motivación:** racha, XP, insignias, corazones con lección de rescate, mapa sin bloqueos, duelo semanal contra los errores y simulacro mensual (primer sábado, 8:00 a. m.).
- **Respaldo:** el avance se guarda en el celular y en Supabase con una clave personal.

## Estructura
- `index.html`, `css/app.css`, `js/app.js`, `js/config.js`: la app (sin dependencias).
- `data/banco.json`: banco de preguntas (casos, ítems, familias de competencias y lecciones de rescate).
- `sw.js`, `manifest.webmanifest`, `icons/`: instalación en el iPhone y uso sin conexión.
- `simulacro.ics`: recordatorios mensuales para el calendario.

## Agregar preguntas
Añade casos en `casos` e ítems en `items` de `data/banco.json`. Cada ítem necesita `familia` (una de `familias`), 3 opciones con justificación, `clave`, `fuente` y `consejo`. Si cambias archivos de la app, sube el número de `CACHE` en `sw.js`.
