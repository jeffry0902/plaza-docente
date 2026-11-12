# -*- coding: utf-8 -*-
"""Plan de lectura: parte los documentos oficiales en "páginas" de lectura (~450-750 palabras),
las ordena por prioridad y vincula cada pregunta del banco con el pasaje del documento donde está su cita.

Uso: python3 tools/fragmentar.py [--fuentes fuentes]
Genera:
  data/lecturas/indice.json   orden del plan (id, doc, titulo, palabras, archivo)
  data/lecturas/pNNN.json     bloques de 10 lecturas con el texto
  data/contextos.json         por ítem: pasaje corto para leer ANTES de responder + lectura a la que pertenece
"""
import json, os, re, sys, glob, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validar import norm, compacto

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (stem, nombre visible, grupo de prioridad, peso dentro del grupo, regex inicio, regex fin, tipo)
DOCS = [
 ("guia30_mineducacion_2008", "Guía 30 MEN (2008)", 1, 1.0, r"Asamblea General por la Educación", r"^Bibliografía", "guia"),
 ("orientaciones_tecnologia_2022", "Orientaciones Curriculares de Tecnología e Informática (MEN, 2022)", 1, 1.0, r"^PRESENTACIÓN ORIENTACIONES", r"^\s*Bibliografía", "guia"),
 ("ley_1620_2013", "Ley 1620 de 2013 (convivencia escolar)", 2, 1.0, r"^ARTÍCULO 1o", None, "ley"),
 ("decreto_1965_2013", "Decreto 1965 de 2013 (reglamenta la Ley 1620)", 2, 1.0, r"^ARTÍCULO 1\b|^Artículo 1\b|^ARTICULO 1\b", None, "ley"),
 ("decreto_1421_2017", "Decreto 1421 de 2017 (educación inclusiva)", 2, 1.0, r"^ARTÍCULO 1\b|^Artículo 1\b|^ARTICULO 1\b", None, "ley"),
 ("decreto_1075_2015", "Decreto 1290 de 2009 · evaluación (compilado en el Decreto 1075)", 3, 0.6, r"^ARTÍCULO 2\.3\.3\.3\.3\.1\.", r"^ARTÍCULO 2\.3\.3\.3\.3\.18\.", "ley"),
 ("ley_115_1994", "Ley 115 de 1994 (Ley General de Educación)", 3, 1.0, r"^ARTICULO 1o", None, "ley"),
 ("decreto_1278_2002", "Decreto 1278 de 2002 (Estatuto docente)", 3, 0.8, r"^ARTÍCULO 1\b|^Artículo 1\b|^ARTICULO 1\b", None, "ley"),
 ("resolucion_3842_2022_ocr", "Resolución 3842 de 2022 (funciones y competencias del docente)", 3, 0.6, r"ULTIMO:^2\.1 DOCENTES DE AULA", r"^2\.2 DOCENTE ORIENTADOR", "guia"),
 ("ley_1098_2006", "Ley 1098 de 2006 (Código de Infancia y Adolescencia)", 3, 0.8, r"^ARTÍCULO 1o|^ARTÍCULO 1\b", r"^LIBRO II", "ley"),
]
PESO_GRUPO = {1: 0.5, 2: 0.3, 3: 0.2}
ART = re.compile(r"^(ART[ÍI]CULO|Artículo|ARTICULO)\s+([\d\.]+[o°]?)", re.I)


def limpiar_lineas(raw):
    out = []
    raw = raw.replace("\u0002", "").replace("\x0c", "\n")
    raw = re.sub(r"\n([A-ZÁÉÍÓÚ])\n\s*\n([a-záéíóúñ])", r"\n\1\2", raw)                  # letra capital separada
    raw = re.sub(r"\d{0,3}\s*Orientaciones Curriculares para el Área de Tecnología e Informática en la Educación Básica y Media\s*\d{0,3}", " ", raw)
    raw = re.sub(r"([a-záéíóúñ])- ([a-záéíóúñ])", r"\1\2", raw)                              # "em- plear"
    raw = raw.replace(" • ", "\n• ")
    for l in raw.split("\n"):
        s = l.strip()
        if not s: out.append(""); continue
        if re.fullmatch(r"\d{1,3}", s): continue                       # número de página
        if re.fullmatch(r"\d{1,3}\s+Orientaciones Curriculares.*", s): continue   # encabezado de página
        if s.startswith("Orientaciones Curriculares para el Área de Tecnología e Informática en la Educación Básica y Media") and len(s) < 110: continue
        if re.fullmatch(r"[•·\-–—_]{1,3}", s): continue
        out.append(s)
    return out


def parrafos(lineas):
    pars, cur = [], ""
    for s in lineas:
        if not s:
            if cur: pars.append(cur); cur = ""
            continue
        nuevo = bool(ART.match(s) or re.match(r"^(PARÁGRAFO|Parágrafo|CAPÍTULO|Capítulo|TÍTULO|SECCIÓN|Sección|LIBRO)\b", s)
                     or re.match(r"^(\d{1,2}[\.\)]|[a-z]\)|[•✔–\-])\s", s))
        if cur and (nuevo or (cur.endswith((".", ":", ";")) and s[:1].isupper() and len(cur) > 200)):
            pars.append(cur); cur = s
        elif cur:
            cur = cur[:-1] + s if cur.endswith("-") and s[:1].islower() else cur + " " + s
        else:
            cur = s
    if cur: pars.append(cur)
    salida = []
    for p in pars:
        p = re.sub(r"\s+", " ", p).strip()
        if len(p) <= 1: continue
        while palabras(p) > 170:
            frases = re.split(r"(?<=[\.;:])\s+(?=[A-ZÁÉÍÓÚ¿¡•])", p)
            acc, k = "", 0
            while k < len(frases) and palabras(acc) < 110: acc = (acc + " " + frases[k]).strip(); k += 1
            if k >= len(frases): break
            salida.append(acc); p = " ".join(frases[k:])
        salida.append(p)
    return salida


def palabras(t): return len(t.split())


def fragmentos(stem, nombre, tipo, pars):
    frs, cur = [], []
    w = lambda: sum(palabras(p) for p in cur)
    for p in pars:
        corte = cur and (w() >= 750 or (w() >= 420 and (ART.match(p) or (tipo == "guia" and es_titulo(p)))))
        if corte: frs.append(cur); cur = []
        cur.append(p)
    if cur:
        if frs and w() < 200: frs[-1].extend(cur)
        else: frs.append(cur)
    out = []
    for k, ps in enumerate(frs, 1):
        arts = [ART.match(p).group(2).rstrip("o°.") for p in ps if ART.match(p)]
        if tipo == "ley" and arts:
            sub = f"Art. {arts[0]}" if len(arts) == 1 else f"Arts. {arts[0]} a {arts[-1]}"
        else:
            tit = next((p for p in ps if es_titulo(p)), None)
            sub = "Presentación" if k == 1 else (tit[:80] if tit else f"Parte {k}")
        out.append(dict(doc=stem, nombre=nombre, parte=k, total=len(frs), titulo=sub, parrafos=ps, palabras=sum(palabras(p) for p in ps)))
    return out


def es_titulo(p):
    return 2 <= palabras(p) <= 12 and not p.endswith((".", ",", ";", ":")) and p[:1].isupper() and not ART.match(p)


def cortar(lineas, ini, fin):
    i0 = 0
    if ini and ini.startswith("ULTIMO:"):
        m = [i for i, l in enumerate(lineas) if re.search(ini[7:], l)]
        i0 = m[-1] if m else 0
    elif ini:
        i0 = next((i for i, l in enumerate(lineas) if re.search(ini, l)), 0)
    i1 = len(lineas)
    if fin:
        i1 = next((i for i, l in enumerate(lineas) if i > i0 and re.search(fin, l)), len(lineas))
    return lineas[i0:i1]


def orden_plan(por_doc):
    """Intercalado por prioridad (stride scheduling): grupo 1 = 50 %, grupo 2 = 30 %, grupo 3 = 20 %.
    Dentro del grupo, los documentos avanzan en paralelo según su peso; la Guía 30 va antes que las Orientaciones."""
    grupos = {}
    for (stem, nombre, g, peso, *_ ) in DOCS:
        if por_doc.get(stem): grupos.setdefault(g, []).append([stem, peso, 0.0])
    cola = {stem: list(fs) for stem, fs in por_doc.items()}
    # grupo 1: secuencial (Guía 30 completa y luego Orientaciones), los demás intercalados
    def siguiente_del_grupo(g):
        docs = [d for d in grupos[g] if cola[d[0]]]
        if not docs: return None
        if g == 1: return cola[docs[0][0]].pop(0)
        d = min(docs, key=lambda d: d[2]); d[2] += 1 / d[1]
        return cola[d[0]].pop(0)
    pase = {g: 0.0 for g in grupos}; plan = []
    while any(cola.values()):
        vivos = [g for g in grupos if any(cola[d[0]] for d in grupos[g])]
        g = min(vivos, key=lambda g: pase[g]); pase[g] += 1 / PESO_GRUPO[g]
        f = siguiente_del_grupo(g)
        if f: plan.append(f)
    return plan


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--fuentes", default=os.path.join(RAIZ, "fuentes")); a = ap.parse_args()
    por_doc = {}
    for stem, nombre, g, peso, ini, fin, tipo in DOCS:
        raw = open(os.path.join(a.fuentes, stem + ".txt"), encoding="utf-8", errors="ignore").read()
        por_doc[stem] = fragmentos(stem, nombre, tipo, parrafos(cortar(limpiar_lineas(raw), ini, fin)))
    plan = orden_plan(por_doc)
    d = os.path.join(RAIZ, "data", "lecturas"); os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, "p*.json")): os.remove(f)
    indice = []
    for i, f in enumerate(plan):
        f["id"] = f"L{i + 1:03d}"; f["archivo"] = f"lecturas/p{i // 10 + 1:03d}.json"
        indice.append({k: f[k] for k in ("id", "doc", "nombre", "parte", "total", "titulo", "palabras", "archivo")})
    for b in range(0, len(plan), 10):
        json.dump([{k: f[k] for k in ("id", "doc", "nombre", "parte", "total", "titulo", "parrafos")} for f in plan[b:b + 10]],
                  open(os.path.join(d, f"p{b // 10 + 1:03d}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"version": 1, "lecturas": indice}, open(os.path.join(d, "indice.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    # ---- vínculo pregunta → pasaje ----
    pasajes = []   # (lectura_id, doc, idx_parrafo, compacto)
    for f in plan:
        for j, p in enumerate(f["parrafos"]): pasajes.append((f["id"], f["doc"], j, compacto(p), f))
    def ubicar(doc, texto):
        c = compacto(texto)[:160]
        if len(c) < 15: return None
        # 1) mismo documento, 2) cualquier documento del plan
        for solo_doc in (True, False):
            for k, (lid, pdoc, j, pc, f) in enumerate(pasajes):
                if solo_doc and pdoc != doc: continue
                ventana = pc + (pasajes[k + 1][3] if k + 1 < len(pasajes) and pasajes[k + 1][0] == lid else "")
                if c[:60] in ventana: return f, j
        return None
    indice_items = json.load(open(os.path.join(RAIZ, "data", "indice.json"), encoding="utf-8"))
    contextos = {}
    sin = 0
    for lote in indice_items["lotes"]:
        for it in json.load(open(os.path.join(RAIZ, "data", lote), encoding="utf-8")).get("items", []):
            r = None
            for ct in it.get("citas", []):
                r = ubicar(ct["doc"], ct["texto"])
                if r: break
            if not r:
                sin += 1; continue
            f, j = r
            ps = f["parrafos"]; a0, a1 = j, j + 1
            while sum(palabras(p) for p in ps[a0:a1]) < 140 and (a0 > 0 or a1 < len(ps)):
                if a0 > 0: a0 -= 1
                if sum(palabras(p) for p in ps[a0:a1]) < 140 and a1 < len(ps): a1 += 1
            texto = ps[a0:a1]
            while sum(palabras(p) for p in texto) > 320 and len(texto) > 1:
                texto = texto[1:] if texto.index(ps[j]) > 0 else texto[:-1]
            contextos[it["id"]] = {"lectura": f["id"], "doc": f["doc"], "nombre": f["nombre"], "titulo": f["titulo"], "parrafos": texto}
    json.dump(contextos, open(os.path.join(RAIZ, "data", "contextos.json"), "w", encoding="utf-8"), ensure_ascii=False)
    tot = sum(f["palabras"] for f in plan)
    print(f"Plan: {len(plan)} lecturas · {tot} palabras · {round(tot / 180)} min de lectura total")
    for stem in por_doc: print(f"  {stem}: {len(por_doc[stem])} lecturas")
    print(f"Ítems con pasaje previo: {len(contextos)} · sin ubicar: {sin}")


if __name__ == "__main__":
    main()
