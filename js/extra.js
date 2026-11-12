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

/* ---------- mapas mentales ---------- */
const V = { mapa: null, esquema: null, abiertos: new Set() };
function vistaMapas() {
  const lista = MAPAS || [], es = J?.esquemas || [];
  return `<div class="top"><button class="icon-btn" data-v="inicio">‹</button><h2>Mapas y juegos</h2><span style="width:44px"></span></div>
  <p class="muted small">Aprende de otra forma: esquemas visuales, mapas de cada documento, juegos de repaso y lectura en voz alta.</p>
  <h3 class="mt2">🧩 Esquemas visuales</h3>
  ${es.map((e, k) => `<button class="node" data-a="verEsquema" data-id="${e.id}"><div class="ico" style="background:${COLORES[k % 8]}">${["🛤️", "🌈", "🗂️", "⚙️"][k] || "📌"}</div><div class="meta"><b>${esc(e.titulo)}</b><span class="tiny muted">${esc(e.fuente)}</span></div><span class="muted">›</span></button>`).join("")}
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
function nodoHTML(n, ruta, prof, color) {
  const id = ruta, hijos = n.h || [], abierto = V.abiertos.has(id) || prof === 0;
  const c = prof <= 1 ? color : color;
  const leer = n.l ? `<button class="mini" data-a="leerParte" data-l="${n.l}">📖</button>` : "";
  const desc = n.d ? `<div class="mm-d">${esc(n.d)}</div>` : "";
  if (!hijos.length) return `<div class="mm-hoja" style="--c:${c}"><span>${esc(n.t)}</span>${leer}${desc}</div>`;
  return `<div class="mm-rama ${abierto ? "abierta" : ""}" style="--c:${c}">
    <div class="mm-t" data-a="mmToggle" data-r="${id}"><span class="mm-flecha">${abierto ? "▾" : "▸"}</span><span>${esc(n.t)}</span><span class="mm-n">${hijos.length}</span>${leer}</div>
    ${desc}${abierto ? `<div class="mm-hijos">${hijos.map((h, k) => nodoHTML(h, id + "." + k, prof + 1, prof === 0 ? COLORES[k % 8] : c)).join("")}</div>` : ""}</div>`;
}
function vistaMapa() {
  const m = (MAPAS || []).find(x => x.doc === V.mapa); if (!m) return vistaMapas();
  return `<div class="top"><button class="icon-btn" data-v="mapas">‹</button><h2 style="font-size:19px">${esc(m.nombre)}</h2><span style="width:44px"></span></div>
  <div class="row wrap"><button class="chip" data-a="mmTodo">Abrir todo</button><button class="chip" data-a="mmNada">Cerrar todo</button></div>
  <div class="mm mt"><div class="mm-raiz">${esc(m.mapa.t)}</div>${(m.mapa.h || []).map((h, k) => nodoHTML(h, "r" + k, 1, COLORES[k % 8])).join("")}</div>`;
}
function todasLasRutas(n, ruta, out) { (n.h || []).forEach((h, k) => { const r = ruta === null ? "r" + k : ruta + "." + k; if ((h.h || []).length) { out.push(r); todasLasRutas(h, r, out); } }); return out; }

/* ---------- esquemas ---------- */
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
  } else if (e.tipo === "matriz") {
    cuerpo = `<div class="chips-g">${e.componentes.map((c, k) => `<details class="pastilla" style="--c:${COLORES[k]}"><summary>${esc(c.t)}</summary><p class="small">${esc(c.d)}</p></details>`).join("")}</div>
      <div class="matriz mt"><table><tr><th>Grados</th>${e.componentes.map((c, k) => `<th style="background:${COLORES[k]}">${esc(c.t)}</th>`).join("")}</tr>
      ${e.grupos.map(g => `<tr><th>${esc(g.t)}</th>${g.celdas.map(x => `<td>${esc(x)}</td>`).join("")}</tr>`).join("")}</table></div>
      <p class="tiny muted">Desliza la tabla hacia los lados. Cada celda es la competencia que la Guía 30 define para ese grupo de grados y componente.</p>`;
  }
  return `<div class="top"><button class="icon-btn" data-v="mapas">‹</button><h2 style="font-size:19px">${esc(e.titulo)}</h2><span style="width:44px"></span></div>
  <div class="row wrap"><span class="tag">${esc(e.fuente)}</span>${Voz.boton(todo, "esq-" + e.id, "Escuchar el esquema")}</div>
  <div class="esquema mt">${cuerpo}</div><p class="tiny muted mt">Todos los textos son literales del documento oficial.</p>`;
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

window.PDX = { Voz, cargar, vistaMapas, vistaMapa, vistaEsquema, juegoHTML, juegoAccion, nuevoJuego, elegirJuegoDelDia, V, todasLasRutas, get MAPAS() { return MAPAS; }, get J() { return J; } };
})();
