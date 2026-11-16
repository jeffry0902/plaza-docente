# -*- coding: utf-8 -*-
"""Apuntes visuales (sketchnotes) del banco de coordinación.
Solo usa textos ya verificados (data/coord/juegos.json y data/coord/mapas.json) y vuelve a verificarlos contra la fuente.
Uso: python3 tools/sketch_coord.py  ->  data/coord/sketch.json   (después de tools/juegos_coord.py)"""
import json, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validar import compacto

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, "fuentes")
D = os.path.join(RAIZ, "data", "coord")
RAW, LECT = {}, []
for f in sorted(glob.glob(os.path.join(D, "lecturas", "p*.json"))):
    LECT += json.load(open(f, encoding="utf-8"))


def literal(doc, texto):
    if doc not in RAW: RAW[doc] = compacto(open(os.path.join(F, doc + ".txt"), encoding="utf-8", errors="ignore").read())
    t = texto.rstrip("…").strip()
    if doc + "#L" not in RAW: RAW[doc + "#L"] = compacto(" ".join(" ".join(l["parrafos"]) for l in LECT if l["doc"] == doc))
    assert compacto(t) in RAW[doc] or compacto(t) in RAW[doc + "#L"], f"NO LITERAL en {doc}: {t[:80]}"
    return texto


def lectura(doc, frase):
    c = compacto(frase.rstrip("…")[:120])
    for l in LECT:
        if l["doc"] == doc and c in compacto(" ".join(l["parrafos"])): return l["id"]
    return None


def corto(t, n=22):
    w = t.split()
    if len(w) <= n: return t
    s = " ".join(w[:n]); k = max(s.rfind(","), s.rfind(";"))
    if k > len(s) * 0.55: s = s[:k]
    return s.rstrip(" ,;:") + "…"


def nodo(doc, t, d, icono, n=22):
    d = corto(d, n); literal(doc, d)
    return {"t": t, "d": d, "i": icono, "lec": lectura(doc, d)}


J = json.load(open(os.path.join(D, "juegos.json"), encoding="utf-8"))
EMP = {e["id"]: e for e in J["emparejar"]}
ORD = {o["id"]: o for o in J["ordenar"]}
CLA = {c["id"]: c for c in J["clasificar"]}


def pares(eid, iconos, n=22):
    e = EMP[eid]
    return [nodo(e["doc"], p["a"], p["b"], ic, n) for p, ic in zip(e["pares"], iconos)]


paginas = []
def pagina(id, doc, capitulo, titulo, centro, tipo, nodos, fuente):
    paginas.append({"id": id, "doc": doc, "capitulo": capitulo, "titulo": titulo, "centro": centro, "tipo": tipo,
                    "nodos": nodos, "fuente": fuente, "lec": next((n.get("lec") for n in nodos if n.get("lec")), None)})


G34, L715, R3842, D75, L20, D65, D21 = ("guia34_mineducacion_2008", "ley_715_2001", "resolucion_3842_2022_ocr", "decreto_1075_2015",
                                         "ley_1620_2013", "decreto_1965_2013", "decreto_1421_2017")

# ---------- Guía 34 ----------
ruta = ORD["O-ruta34"]["pasos"]
anclas = ["La primera etapa de la ruta del mejoramiento continuo es la autoevaluación institucional",
          "La segunda etapa consiste en la elaboración del plan de mejoramiento",
          "la tercera etapa consiste en el seguimiento periódico al desarrollo del plan de mejoramiento"]
pagina("C-ruta34", G34, "Guía 34 · Ruta", "La ruta del mejoramiento continuo", "Tres etapas que se repiten", "flujo",
       [nodo(G34, f"Etapa {k}", a, ic, 18) for k, (a, ic) in enumerate(zip(anclas, ["🔎", "🗺️", "📈"]), 1)], "Guía 34 MEN (2008), 1.11")
pagina("C-escala34", G34, "Guía 34 · Etapa 1", "Escala de la autoevaluación", "¿Qué tan desarrollado está cada proceso?", "columnas",
       pares("E-escala34", ["1️⃣", "2️⃣", "3️⃣", "4️⃣"], 20), "Guía 34 MEN (2008), Etapa 1, paso 2")
cats = CLA["C-areas34"]["categorias"]
pagina("C-areas34", G34, "Guía 34 · Cuadro No. 3", "Las cuatro áreas de gestión", "Gestión institucional", "radial",
       [{"t": a, "d": None, "lista": ps, "i": ic, "lec": None} for (a, ps), ic in zip(cats.items(), ["🧭", "📚", "🗂️", "🤝"])], "Guía 34 MEN (2008), Cuadro No. 3")
pagina("C-procesos34", G34, "Guía 34 · Cuadro No. 3", "Para qué sirve cada proceso", "Procesos clave para el coordinador", "radial",
       pares("E-procesos34", ["🏛️", "🌤️", "🧑‍🏫", "👥", "🏘️", "⛑️"], 16), "Guía 34 MEN (2008), Cuadro No. 3")
pasos = ORD["O-plan34"]["pasos"]
pagina("C-plan34", G34, "Guía 34 · Etapa 2", "Pasos del plan de mejoramiento", "Horizonte de tres años", "flujo",
       [nodo(G34, f"Paso {k}", p, ic, 14) for k, (p, ic) in enumerate(zip(pasos, ["🎯", "📏", "📊", "👤", "🗓️", "💰", "📣"]), 1)], "Guía 34 MEN (2008), Etapa 2")

# ---------- Funciones ----------
fun = CLA["C-funciones"]["categorias"]
docs_fun = {"Rector (Ley 715)": L715, "Coordinador (Res. 3842)": R3842, "Consejo directivo (Decreto 1075)": D75}
ns = []
for (k, items), ic in zip(fun.items(), ["👔", "🧑‍💼", "🏛️"]):
    doc = docs_fun[k]
    for x in items: literal(doc, corto(x, 12))
    ns.append({"t": k, "d": None, "lista": [corto(x, 12) for x in items], "i": ic, "lec": lectura(doc, items[0])})
pagina("C-quien", R3842, "Ley 715 · Res. 3842 · Decreto 1075", "¿Rector, coordinador o consejo directivo?", "¿A quién le corresponde?", "columnas",
       ns, "Ley 715 de 2001, art. 10; Resolución 3842 de 2022, 1.3.1; Decreto 1075 de 2015")

# ---------- SIEE ----------
siee = ORD["O-siee"]["pasos"]
pagina("C-siee", D75, "Decreto 1290 (en el 1075)", "Crear o modificar el SIEE", "Procedimiento mínimo", "flujo",
       [nodo(D75, f"Paso {k}", p, "📝", 14) for k, p in enumerate(siee, 1)], "Decreto 1075 de 2015, art. 2.3.3.3.3.8")

# ---------- Convivencia ----------
pagina("C-ruta", L20, "Ley 1620 · Art. 30", "Ruta de Atención Integral: 4 componentes", "Ruta de Atención Integral para la Convivencia Escolar", "flujo",
       pares("E-ruta", ["🌱", "🛡️", "🤝", "📊"], 18), "Ley 1620 de 2013, art. 30")
pagina("C-tipos", D65, "Decreto 1965 · Art. 40", "Situaciones tipo I, II y III", "¿Qué tan grave es la situación?", "columnas",
       pares("E-situaciones", ["🟢", "🟠", "🔴"], 24), "Decreto 1965 de 2013, art. 40")
t2 = ORD["O-tipo2"]["pasos"][:5]
pagina("C-proto2", D65, "Decreto 1965 · Art. 43", "Protocolo tipo II: lo primero", "Pasos en orden", "flujo",
       [nodo(D65, f"Paso {k}", p, ic, 16) for k, (p, ic) in enumerate(zip(t2, ["🚑", "🛡️", "📞", "🗣️", "🔧"]), 1)], "Decreto 1965 de 2013, art. 43")

# ---------- Inclusión ----------
pagina("C-inclusion", D21, "Decreto 1421 · Definiciones", "Educación inclusiva: palabras clave", "Atención educativa a la población con discapacidad", "radial",
       pares("E-inclusion", ["🔧", "📚", "🌐", "🤗", "📝"], 18), "Decreto 1421 de 2017, art. 2.3.3.5.1.4")

json.dump({"version": 1, "cargo": "coordinador", "paginas": paginas}, open(os.path.join(D, "sketch.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"apuntes: {len(paginas)} páginas · {sum(len(p['nodos']) for p in paginas)} notas · sin lectura: {[n['t'] for p in paginas for n in p['nodos'] if not n.get('lec')]}")
