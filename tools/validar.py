#!/usr/bin/env python3
"""Validador del banco de Plaza Docente.

Uso:
  python3 tools/validar.py --fuentes RUTA_FUENTES [--estricto]
  python3 tools/validar.py --fuentes RUTA_FUENTES --buscar DOC "texto"

Verifica:
  1. Estructura de marco.json, indice.json y cada lote.
  2. Que toda cita textual exista LITERALMENTE (normalizando espacios, guiones de corte
     de línea y comillas) en el documento oficial correspondiente de la carpeta de fuentes.
  3. Que los ítems de los componentes DIS, PED y NOR (y todas las fichas) tengan al menos una cita.
  4. Ids únicos, 3 opciones, clave válida, familias existentes, justificación por opción.
Sale con código 1 si hay errores. Los avisos no bloquean.
"""
import argparse, json, os, re, sys, unicodedata, collections

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIERE_CITA = {"DIS", "PED", "NOR"}


def norm(t: str) -> str:
    t = unicodedata.normalize("NFC", t)
    t = t.replace("\u0002", "").replace("­", "").replace("﻿", "")
    t = re.sub(r"[«»“”\"'‘’`´]", "", t)
    t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)          # palabra cortada al final de línea
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\s+([,.;:)])", r"\1", t)
    t = re.sub(r"\(\s+", "(", t)
    return t.lower().strip()


def compacto(t: str) -> str:
    """Versión sin espacios ni puntuación: tolera cortes de línea raros del PDF."""
    return re.sub(r"[\W_]+", "", norm(t))


def cargar_fuentes(carpeta):
    docs = {}
    for f in os.listdir(carpeta):
        if f.endswith(".txt"):
            with open(os.path.join(carpeta, f), encoding="utf-8", errors="ignore") as fh:
                raw = fh.read()
            docs[f[:-4]] = (norm(raw), compacto(raw))
    return docs


def cita_ok(docs, doc, texto):
    if doc not in docs:
        return False, f"documento '{doc}' no existe en fuentes"
    n, c = docs[doc]
    if norm(texto) in n or compacto(texto) in c:
        return True, ""
    return False, "la cita no aparece literalmente en el documento"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fuentes", required=True)
    ap.add_argument("--estricto", action="store_true", help="los avisos también fallan")
    ap.add_argument("--buscar", nargs=2, metavar=("DOC", "TEXTO"))
    a = ap.parse_args()
    docs = cargar_fuentes(a.fuentes)
    if a.buscar:
        ok, msg = cita_ok(docs, *a.buscar)
        print("OK" if ok else f"NO: {msg}")
        sys.exit(0 if ok else 1)

    errores, avisos = [], []
    marco = json.load(open(os.path.join(RAIZ, "data", "marco.json"), encoding="utf-8"))
    indice = json.load(open(os.path.join(RAIZ, "data", "indice.json"), encoding="utf-8"))
    comps = {c["id"] for c in marco["componentes"]}
    fams = marco["familias"]
    afirm = {x["id"]: x for x in marco["afirmaciones"]}
    for fid, f in fams.items():
        if f.get("componente") not in comps: errores.append(f"familia {fid}: componente inválido")
        if f.get("afirmacion") not in afirm: errores.append(f"familia {fid}: afirmación inválida")
        if not f.get("evidencia"): errores.append(f"familia {fid}: falta texto de evidencia")
        L = f.get("leccion", {})
        for k in ("idea", "claves", "trampa", "fuente"):
            if not L.get(k): errores.append(f"familia {fid}: lección sin '{k}'")

    ids, casos, fichas = set(), {}, {}
    items = []
    for lote in indice["lotes"]:
        d = json.load(open(os.path.join(RAIZ, "data", lote), encoding="utf-8"))
        for c in d.get("casos", []):
            if c["id"] in casos: errores.append(f"caso duplicado {c['id']}")
            casos[c["id"]] = c
        for fi in d.get("fichas", []):
            if fi["id"] in fichas: errores.append(f"ficha duplicada {fi['id']}")
            fichas[fi["id"]] = fi
            if fi.get("familia") not in fams: errores.append(f"ficha {fi['id']}: familia inexistente")
            if not fi.get("citas"): errores.append(f"ficha {fi['id']}: sin citas")
            for ct in fi.get("citas", []):
                ok, m = cita_ok(docs, ct.get("doc", ""), ct.get("texto", ""))
                if not ok: errores.append(f"ficha {fi['id']}: {m} → «{ct.get('texto','')[:90]}»")
        for it in d.get("items", []):
            it["_lote"] = lote
            items.append(it)

    letras = collections.Counter()
    for it in items:
        i = it.get("id")
        if i in ids: errores.append(f"ítem duplicado {i}")
        ids.add(i)
        f = fams.get(it.get("familia"))
        if not f: errores.append(f"{i}: familia inexistente {it.get('familia')}"); continue
        if it.get("tipo") not in ("caso", "conocimiento"): errores.append(f"{i}: tipo inválido")
        if it.get("tipo") == "caso" and it.get("caso") not in casos: errores.append(f"{i}: caso inexistente")
        if it.get("tipo") == "conocimiento" and it.get("ficha") and it["ficha"] not in fichas:
            errores.append(f"{i}: ficha inexistente")
        ops = it.get("opciones", [])
        if len(ops) != 3 or sorted(o["l"] for o in ops) != ["A", "B", "C"]: errores.append(f"{i}: debe tener opciones A, B, C")
        if it.get("clave") not in [o["l"] for o in ops]: errores.append(f"{i}: clave inválida")
        for o in ops:
            if not o.get("t") or not o.get("j"): errores.append(f"{i}: opción {o.get('l')} sin texto o justificación")
        correctas = [o for o in ops if o.get("j", "").lower().startswith("es correcta")]
        if len(correctas) != 1 or correctas[0]["l"] != it.get("clave"):
            errores.append(f"{i}: la justificación 'Es correcta' no coincide con la clave")
        letras[it.get("clave")] += 1
        if not it.get("fuente") or not it.get("consejo"): errores.append(f"{i}: falta fuente o consejo")
        if f["componente"] in REQUIERE_CITA and not it.get("citas"):
            errores.append(f"{i}: componente {f['componente']} exige al menos una cita textual")
        for ct in it.get("citas", []):
            ok, m = cita_ok(docs, ct.get("doc", ""), ct.get("texto", ""))
            if not ok: errores.append(f"{i}: {m} → «{ct.get('texto','')[:90]}»")
        largos = [len(o.get("t", "")) for o in ops]
        if largos and max(largos) > 1.9 * max(1, min(largos)):
            avisos.append(f"{i}: opciones de longitud muy desigual (pista involuntaria)")

    usadas = collections.Counter(it["familia"] for it in items if it.get("familia"))
    for fid in fams:
        if usadas[fid] < 2: avisos.append(f"familia {fid}: solo {usadas[fid]} ítem(s); el repaso necesita variantes")

    print(f"Ítems: {len(items)} · casos: {len(casos)} · fichas: {len(fichas)} · familias: {len(fams)}")
    print(f"Claves: {dict(letras)} (la app baraja las opciones al mostrarlas)")
    for e in errores: print("ERROR  ", e)
    for w in avisos: print("AVISO  ", w)
    malo = errores or (a.estricto and avisos)
    print("RESULTADO:", "FALLA" if malo else "OK")
    sys.exit(1 if malo else 0)


if __name__ == "__main__":
    main()
