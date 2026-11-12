# -*- coding: utf-8 -*-
"""Juegos (retos distintos) y esquemas visuales, construidos SOLO con texto literal de los documentos oficiales.
Cada texto se verifica contra la fuente antes de guardarse.
Uso: python3 tools/juegos.py  ->  data/juegos.json"""
import json, os, re, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validar import compacto
from fragmentar import limpiar_lineas

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, "fuentes")
RAW, TXT = {}, {}
for stem in ("decreto_1965_2013", "ley_1620_2013", "decreto_1421_2017", "guia30_mineducacion_2008", "decreto_1075_2015", "ley_115_1994"):
    RAW[stem] = open(os.path.join(F, stem + ".txt"), encoding="utf-8", errors="ignore").read()
    t = " ".join(l for l in limpiar_lineas(RAW[stem]) if l)
    t = re.sub(r"(\w)- (\w)", r"\1\2", t)
    TXT[stem] = re.sub(r"\s+", " ", t)


def literal(doc, texto):
    assert compacto(texto) in compacto(RAW[doc]), f"NO LITERAL en {doc}: {texto[:80]}"
    return texto


def frase(doc, inicio, max_pal=45):
    """Desde 'inicio' hasta el final de la primera oración (o max_pal palabras con '…')."""
    t = TXT[doc]; i = t.find(inicio)
    assert i >= 0, f"no encontrado en {doc}: {inicio}"
    resto = t[i:]
    m = re.search(r"(?<!\b[a-z])\.\s", resto[len(inicio):])
    s = resto[: len(inicio) + m.start() + 1] if m else resto[:400]
    pal = s.split()
    if len(pal) > max_pal: s = " ".join(pal[:max_pal]).rstrip(",;:") + "…"
    literal(doc, s.rstrip("…")); return s


def items_numerados(doc, art_ini, art_fin):
    t = TXT[doc]; i = t.find(art_ini); j = t.find(art_fin, i + 10)
    seg = re.split(r"\b(?:PARÁGRAFO|Parágrafo)\b", t[i:j])[0]
    partes = re.split(r"\s(?=\d{1,2}\.\s[A-ZÁÉÍÓÚ])", seg)
    k = next(n for n, x in enumerate(partes) if x.startswith("1. "))
    partes = partes[k:]
    out = []
    for p in partes:
        p = re.sub(r"^\d{1,2}\.\s", "", p).strip()
        p = re.split(r"\s(?:PARÁGRAFO|Parágrafo)\b", p)[0].strip()
        corto = " ".join(p.split()[:26]).rstrip(",;:") + ("…" if len(p.split()) > 26 else "")
        literal(doc, corto.rstrip("…")); out.append(corto)
    return out


D65, L20, D21, G30, D75, L115 = "decreto_1965_2013", "ley_1620_2013", "decreto_1421_2017", "guia30_mineducacion_2008", "decreto_1075_2015", "ley_115_1994"
FUENTE = {D65: "Decreto 1965 de 2013", L20: "Ley 1620 de 2013", D21: "Decreto 1421 de 2017", G30: "Guía 30 MEN (2008)", D75: "Decreto 1075 de 2015 (Decreto 1290)", L115: "Ley 115 de 1994"}

emparejar = [
 {"id": "E-agresion", "titulo": "Tipos de agresión escolar", "fuente": "Decreto 1965 de 2013, art. 39", "doc": D65, "pares": [
   {"a": "Agresión física", "b": frase(D65, "Es toda acción que tenga como finalidad causar daño al cuerpo")},
   {"a": "Agresión verbal", "b": frase(D65, "Es toda acción que busque con las palabras")},
   {"a": "Agresión gestual", "b": frase(D65, "Es toda acción que busque con los gestos")},
   {"a": "Agresión relacional", "b": frase(D65, "Es toda acción que busque afectar negativamente las relaciones")},
   {"a": "Agresión electrónica", "b": frase(D65, "Es toda acción que busque afectar negativamente a otros a través de medios electrónicos")}]},
 {"id": "E-situaciones", "titulo": "Situaciones tipo I, II y III", "fuente": "Decreto 1965 de 2013, art. 40", "doc": D65, "pares": [
   {"a": "Situación tipo I", "b": frase(D65, "Corresponden a este tipo los conflictos manejados inadecuadamente")},
   {"a": "Situación tipo II", "b": frase(D65, "Corresponden a esta tipo las situaciones de agresión escolar", 30)},
   {"a": "Situación tipo III", "b": "Corresponden a este tipo las situaciones de agresión escolar que sean constitutivas de presuntos delitos contra la libertad, integridad y formación sexual…"}]},
 {"id": "E-ruta", "titulo": "Componentes de la Ruta de Atención Integral", "fuente": "Ley 1620 de 2013, art. 30", "doc": L20, "pares": [
   {"a": "Promoción", "b": frase(L20, "El componente de promoción se centrará")},
   {"a": "Prevención", "b": frase(L20, "El componente de prevención deberá ejecutarse", 30)},
   {"a": "Atención", "b": frase(L20, "El componente de atención deberá desarrollar estrategias", 30)},
   {"a": "Seguimiento", "b": frase(L20, "El componente de seguimiento se centrará")}]},
 {"id": "E-inclusion", "titulo": "Educación inclusiva: conceptos clave", "fuente": "Decreto 1421 de 2017", "doc": D21, "pares": [
   {"a": "Ajustes razonables", "b": frase(D21, "Ajustes razonables: son las acciones", 32)},
   {"a": "Currículo flexible", "b": frase(D21, "Currículo flexible: es aquel que mantiene")},
   {"a": "Diseño Universal del Aprendizaje (DUA)", "b": frase(D21, "Diseño Universal del Aprendizaje (DUA): diseño de productos", 32)},
   {"a": "Educación inclusiva", "b": frase(D21, "Educación inclusiva: es un proceso permanente", 32)},
   {"a": "PIAR", "b": frase(D21, "Plan Individual de Ajustes Razonables (PIAR): herramienta utilizada", 32)}]},
 {"id": "E-guia30", "titulo": "Conceptos básicos de la tecnología", "fuente": "Guía 30 MEN (2008)", "doc": G30, "pares": [
   {"a": "Artefactos", "b": frase(G30, "Los artefactos: son dispositivos")},
   {"a": "Procesos", "b": frase(G30, "Los procesos: son fases sucesivas", 30)},
   {"a": "Sistemas", "b": frase(G30, "Los sistemas: son conjuntos o grupos de elementos")},
   {"a": "Innovación", "b": frase(G30, "La innovación implica introducir cambios", 30)},
   {"a": "Invención", "b": frase(G30, "La invención corresponde a un nuevo producto")},
   {"a": "Descubrimiento", "b": frase(G30, "El descubrimiento es un hallazgo", 25)}]},
]
# tipo III: verificar el texto armado a mano
literal(D65, emparejar[1]["pares"][2]["b"].rstrip("…").replace("Corresponden a este tipo las situaciones de agresión escolar que sean", "situaciones de agresión escolar que sean"))

ordenar = [
 {"id": "O-tipo1", "titulo": "Protocolo para situaciones tipo I", "fuente": "Decreto 1965 de 2013, art. 42", "doc": D65,
  "pasos": items_numerados(D65, "Artículo 42. Protocolo para la atención de Situaciones Tipo I", "Artículo 43.")},
 {"id": "O-tipo2", "titulo": "Protocolo para situaciones tipo II", "fuente": "Decreto 1965 de 2013, art. 43", "doc": D65,
  "pasos": items_numerados(D65, "Artículo 43. Protocolo para la atención de Situaciones Tipo II", "Artículo 44.")},
 {"id": "O-tipo3", "titulo": "Protocolo para situaciones tipo III", "fuente": "Decreto 1965 de 2013, art. 44", "doc": D65,
  "pasos": items_numerados(D65, "Artículo 44. Protocolo para la atención de de Situaciones Tipo III", "Artículo 45.")},
 {"id": "O-ruta", "titulo": "Los 4 componentes de la Ruta, en el orden de la ley", "fuente": "Ley 1620 de 2013, art. 30", "doc": L20,
  "pasos": ["Promoción", "Prevención", "Atención", "Seguimiento"]},
]
literal(L20, "cuatro componentes: de promoción, de prevención, de atención y de seguimiento")

# clasificar: desempeños de la Guía 30 por componente (desde el mapa ya extraído)
mapas = json.load(open(os.path.join(RAIZ, "data", "mapas.json"), encoding="utf-8"))
g30 = next(m for m in mapas if m["doc"] == G30)["mapa"]
clasificar = []
for grupo in g30["h"][1]["h"]:
    cats = {c["t"]: [d["t"] for d in c.get("h", [])] for c in grupo["h"]}
    if len(cats) == 4:
        for c, ds in cats.items():
            for d in ds: literal(G30, d)
        clasificar.append({"id": "C-" + grupo["t"].split()[0].lower(), "titulo": f"Desempeños de {grupo['t']}: ¿a qué componente pertenecen?",
                           "fuente": "Guía 30 MEN (2008), tablas por grupos de grados", "doc": G30, "categorias": cats})

# sopa de letras: términos con su definición literal (de los juegos de emparejar)
sopa = []
def palabra(t): return re.sub(r"[^A-ZÑ]", "", t.upper().replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U"))
for e in emparejar:
    pal = []
    for p in e["pares"]:
        w = palabra(p["a"].split("(")[0].replace("Agresión ", "").replace("Situación tipo", "TIPO"))
        if 3 <= len(w) <= 12: pal.append({"w": w, "t": p["a"], "d": p["b"]})
    if len(pal) >= 4: sopa.append({"id": "S-" + e["id"][2:], "titulo": e["titulo"], "fuente": e["fuente"], "palabras": pal})

# esquemas visuales
esquemas = [
 {"id": "X-ruta", "titulo": "Ruta de Atención Integral para la Convivencia Escolar", "tipo": "ruta",
  "fuente": "Ley 1620 de 2013 (arts. 29-31) y Decreto 1965 de 2013 (arts. 39-44)",
  "componentes": [{"t": p["a"], "d": p["b"]} for p in emparejar[2]["pares"]],
  "situaciones": [{"t": p["a"], "d": p["b"], "pasos": o["pasos"]} for p, o in zip(emparejar[1]["pares"], ordenar[:3])],
  "agresiones": [{"t": p["a"], "d": p["b"]} for p in emparejar[0]["pares"]]},
 {"id": "X-inclusion", "titulo": "Educación inclusiva: del DUA al PIAR", "tipo": "flujo", "fuente": "Decreto 1421 de 2017",
  "pasos": [{"t": p["a"], "d": p["b"]} for p in [emparejar[3]["pares"][i] for i in (3, 2, 1, 0, 4)]]},
 {"id": "X-guia30", "titulo": "Guía 30: 4 componentes en 5 grupos de grados", "tipo": "matriz", "fuente": "Guía 30 MEN (2008)",
  "componentes": [{"t": c["t"], "d": c["d"]} for c in g30["h"][0]["h"]],
  "grupos": [{"t": g["t"], "celdas": [c.get("d", "") for c in g["h"]]} for g in g30["h"][1]["h"]]},
 {"id": "X-conceptos", "titulo": "Conceptos básicos de la tecnología", "tipo": "flujo", "fuente": "Guía 30 MEN (2008)",
  "pasos": [{"t": p["a"], "d": p["b"]} for p in emparejar[4]["pares"]]},
]

out = {"version": 1, "emparejar": emparejar, "ordenar": ordenar, "clasificar": clasificar, "sopa": sopa, "esquemas": esquemas}
json.dump(out, open(os.path.join(RAIZ, "data", "juegos.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(f"emparejar {len(emparejar)} · ordenar {len(ordenar)} ({[len(o['pasos']) for o in ordenar]}) · clasificar {len(clasificar)} · sopa {len(sopa)} · esquemas {len(esquemas)}")
