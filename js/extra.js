/* Plaza Docente · módulo visual: mapas mentales, esquemas, juegos (retos distintos) y lectura en voz alta.
   Se integra con app.js a través de window.PD (expuesto por app.js). */
(() => {
"use strict";
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const COLORES = ["#58CC02", "#1CB0F6", "#FF9600", "#CE82FF", "#FF4B4B", "#00CD9C", "#FFC800", "#2B70C9"];

/* ---------- voz ---------- */
const Voz = {
  activo: null,
  ok: "speechSynthesis" in window,
  voz() { const vs = speechSynthesis.getVoices(); return vs.find(v => /es[-_](CO|MX|US|419)/i.test(v.lang)) || vs.find(v => /^es/i.test(v.lang)); },
  hablar(txt, id) {
    if (!this.ok) { PD.toast("Tu navegador no permite lectura en voz alta"); return; }
    if (this.activo === id) { speechSynthesis.cancel(); this.activo = null; PD.render(); return; }
    speechSynthesis.cancel();
    const partes = String(txt).match(/[^.!?;:]+[.!?;:]*/g) || [txt];      // iOS corta textos largos: se dicta por frases
    const v = this.voz(); this.activo = id;
    partes.forEach((p, i) => { const u = new SpeechSynthesisUtterance(p.trim()); u.lang = v?.lang || "es-CO"; if (v) u.voice = v; u.rate = 1;
      if (i === partes.length - 1) u.onend = () => { if (this.activo === id) { this.activo = null; PD.render(); } };
      speechSynthesis.speak(u); });
    PD.render();
  },
  boton(txt, id, etiqueta = "Escuchar") {
    if (!this.ok) return "";
    return `<button class="chip voz ${this.activo === id ? "xp" : ""}" data-a="voz" data-id="${esc(id)}" data-txt="${esc(txt)}">${this.activo === id ? "⏹ Detener" : "🔊 " + etiqueta}</button>`;
  }
};
if (Voz.ok) speechSynthesis.getVoices();

/* ---------- datos ---------- */
let J = null;   // juegos.json
let MAPAS = null;
async function cargar() {
  if (J && MAPAS) return;
  const get = u => fetch(u, { cache: "no-cache" }).then(r => r.json());
  try { [J, MAPAS] = await Promise.all([get("data/juegos.json"), get("data/mapas.json")]); }
  catch { PD.toast("Sin conexión: los mapas y juegos se cargarán con internet."); }
}

/* ---------- librerías gráficas (se cargan solo cuando se necesitan) ---------- */
const _scripts = {};
function cargarScript(src) { return _scripts[src] ||= new Promise((ok, mal) => { const s = document.createElement("script"); s.src = src; s.onload = ok; s.onerror = mal; document.head.appendChild(s); }); }
async function libsMapa() { await cargarScript("js/vendor/d3.min.js"); await cargarScript("js/vendor/markmap-view.js"); }
async function libsMermaid() {
  await cargarScript("js/vendor/mermaid.min.js");
  if (!libsMermaid.ok) {
    const osc = document.documentElement.classList.contains("oscuro");
    mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: "base",
      themeVariables: { fontFamily: "Nunito, -apple-system, sans-serif", fontSize: "15px", primaryColor: osc ? "#1E3A12" : "#D7FFB8", primaryBorderColor: "#58CC02",
        primaryTextColor: osc ? "#F1F7FB" : "#3C3C3C", lineColor: osc ? "#52656D" : "#AFAFAF", secondaryColor: "#DDF4FF", tertiaryColor: "#FFF0D5", edgeLabelBackground: osc ? "#131F24" : "#FFFFFF" },
      flowchart: { curve: "basis", htmlLabels: true, padding: 14, nodeSpacing: 30, rankSpacing: 42, useMaxWidth: true },
      mindmap: { padding: 14, useMaxWidth: true } });
    libsMermaid.ok = true;
  }
}

/* ---------- mapas mentales ---------- */
const V = { mapa: null, esquema: null, abiertos: new Set() };
function vistaMapas() {
  const lista = MAPAS || [], es = J?.esquemas || [];
  return `<div class="top"><button class="icon-btn" data-v="inicio">‹</button><h2>Mapas y juegos</h2><span style="width:44px"></span></div>
  <p class="muted small">Aprende de otra forma: esquemas visuales, mapas de cada documento, juegos de repaso y lectura en voz alta.</p>
  <h3 class="mt2">🧩 Esquemas visuales</h3>
  ${es.map((e, k) => `<button class="node" data-a="verEsquema" data-id="${e.id}"><div class="ico" style="background:${COLORES[k % 8]}">${["🛤️", "🌈", "🗂️", "⚙️", "🏛️"][k] || "📌"}</div><div class="meta"><b>${esc(e.titulo)}</b><span class="tiny muted">${esc(e.fuente)}</span></div><span class="muted">›</span></button>`).join("")}
  <h3 class="mt2">🗺️ Mapa de cada documento</h3>
  <p class="tiny muted">Cómo está organizado cada documento: títulos, capítulos y artículos. Toca una rama para abrirla y 📖 para leer esa parte.</p>
  ${lista.map((m, k) => `<button class="node" data-a="verMapa" data-d="${m.doc}"><div class="ico" style="background:${COLORES[k % 8]}">🗺️</div><div class="meta"><b>${esc(m.nombre)}</b></div><span class="muted">›</span></button>`).join("")}
  <h3 class="mt2">🎮 Juegos de repaso</h3>
  ${juegosLista().map(g => `<button class="node" data-a="jugar" data-tipo="${g.tipo}" data-id="${g.id}"><div class="ico" style="background:${g.color}">${g.e}</div><div class="meta"><b>${esc(g.titulo)}</b><span class="tiny muted">${g.nombre} · ${esc(g.fuente)}</span></div><span class="muted">›</span></button>`).join("")}`;
}
const TIPOS = { emparejar: { e: "🔗", nombre: "Relacionar", color: "#1CB0F6" }, ordenar: { e: "🔢", nombre: "Ordenar los pasos", color: "#FF9600" },
  clasificar: { e: "🗃️", nombre: "Clasificar", color: "#CE82FF" }, sopa: { e: "🔤", nombre: "Sopa de letras", color: "#58CC02" } };
function juegosLista() {
  if (!J) return [];
  return ["emparejar", "ordenar", "clasificar", "sopa"].flatMap(t => (J[t] || []).map(x => ({ tipo: t, id: x.id, titulo: x.titulo, fuente: x.fuente, ...TIPOS[t] })));
}
function aMarkmap(n, prof = 0) {
  const hijos = (n.h || []).map(h => aMarkmap(h, prof + 1));
  if (n.d) hijos.unshift({ content: `<span class="mm-def">${esc(n.d.length > 160 ? n.d.slice(0, 157) + "…" : n.d)}</span>`, children: [], payload: {} });
  const titulo = esc(n.t.length > 70 ? n.t.slice(0, 67) + "…" : n.t);
  return { content: titulo + (n.l ? ` <span class="mm-leer">📖</span>` : ""), children: hijos, payload: { l: n.l || null } };
}
let MM = null;
function vistaMapa() {
  const m = (MAPAS || []).find(x => x.doc === V.mapa); if (!m) return vistaMapas();
  return `<div class="top"><button class="icon-btn" data-v="mapas">‹</button><h2 style="font-size:19px">${esc(m.nombre)}</h2><span style="width:44px"></span></div>
  <p class="tiny muted">Toca una idea para abrir o cerrar sus ramas. Si tiene 📖, tócala de nuevo para leer esa parte. Pellizca para acercar.</p>
  <div class="row wrap"><button class="chip" data-a="mmNivel" data-n="2">Lo principal</button><button class="chip" data-a="mmNivel" data-n="3">Más detalle</button><button class="chip" data-a="mmNivel" data-n="9">Todo</button><button class="chip" data-a="mmFit">⤢ Centrar</button></div>
  <div class="mmwrap mt"><svg id="mmsvg"></svg></div>`;
}
async function pintarMapa(nivel = 2) {
  const m = (MAPAS || []).find(x => x.doc === V.mapa), svg = document.getElementById("mmsvg"); if (!m || !svg) return;
  await libsMapa();
  svg.innerHTML = "";
  const datos = aMarkmap(m.mapa);
  MM = markmap.Markmap.create(svg, { initialExpandLevel: nivel, duration: 300, maxWidth: 260, spacingVertical: 8, spacingHorizontal: 70, paddingX: 10,
    color: (node) => COLORES[(String(node.state?.path || "").split(".")[1] || 0) % COLORES.length] }, datos);
  let ultimo = null;
  svg.onclick = e => {
    const g = e.target.closest("g.markmap-node"); if (!g || e.target.tagName === "circle") return;
    const d = d3.select(g).datum();
    if (d.children?.length) { MM.toggleNode(d); ultimo = d; }
    else if (d.payload?.l) PD.abrirLectura(d.payload.l);
    if (d.children?.length && d.payload?.l && ultimo === d && d.payload.fold === 0 && e.detail === 2) PD.abrirLectura(d.payload.l);
  };
}
function todasLasRutas(n, ruta, out) { (n.h || []).forEach((h, k) => { const r = ruta === null ? "r" + k : ruta + "." + k; if ((h.h || []).length) { out.push(r); todasLasRutas(h, r, out); } }); return out; }

/* ---------- esquemas ---------- */
const DIAG = {
  "X-ruta": [
`flowchart LR
  P1(["1 · Promoción<br/><small>competencias y derechos;<br/>clima escolar</small>"]):::verde --> P2(["2 · Prevención<br/><small>formación continua; incide<br/>en las causas</small>"]):::azul --> P3(["3 · Atención<br/><small>asistir de manera inmediata,<br/>pertinente, ética e integral</small>"]):::naranja --> P4(["4 · Seguimiento<br/><small>reporte oportuno al Sistema<br/>de Información Unificado</small>"]):::morado`,
`flowchart TD
  A(["Situación que afecta<br/>la convivencia escolar"]):::gris --> B{"¿Es un presunto delito?"}:::gris
  B -- Sí --> T3["<b>Tipo III</b><br/><small>presuntos delitos</small>"]:::rojo
  B -- No --> C{"¿Es repetida o sistemática,<br/>o causa daño al cuerpo o a la salud<br/>sin incapacidad?"}:::gris
  C -- Sí --> T2["<b>Tipo II</b><br/><small>agresión, acoso o ciberacoso<br/>que no es delito</small>"]:::naranja
  C -- No --> T1["<b>Tipo I</b><br/><small>conflicto mal manejado o esporádico,<br/>sin daño al cuerpo ni a la salud</small>"]:::verde
  T1 --> a1["1 · Reunir a las partes<br/>y mediar pedagógicamente"]:::verde --> a2["2 · Fijar una solución imparcial,<br/>equitativa y justa"]:::verde --> a3["3 · Seguimiento del caso<br/>y de los compromisos"]:::verde
  T2 --> b1["1 · Si hay daño: atención<br/>inmediata en salud"]:::naranja --> b2["2 · Proteger a los involucrados"]:::naranja --> b3["3 · Informar de inmediato<br/>a padres o acudientes"]:::naranja --> b4["4 · Espacios para exponer<br/>lo ocurrido"]:::naranja --> b5["5 · Si no es tipo III: acciones<br/>restaurativas y consecuencias"]:::naranja --> b6["6 · Si es tipo III:<br/>aplicar ese protocolo"]:::naranja --> b7["7 · El presidente informa<br/>al Comité, que hace seguimiento"]:::naranja --> b8["8 · Acta de lo ocurrido<br/>y lo decidido"]:::naranja --> b9["9 · Reporte al Sistema<br/>de Información Unificado"]:::naranja
  T3 --> c1["1 · Si hay daño: atención<br/>inmediata en salud"]:::rojo --> c2["2 · Informar de inmediato<br/>a padres o acudientes"]:::rojo --> c3["3 · El presidente del Comité informa<br/>a la <b>Policía Nacional</b>"]:::rojo --> c4["4 · Citar al Comité<br/>Escolar de Convivencia"]:::rojo --> c5["5 · Informar los hechos<br/>guardando reserva"]:::rojo --> c6["6 · Medidas de protección<br/>para los involucrados"]:::rojo --> c7["7 · Reporte al Sistema<br/>de Información Unificado"]:::rojo --> c8["8 · Seguimiento del Comité,<br/>la autoridad y el comité municipal"]:::rojo`],
  "X-inclusion": [
`flowchart TD
  E(["<b>Educación inclusiva</b><br/><small>proceso permanente que reconoce, valora<br/>y responde a la diversidad</small>"]):::verde --> D(["<b>DUA</b> · Diseño Universal del Aprendizaje<br/><small>diseñar desde el inicio para todos:<br/>objetivos, métodos, materiales, apoyos y evaluación</small>"]):::azul
  D --> C(["<b>Currículo flexible</b><br/><small>mismos objetivos generales,<br/>diferentes oportunidades de acceder a ellos</small>"]):::azul
  C --> A(["<b>Ajustes razonables</b><br/><small>según las barreras,<br/>no según un diagnóstico médico</small>"]):::naranja
  A --> P(["<b>PIAR</b> · Plan Individual de Ajustes Razonables<br/><small>lo lideran docentes de aula con el docente de apoyo,<br/>la familia y el estudiante · primer trimestre</small>"]):::morado`],
  "X-conceptos": [
`mindmap
  root((Tecnología))
    Productos
      Artefactos
        dispositivos, herramientas, máquinas
      Procesos
        fases sucesivas que transforman recursos
      Sistemas
        elementos ligados con un objetivo común
    Cambio tecnológico
      Innovación
        mejorar lo que ya existe
      Invención
        algo nuevo, inexistente
      Descubrimiento
        hallar lo oculto o desconocido
    Relaciones
      Técnica
        saber hacer
      Ciencia
        entender el mundo natural
      Informática
        parte de las TIC
      Ética
        privacidad, autoría, acceso equitativo`],
  "X-guia30": [
`mindmap
  root((Guía 30))
    Naturaleza y evolución
      conceptos fundamentales
      relación con otras disciplinas
      evolución en la historia y la cultura
    Apropiación y uso
      uso adecuado, pertinente y crítico
      artefactos, productos, procesos y sistemas
    Solución de problemas
      detectar fallas y necesidades
      diseñar y evaluar
      complejidad creciente por grados
    Tecnología y sociedad
      actitudes
      valoración social
      participación social y ética
    5 grupos de grados
      1° a 3°
      4° a 5°
      6° a 7°
      8° a 9°
      10° a 11°`],
  "X-gobierno": [
`mindmap
  root((Gobierno escolar))
    Rector
      preside el consejo directivo y el académico
    Consejo directivo
      el rector, quien lo preside
      2 representantes de los docentes
      2 representantes de los padres
      1 estudiante del último grado
      1 representante de los exalumnos
      1 del sector productivo
    Consejo académico
      directivos docentes
      1 docente por cada área o grado
      currículo, plan de estudio y evaluación
    Comité escolar de convivencia
      rector, quien lo preside
      personero estudiantil
      docente con función de orientación
      coordinador
      presidente del consejo de padres
      presidente del consejo de estudiantes
      1 docente que lidere convivencia`]
};
const CLASES = `
  classDef verde fill:#D7FFB8,stroke:#58CC02,stroke-width:3px,color:#2B2B2B
  classDef azul fill:#DDF4FF,stroke:#1CB0F6,stroke-width:3px,color:#2B2B2B
  classDef naranja fill:#FFF0D5,stroke:#FF9600,stroke-width:3px,color:#2B2B2B
  classDef rojo fill:#FFDFE0,stroke:#FF4B4B,stroke-width:3px,color:#2B2B2B
  classDef morado fill:#F4E5FF,stroke:#CE82FF,stroke-width:3px,color:#2B2B2B
  classDef gris fill:#FFFFFF,stroke:#AFAFAF,stroke-width:2px,color:#2B2B2B`;
async function pintarEsquema() {
  const cont = document.querySelectorAll(".diag[data-k]"); if (!cont.length) return;
  await libsMermaid();
  const defs = DIAG[V.esquema] || [];
  for (const el of cont) {
    const k = +el.dataset.k, def = defs[k]; if (!def) continue;
    try { const { svg } = await mermaid.render(`dg-${V.esquema}-${k}-${Date.now()}`, def.startsWith("flowchart") ? def + CLASES : def); el.innerHTML = svg; }
    catch (err) { el.innerHTML = `<p class="small muted">No se pudo dibujar el diagrama.</p>`; console.error(err); }
  }
}
function vistaEsquema() {
  const e = (J?.esquemas || []).find(x => x.id === V.esquema); if (!e) return vistaMapas();
  const todo = e.tipo === "ruta" ? [...e.componentes, ...e.situaciones].map(x => x.t + ". " + x.d).join(" ") : (e.pasos || e.componentes || []).map(x => x.t + ". " + x.d).join(" ");
  let cuerpo = "";
  if (e.tipo === "ruta") {
    cuerpo = `<h3>Componentes de la Ruta</h3><div class="flujo-h">${e.componentes.map((c, k) => `<div class="paso" style="--c:${COLORES[k]}"><b>${k + 1}. ${esc(c.t)}</b><p>${esc(c.d)}</p></div>`).join('<div class="flecha">➜</div>')}</div>
      <h3 class="mt2">Tipos de situaciones y su protocolo</h3>
      <div class="tres">${e.situaciones.map((s, k) => `<div class="sit" style="--c:${["#58CC02", "#FF9600", "#FF4B4B"][k]}"><div class="sit-t">${esc(s.t)}</div><p class="small">${esc(s.d)}</p>
        <details><summary class="small"><b>Protocolo: ${s.pasos.length} pasos</b></summary><ol class="small">${s.pasos.map(p => `<li>${esc(p)}</li>`).join("")}</ol></details></div>`).join("")}</div>
      <h3 class="mt2">Formas de agresión escolar</h3><div class="chips-g">${e.agresiones.map((a, k) => `<details class="pastilla" style="--c:${COLORES[k]}"><summary>${esc(a.t)}</summary><p class="small">${esc(a.d)}</p></details>`).join("")}</div>`;
  } else if (e.tipo === "flujo") {
    cuerpo = `<div class="flujo-v">${e.pasos.map((p, k) => `<div class="paso" style="--c:${COLORES[k % 8]}"><b>${esc(p.t)}</b><p>${esc(p.d)}</p></div>`).join('<div class="flecha v">⬇</div>')}</div>`;
  } else if (e.tipo === "lista") {
    cuerpo = e.grupos.map((g, k) => `<div class="paso mt" style="--c:${COLORES[k % 8]}"><b>${esc(g.t)}</b><ul class="small">${g.items.map(x => `<li>${esc(x)}</li>`).join("")}</ul><p class="tiny muted">${esc(g.f)}</p></div>`).join("");
  } else if (e.tipo === "matriz") {
    cuerpo = `<div class="chips-g">${e.componentes.map((c, k) => `<details class="pastilla" style="--c:${COLORES[k]}"><summary>${esc(c.t)}</summary><p class="small">${esc(c.d)}</p></details>`).join("")}</div>
      <div class="matriz mt"><table><tr><th>Grados</th>${e.componentes.map((c, k) => `<th style="background:${COLORES[k]}">${esc(c.t)}</th>`).join("")}</tr>
      ${e.grupos.map(g => `<tr><th>${esc(g.t)}</th>${g.celdas.map(x => `<td>${esc(x)}</td>`).join("")}</tr>`).join("")}</table></div>
      <p class="tiny muted">Desliza la tabla hacia los lados. Cada celda es la competencia que la Guía 30 define para ese grupo de grados y componente.</p>`;
  }
  const diags = (DIAG[e.id] || []).map((d, k) => `<div class="diag card mt ${d.startsWith("mindmap") ? "mind" : ""}" data-k="${k}"><p class="small muted center">Dibujando el esquema…</p></div>${d.startsWith("mindmap") ? `<p class="tiny muted center">Desliza hacia los lados para ver todo el mapa.</p>` : ""}`).join("");
  return `<div class="top"><button class="icon-btn" data-v="mapas">‹</button><h2 style="font-size:19px">${esc(e.titulo)}</h2><span style="width:44px"></span></div>
  <div class="row wrap"><span class="tag">${esc(e.fuente)}</span>${Voz.boton(todo, "esq-" + e.id, "Escuchar el esquema")}</div>
  ${diags}
  <details class="card mt" ${diags ? "" : "open"}><summary><b>📜 Ver el texto oficial completo</b></summary><div class="esquema mt">${cuerpo}</div>
  <p class="tiny muted mt">Estos textos son literales del documento oficial. Los rótulos cortos del diagrama los resumen.</p></details>`;
}

/* ---------- juegos ---------- */
function nuevoJuego(tipo, id) {
  const d = (J?.[tipo] || []).find(x => x.id === id); if (!d) return null;
  const G = { tipo, id, d, errores: 0, fin: false };
  if (tipo === "emparejar") { G.izq = shuffle(d.pares.map((p, i) => i)); G.der = shuffle(d.pares.map((p, i) => i)); G.ok = new Set(); G.sel = null; G.mal = null; }
  if (tipo === "ordenar") { G.orden = shuffle(d.pasos.map((p, i) => i)); while (d.pasos.length > 1 && G.orden.every((v, i) => v === i)) G.orden = shuffle(G.orden); G.revisado = false; }
  if (tipo === "clasificar") { const cats = Object.keys(d.categorias); G.cats = cats;
    G.cartas = shuffle(cats.flatMap(c => d.categorias[c].map(t => ({ t, c })))).slice(0, 8); G.i = 0; G.resp = null; G.aciertos = 0; }
  if (tipo === "sopa") { Object.assign(G, armarSopa(shuffle(d.palabras).slice(0, 6))); G.hallados = new Set(); G.a = null; }
  return G;
}
function armarSopa(pals) {
  const N = 12, g = Array.from({ length: N }, () => Array(N).fill("")), dirs = [[0, 1], [1, 0], [1, 1], [-1, 1]], pos = {};
  const ordenadas = pals.slice().sort((a, b) => b.w.length - a.w.length), usadas = [];
  for (const p of ordenadas) {
    let ok = false;
    for (let t = 0; t < 400 && !ok; t++) {
      const [dr, dc] = dirs[Math.floor(Math.random() * (t < 200 ? 4 : 2))], L = p.w.length;
      const r0 = Math.floor(Math.random() * N), c0 = Math.floor(Math.random() * N), r1 = r0 + dr * (L - 1), c1 = c0 + dc * (L - 1);
      if (r1 < 0 || r1 >= N || c1 < 0 || c1 >= N) continue;
      let cabe = true; for (let k = 0; k < L; k++) { const ch = g[r0 + dr * k][c0 + dc * k]; if (ch && ch !== p.w[k]) { cabe = false; break; } }
      if (!cabe) continue;
      const celdas = []; for (let k = 0; k < L; k++) { g[r0 + dr * k][c0 + dc * k] = p.w[k]; celdas.push((r0 + dr * k) * N + c0 + dc * k); }
      pos[p.w] = celdas; usadas.push(p); ok = true;
    }
  }
  const ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) if (!g[r][c]) g[r][c] = ABC[Math.floor(Math.random() * 26)];
  return { N, grid: g.flat(), pos, pals: usadas };
}
function juegoHTML(G, enSesion) {
  const d = G.d, T = TIPOS[G.tipo];
  let h = `<div class="review-banner juego" style="--c:${T.color}">${T.e} ${T.nombre} · ${esc(d.titulo)}</div><p class="tiny muted">${esc(d.fuente)} · texto literal</p>`;
  if (G.tipo === "emparejar") {
    h += `<p class="small">Toca un concepto y luego su definición.</p><div class="emp">
      <div>${G.izq.map(i => `<button class="emp-a ${G.ok.has(i) ? "ok" : ""} ${G.sel === i ? "sel" : ""}" data-a="jE" data-l="a" data-i="${i}" ${G.ok.has(i) ? "disabled" : ""}>${esc(d.pares[i].a)}</button>`).join("")}</div>
      <div>${G.der.map(i => `<button class="emp-b ${G.ok.has(i) ? "ok" : ""} ${G.mal === i ? "bad" : ""}" data-a="jE" data-l="b" data-i="${i}" ${G.ok.has(i) ? "disabled" : ""}>${esc(d.pares[i].b)}</button>`).join("")}</div></div>`;
  }
  if (G.tipo === "ordenar") {
    h += `<p class="small">Ordena los pasos como los establece la norma. Usa las flechas.</p><div class="ord">${G.orden.map((i, k) => `<div class="ord-i ${G.revisado ? (i === k ? "ok" : "bad") : ""}">
      <span class="ord-n">${k + 1}</span><span class="ord-t">${esc(d.pasos[i])}</span>
      ${G.revisado ? "" : `<span class="ord-b"><button data-a="jO" data-k="${k}" data-m="-1" ${k === 0 ? "disabled" : ""}>▲</button><button data-a="jO" data-k="${k}" data-m="1" ${k === G.orden.length - 1 ? "disabled" : ""}>▼</button></span>`}</div>`).join("")}</div>
      ${G.revisado ? `<div class="fb ${G.orden.every((v, i) => v === i) ? "ok" : "bad"} mt"><h3>${G.orden.every((v, i) => v === i) ? "¡Orden perfecto!" : "Este es el orden oficial"}</h3><ol class="small">${d.pasos.map(p => `<li>${esc(p)}</li>`).join("")}</ol></div>` : `<button class="btn mt" data-a="jOrev">Comprobar orden</button>`}`;
  }
  if (G.tipo === "clasificar") {
    const c = G.cartas[G.i];
    if (c) h += `<p class="small">Carta ${G.i + 1} de ${G.cartas.length}. ¿A qué componente de la Guía 30 pertenece este desempeño?</p>
      <div class="carta">${esc(c.t)}</div>
      <div class="cats">${G.cats.map((k, n) => `<button class="cat ${G.resp ? (k === c.c ? "ok" : (k === G.resp ? "bad" : "")) : ""}" style="--c:${COLORES[n]}" data-a="jC" data-c="${esc(k)}" ${G.resp ? "disabled" : ""}>${esc(k)}</button>`).join("")}</div>
      ${G.resp ? `<button class="btn mt" data-a="jCsig">${G.i + 1 < G.cartas.length ? "Siguiente carta" : "Ver resultado"}</button>` : ""}`;
    else h += `<div class="fb ok"><h3>${G.aciertos} de ${G.cartas.length} bien clasificados</h3><p class="small">Recuerda: conceptos e historia → Naturaleza; uso seguro y adecuado → Apropiación; fallas, diseño y construcción → Solución de problemas; impactos, ética y participación → Tecnología y sociedad.</p></div>`;
  }
  if (G.tipo === "sopa") {
    h += `<p class="small">Toca la primera y la última letra de cada palabra.</p><div class="sopa" style="--n:${G.N}">${G.grid.map((ch, i) => {
      const hall = [...G.hallados].some(w => G.pos[w].includes(i));
      return `<button class="sl ${hall ? "ok" : ""} ${G.a === i ? "sel" : ""}" data-a="jS" data-i="${i}">${ch}</button>`; }).join("")}</div>
      <div class="sopa-l">${G.pals.map(p => `<div class="${G.hallados.has(p.w) ? "ok" : ""}"><b>${G.hallados.has(p.w) ? "✓ " + esc(p.t) : `🔎 Pista (${p.w.length} letras)`}</b><p class="small">${G.hallados.has(p.w) ? esc(p.d) : esc(p.d.replace(new RegExp(p.t.split(" ").pop(), "ig"), "____"))}</p></div>`).join("")}</div>`;
  }
  if (G.fin) h += `<div class="fb ok mt"><h3>¡Juego completado! +20 XP</h3><p class="small">${G.errores ? `${G.errores} ${G.errores === 1 ? "intento fallido" : "intentos fallidos"}: vuelve a jugarlo en unos días para afianzar.` : "Sin errores. 👏"}</p></div>
    <div class="sticky-bottom"><button class="btn" data-a="${enSesion ? "jFin" : "jSalir"}">${enSesion ? "Continuar el reto" : "Volver"}</button>${enSesion ? "" : `<button class="btn ghost" data-a="jugar" data-tipo="${G.tipo}" data-id="${G.id}">Jugar de nuevo</button>`}</div>`;
  return h;
}
function juegoAccion(a, b, G) {
  const d = G.d;
  if (a === "jE") {
    const i = +b.dataset.i, lado = b.dataset.l; G.mal = null;
    if (lado === "a") G.sel = i;
    else if (G.sel !== null) { if (G.sel === i) { G.ok.add(i); G.sel = null; PD.sonar("ok"); } else { G.errores++; G.mal = i; PD.sonar("mal"); } }
    else PD.toast("Primero toca un concepto de la izquierda");
    if (G.ok.size === d.pares.length) terminar(G);
  }
  if (a === "jO") { const k = +b.dataset.k, m = +b.dataset.m, o = G.orden; [o[k], o[k + m]] = [o[k + m], o[k]]; }
  if (a === "jOrev") { G.revisado = true; G.errores = G.orden.filter((v, i) => v !== i).length; G.orden.every((v, i) => v === i) ? PD.sonar("ok") : PD.sonar("mal"); terminar(G); }
  if (a === "jC") { const c = G.cartas[G.i]; G.resp = b.dataset.c; if (G.resp === c.c) { G.aciertos++; PD.sonar("ok"); } else { G.errores++; PD.sonar("mal"); } }
  if (a === "jCsig") { G.i++; G.resp = null; if (G.i >= G.cartas.length) terminar(G); }
  if (a === "jS") {
    const i = +b.dataset.i;
    if (G.a === null) G.a = i;
    else { const w = Object.keys(G.pos).find(w => { const p = G.pos[w]; return (p[0] === G.a && p[p.length - 1] === i) || (p[0] === i && p[p.length - 1] === G.a); });
      if (w && !G.hallados.has(w)) { G.hallados.add(w); PD.sonar("ok"); } else if (G.a !== i) { G.errores++; PD.sonar("mal"); }
      G.a = null; if (G.hallados.size === G.pals.length) terminar(G); }
  }
}
function terminar(G) { if (G.fin) return; G.fin = true; PD.premiar(20, G); }
function elegirJuegoDelDia(fecha) {
  const lista = juegosLista(); if (!lista.length) return null;
  const n = Math.floor(new Date(fecha + "T12:00:00") / 864e5);
  const tipos = ["emparejar", "ordenar", "sopa", "clasificar"], t = tipos[n % tipos.length];
  const deTipo = lista.filter(g => g.tipo === t); return deTipo[Math.floor(n / tipos.length) % deTipo.length];
}

function postRender(vista) {
  if (vista === "mapa") pintarMapa(V.nivel || (V.mapa && V.mapa.startsWith("guia30") ? 3 : 2));
  if (vista === "esquema") pintarEsquema();
}
window.PDX = { postRender, pintarMapa, get MM() { return MM; }, Voz, cargar, vistaMapas, vistaMapa, vistaEsquema, juegoHTML, juegoAccion, nuevoJuego, elegirJuegoDelDia, V, todasLasRutas, get MAPAS() { return MAPAS; }, get J() { return J; } };
})();
