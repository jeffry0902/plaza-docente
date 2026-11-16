# -*- coding: utf-8 -*-
"""Mapas de estructura de cada documento oficial (para la sección "Mapas y esquemas").
Todo se extrae del texto oficial: títulos, capítulos, artículos con su nombre, y en la Guía 30
las competencias y desempeños de cada grupo de grados por componente. Cada hoja enlaza a la lectura del plan.
Uso: python3 tools/mapas.py   (después de tools/fragmentar.py)"""
import json, os, re, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fragmentar
from fragmentar import DOCS, DOCS_COORD, limpiar_lineas, cortar, ART
from validar import compacto

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = os.path.join(RAIZ, "fuentes")

# lecturas: doc -> [(id, compacto del texto)]
LECT = {}
COORD = "--cargo" in sys.argv and sys.argv[sys.argv.index("--cargo") + 1] == "coordinador"
SUB = "coord" if COORD else ""
if COORD: fragmentar.CARGO = "coordinador"      # misma limpieza de encabezados que el plan de coordinación
for f in sorted(glob.glob(os.path.join(RAIZ, "data", SUB, "lecturas", "p*.json"))):
    for l in json.load(open(f, encoding="utf-8")):
        LECT.setdefault(l["doc"], []).append((l["id"], compacto(" ".join(l["parrafos"]))))


def lectura_de(doc, texto):
    c = compacto(texto)[:70]
    if len(c) < 8: return None
    for lid, t in LECT.get(doc, []):
        if c in t: return lid
    return None


def nombre_articulo(linea):
    m = ART.match(linea)
    resto = linea[m.end():].lstrip(" .o°-–")
    t = re.split(r"(?<=[a-záéíóúñA-ZÁÉÍÓÚÑ\)])\.\s", resto, maxsplit=1)[0].strip(" .")
    if len(t) > 110: t = t[:107].rsplit(" ", 1)[0] + "…"
    num = m.group(2).rstrip("o°.")
    if t.isupper(): t = t.capitalize()
    return num, t


def mapa_norma(stem, nombre, ini, fin):
    raw = open(os.path.join(FUENTES, stem + ".txt"), encoding="utf-8", errors="ignore").read()
    lineas = [l for l in cortar(limpiar_lineas(raw), ini, fin) if l]
    raiz = {"t": nombre, "h": []}
    pila = [(0, raiz)]                        # (nivel, nodo)
    NIV = {"LIBRO": 1, "TÍTULO": 2, "TITULO": 2, "CAPÍTULO": 3, "CAPITULO": 3, "SECCIÓN": 4, "SECCION": 4}
    i = 0
    while i < len(lineas):
        l = lineas[i]
        m = re.match(r"^(LIBRO|T[ÍI]TULO|CAP[ÍI]TULO|SECCI[ÓO]N)\s+([IVXLC\d]+[°o]?\.?)\s*(.*)$", l, re.I)
        if m and len(l) < 120:
            nivel = NIV[m.group(1).upper()]
            nom = m.group(3).strip(" .")
            if not nom and i + 1 < len(lineas) and not ART.match(lineas[i + 1]) and len(lineas[i + 1]) < 260:
                nom = lineas[i + 1].strip(" ."); i += 1
            if len(nom) > 90: nom = nom[:87].rsplit(" ", 1)[0] + "…"
            nodo = {"t": f"{m.group(1).capitalize()} {m.group(2).rstrip('.')}" + (f" · {nom.capitalize() if nom.isupper() else nom}" if nom else ""), "h": []}
            while pila[-1][0] >= nivel: pila.pop()
            pila[-1][1]["h"].append(nodo); pila.append((nivel, nodo))
        elif ART.match(l):
            num, t = nombre_articulo(l)
            hoja = {"t": f"Art. {num}" + (f" · {t}" if t else ""), "l": lectura_de(stem, l)}
            pila[-1][1]["h"].append(hoja)
        i += 1
    return raiz


def mapa_numerado(stem, nombre, ini, fin):
    """Documentos con títulos numerados (1., 1.1., 2.1.1 …)."""
    raw = open(os.path.join(FUENTES, stem + ".txt"), encoding="utf-8", errors="ignore").read()
    lineas = [l for l in cortar(limpiar_lineas(raw), ini, fin) if l]
    raiz = {"t": nombre, "h": []}; pila = [(0, raiz)]
    vistos = set()
    for l in lineas:
        m = re.match(r"^(\d{1,2}(?:\.\d{1,2}){0,3})\.?\s+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ0-9 ,\-–:()]{6,90})$", l.strip())
        if not m or m.group(1) in vistos: continue
        vistos.add(m.group(1))
        nivel = m.group(1).count(".") + 1
        tit = m.group(2).strip(" .").capitalize()
        nodo = {"t": f"{m.group(1)} {tit}", "h": [], "l": lectura_de(stem, l)}
        while pila[-1][0] >= nivel: pila.pop()
        pila[-1][1]["h"].append(nodo); pila.append((nivel, nodo))
    return raiz


def mapa_guia30():
    raw = open(os.path.join(FUENTES, "guia30_mineducacion_2008.txt"), encoding="utf-8", errors="ignore").read()
    L = raw.split("\n")
    comps = ["Naturaleza y evolución de la tecnología", "Apropiación y uso de la tecnología",
             "Solución de problemas con tecnología", "Tecnología y sociedad"]
    grupos = [("Primero", "Tercero"), ("Cuarto", "Quinto"), ("Sexto", "Séptimo"), ("Octavo", "Noveno"), ("Décimo", "Undécimo")]
    inicios = []
    for a, b in grupos:
        k = next(i for i in range(len(L) - 2) if L[i].strip() == a and L[i + 1].strip() == "a" and L[i + 2].strip() == b and i > 600)
        inicios.append(k)
    inicios.append(next(i for i, l in enumerate(L) if i > inicios[-1] and re.match(r"^\s*(4\.|Sugerencias)", l)) if any(re.match(r"^\s*(4\.|Sugerencias)", l) for l in L[inicios[-1]:]) else len(L))

    def bloques(seg):
        out, cur = [], []
        for l in seg:
            s = l.strip()
            if not s:
                if cur: out.append(cur); cur = []
            else: cur.append(s)
        if cur: out.append(cur)
        return out

    raiz = {"t": "Guía 30 · Ser competente en tecnología", "h": []}
    def_comp = {   # texto literal de la Guía 30, p. 14
        comps[0]: "Se refiere a las características y objetivos de la tecnología, a sus conceptos fundamentales (sistema, componente, estructura, función, recurso, optimización, proceso, etc.), a sus relaciones con otras disciplinas y al reconocimiento de su evolución a través de la historia y la cultura.",
        comps[1]: "Se trata de la utilización adecuada, pertinente y crítica de la tecnología (artefactos, productos, procesos y sistemas) con el fin de optimizar, aumentar la productividad, facilitar la realización de diferentes tareas y potenciar los procesos de aprendizaje, entre otros.",
        comps[2]: "Se refiere al manejo de estrategias en y para la identificación, formulación y solución de problemas con tecnología, así como para la jerarquización y comunicación de ideas. Comprende estrategias que van desde la detección de fallas y necesidades, hasta llegar al diseño y a su evaluación. Utiliza niveles crecientes de complejidad según el grupo de grados de que se trate.",
        comps[3]: "Trata tres aspectos: 1) Las actitudes de los estudiantes hacia la tecnología, en términos de sensibilización social y ambiental, curiosidad, cooperación, trabajo en equipo, apertura intelectual, búsqueda, manejo de información y deseo de informarse; 2) La valoración social que el estudiante hace de la tecnología para reconocer el potencial de los recursos, la evaluación de los procesos y el análisis de sus impactos (sociales, ambientales y culturales) así como sus causas y consecuencias; y 3) La participación social que involucra temas como la ética y responsabilidad social, la comunicación, la interacción social, las propuestas de soluciones y la participación, entre otras.",
    }
    from validar import norm
    for c, d in def_comp.items():
        assert compacto(d) in compacto(raw), c
    # verificar que la definición resumida tiene su texto oficial (prefijo literal) en la guía
    rama_c = {"t": "4 componentes", "h": [{"t": c, "d": def_comp[c], "h": []} for c in comps]}
    rama_g = {"t": "5 grupos de grados · competencias y desempeños", "h": []}
    for gi, (a, b) in enumerate(grupos):
        seg = L[inicios[gi]:inicios[gi + 1]]
        bl = [x for x in bloques(seg) if not re.fullmatch(r"\d{1,3}|TECNOLOGÍA|a|" + a + "|" + b, " ".join(x))]
        # dos mitades: [comp0, comp1] y [comp2, comp3]
        nodo_g = {"t": f"{a} a {b}", "h": []}
        partes = {c: {"comp": None, "des": []} for c in comps}
        mitad, pendientes_comp, listas = 0, [], []
        for x in bl:
            txt = " ".join(x)
            if txt in comps or txt in (comps[0] + " " + comps[1], comps[2] + " " + comps[3]):
                continue
            if x[0].startswith("•"):
                items, cur = [], ""
                for s in x:
                    if s.startswith("•"):
                        if cur: items.append(cur)
                        cur = s.lstrip("• ").strip()
                    else: cur += " " + s
                if cur: items.append(cur)
                listas.append(items)
            elif len(txt) > 40:
                pendientes_comp.append(re.sub(r"\s+", " ", txt))
        # orden esperado: comp0, comp1, lista0, lista1, comp2, comp3, lista2, lista3
        if len(pendientes_comp) >= 4 and len(listas) >= 4:
            for k, c in enumerate(comps):
                partes[c]["comp"] = pendientes_comp[k]; partes[c]["des"] = listas[k]
        for k, c in enumerate(comps):
            p = partes[c]
            if not p["comp"]: continue
            nodo_g["h"].append({"t": c, "d": p["comp"], "h": [{"t": d} for d in p["des"]], "l": lectura_de("guia30_mineducacion_2008", p["comp"])})
            rama_c["h"][k]["h"].append({"t": f"{a} a {b}", "d": p["comp"], "l": lectura_de("guia30_mineducacion_2008", p["comp"])})
        rama_g["h"].append(nodo_g)
    raiz["h"] = [rama_c, rama_g]
    return raiz


# Guía 34: áreas → procesos → componentes (Cuadro No. 3) y la ruta del mejoramiento. Los textos son los de la guía.
G34_AREAS = [
 ("Gestión directiva", [
  ("Direccionamiento estratégico y horizonte institucional", "misión, visión, valores institucionales (principios), metas, conocimiento y apropiación del direccionamiento, política de inclusión de personas con capacidades disímiles y diversidad cultural"),
  ("Gestión estratégica", "Liderazgo, articulación de planes, proyectos y acciones, estrategia pedagógica, uso de información (interna y externa) para la toma de decisiones, seguimiento y autoevaluación"),
  ("Gobierno escolar", "Consejos directivo, académico, estudiantil y de padres de familia, comisión de evaluación y promoción, comité de convivencia, personero estudiantil, y asamblea de padres de familia"),
  ("Cultura institucional", "Mecanismos de comunicación, trabajo en equipo, reconocimiento de logros, identificación y divulgación de buenas prácticas"),
  ("Clima escolar", "ambiente físico, inducción a los nuevos estudiantes, motivación hacia el aprendizaje, manual de convivencia, actividades extracurriculares, bienestar de los alumnos, manejo de conflictos y casos difíciles"),
  ("Relaciones con el entorno", "Padres de familia, autoridades educativas, otras instituciones, sector productivo")]),
 ("Gestión académica", [
  ("Diseño pedagógico (curricular)", "Plan de estudios, enfoque metodológico, recursos para el aprendizaje, jornada escolar, evaluación"),
  ("Prácticas pedagógicas", "Opciones didácticas para las áreas, asignaturas y proyectos transversales, estrategias para las tareas escolares, uso articulado de los recursos y los tiempos para el aprendizaje"),
  ("Gestión de aula", "Relación y estilo pedagógico, planeación de clases y evaluación en el aula"),
  ("Seguimiento académico", "Seguimiento a los resultados académicos, a la asistencia de los estudiantes y a los egresados, uso pedagógico de las evaluaciones externas, actividades de recuperación y apoyos pedagógicos adicionales para estudiantes con necesidades educativas especiales")]),
 ("Gestión administrativa y financiera", [
  ("Apoyo a la gestión académica", "Proceso de matrícula, archivo académico y boletines de calificaciones"),
  ("Administración de la planta física y de los recursos", "Mantenimiento, adecuación y embellecimiento de la planta física, seguimiento al uso de los espacios, adquisición y mantenimiento de los recursos para el aprendizaje, suministros, dotación y mantenimiento de equipos, seguridad y protección"),
  ("Administración de servicios complementarios", "Servicios de transporte, restaurante, cafetería y salud (enfermería, odontología, psicología), apoyo a estudiantes con necesidades educativas especiales"),
  ("Talento humano", "Perfiles, inducción, formación y capacitación, asignación académica, pertenencia a la institución, evaluación del desempeño, estímulos, apoyo a la investigación, convivencia y manejo de conflictos, bienestar del talento humano"),
  ("Apoyo financiero y contable", "Presupuesto anual del Fondo de Servicios Educativos, contabilidad, ingresos y gastos, control fiscal")]),
 ("Gestión de la comunidad", [
  ("Inclusión", "Atención educativa a grupos poblacionales con necesidades especiales y a personas pertenecientes a grupos étnicos, necesidades y expectativas de los estudiantes, proyectos de vida"),
  ("Proyección a la comunidad", "Escuela de padres, oferta de servicios a la comunidad, uso de la planta física y de medios, servicio social estudiantil"),
  ("Participación y convivencia", "Participación de estudiantes y padres de familia, asamblea y consejo de padres"),
  ("Prevención de riesgos", "Prevención de riesgos físicos y psicosociales, programas de seguridad")]),
]
G34_RUTA = [
 ("Etapa 1 · Autoevaluación institucional", "La primera etapa de la ruta del mejoramiento continuo es la autoevaluación institucional",
  ["Paso 1. Revisión de la identidad institucional", "Paso 2. Evaluación de cada una de las áreas de gestión (escala: 1 existencia, 2 pertinencia, 3 apropiación, 4 mejoramiento continuo)",
   "Paso 3. Elaboración del perfil institucional", "Paso 4. Establecimiento de las fortalezas y oportunidades de mejoramiento"]),
 ("Etapa 2 · Elaboración del plan de mejoramiento (horizonte de tres años)", "La segunda etapa consiste en la elaboración del plan de mejoramiento",
  ["Paso 1. Formulación de los objetivos", "Paso 2. Formulación de las metas", "Paso 3. Definición de los indicadores de resultados", "Paso 4. Definición de las actividades y de sus responsables",
   "Paso 5. Elaboración del cronograma de actividades", "Paso 6. Definición de los recursos necesarios", "Paso 7. Divulgación del plan de mejoramiento a la comunidad educativa"]),
 ("Etapa 3 · Seguimiento y evaluación de los resultados del plan", "la tercera etapa consiste en el seguimiento periódico al desarrollo del plan de mejoramiento",
  ["Paso 1. Montaje del sistema de seguimiento", "Paso 2. Revisión periódica del plan", "Paso 3. Evaluación del plan de mejoramiento: insumo de la siguiente autoevaluación"]),
]


def comps(txt):
    partes = [x.strip() for x in re.split(r",\s*(?![^()]*\))|\sy\s(?=[a-záéíóú])", txt) if x.strip()]
    return [p[0].upper() + p[1:] for p in partes]


def mapa_guia34():
    stem = "guia34_mineducacion_2008"
    raiz = {"t": "Guía 34: mejoramiento institucional", "h": []}
    areas = {"t": "Las cuatro áreas de gestión (Cuadro No. 3)", "h": []}
    for area, procs in G34_AREAS:
        na = {"t": area, "h": []}
        for proc, componentes in procs:
            na["h"].append({"t": proc, "l": lectura_de(stem, componentes), "h": [{"t": "Componentes: " + componentes[0].lower() + componentes[1:] + "."}]})
        areas["h"].append(na)
    ruta = {"t": "Ruta del mejoramiento continuo", "h": []}
    for etapa, ancla, pasos in G34_RUTA:
        ruta["h"].append({"t": etapa, "l": lectura_de(stem, ancla), "h": [{"t": p} for p in pasos]})
    raiz["h"] = [ruta, areas]
    return raiz


def main_coord():
    cfg = {d[7]: d for d in DOCS_COORD}
    out = [{"doc": "guia34_mineducacion_2008", "nombre": cfg["g34"][1], "mapa": mapa_guia34()}]
    s, nombre, g, p, ini, fin, tipo, k = cfg["r3842"]
    out.append({"doc": s, "nombre": nombre, "mapa": mapa_numerado(s, "Res. 3842 de 2022 · Directivos docentes", ini, fin)})
    for clave in ("l715", "l1620", "d1965", "d1421", "d1075-gob", "d1075-siee", "d1075-fse", "d1278"):
        s, nombre, g, p, ini, fin, tipo, k = cfg[clave]
        out.append({"doc": s, "clave": clave, "nombre": nombre, "mapa": mapa_norma(s, nombre.split(" (")[0], ini, fin)})
    json.dump(out, open(os.path.join(RAIZ, "data", "coord", "mapas.json"), "w", encoding="utf-8"), ensure_ascii=False)
    for m in out: print(f"{m.get('clave', m['doc'])}: {contar(m['mapa'])} nodos")


def contar(n): return 1 + sum(contar(h) for h in n.get("h", []))


def main():
    cfg = {d[0]: d for d in DOCS}
    out = []
    out.append({"doc": "guia30_mineducacion_2008", "nombre": cfg["guia30_mineducacion_2008"][1], "mapa": mapa_guia30()})
    out.append({"doc": "orientaciones_tecnologia_2022", "nombre": cfg["orientaciones_tecnologia_2022"][1],
                "mapa": mapa_numerado("orientaciones_tecnologia_2022", "Orientaciones Curriculares T&I (2022)", r"^PRESENTACIÓN ORIENTACIONES", r"^\s*Bibliografía")})
    for stem in ("ley_1620_2013", "decreto_1965_2013", "decreto_1421_2017", "decreto_1075_2015", "ley_115_1994", "decreto_1278_2002", "ley_1098_2006"):
        s, nombre, g, p, ini, fin, tipo = cfg[stem]
        out.append({"doc": stem, "nombre": nombre, "mapa": mapa_norma(stem, nombre.split(" (")[0] if stem != "decreto_1075_2015" else "Decreto 1290 de 2009 (en el Decreto 1075)", ini, fin)})
    s, nombre, g, p, ini, fin, tipo = cfg["resolucion_3842_2022_ocr"]
    out.append({"doc": "resolucion_3842_2022_ocr", "nombre": nombre, "mapa": mapa_numerado("resolucion_3842_2022_ocr", "Res. 3842 de 2022 · Docente de aula", ini, fin)})
    json.dump(out, open(os.path.join(RAIZ, "data", "mapas.json"), "w", encoding="utf-8"), ensure_ascii=False)
    for m in out: print(f"{m['doc']}: {contar(m['mapa'])} nodos")


if __name__ == "__main__":
    main_coord() if COORD else main()
