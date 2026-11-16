# -*- coding: utf-8 -*-
"""Sketchnotes (apuntes visuales dibujados a mano) por documento y capítulo.
Solo usa textos que ya están verificados literalmente (data/juegos.json y data/mapas.json),
recortados como prefijo con "…" cuando son largos. Cada texto se vuelve a verificar contra la fuente.
Uso: python3 tools/sketch.py  ->  data/sketch.json"""
import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validar import compacto

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, "fuentes")
RAW = {}
import glob as _g
LECT = []
for f in sorted(glob.glob(os.path.join(RAIZ, "data", "lecturas", "p*.json"))):
    LECT += json.load(open(f, encoding="utf-8"))
def literal(doc, texto):
    if doc not in RAW: RAW[doc] = compacto(open(os.path.join(F, doc + ".txt"), encoding="utf-8", errors="ignore").read())
    t = texto.rstrip("…").strip()
    # también vale el texto de las lecturas (mismo documento, con las columnas del PDF ya en orden)
    if doc + "#L" not in RAW: RAW[doc + "#L"] = compacto(" ".join(" ".join(l["parrafos"]) for l in LECT if l["doc"] == doc))
    assert compacto(t) in RAW[doc] or compacto(t) in RAW[doc + "#L"], f"NO LITERAL en {doc}: {t[:80]}"
    return texto

J = json.load(open(os.path.join(RAIZ, "data", "juegos.json"), encoding="utf-8"))
M = {m["doc"]: m["mapa"] for m in json.load(open(os.path.join(RAIZ, "data", "mapas.json"), encoding="utf-8"))}
EMP = {e["id"]: e for e in J["emparejar"]}

def lectura(doc, frase):
    c = compacto(frase.rstrip("…")[:120])
    for l in LECT:
        if l["doc"] == doc and c in compacto(" ".join(l["parrafos"])): return l["id"]
    return None

def corto(t, n=22):
    """Prefijo literal: hasta n palabras, cortando en coma/punto y coma si se puede."""
    w = t.split()
    if len(w) <= n: return t
    s = " ".join(w[:n]); k = max(s.rfind(","), s.rfind(";"))
    if k > len(s) * 0.55: s = s[:k]
    return s.rstrip(" ,;:") + "…"

G30, L20, D65, D21, L115 = "guia30_mineducacion_2008", "ley_1620_2013", "decreto_1965_2013", "decreto_1421_2017", "ley_115_1994"
def nodo(doc, t, d, icono, n=22):
    d = corto(d, n); literal(doc, d)
    return {"t": t, "d": d, "i": icono, "lec": lectura(doc, d)}

def pares(eid, iconos, n=22):
    e = EMP[eid]
    return [nodo(e["doc"], p["a"], p["b"], ic, n) for p, ic in zip(e["pares"], iconos)]

paginas = []
def pagina(id, doc, capitulo, titulo, centro, tipo, nodos, fuente, frase=None):
    paginas.append({"id": id, "doc": doc, "capitulo": capitulo, "titulo": titulo, "centro": centro, "tipo": tipo,
                    "nodos": nodos, "fuente": fuente, "lec": nodos[0].get("lec") if nodos else None})

# ---------- Guía 30 ----------
for e in J["emparejar"]: pass
pagina("K-tec", G30, "Guía 30 · Cap. 1", "La tecnología: conceptos básicos", "¿Qué involucra la tecnología?", "radial",
       pares("E-guia30", ["⚙️", "🔄", "🧩"])[:3], "Guía 30 MEN (2008), págs. 5-6")
pagina("K-innova", G30, "Guía 30 · Cap. 1", "Innovar, inventar, descubrir", "Tecnología, innovación, invención y descubrimiento", "columnas",
       pares("E-guia30", ["", "", "", "💡", "🛠️", "🔭"])[3:], "Guía 30 MEN (2008), pág. 8")
comps = M[G30]["h"][0]["h"]
pagina("K-comp", G30, "Guía 30 · Cap. 2", "Los 4 componentes del área", "Educación en tecnología", "radial",
       [nodo(G30, c["t"], c["d"], ic, 20) for c, ic in zip(comps, ["🕰️", "📱", "🧠", "🌍"])], "Guía 30 MEN (2008), pág. 14")
grupos = M[G30]["h"][1]["h"]
pagina("K-grados", G30, "Guía 30 · Cap. 3", "Competencias por grupos de grados", "5 grupos de grados", "flujo",
       [{"t": g["t"], "d": "4 componentes · " + str(sum(len(c.get("h", [])) for c in g["h"])) + " desempeños", "i": ic, "lec": None}
        for g, ic in zip(grupos, ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"])], "Guía 30 MEN (2008), págs. 16-25")

# ---------- Ley 1620 y Decreto 1965 ----------
pagina("K-ruta", L20, "Ley 1620 · Art. 30", "Ruta de Atención Integral: 4 componentes", "Ruta de Atención Integral para la Convivencia Escolar", "flujo",
       pares("E-ruta", ["🌱", "🛡️", "🤝", "📊"], 18), "Ley 1620 de 2013, art. 30")
pagina("K-tipos", D65, "Decreto 1965 · Art. 40", "Situaciones tipo I, II y III", "¿Qué tan grave es la situación?", "columnas",
       pares("E-situaciones", ["🟢", "🟠", "🔴"], 24), "Decreto 1965 de 2013, art. 40")
pt1 = J["ordenar"][0]
pagina("K-proto1", D65, "Decreto 1965 · Art. 42", "Protocolo para situaciones tipo I", "Pasos en orden", "flujo",
       [nodo(D65, f"Paso {k}", p, ic, 18) for k, (p, ic) in enumerate(zip(pt1["pasos"], ["👥", "⚖️", "🔍"]), 1)], "Decreto 1965 de 2013, art. 42")
pagina("K-agresion", D65, "Decreto 1965 · Art. 39", "Tipos de agresión escolar", "Agresión escolar", "radial",
       pares("E-agresion", ["👊", "🗣️", "🙄", "💔", "📲"], 16), "Decreto 1965 de 2013, art. 39")

# ---------- Decreto 1421 ----------
pagina("K-inclusion", D21, "Decreto 1421 · Definiciones", "Educación inclusiva: palabras clave", "Atención educativa a la población con discapacidad", "radial",
       pares("E-inclusion", ["🔧", "📚", "🌐", "🤗", "📝"], 18), "Decreto 1421 de 2017, art. 2.3.3.5.1.4")

# ---------- Ley 115 y Ley 1620: gobierno escolar ----------
gob = next(e for e in J["esquemas"] if e["id"] == "X-gobierno")
ns = []
for g, ic in zip(gob["grupos"], ["🏛️", "👔", "📖", "🕊️"]):
    doc = L20 if "1620" in g["f"] else L115
    txt = "; ".join(g["items"][:4]) if len(g["items"]) > 1 else g["items"][0]
    d = corto(g["items"][0], 20) if len(g["items"]) == 1 else None
    if d: literal(doc, d)
    else:
        for x in g["items"][:4]: literal(doc, corto(x, 12))
    ns.append({"t": g["t"].split(" (")[0], "d": d, "lista": None if d else [corto(x, 12) for x in g["items"][:4]] + (["…"] if len(g["items"]) > 4 else []),
               "i": ic, "lec": lectura(doc, g["items"][0]), "f": g["f"]})
pagina("K-gobierno", L115, "Ley 115 · Arts. 142-145 · Ley 1620 · Art. 12", "Gobierno escolar y comité de convivencia", "¿Quién decide en el colegio?", "columnas",
       ns, "Ley 115 de 1994 y Ley 1620 de 2013")

out = {"version": 1, "paginas": paginas}
json.dump(out, open(os.path.join(RAIZ, "data", "sketch.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"sketchnotes: {len(paginas)} páginas · {sum(len(p['nodos']) for p in paginas)} notas · sin lectura: {[n['t'] for p in paginas for n in p['nodos'] if not n.get('lec')]}")
