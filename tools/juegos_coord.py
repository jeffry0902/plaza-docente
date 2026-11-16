# -*- coding: utf-8 -*-
"""Juegos y esquemas del banco de coordinación, SOLO con texto literal de los documentos oficiales.
Reutiliza los juegos de convivencia e inclusión del banco docente (ya verificados) y agrega los de gestión:
Guía 34, Ley 715, Resolución 3842 y Decreto 1075 (PEI, SIEE, gobierno escolar).
Uso: python3 tools/juegos_coord.py  ->  data/coord/juegos.json   (después de tools/mapas.py --cargo coordinador)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validar import compacto
import fragmentar
fragmentar.CARGO = "coordinador"
from fragmentar import limpiar_lineas

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, "fuentes")
G34, L715, R3842, D75, L20 = "guia34_mineducacion_2008", "ley_715_2001", "resolucion_3842_2022_ocr", "decreto_1075_2015", "ley_1620_2013"
RAW, TXT = {}, {}
for stem in (G34, L715, R3842, D75, L20):
    RAW[stem] = open(os.path.join(F, stem + ".txt"), encoding="utf-8", errors="ignore").read()
    t = " ".join(l for l in limpiar_lineas(RAW[stem]) if l)
    t = re.sub(r"(\w)- (\w)", r"\1\2", t)
    TXT[stem] = re.sub(r"\s+", " ", t)


def literal(doc, texto):
    assert compacto(texto) in compacto(RAW[doc]), f"NO LITERAL en {doc}: {texto[:80]}"
    return texto


def items_numerados(doc, art_ini, art_fin, max_pal=26):
    t = TXT[doc]; i = t.find(art_ini); j = t.find(art_fin, i + 10)
    assert i >= 0 and j > i, (doc, art_ini)
    seg = re.split(r"\b(?:PARÁGRAFO|Parágrafo)\b", t[i:j])[0]
    partes = re.split(r"\s(?=\d{1,2}\.\s[A-ZÁÉÍÓÚ])", seg)
    k = next(n for n, x in enumerate(partes) if x.startswith("1. "))
    out = []
    for p in partes[k:]:
        p = re.sub(r"^\d{1,2}\.\s", "", p).strip()
        corto = " ".join(p.split()[:max_pal]).rstrip(",;:") + ("…" if len(p.split()) > max_pal else "")
        literal(doc, corto.rstrip("…")); out.append(corto)
    return out


base = json.load(open(os.path.join(RAIZ, "data", "juegos.json"), encoding="utf-8"))
toma = lambda grupo, ids: [x for x in base[grupo] if x["id"] in ids]

# ------------------------------------------------------------------ Relacionar
emparejar = toma("emparejar", {"E-situaciones", "E-ruta", "E-inclusion"})
emparejar += [
 {"id": "E-escala34", "titulo": "Escala de la autoevaluación (Guía 34)", "fuente": "Guía 34 MEN (2008), Etapa 1, paso 2", "doc": G34, "pares": [
   {"a": "1 · Existencia", "b": literal(G34, "hay un desarrollo incipiente, parcial o desordenado, y las acciones se llevan a cabo de manera desarticulada.")},
   {"a": "2 · Pertinencia", "b": literal(G34, "hay algunos principios de planeación y articulación de los esfuerzos y acciones para dar cumplimiento a los objetivos y metas.")},
   {"a": "3 · Apropiación", "b": literal(G34, "las acciones institucionales tienen un mayor grado de articulación y, en general, son conocidas por la comunidad educativa.")},
   {"a": "4 · Mejoramiento continuo", "b": literal(G34, "los procesos están consolidados y son evaluados periódicamente para fortalecerlos.")}]},
 {"id": "E-procesos34", "titulo": "Procesos de la gestión y su propósito (Guía 34)", "fuente": "Guía 34 MEN (2008), Cuadro No. 3", "doc": G34, "pares": [
   {"a": "Gobierno escolar", "b": literal(G34, "Favorecer la participación y la toma de decisiones en la institución a través de diversas instancias y dentro de sus competencias y ámbitos de acción.")},
   {"a": "Clima escolar", "b": literal(G34, "Generar un ambiente sano y agradable que propicie el desarrollo de los estudiantes, así como los aprendizajes y la convivencia entre todos los integrantes de la institución.")},
   {"a": "Gestión de aula", "b": literal(G34, "Concretar los actos de enseñanza y aprendizaje en el aula de clase.")},
   {"a": "Talento humano", "b": literal(G34, "Garantizar buenas condiciones de trabajo y desarrollo profesional a las personas vinculadas al establecimiento educativo.")},
   {"a": "Proyección a la comunidad", "b": literal(G34, "Poner a disposición de la comunidad educativa un conjunto de servicios para apoyar su bienestar.")},
   {"a": "Prevención de riesgos", "b": literal(G34, "Disponer de estrategias para prevenir posibles riesgos que podrían afectar el buen funcionamiento de la institución y el bienestar de la comunidad educativa.")}]},
 {"id": "E-quien", "titulo": "¿Quién lo hace? Funciones del gobierno escolar", "fuente": "Decreto 1075 de 2015; Ley 715 de 2001; Resolución 3842 de 2022", "doc": D75, "pares": [
   {"a": "Consejo directivo", "b": literal(D75, "Fijar los criterios para la asignación de cupos disponibles para la admisión de nuevos alumnos")},
   {"a": "Consejo académico", "b": literal(D75, "Organizar el plan de estudios y orientar su ejecución")},
   {"a": "Rector", "b": literal(L715, "Distribuir las asignaciones académicas, y demás funciones de docentes, directivos docentes y administrativos a su cargo")},
   {"a": "Coordinador", "b": literal(R3842, "Participar en la inducción a los docentes nuevos sobre el Proyecto Educativo Institucional")},
   {"a": "Personero de los estudiantes", "b": literal(D75, "Recibir y evaluar las quejas y reclamos que presenten los educandos sobre lesiones a sus derechos")}]},
]


def ocultar(a, b):
    """La definición no puede traer el nombre del término."""
    base_ = re.sub(r"^\d · ", "", a.split("(")[0]).strip()
    for pt in [re.escape(base_)] + ([re.escape(base_[:-2]) + r"\w*"] if len(base_.split()) == 1 else []):
        b = re.sub(r"(?i)\b" + pt + r"\b", "____", b)
    return b[:1].upper() + b[1:]
for e in emparejar:
    for p in e["pares"]:
        if "o" not in p: p["o"] = ocultar(p["a"], p["b"])

# ------------------------------------------------------------------ Ordenar
ordenar = toma("ordenar", {"O-tipo2", "O-tipo3", "O-ruta"})
pasos34 = ["Formulación de los objetivos teniendo en cuenta criterios de inclusión", "Formulación de las metas que parten de la equidad como principio",
           "Definición de los indicadores de resultados", "Definición de las actividades y de sus responsables", "Elaboración del cronograma de actividades",
           "Definición de los recursos necesarios para la ejecución del plan de mejoramiento", "Divulgación del plan de mejoramiento a la comunidad educativa"]
for p in pasos34: literal(G34, p)
etapas34 = ["Autoevaluación institucional", "Elaboración del plan de mejoramiento", "Seguimiento y evaluación de los resultados del plan de mejoramiento"]
literal(G34, "La primera etapa de la ruta del mejoramiento continuo es la autoevaluación institucional")
literal(G34, "La segunda etapa consiste en la elaboración del plan de mejoramiento")
literal(G34, "la tercera etapa consiste en el seguimiento periódico al desarrollo del plan de mejoramiento")
autoev = ["Revisión de la identidad institucional", "Evaluación de cada una de las áreas de gestión teniendo en cuenta los criterios de inclusión",
          "Elaboración del perfil institucional", "Establecimiento de las fortalezas y oportunidades de mejoramiento"]
for p in autoev: literal(G34, p)
ordenar += [
 {"id": "O-ruta34", "titulo": "Las 3 etapas de la ruta del mejoramiento", "fuente": "Guía 34 MEN (2008), 1.11", "doc": G34, "pasos": etapas34},
 {"id": "O-autoev", "titulo": "Pasos de la autoevaluación institucional", "fuente": "Guía 34 MEN (2008), Etapa 1", "doc": G34, "pasos": autoev},
 {"id": "O-plan34", "titulo": "Pasos del plan de mejoramiento", "fuente": "Guía 34 MEN (2008), Etapa 2", "doc": G34, "pasos": pasos34},
 {"id": "O-siee", "titulo": "Procedimiento para crear (o modificar) el SIEE", "fuente": "Decreto 1075 de 2015, art. 2.3.3.3.3.8", "doc": D75,
  "pasos": items_numerados(D75, "ARTÍCULO 2.3.3.3.3.8.", "ARTÍCULO 2.3.3.3.3.9.")},
]

# ------------------------------------------------------------------ Clasificar
mapas = json.load(open(os.path.join(RAIZ, "data", "coord", "mapas.json"), encoding="utf-8"))
g34 = next(m for m in mapas if m["doc"] == G34)["mapa"]
areas = next(h for h in g34["h"] if h["t"].startswith("Las cuatro áreas"))
cats = {a["t"]: [p["t"] for p in a["h"]] for a in areas["h"]}
clasificar = [{"id": "C-areas34", "titulo": "Procesos de la Guía 34: ¿a qué área de gestión pertenecen?", "fuente": "Guía 34 MEN (2008), Cuadro No. 3", "doc": G34, "categorias": cats}]
rector = [literal(L715, x) for x in ["Distribuir las asignaciones académicas", "Imponer las sanciones disciplinarias propias del sistema de control interno disciplinario",
          "Administrar el Fondo de Servicios Educativos y los recursos que por incentivos se le asignen", "Publicar una vez al semestre en lugares públicos y comunicar por escrito a los padres de familia"]]
coord = [literal(R3842, x) for x in ["Orientar las reuniones de área, de ciclos y de otros equipos pedagógicos", "Participar en el Comité de Convivencia Escolar y en el Consejo Académico.",
          "Coordinar la articulación del plan de estudios", "Participar en la inducción a los docentes nuevos"]]
consejo = [literal(D75, x) for x in ["Adoptar el manual de convivencia y el reglamento de la institución", "Fijar los criterios para la asignación de cupos disponibles",
           "Aprobar el plan anual de actualización académica del personal docente presentado por el Rector", "Reglamentar los procesos electorales previstos en el presente Capítulo"]]
clasificar.append({"id": "C-funciones", "titulo": "¿Rector, coordinador o consejo directivo?", "fuente": "Ley 715 de 2001, art. 10; Resolución 3842 de 2022; Decreto 1075 de 2015, art. 2.3.3.1.5.6",
                   "doc": L715, "categorias": {"Rector (Ley 715)": rector, "Coordinador (Res. 3842)": coord, "Consejo directivo (Decreto 1075)": consejo}})

# ------------------------------------------------------------------ Sopa de letras
sopa = toma("sopa", {"S-ruta"})
sopa.append({"id": "S-escala34", "titulo": "Escala de la autoevaluación", "fuente": "Guía 34 MEN (2008)",
             "palabras": [{"w": w, "t": p["a"], "d": p["o"]} for w, p in zip(["EXISTENCIA", "PERTINENCIA", "APROPIACION", "MEJORAMIENTO"], emparejar[3]["pares"])]})
sopa.append({"id": "S-procesos34", "titulo": "Procesos de la gestión", "fuente": "Guía 34 MEN (2008)",
             "palabras": [{"w": w, "t": p["a"], "d": p["o"]} for w, p in zip(["GOBIERNO", "CLIMA", "AULA", "TALENTO", "PROYECCION", "RIESGOS"], emparejar[4]["pares"])]})

# ------------------------------------------------------------------ Esquemas
esquemas = [x for x in base["esquemas"] if x["id"] in {"X-ruta", "X-inclusion", "X-gobierno"}]
esquemas.insert(0, {"id": "X-ruta34", "titulo": "Ruta del mejoramiento institucional (Guía 34)", "tipo": "flujo", "fuente": "Guía 34 MEN (2008)",
                    "pasos": [{"t": "1. Autoevaluación institucional", "d": "; ".join(autoev)}, {"t": "2. Plan de mejoramiento (horizonte de tres años)", "d": "; ".join(pasos34)},
                              {"t": "3. Seguimiento y evaluación", "d": "la tercera etapa consiste en el seguimiento periódico al desarrollo del plan de mejoramiento"}]})
esquemas.insert(1, {"id": "X-areas34", "titulo": "Las cuatro áreas de gestión y sus procesos", "tipo": "lista", "fuente": "Guía 34 MEN (2008), Cuadro No. 3",
                    "grupos": [{"t": a, "f": "Guía 34, Cuadro No. 3", "items": ps} for a, ps in cats.items()],
                    "pasos": [{"t": a, "d": "; ".join(ps)} for a, ps in cats.items()]})

out = {"version": 1, "cargo": "coordinador", "emparejar": emparejar, "ordenar": ordenar, "clasificar": clasificar, "sopa": sopa, "esquemas": esquemas}
json.dump(out, open(os.path.join(RAIZ, "data", "coord", "juegos.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(f"emparejar {len(emparejar)} · ordenar {len(ordenar)} ({[len(o['pasos']) for o in ordenar]}) · clasificar {len(clasificar)} · sopa {len(sopa)} · esquemas {len(esquemas)}")
