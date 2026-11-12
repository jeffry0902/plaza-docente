# -*- coding: utf-8 -*-
"""Convierte el banco piloto (data/banco.json) + fichas al formato del Modelo Basado en Evidencias:
data/marco.json, data/indice.json y data/lotes/2026-11-12-piloto.json.
Uso: python3 tools/construir.py RUTA_CITAS_PY"""
import json, os, sys, importlib.util
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
from contenido_fichas import FICHAS

spec = importlib.util.spec_from_file_location("citas", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
CITAS = m.CITAS

AFIRMACIONES = [
 ("DIS-A1", "DIS", "Naturaleza y evolución", "Comprende los conceptos fundamentales de la tecnología y la informática (artefacto, proceso, sistema, innovación, información) y su evolución."),
 ("DIS-A2", "DIS", "Apropiación y uso", "Orienta la utilización adecuada, segura, pertinente y crítica de la tecnología y la informática."),
 ("DIS-A3", "DIS", "Solución de problemas", "Orienta estrategias para identificar, formular y resolver problemas con tecnología: algoritmos, diseño y detección de fallas."),
 ("DIS-A4", "DIS", "Tecnología y sociedad", "Promueve la valoración crítica, ética y responsable de los impactos de la tecnología en la sociedad y el ambiente."),
 ("DIS-A5", "DIS", "Didáctica del área", "Selecciona estrategias didácticas propias del área y organiza el currículo por componentes y grupos de grados."),
 ("PED-A1", "PED", "Evaluar", "Evalúa con enfoque formativo, conforme al Sistema Institucional de Evaluación de los Estudiantes."),
 ("PED-A2", "PED", "Enseñar", "Planea y desarrolla la enseñanza según el currículo, el PEI y las competencias del docente."),
 ("PED-A3", "PED", "Formar en la diversidad", "Garantiza la educación inclusiva con DUA, PIAR y ajustes razonables."),
 ("NOR-A1", "NOR", "Convivencia y protección", "Actúa ante situaciones de convivencia según la Ley 1620, el Decreto 1965 y la protección integral de la Ley 1098."),
 ("NOR-A2", "NOR", "Organización escolar y carrera", "Conoce el gobierno escolar, el PEI y el Estatuto de Profesionalización Docente."),
 ("LC-A", "LC", "Lectura crítica", "Comprende, interpreta y evalúa textos pedagógicos y normativos."),
 ("RC-A", "RC", "Razonamiento cuantitativo", "Interpreta, formula y argumenta con información cuantitativa en contextos escolares."),
 ("CB-A", "CB", "Competencias blandas", "Actúa con ética, ciudadanía y trabajo en equipo en situaciones de la vida escolar."),
 ("PSI-A", "PSI", "Psicotécnica", "Demuestra las competencias comportamentales del docente (Res. 3842 de 2022)."),
]
FAM_AFIRM = {
 "DIS-CONC":"DIS-A1","DIS-INNOV":"DIS-A1","DIS-SIST":"DIS-A1","DIS-DATOS":"DIS-A1","DIS-SEG":"DIS-A2",
 "DIS-ALGO":"DIS-A3","DIS-FALLAS":"DIS-A3","DIS-DISENO":"DIS-A3","DIS-CTS":"DIS-A4","DIS-DIDAC":"DIS-A5","DIS-COMP":"DIS-A5",
 "PED-EVAL":"PED-A1","PED-EVAL-NORM":"PED-A1","PED-ENSENAR":"PED-A2","PED-CURR":"PED-A2","PED-INCL":"PED-A3",
 "NOR-CONV-TIPO":"NOR-A1","NOR-CONV-RUTA":"NOR-A1","NOR-DERECHOS":"NOR-A1","NOR-FORMAR":"NOR-A1","NOR-ORG":"NOR-A2","NOR-ESTATUTO":"NOR-A2",
}
EVID = {
 "DIS-CONC":"Distingue artefactos, procesos y sistemas en situaciones cotidianas y escolares.",
 "DIS-INNOV":"Diferencia técnica, tecnología y ciencia, y reconoce invención, innovación y descubrimiento.",
 "DIS-SIST":"Explica el funcionamiento de sistemas tecnológicos y el papel de la realimentación.",
 "DIS-DATOS":"Relaciona la informática con las TIC y la representación digital de la información.",
 "DIS-SEG":"Orienta el uso seguro, responsable y autónomo de herramientas y de las TIC.",
 "DIS-ALGO":"Orienta el pensamiento computacional y la programación, con o sin computadores.",
 "DIS-FALLAS":"Orienta la detección de fallas según el grupo de grados (prueba y descarte, hipótesis).",
 "DIS-DISENO":"Reconoce especificaciones, restricciones y alternativas en el proceso de diseño.",
 "DIS-CTS":"Promueve la reflexión ética y la valoración de impactos de la tecnología.",
 "DIS-DIDAC":"Elige la estrategia didáctica del área adecuada para un propósito de aprendizaje.",
 "DIS-COMP":"Ubica desempeños en los cuatro componentes del área y en los grupos de grados.",
}
NUEVAS = {
 "DIS-CONC": dict(componente="DIS", nombre="Artefactos, procesos y sistemas", leccion=dict(
   idea="La Guía 30 organiza los productos de la tecnología en artefactos (objetos), procesos (secuencias que transforman recursos) y sistemas (elementos relacionados con un objetivo común).",
   claves=["Artefacto = dispositivo o herramienta.", "Proceso = fases sucesivas de operaciones.", "Sistema = elementos ligados que logran juntos un objetivo."],
   trampa="Llamar «sistema» a cualquier actividad con etapas: eso es un proceso.", fuente="Guía 30 MEN (2008), p. 6-7.")),
 "DIS-INNOV": dict(componente="DIS", nombre="Técnica, tecnología, ciencia e innovación", leccion=dict(
   idea="Técnica es saber hacer; tecnología agrega el porqué. La ciencia busca entender el mundo; la tecnología lo modifica. Invención crea, innovación mejora, descubrimiento halla lo que existía.",
   claves=["Invención = no existía.", "Innovación = mejora de lo existente.", "Descubrimiento = fenómeno oculto o desconocido."],
   trampa="Llamar invención a una mejora de un artefacto existente.", fuente="Guía 30 MEN (2008), p. 7-8.")),
 "DIS-COMP": dict(componente="DIS", nombre="Componentes del área y grupos de grados", leccion=dict(
   idea="El área se organiza en cuatro componentes: naturaleza y evolución, apropiación y uso, solución de problemas y tecnología y sociedad, en cinco grupos de grados.",
   claves=["Conceptos e historia → naturaleza y evolución.", "Uso seguro → apropiación y uso.", "Fallas y diseño → solución de problemas.", "Impactos y ética → tecnología y sociedad."],
   trampa="Ubicar «ensamblar y desarmar» en apropiación y uso: la guía lo pone en solución de problemas.", fuente="Guía 30 MEN (2008), p. 13-17.")),
}

def main():
    b = json.load(open(os.path.join(RAIZ, "data", "banco.json"), encoding="utf-8"))
    fams = dict(b["familias"]); fams.update(NUEVAS)
    for fid, f in fams.items():
        c = f["componente"]
        f["afirmacion"] = FAM_AFIRM.get(fid) or f"{c}-A"
        f["evidencia"] = EVID.get(fid) or f["nombre"]
    marco = dict(version="mbe-1", actualizado="2026-11-12", componentes=b["componentes"],
                 afirmaciones=[dict(id=i, componente=c, nombre=n, texto=t) for i, c, n, t in AFIRMACIONES], familias=fams)
    items = []
    for it in b["items"]:
        it = dict(it); it["tipo"] = "caso"
        it["citas"] = [dict(doc=d, texto=t) for d, t in CITAS.get(it["id"], [])]
        items.append(it)
    fichas = []; n = 0
    for f in FICHAS:
        fichas.append(dict(id=f["id"], familia=f["familia"], titulo=f["titulo"], lectura=f["lectura"], puntos=f["puntos"],
                           citas=[dict(doc=d, texto=t, ubicacion=u) for d, t, u in f["citas"]]))
        for q in f["preguntas"]:
            n += 1
            ops = [dict(l="ABC"[k], t=t, j=j) for k, (t, j) in enumerate(q["opciones"])]
            clave = next(o["l"] for o in ops if o["j"].startswith("Es correcta"))
            fam = fams[f["familia"]]
            items.append(dict(id=f"K{n:03d}", tipo="conocimiento", ficha=f["id"], familia=f["familia"],
                competencia=next(a[2] for a in AFIRMACIONES if a[0] == fam["afirmacion"]),
                enunciado=q["enunciado"], opciones=ops, clave=clave, fuente=q["citas"][0][2] if len(q["citas"][0]) > 2 else f["citas"][0][2],
                consejo="Pregunta de conocimiento: vuelve a la ficha si dudaste. En el examen este saber aparece dentro de un caso.",
                citas=[dict(doc=d, texto=t, ubicacion=u) for d, t, u in q["citas"]]))
    lote = dict(id="2026-11-12-piloto", fecha="2026-11-12", casos=b["casos"], fichas=fichas, items=items)
    os.makedirs(os.path.join(RAIZ, "data", "lotes"), exist_ok=True)
    w = lambda p, o: json.dump(o, open(os.path.join(RAIZ, "data", p), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    w("marco.json", marco); w("lotes/2026-11-12-piloto.json", lote); w("indice.json", dict(version=1, lotes=["lotes/2026-11-12-piloto.json"]))
    print(len(items), "ítems,", len(fichas), "fichas,", len(fams), "familias")

if __name__ == "__main__":
    main()
