/* Plaza Docente — entrenamiento diario CNSC (Tecnología e Informática)
   App de una sola página, sin dependencias. Datos locales + respaldo en Supabase. */
(() => {
"use strict";
const CFG = window.PLAZA_CONFIG;
const $app = document.getElementById("app");
const K = { clave: "pd_clave", estado: "pd_estado", outbox: "pd_outbox", banco: "pd_banco" };

/* ---------- utilidades ---------- */
const pad = n => String(n).padStart(2, "0");
const fechaISO = d => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
const hoy = () => fechaISO(new Date());
const masDias = (iso, n) => { const d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + n); return fechaISO(d); };
const difDias = (a, b) => Math.round((new Date(b + "T12:00:00") - new Date(a + "T12:00:00")) / 864e5);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const pick = a => a[Math.floor(Math.random() * a.length)];
const MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"];
const DIAS = ["dom","lun","mar","mié","jue","vie","sáb"];
const fechaLarga = iso => { const d = new Date(iso + "T12:00:00"); return `${["domingo","lunes","martes","miércoles","jueves","viernes","sábado"][d.getDay()]} ${d.getDate()} de ${MESES[d.getMonth()]}`; };
async function sha256(txt) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(txt));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("");
}
function toast(msg, ms = 2400) {
  const t = document.getElementById("toast"); t.textContent = msg; t.classList.add("on");
  clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove("on"), ms);
}

/* ---------- sonido y confeti ---------- */
let audioCtx = null;
function sonar(tipo) {
  if (!S.estado || !S.estado.ajustes || S.estado.ajustes.sonido === false) return;
  try {
    audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
    const notas = tipo === "ok" ? [659, 880] : tipo === "fin" ? [523, 659, 784, 1047] : [330, 262];
    notas.forEach((f, i) => {
      const o = audioCtx.createOscillator(), g = audioCtx.createGain();
      o.type = tipo === "mal" ? "triangle" : "sine"; o.frequency.value = f;
      const t0 = audioCtx.currentTime + i * 0.11;
      g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(0.18, t0 + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.22);
      o.connect(g).connect(audioCtx.destination); o.start(t0); o.stop(t0 + 0.25);
    });
  } catch (e) { /* sin sonido */ }
}
function confeti(n = 90) {
  const cv = document.getElementById("confeti"), ctx = cv.getContext("2d");
  const dpr = window.devicePixelRatio || 1; cv.width = innerWidth * dpr; cv.height = innerHeight * dpr; ctx.scale(dpr, dpr);
  const cols = ["#0E7C66", "#F2A541", "#E4572E", "#2F6FDE", "#7A4FD0", "#23934A"];
  const ps = Array.from({ length: n }, () => ({ x: innerWidth / 2 + (Math.random() - .5) * 80, y: innerHeight * .35,
    vx: (Math.random() - .5) * 9, vy: -Math.random() * 10 - 4, r: Math.random() * 6 + 4, c: pick(cols), a: Math.random() * 6, va: (Math.random() - .5) * .3 }));
  let f = 0;
  (function loop() {
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    ps.forEach(p => { p.x += p.vx; p.y += p.vy; p.vy += .32; p.a += p.va;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.fillStyle = p.c; ctx.fillRect(-p.r / 2, -p.r / 4, p.r, p.r / 2); ctx.restore(); });
    if (++f < 110) requestAnimationFrame(loop); else ctx.clearRect(0, 0, innerWidth, innerHeight);
  })();
}

/* ---------- estado ---------- */
const S = { banco: null, estado: null, clave: null, vista: "inicio", ses: null, sync: { ok: true, msg: "" } };
const estadoInicial = () => ({
  v: 1, t: 0,
  perfil: { nombre: "", inicio: null, xp: 0, racha: 0, mejorRacha: 0, ultimoDia: null, dias: [], insignias: {}, rescates: 0, dueloSemana: null, respondidas: 0 },
  items: {}, familias: {}, fichas: {}, lecturas: {}, cuaderno: { notas: {}, conceptos: [] }, sesiones: [], simulacros: [], retoHoy: null,
  ajustes: { sonido: true, avisoSimulacro: null, tema: "claro" }
});
const INTERVALOS = [0, 1, 3, 7, 14, 30]; // días según la caja de repaso
const DOMINIO = 3; // caja desde la cual la familia se considera dominada

function guardarLocal() {
  S.estado.t = Date.now();
  localStorage.setItem(K.estado, JSON.stringify(S.estado));
  programarSync();
}
const outbox = () => { let o; try { o = JSON.parse(localStorage.getItem(K.outbox)); } catch {} o ||= {}; o.intentos ||= []; o.sesiones ||= []; o.reportes ||= []; return o; };
const setOutbox = o => localStorage.setItem(K.outbox, JSON.stringify(o));

/* ---------- Supabase ---------- */
async function rpc(fn, body) {
  const r = await fetch(`${CFG.supabaseUrl}/rest/v1/rpc/${fn}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", apikey: CFG.supabaseKey, Authorization: `Bearer ${CFG.supabaseKey}` },
    body: JSON.stringify(body)
  });
  const txt = await r.text();
  if (!r.ok) { const e = new Error(txt.includes("clave_invalida") ? "clave_invalida" : `HTTP ${r.status}`); e.status = r.status; throw e; }
  return txt ? JSON.parse(txt) : null;
}
let syncTimer = null, sincronizando = false;
function programarSync(ms = 1500) { clearTimeout(syncTimer); syncTimer = setTimeout(sincronizar, ms); }
async function sincronizar() {
  if (!S.clave || sincronizando) return;
  sincronizando = true;
  try {
    let ob = outbox();
    do {
      const ses = ob.sesiones[0] || null;
      const ints = ob.intentos.slice(0, 400);
      await rpc("pd_guardar", { p_clave: S.clave, p_datos: S.estado, p_intentos: ints, p_sesion: ses });
      ob = outbox(); ob.intentos.splice(0, ints.length); if (ses) ob.sesiones.shift(); setOutbox(ob);
    } while (ob.sesiones.length || ob.intentos.length);
    while (ob.reportes.length) {
      const rp = ob.reportes[0];
      await rpc("pd_reportar", { p_clave: S.clave, p_item: rp.item, p_motivo: rp.motivo, p_nota: rp.nota || "", p_lote: rp.lote || "" });
      ob = outbox(); ob.reportes.shift(); setOutbox(ob);
    }
    S.sync = { ok: true, msg: "Guardado en la nube " + new Date().toLocaleTimeString("es-CO", { hour: "2-digit", minute: "2-digit" }) };
  } catch (e) {
    S.sync = { ok: false, msg: e.message === "clave_invalida" ? "Clave no válida" : "Sin conexión: se guardará al reconectar" };
  } finally { sincronizando = false; pintarSync(); }
}
function pintarSync() { const el = document.querySelector("[data-sync]"); if (el) el.innerHTML = syncHTML(); }
const syncHTML = () => `<span class="dot ${S.sync.ok ? "" : "off"}"></span>${esc(S.sync.msg || "Listo")}`;
addEventListener("online", () => programarSync(200));
document.addEventListener("visibilitychange", () => { if (document.visibilityState === "hidden") sincronizar(); else revisarDia(); });

/* ---------- banco ---------- */
let IDX = null;
function indexar(b) {
  const items = {}, casos = {}, porFam = {}, porComp = {}, porCaso = {}, porFicha = {}, fichas = {};
  b.casos.forEach(c => casos[c.id] = c);
  (b.fichas || []).forEach(f => fichas[f.id] = f);
  b.items.forEach(it => {
    if (!b.familias[it.familia]) return;
    it.comp = b.familias[it.familia].componente; it.tipo ||= "caso";
    items[it.id] = it;
    (porFam[it.familia] ||= []).push(it.id);
    (porComp[it.comp] ||= []).push(it.id);
    if (it.tipo === "conocimiento") (porFicha[it.ficha] ||= []).push(it.id);
    else (porCaso[it.caso] ||= []).push(it.id);
  });
  const comps = {}; b.componentes.forEach(c => comps[c.id] = c);
  IDX = { items, casos, porFam, porComp, porCaso, porFicha, fichas, comps };
}
async function cargarBanco() {
  try {
    const get = u => fetch(u, { cache: "no-cache" }).then(r => { if (!r.ok) throw new Error(u); return r.json(); });
    const [marco, indice] = await Promise.all([get(CFG.marcoUrl), get(CFG.indiceUrl)]);
    const lotes = await Promise.all(indice.lotes.map(l => get("data/" + l)));
    const retirados = new Set(indice.retirados || []);
    const b = { version: marco.version, actualizado: lotes.length ? lotes[lotes.length - 1].fecha : marco.actualizado, lotes: lotes.length,
      componentes: marco.componentes, afirmaciones: marco.afirmaciones, familias: marco.familias, casos: [], fichas: [], items: [] };
    const [ctx, plan] = await Promise.all([get("data/contextos.json").catch(() => ({})), get("data/lecturas/indice.json").catch(() => ({ lecturas: [] }))]);
    b.contextos = ctx; b.plan = plan.lecturas || [];
    lotes.forEach(l => { b.casos.push(...(l.casos || [])); b.fichas.push(...(l.fichas || [])); b.items.push(...(l.items || []).filter(it => !retirados.has(it.id))); });
    localStorage.setItem(K.banco, JSON.stringify(b)); return b;
  } catch { const c = localStorage.getItem(K.banco); if (c) return JSON.parse(c); throw new Error("No se pudo cargar el banco de preguntas."); }
}

/* ---------- lógica de aprendizaje ---------- */
const stItem = id => (S.estado.items[id] ||= { vistos: 0, aciertos: 0, ultimo: 0, ultimoOk: null });
const stFam = f => (S.estado.familias[f] ||= { caja: 0, proxima: null, fallos: 0, aciertos: 0, enCofre: false });
const familiasVencidas = () => Object.entries(S.estado.familias)
  .filter(([, s]) => s.enCofre && s.proxima && s.proxima <= hoy()).map(([f]) => f);
const cofre = () => Object.entries(S.estado.familias).filter(([, s]) => s.enCofre).map(([f, s]) => ({ f, ...s }));

function itemVariante(fam, excluir = []) {
  let cands = (IDX.porFam[fam] || []).filter(id => !excluir.includes(id));
  if (!cands.length) {
    const comp = S.banco.familias[fam].componente;
    cands = (IDX.porComp[comp] || []).filter(id => !excluir.includes(id) && IDX.items[id].familia !== fam);
  }
  if (!cands.length) cands = (IDX.porFam[fam] || []).slice();
  cands.sort((a, b) => {
    const sa = S.estado.items[a] || { vistos: 0, ultimo: 0 }, sb = S.estado.items[b] || { vistos: 0, ultimo: 0 };
    return (sa.vistos > 0) - (sb.vistos > 0) || sa.ultimo - sb.ultimo;
  });
  return cands[0];
}
function ultimoFallado(fam) {
  const ids = IDX.porFam[fam] || [];
  return ids.filter(id => S.estado.items[id]?.ultimoOk === false).sort((a, b) => S.estado.items[b].ultimo - S.estado.items[a].ultimo)[0];
}
function casosNuevos(filtroComp) {
  return Object.keys(IDX.porCaso).filter(c => IDX.porCaso[c].every(id => !(S.estado.items[id]?.vistos)))
    .filter(c => !filtroComp || IDX.porCaso[c].some(id => IDX.items[id].comp === filtroComp));
}
function puntajeItem(id) { const s = S.estado.items[id]; if (!s || !s.vistos) return -1; return s.aciertos / s.vistos; }

const fichaLeida = id => !!S.estado.fichas?.[id];
const LECT = {};
const lecturaLeida = id => !!S.estado.lecturas?.[id];
const lecturaPendiente = () => (S.banco.plan || []).find(l => !lecturaLeida(l.id));
const planInfo = () => { const pl = S.banco.plan || []; return { total: pl.length, leidas: pl.filter(l => lecturaLeida(l.id)).length }; };
async function asegurarLectura(id) {
  if (!id || LECT[id]) return;
  const meta = (S.banco.plan || []).find(l => l.id === id); if (!meta) return;
  try { const r = await fetch("data/" + meta.archivo, { cache: "no-cache" }); (await r.json()).forEach(l => LECT[l.id] = l); } catch { toast("Sin conexión: la lectura se cargará cuando vuelva la red."); }
}
const itemsDeLectura = id => Object.entries(S.banco.contextos || {}).filter(([iid, c]) => c.lectura === id && IDX.items[iid]).map(([iid]) => iid);
function fichaPendiente(comp) {
  return (S.banco.fichas || []).find(f => !fichaLeida(f.id) && (!comp || S.banco.familias[f.familia].componente === comp));
}
function armarCola(tipo, opts = {}) {
  const cola = [], usados = new Set();
  const add = (id, extra = {}) => { if (id && !usados.has(id)) { usados.add(id); cola.push({ id, ...extra }); } };
  if (tipo === "estudio") {
    const f = IDX.fichas[opts.ficha]; if (!f) return cola;
    cola.push({ ficha: f.id });
    (IDX.porFicha[f.id] || []).forEach(id => add(id));
    const casosFam = shuffle((IDX.porFam[f.familia] || []).filter(id => IDX.items[id].tipo === "caso"))
      .sort((a, b) => (S.estado.items[a]?.vistos ? 1 : 0) - (S.estado.items[b]?.vistos ? 1 : 0));
    casosFam.slice(0, 2).forEach(id => add(id));
    return cola;
  }
  if (tipo === "lectura") {
    if (!LECT[opts.lectura]) return cola;
    cola.push({ lectura: opts.lectura });
    shuffle(itemsDeLectura(opts.lectura)).sort((a, b) => (S.estado.items[a]?.vistos ? 1 : 0) - (S.estado.items[b]?.vistos ? 1 : 0)).slice(0, 4).forEach(id => add(id));
    return cola;
  }
  let extraN = 0;
  if (tipo === "reto" && !opts.sinFicha) {
    const L = lecturaPendiente();
    if (L && LECT[L.id]) {
      cola.push({ lectura: L.id }); extraN++;
      shuffle(itemsDeLectura(L.id)).filter(id => !S.estado.items[id]?.vistos).slice(0, 3).forEach(id => add(id));
    }
  }
  if (tipo === "reto" && !opts.sinFicha) {
    const f = fichaPendiente();
    if (f) { cola.push({ ficha: f.id }); extraN++; (IDX.porFicha[f.id] || []).forEach(id => add(id)); }
  }
  const n = (opts.n || CFG.preguntasPorReto) + extraN;

  if (tipo === "reto" || tipo === "duelo") {
    const vencidas = tipo === "duelo" ? cofre().map(x => x.f) : shuffle(familiasVencidas());
    const max = tipo === "duelo" ? n : CFG.maxRepasoPorReto;
    vencidas.slice(0, max).forEach(f => add(itemVariante(f, [ultimoFallado(f)].filter(Boolean)), { repaso: true }));
    if (tipo === "duelo") return cola;
  }
  // casos completos que no ha visto (prioriza componentes menos trabajados)
  const cobertura = c => { const ids = IDX.porComp[c] || []; return ids.filter(id => S.estado.items[id]?.vistos).length / (ids.length || 1); };
  let casos = casosNuevos(opts.comp);
  casos = shuffle(casos).sort((a, b) => cobertura(IDX.items[IDX.porCaso[a][0]].comp) - cobertura(IDX.items[IDX.porCaso[b][0]].comp));
  for (const c of casos) {
    if (cola.length >= n) break;
    const ids = IDX.porCaso[c].filter(id => !opts.comp || IDX.items[id].comp === opts.comp);
    if (cola.length + ids.length > n + 1 && cola.length > 0) continue;
    ids.forEach(id => add(id));
  }
  // si ya vio todo: refuerza lo de menor desempeño, agrupando por caso
  if (cola.length < n) {
    let pool = Object.keys(IDX.items).filter(id => IDX.items[id].tipo === "caso" && !usados.has(id) && (!opts.comp || IDX.items[id].comp === opts.comp));
    pool = shuffle(pool).sort((a, b) => puntajeItem(a) - puntajeItem(b) || (S.estado.items[a]?.ultimo || 0) - (S.estado.items[b]?.ultimo || 0));
    for (const id of pool) {
      if (cola.length >= n) break;
      IDX.porCaso[IDX.items[id].caso].filter(x => !usados.has(x) && (!opts.comp || IDX.items[x].comp === opts.comp)).slice(0, n - cola.length).forEach(x => add(x));
    }
  }
  return cola;
}

function armarSimulacro() {
  const n = CFG.simulacroPreguntas, casos = shuffle(Object.keys(IDX.porCaso));
  const comp = c => IDX.items[IDX.porCaso[c][0]].comp;
  // al menos un caso de cada componente, luego completa
  const elegidos = [], vistosComp = new Set();
  casos.forEach(c => { if (!vistosComp.has(comp(c))) { vistosComp.add(comp(c)); elegidos.push(c); } });
  casos.forEach(c => { if (!elegidos.includes(c)) elegidos.push(c); });
  const cola = [];
  for (const c of elegidos) { if (cola.length >= n) break; IDX.porCaso[c].forEach(id => cola.length < n && cola.push({ id })); }
  // orden de examen: primero aptitudes y competencias básicas, al final psicotécnica
  return cola.sort((a, b) => (IDX.items[a.id].comp === "PSI") - (IDX.items[b.id].comp === "PSI"));
}

function iniciarSesion(tipo, opts = {}) {
  const cola = tipo === "simulacro" ? armarSimulacro() : armarCola(tipo, opts);
  if (!cola.length) { toast(tipo === "duelo" ? "Tu cofre está vacío. ¡Bien!" : "No hay preguntas disponibles."); return; }
  S.ses = { tipo, comp: opts.comp || null, cola, i: 0, vidas: CFG.vidas, res: [], xp: 0, inicio: Date.now(),
    fin: tipo === "simulacro" ? Date.now() + cola.length * CFG.minutosPorPregunta * 60000 : null, orden: null, sel: null, respondida: false };
  prepararPregunta(); ir("pregunta");
}
function prepararPregunta() {
  const q = S.ses.cola[S.ses.i];
  if (q.ficha || q.lectura) { S.ses.orden = null; S.ses.sel = null; S.ses.respondida = false; return; }
  const it = IDX.items[q.id];
  S.ses.preLeer = S.ses.tipo !== "simulacro" && !q.repaso && !q.rescate && !(S.estado.items[q.id]?.vistos);
  S.ses.orden = shuffle(it.opciones.map(o => o.l)); S.ses.sel = null; S.ses.respondida = false; S.ses.t0 = Date.now();
}
const letraVisible = (orig) => "ABC"[S.ses.orden.indexOf(orig)];

function registrarRespuesta(itemId, letra, ok, modo, ms) {
  const it = IDX.items[itemId], si = stItem(itemId), sf = stFam(it.familia), P = S.estado.perfil;
  si.vistos++; if (ok) si.aciertos++; si.ultimo = Date.now(); si.ultimoOk = ok; P.respondidas++;
  if (ok) {
    sf.aciertos++;
    if (sf.enCofre) {
      sf.caja = Math.min(sf.caja + 1, INTERVALOS.length - 1);
      sf.proxima = masDias(hoy(), INTERVALOS[sf.caja]);
      if (sf.caja >= DOMINIO) sf.enCofre = false;
    } else if (sf.caja < DOMINIO) { sf.caja = Math.max(sf.caja, 1); }
  } else {
    sf.fallos++; sf.caja = 0; sf.enCofre = true; sf.proxima = masDias(hoy(), 1);
  }
  const ob = outbox(); ob.intentos.push({ item: itemId, familia: it.familia, componente: it.comp, ok, resp: letra, modo, ms, t: new Date().toISOString() }); setOutbox(ob);
}

function responder() {
  const s = S.ses, q = s.cola[s.i], it = IDX.items[q.id];
  if (!s.sel || s.respondida) return;
  const ok = s.sel === it.clave, ms = Date.now() - s.t0;
  s.respondida = true;
  s.res.push({ id: q.id, ok, sel: s.sel, repaso: !!q.repaso, rescate: !!q.rescate });
  registrarRespuesta(q.id, s.sel, ok, s.tipo, ms);
  if (s.tipo === "simulacro") { guardarLocal(); siguiente(); return; }
  let xp = 0;
  if (ok) {
    xp = q.rescate ? 15 : q.repaso ? 15 : 10;
    if (q.rescate) { s.vidas = Math.min(CFG.vidas, s.vidas + 2); S.estado.perfil.rescates++; }
    sonar("ok"); confeti(40);
  } else { s.vidas = Math.max(0, s.vidas - 1); sonar("mal"); }
  s.xp += xp; S.estado.perfil.xp += xp; s.ultimoXp = xp;
  guardarLocal(); render();
  setTimeout(() => document.querySelector(".fb")?.scrollIntoView({ behavior: "smooth", block: "start" }), 60);
}
function siguiente() {
  const s = S.ses;
  if (s.i + 1 >= s.cola.length) { terminarSesion(); return; }
  s.i++; prepararPregunta(); render(); scrollTo({ top: 0 });
}
function abrirRescate() {
  const s = S.ses, it = IDX.items[s.cola[s.i].id];
  const usados = s.cola.map(c => c.id);
  const varId = itemVariante(it.familia, usados);
  modalLeccion(it.familia, varId ? () => {
    s.cola.splice(s.i + 1, 0, { id: varId, rescate: true });
    cerrarModal(); siguiente();
  } : null);
}

function terminarSesion() {
  const s = S.ses, P = S.estado.perfil, ok = s.res.filter(r => r.ok).length, total = s.res.length;
  if (s.tipo === "simulacro") { cerrarSimulacro(); return; }
  let bonus = 0;
  const cuentaParaRacha = s.tipo === "reto" || s.tipo === "duelo";
  if (cuentaParaRacha) {
    const d = hoy();
    if (P.ultimoDia !== d) {
      P.racha = P.ultimoDia === masDias(d, -1) ? P.racha + 1 : 1;
      P.ultimoDia = d; if (!P.dias.includes(d)) P.dias.push(d); P.dias = P.dias.slice(-120);
      P.mejorRacha = Math.max(P.mejorRacha, P.racha); bonus += 20;
    }
    if (s.tipo === "reto") S.estado.retoHoy = d;
  }
  if (total >= 5 && ok === total) bonus += 30;
  if (s.tipo === "duelo") P.dueloSemana = semanaISO();
  P.xp += bonus; s.xp += bonus; s.bonus = bonus;
  const resumen = { fecha: hoy(), tipo: s.tipo, total, ok, xp: s.xp, comp: s.comp };
  S.estado.sesiones.push(resumen); S.estado.sesiones = S.estado.sesiones.slice(-200);
  s.nuevas = revisarInsignias(resumen);
  const ob = outbox(); ob.sesiones.push({ tipo: s.tipo, total, correctas: ok, xp: s.xp, detalle: { res: s.res, comp: s.comp } }); setOutbox(ob);
  guardarLocal(); programarSync(100);
  sonar("fin"); confeti(ok / Math.max(total, 1) >= .7 ? 140 : 60);
  ir("resumen");
}

/* ---------- simulacro mensual ---------- */
function primerSabado(y, m) { const d = new Date(y, m, 1, 12); while (d.getDay() !== 6) d.setDate(d.getDate() + 1); return fechaISO(d); }
function simulacroInfo() {
  const now = new Date(), y = now.getFullYear(), m = now.getMonth(), h = hoy();
  const mesKey = `${y}-${pad(m + 1)}`;
  const hecho = S.estado.simulacros.some(x => x.fecha.startsWith(mesKey));
  const fechaMes = primerSabado(y, m);
  const inicio = S.estado.perfil.inicio || h;
  if (!hecho && h >= fechaMes && fechaMes >= inicio) return { disponible: true, fecha: fechaMes, dias: 0 };
  const prox = (h < fechaMes && !hecho) ? fechaMes : primerSabado(m === 11 ? y + 1 : y, (m + 1) % 12);
  return { disponible: false, fecha: prox, dias: difDias(h, prox) };
}
function cerrarSimulacro() {
  const s = S.ses, porComp = {};
  s.res.forEach(r => { const c = IDX.items[r.id].comp; (porComp[c] ||= { ok: 0, n: 0 }); porComp[c].n++; if (r.ok) porComp[c].ok++; });
  const acb = s.res.filter(r => IDX.items[r.id].comp !== "PSI");
  const puntaje = acb.length ? Math.round(acb.filter(r => r.ok).length / acb.length * 10000) / 100 : 0;
  const psiR = s.res.filter(r => IDX.items[r.id].comp === "PSI");
  const psi = psiR.length ? Math.round(psiR.filter(r => r.ok).length / psiR.length * 100) : null;
  const minutos = Math.round((Date.now() - s.inicio) / 60000);
  const reg = { fecha: hoy(), puntaje, psi, porComp, total: s.res.length, minutos };
  S.estado.simulacros.push(reg);
  const xp = 50 + Math.round(puntaje / 2); S.estado.perfil.xp += xp; s.xp = xp;
  S.estado.sesiones.push({ fecha: hoy(), tipo: "simulacro", total: s.res.length, ok: s.res.filter(r => r.ok).length, xp });
  s.sim = reg; s.nuevas = revisarInsignias({ tipo: "simulacro", puntaje });
  const ob = outbox(); ob.sesiones.push({ tipo: "simulacro", total: s.res.length, correctas: s.res.filter(r => r.ok).length, xp, detalle: reg }); setOutbox(ob);
  guardarLocal(); programarSync(100); sonar("fin"); if (puntaje >= 60) confeti(160);
  ir("resumenSimulacro");
}
function descargarICS() { location.href = "simulacro.ics"; }

/* ---------- insignias ---------- */
const INSIGNIAS = [
  { id: "primer_reto", e: "🌱", n: "Primer reto", d: "Completa tu primer reto diario" },
  { id: "racha3", e: "🔥", n: "Racha de 3", d: "3 días seguidos" },
  { id: "racha7", e: "🔥", n: "Racha de 7", d: "7 días seguidos" },
  { id: "racha15", e: "🌋", n: "Racha de 15", d: "15 días seguidos" },
  { id: "racha30", e: "☀️", n: "Racha de 30", d: "30 días seguidos" },
  { id: "perfecto", e: "💯", n: "Reto perfecto", d: "Un reto sin errores" },
  { id: "semana80", e: "🎯", n: "Semana certera", d: "7 días seguidos con 80 % o más" },
  { id: "rescatista", e: "🛟", n: "Rescatista", d: "Supera 3 lecciones de rescate" },
  { id: "duelista", e: "⚔️", n: "Duelista", d: "Gana un duelo contra tus errores" },
  { id: "algoritmo", e: "🧩", n: "Maestra del algoritmo", d: "Domina algoritmos y detección de fallas" },
  { id: "convivencia", e: "🕊️", n: "Experta en Ruta de Convivencia", d: "Domina la clasificación y los protocolos" },
  { id: "d1278", e: "📜", n: "Experta en Decreto 1278", d: "Domina el estatuto docente" },
  { id: "siee", e: "📝", n: "Guardiana del SIEE", d: "Domina la evaluación y el Decreto 1290" },
  { id: "inclusion", e: "🌈", n: "Aula para todos", d: "Domina PIAR y DUA" },
  { id: "lectora", e: "📚", n: "Lectora crítica", d: "Domina los tres niveles de lectura" },
  { id: "numeros", e: "🧮", n: "Mente cuantitativa", d: "Domina razonamiento cuantitativo" },
  { id: "cien", e: "🏅", n: "100 preguntas", d: "Responde 100 preguntas" },
  { id: "xp1000", e: "⭐", n: "1.000 XP", d: "Acumula 1.000 puntos" },
  { id: "sim1", e: "⏱️", n: "Primer simulacro", d: "Presenta tu primer simulacro" },
  { id: "aprobada", e: "✅", n: "Sobre la línea", d: "60 o más en un simulacro" },
  { id: "sobresaliente", e: "🏆", n: "Sobresaliente", d: "80 o más en un simulacro" }
];
const domina = fams => fams.every(f => (S.estado.familias[f]?.caja || 0) >= DOMINIO);
function revisarInsignias(ev) {
  const P = S.estado.perfil, I = P.insignias, nuevas = [];
  const dar = id => { if (!I[id]) { I[id] = hoy(); nuevas.push(INSIGNIAS.find(x => x.id === id)); } };
  if (ev.tipo === "reto") dar("primer_reto");
  if (P.racha >= 3) dar("racha3"); if (P.racha >= 7) dar("racha7"); if (P.racha >= 15) dar("racha15"); if (P.racha >= 30) dar("racha30");
  if (ev.tipo === "reto" && ev.total >= 5 && ev.ok === ev.total) dar("perfecto");
  if (P.rescates >= 3) dar("rescatista");
  if (ev.tipo === "duelo" && ev.ok === ev.total) dar("duelista");
  if (domina(["DIS-ALGO", "DIS-FALLAS"])) dar("algoritmo");
  if (domina(["NOR-CONV-TIPO", "NOR-CONV-RUTA"])) dar("convivencia");
  if (domina(["NOR-ESTATUTO"])) dar("d1278");
  if (domina(["PED-EVAL", "PED-EVAL-NORM"])) dar("siee");
  if (domina(["PED-INCL"])) dar("inclusion");
  if (domina(["LC-LIT", "LC-INF", "LC-CRIT"])) dar("lectora");
  if (domina(["RC-INT", "RC-FORM", "RC-ARG"])) dar("numeros");
  if (P.respondidas >= 100) dar("cien");
  if (P.xp >= 1000) dar("xp1000");
  if (ev.tipo === "simulacro") { dar("sim1"); if (ev.puntaje >= 60) dar("aprobada"); if (ev.puntaje >= 80) dar("sobresaliente"); }
  // semana certera: 7 días consecutivos con reto >= 80 %
  const porDia = {}; S.estado.sesiones.filter(x => x.tipo === "reto").forEach(x => { const p = x.ok / Math.max(1, x.total); porDia[x.fecha] = Math.max(porDia[x.fecha] || 0, p); });
  let seguidos = 0; for (let k = 0; k < 7; k++) { if ((porDia[masDias(hoy(), -k)] || 0) >= .8) seguidos++; else break; }
  if (seguidos >= 7) dar("semana80");
  return nuevas;
}
function semanaISO(d = new Date()) {
  const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())); const dn = t.getUTCDay() || 7;
  t.setUTCDate(t.getUTCDate() + 4 - dn); const y0 = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
  return `${t.getUTCFullYear()}-W${Math.ceil(((t - y0) / 864e5 + 1) / 7)}`;
}

/* ---------- métricas ---------- */
function statsComp(c) {
  const ids = IDX.porComp[c] || []; let n = 0, ok = 0, vistos = 0;
  ids.forEach(id => { const s = S.estado.items[id]; if (s?.vistos) { vistos++; n += s.vistos; ok += s.aciertos; } });
  const fams = Object.keys(S.banco.familias).filter(f => S.banco.familias[f].componente === c);
  const dom = fams.filter(f => (S.estado.familias[f]?.caja || 0) >= DOMINIO).length;
  return { total: ids.length, vistos, precision: n ? ok / n : null, fams: fams.length, dom,
    avance: Math.round(((vistos / (ids.length || 1)) * .5 + (dom / (fams.length || 1)) * .5) * 100) };
}
function rachaVisible() { const P = S.estado.perfil; return (P.ultimoDia === hoy() || P.ultimoDia === masDias(hoy(), -1)) ? P.racha : 0; }
function nivel(xp) { const n = Math.floor(Math.sqrt(xp / 50)) + 1; const base = (n - 1) ** 2 * 50, sig = n ** 2 * 50; return { n, p: (xp - base) / (sig - base), falta: sig - xp }; }
function preparacion() {
  const comps = S.banco.componentes.filter(c => c.id !== "PSI").map(c => statsComp(c.id));
  const prec = comps.filter(c => c.precision !== null);
  const media = prec.length ? prec.reduce((a, c) => a + c.precision, 0) / prec.length : 0;
  const cobertura = comps.reduce((a, c) => a + c.vistos, 0) / comps.reduce((a, c) => a + c.total, 0);
  return Math.round(media * cobertura * 100);
}

/* ---------- navegación ---------- */
function ir(v) { S.vista = v; render(); scrollTo({ top: 0 }); }
function revisarDia() { if (S.vista === "inicio" && S.estado) render(); }

/* ---------- vistas ---------- */
function vistaLogin() {
  return `<div class="stack" style="padding-top:8vh">
    <div class="center"><div style="font-size:64px">🎓</div><h1>Plaza Docente</h1>
    <p class="muted">Tu dosis diaria para la plaza docente</p></div>
    <div class="card stack">
      <label class="lab" for="clave">Clave de acceso</label>
      <input id="clave" class="input" type="password" autocomplete="current-password" autocapitalize="none" placeholder="La clave que te dieron">
      <button class="btn" data-a="entrar">Entrar</button>
      <p class="small muted">Tu avance se guarda en la nube con esta clave. Si cambias de celular o se borran los datos, solo vuelve a escribirla.</p>
    </div></div>`;
}
function vistaNombre() {
  return `<div class="stack" style="padding-top:8vh"><div class="center"><div style="font-size:56px">👋</div><h1>¡Bienvenida!</h1></div>
    <div class="card stack"><label class="lab" for="nombre">¿Cómo quieres que te llame?</label>
    <input id="nombre" class="input" autocomplete="given-name" placeholder="Tu nombre">
    <button class="btn" data-a="guardarNombre">Comenzar</button></div></div>`;
}
function semanaHTML() {
  const d = hoy(), P = S.estado.perfil; let h = "";
  for (let k = 6; k >= 0; k--) { const f = masDias(d, -k), dt = new Date(f + "T12:00:00");
    h += `<div class="d ${P.dias.includes(f) ? "on" : ""} ${k === 0 ? "hoy" : ""}">${DIAS[dt.getDay()]}<b>${P.dias.includes(f) ? "🔥" : dt.getDate()}</b></div>`; }
  return h;
}
function vistaInicio() {
  const P = S.estado.perfil, r = rachaVisible(), lv = nivel(P.xp), hecho = S.estado.retoHoy === hoy();
  const venc = familiasVencidas().length, cof = cofre().length, sim = simulacroInfo();
  const prep = preparacion();
  const standalone = navigator.standalone || matchMedia("(display-mode: standalone)").matches;
  const dueloOk = cof > 0 && P.dueloSemana !== semanaISO();
  const saludo = new Date().getHours() < 12 ? "Buenos días" : new Date().getHours() < 19 ? "Buenas tardes" : "Buenas noches";
  return `
  <div class="top"><div><div class="muted small">${saludo},</div><h1>${esc(P.nombre || "aspirante")}</h1></div>
    <div class="row"><button class="icon-btn" data-v="insignias" aria-label="Insignias">🏆</button><button class="icon-btn" data-v="ajustes" aria-label="Ajustes">⚙️</button></div></div>
  <div class="chips" style="margin-bottom:14px">
    <span class="chip fire">🔥 ${r} ${r === 1 ? "día" : "días"}</span>
    <span class="chip xp">⭐ ${P.xp} XP · Nivel ${lv.n}</span>
    ${cof ? `<button class="chip" data-v="cofre">🧠 Cofre ${cof}</button>` : ""}
  </div>
  ${!standalone && /iP(hone|ad)/.test(navigator.userAgent) ? `<div class="card flat small" style="margin-bottom:12px">📲 <b>Instálala:</b> toca <b>Compartir</b> en Safari y luego <b>Agregar a inicio</b>. Así se abre como app, sin barras.</div>` : ""}
  <section class="hero">
    <div class="row between"><div><div class="small" style="opacity:.9">Reto de hoy · ${fechaLarga(hoy())}</div>
      <div class="big">${hecho ? "¡Cumplido! ✓" : `${lecturaPendiente() ? "Lectura + " : ""}${CFG.preguntasPorReto} preguntas`}</div>
      <div class="small" style="opacity:.92">${hecho ? "Tu racha está a salvo. Puedes seguir practicando." : venc ? `Incluye ${Math.min(venc, CFG.maxRepasoPorReto)} de repaso: misma competencia, otro contexto` : `Unos 15 minutos · lees el documento oficial y luego respondes`}</div></div>
      <div class="flame">${hecho ? "🏅" : "🔥"}</div></div>
    <div class="week">${semanaHTML()}</div>
    <button class="btn" data-a="reto">${hecho ? "Practicar un reto más" : "Empezar el reto de hoy"}</button>
  </section>

  ${sim.disponible ? `<div class="card mt" style="border:2px solid var(--violet)"><div class="row"><div style="font-size:34px">⏱️</div><div><h3>Simulacro del mes disponible</h3>
     <p class="small muted">${CFG.simulacroPreguntas} preguntas · ${CFG.simulacroPreguntas * CFG.minutosPorPregunta} minutos · sin retroalimentación hasta el final, como el examen.</p></div></div>
     <button class="btn violet mt" data-a="simulacro">Presentar simulacro</button></div>`
   : `<div class="card mt"><div class="row"><div style="font-size:30px">🗓️</div><div style="flex:1"><h3>Próximo simulacro: ${fechaLarga(sim.fecha)}</h3>
     <p class="small muted">${sim.dias <= 7 ? `Faltan ${sim.dias} ${sim.dias === 1 ? "día" : "días"}. Reserva ${CFG.simulacroPreguntas * CFG.minutosPorPregunta} minutos sin interrupciones desde las 8:00 a. m.` : "Cada primer sábado del mes, a las 8:00 a. m., como el examen real."}</p></div></div>
     <button class="btn sec mt" data-a="ics">📅 Agregar recordatorios al calendario</button></div>`}

  ${dueloOk ? `<div class="card mt"><div class="row"><div style="font-size:30px">⚔️</div><div style="flex:1"><h3>Duelo contra tus errores</h3>
     <p class="small muted">${cof} ${cof === 1 ? "competencia" : "competencias"} en tu cofre. Enfréntalas con casos nuevos.</p></div></div>
     <button class="btn amber mt" data-a="duelo">Aceptar el duelo</button></div>` : ""}

  <div class="card mt"><div class="row between"><h3>Preparación estimada</h3><b>${prep}%</b></div>
    <div class="bar amber mt"><i style="width:${prep}%"></i></div>
    <p class="tiny muted mt">Combina tu precisión y cuánto del banco has trabajado. La prueba eliminatoria exige 60/100.</p>
    <button class="btn ghost" data-v="progreso">Ver progreso por componente →</button></div>

  <div class="card mt"><div class="row"><div style="font-size:30px">📝</div><div style="flex:1"><h3>Cuaderno de estudio</h3>
     <p class="small muted">Para sentarte con calma: lee los documentos completos, guarda conceptos con tus palabras y repásalos. ${S.estado.cuaderno.conceptos.length ? `Llevas ${S.estado.cuaderno.conceptos.length} ${S.estado.cuaderno.conceptos.length === 1 ? "concepto" : "conceptos"}.` : ""}</p></div></div>
     <button class="btn blue mt" data-v="cuaderno">Abrir cuaderno</button></div>

  <div class="card mt"><div class="row"><div style="font-size:30px">📚</div><div style="flex:1"><h3>Biblioteca: estudia y responde</h3>
     <p class="small muted">${(S.banco.fichas || []).filter(f => fichaLeida(f.id)).length} de ${(S.banco.fichas || []).length} fichas estudiadas. Cada ficha resume un tema con el texto oficial y te pregunta enseguida.</p></div></div>
     <button class="btn sec mt" data-v="biblioteca">Abrir biblioteca</button></div>

  <h2 class="mt2">Mapa de estudio</h2>
  <p class="small muted">Todos los módulos están abiertos. Toca uno para practicarlo.</p>
  <div class="map">${S.banco.componentes.map(c => { const st = statsComp(c.id);
    return `<button class="node" data-a="modulo" data-c="${c.id}"><div class="ring" style="--p:${st.avance}"><span>${c.icono}</span></div>
      <div class="meta"><b>${esc(c.nombre)}</b><span class="tiny muted">${st.dom}/${st.fams} competencias dominadas · ${st.vistos}/${st.total} preguntas</span></div><span class="muted">›</span></button>`; }).join("")}</div>
  <p class="sync center mt" data-sync>${syncHTML()}</p>`;
}

function citasHTML(citas, titulo = "📜 Lo que dice el documento oficial") {
  if (!citas?.length) return "";
  return `<div class="cita"><b>${titulo}</b>${citas.map(c => `<blockquote>«${esc(c.texto)}»<cite>${esc(DOCS[c.doc] || c.doc)}${c.ubicacion ? " · " + esc(c.ubicacion) : ""}</cite></blockquote>`).join("")}</div>`;
}
function vistaFicha() {
  const s = S.ses, q = s.cola[s.i], f = IDX.fichas[q.ficha], F = S.banco.familias[f.familia], comp = IDX.comps[F.componente];
  const nPreg = (IDX.porFicha[f.id] || []).length;
  return `
  <div class="qhead"><button class="icon-btn" data-a="salir" aria-label="Salir">✕</button>
    <div class="bar"><i style="width:${(s.i / s.cola.length) * 100}%"></i></div><span class="tiny muted">${s.i + 1}/${s.cola.length}</span></div>
  <div class="review-banner">📘 Estudia y responde: lee con calma, luego vienen ${nPreg} preguntas sobre esta ficha${s.tipo === "estudio" ? " y casos tipo examen" : ""}.</div>
  <div class="chips" style="margin-bottom:10px"><span class="tag amber">${comp.icono} ${esc(comp.nombre)}</span><span class="tag blue">${esc(F.nombre)}</span></div>
  <h2>${esc(f.titulo)}</h2>
  <div class="lectura">${esc(f.lectura)}</div>
  <div class="card flat mt"><b>Ideas clave</b><ul class="small">${f.puntos.map(p => `<li>${esc(p)}</li>`).join("")}</ul></div>
  ${citasHTML(f.citas, "📜 Textual de los documentos oficiales")}
  <div class="sticky-bottom"><button class="btn" data-a="leido">Ya lo leí: ¡a practicar!</button></div>`;
}
function vistaLectura() {
  const s = S.ses, q = s.cola[s.i], L = LECT[q.lectura], pi = planInfo(), palabras = L.parrafos.join(" ").split(/\s+/).length;
  const nPreg = s.cola.slice(s.i + 1).filter(c => c.id && S.banco.contextos?.[c.id]?.lectura === q.lectura).length;
  return `
  <div class="qhead"><button class="icon-btn" data-a="salir" aria-label="Salir">✕</button>
    <div class="bar"><i style="width:${(s.i / s.cola.length) * 100}%"></i></div><span class="tiny muted">${s.i + 1}/${s.cola.length}</span></div>
  <div class="review-banner lect">📖 Lectura del día · ${pi.leidas + (lecturaLeida(q.lectura) ? 0 : 1)} de ${pi.total} del plan · unos ${Math.max(2, Math.round(palabras / 170))} min${nPreg ? ` · luego ${nPreg} ${nPreg === 1 ? "pregunta" : "preguntas"} sobre este texto` : ""}</div>
  <div class="chips" style="margin-bottom:10px"><span class="tag blue">${esc(L.nombre)}</span><span class="tag">Parte ${L.parte} de ${L.total}</span></div>
  <h2>${esc(L.titulo)}</h2>
  <div class="lectura doc">${L.parrafos.map(p => `<p>${esc(p)}</p>`).join("")}</div>
  <p class="tiny muted mt">Texto oficial, tal como aparece en el documento. Léelo completo: las preguntas de hoy se responden con lo que dice aquí.</p>
  <div class="sticky-bottom"><button class="btn" data-a="leidoL">Ya la leí: ¡a practicar!</button></div>`;
}
function preLecturaHTML(it, abierta) {
  const c = S.banco.contextos?.[it.id]; if (!c) return "";
  return `<details class="prelee" ${abierta ? "open" : ""}><summary><span>📖 ${abierta ? "Antes de responder, lee esto" : "Releer el documento"}</span><span class="muted tiny">${esc(c.nombre.split(" (")[0])}</span></summary>
    <div class="txt">${c.parrafos.map(p => `<p>${esc(p)}</p>`).join("")}</div>
    <div class="tiny muted">${esc(c.nombre)} · ${esc(c.titulo)}</div></details>`;
}
function vistaPregunta() {
  const s = S.ses, q = s.cola[s.i];
  if (q.ficha) return vistaFicha();
  if (q.lectura) return vistaLectura();
  const it = IDX.items[q.id], caso = IDX.casos[it.caso], comp = IDX.comps[it.comp];
  const sim = s.tipo === "simulacro";
  const pq = s.i > 0 ? s.cola[s.i - 1] : null;
  const prev = pq?.id ? IDX.items[pq.id].caso : null;
  const pre = it.tipo === "caso" && !sim ? preLecturaHTML(it, s.preLeer && !s.respondida) : "";
  const abierto = prev !== it.caso || s.respondida === false;
  const res = s.respondida ? s.res[s.res.length - 1] : null;
  const vidas = sim ? "" : `<span class="chip heart" aria-label="${s.vidas} vidas">${s.vidas ? "❤️".repeat(s.vidas) : "💔"}</span>`;
  const reloj = sim ? `<span class="chip timer" data-timer>⏱️ --:--</span>` : "";
  const opciones = s.orden.map((orig, k) => {
    const o = it.opciones.find(x => x.l === orig), L = "ABC"[k];
    let cls = "";
    if (s.respondida && !sim) { if (orig === it.clave) cls = "ok"; else if (orig === s.sel) cls = "bad"; }
    else if (s.sel === orig) cls = "sel";
    return `<button class="opt ${cls}" data-a="sel" data-l="${orig}" ${s.respondida ? "disabled" : ""}><span class="L">${L}</span><span>${esc(o.t)}</span></button>`;
  }).join("");
  const etiqueta = q.rescate ? `<div class="review-banner">🛟 Lección de rescate: misma competencia, otro contexto</div>`
    : q.repaso ? `<div class="review-banner">🔁 Repaso: fallaste esta competencia antes. Ahora en otro contexto.</div>` : "";
  let fb = "";
  if (s.respondida && !sim) {
    const just = s.orden.map(orig => { const o = it.opciones.find(x => x.l === orig);
      return `<p><b>${letraVisible(orig)}.</b> ${esc(o.j)}</p>`; }).join("");
    fb = `<div class="fb ${res.ok ? "ok" : "bad"} pop">
      <h3>${res.ok ? pick(["¡Exacto!", "¡Muy bien!", "¡Así se hace!", "¡Correcto!"]) + ` +${s.ultimoXp} XP` : `La respuesta era la ${letraVisible(it.clave)}`}</h3>
      ${res.ok ? "" : `<p class="small">Esta competencia queda en tu cofre: te la volveré a presentar en otro contexto hasta que la domines.</p>`}
      ${it.explicacion ? `<div class="expl"><b>🧭 Por qué</b><p>${esc(it.explicacion)}</p></div>` : ""}
      <div class="just">${just}</div>
      ${citasHTML(it.citas)}
      <div class="tip">💡 <b>Clave CNSC:</b> ${esc(it.consejo)}</div>
      <div class="src">📚 ${esc(it.fuente)}</div>
      <button class="linkbtn" data-a="reportar">🚩 ¿Algo raro en esta pregunta? Repórtala</button>
    </div>`;
  }
  const tablaHTML = caso?.tabla ? `<table class="t"><tr>${caso.tabla.encabezado.map(h => `<th>${esc(h)}</th>`).join("")}</tr>${caso.tabla.filas.map(f => `<tr>${f.map(c => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</table>` : "";
  return `
  <div class="qhead"><button class="icon-btn" data-a="salir" aria-label="Salir">✕</button>
    <div class="bar"><i style="width:${(s.i / s.cola.length) * 100}%"></i></div>
    <span class="tiny muted">${s.i + 1}/${s.cola.length}</span>${vidas}${reloj}</div>
  ${etiqueta}
  <div class="chips" style="margin-bottom:10px">
    <span class="tag">${esc(comp.prueba.split(" (")[0])}</span>
    <span class="tag amber">${comp.icono} ${esc(comp.oficial)}</span>
    <span class="tag blue">${esc(it.competencia)}</span>${it.dificultad ? `<span class="tag ${it.dificultad === 3 ? "amber" : ""}">${["", "Básica", "Media", "Alta"][it.dificultad]}</span>` : ""}
  </div>
  ${pre}
  ${caso ? `<details class="case" ${abierto ? "open" : ""}><summary><span>📄 Caso: ${esc(caso.titulo)}</span><span class="muted tiny">ver/ocultar</span></summary>
    <div class="txt">${esc(caso.texto)}</div>
    ${caso.lectura ? `<blockquote>${esc(caso.lectura)}</blockquote>` : ""}
    ${caso.codigo ? `<pre>${esc(caso.codigo)}</pre>` : ""}${tablaHTML}
  </details>` : `<details class="case"><summary><span>📘 Pregunta de conocimiento · ${esc(IDX.fichas[it.ficha]?.titulo || "")}</span><span class="muted tiny">releer ficha</span></summary>
    <div class="txt">${esc(IDX.fichas[it.ficha]?.lectura || "")}</div></details>`}
  <div class="enun">${esc(it.enunciado)}…</div>
  ${opciones}
  ${fb}
  <div class="sticky-bottom">
    ${!s.respondida ? `<button class="btn" data-a="responder" ${s.sel ? "" : "disabled"}>${sim ? "Responder y continuar" : "Comprobar"}</button>`
      : `<button class="btn" data-a="siguiente">${s.i + 1 >= s.cola.length ? "Ver resultado" : "Continuar"}</button>
         ${!res.ok && !q.rescate ? `<button class="btn ghost" data-a="rescate">🛟 Lección de rescate (+15 XP${s.vidas < CFG.vidas ? ", +2 ❤️" : ""})</button>` : ""}`}
  </div>`;
}

const MENSAJES = {
  alto: ["Estás pensando como evaluadora de la CNSC. Así se gana una plaza.", "Excelente. Ese criterio es el que separa a quien pasa de quien queda en lista.", "¡Qué nivel! Mantén el ritmo y la plaza está más cerca."],
  medio: ["Buen trabajo. Cada error de hoy es un punto que no perderás el día del examen.", "Vas bien. Lo que fallaste ya está en tu cofre para repasarlo en otro contexto.", "Constancia > perfección. Mañana vuelves más fuerte."],
  bajo: ["Hoy fue un día de aprendizaje intenso. Lee las justificaciones: ahí está la lógica de la CNSC.", "Los errores aquí son gratis; en el examen no. Hoy ganaste mucho.", "Tranquila: tu cofre guardó estas competencias y las vamos a entrenar juntas."]
};
function vistaResumen() {
  if (!S.ses.res.length) return `<div class="center stack" style="padding-top:8vh"><div style="font-size:64px" class="pop">📖</div><h1>¡Lectura registrada!</h1>
    <p class="muted">Llevas ${planInfo().leidas} de ${planInfo().total} lecturas del plan.</p><button class="btn" data-v="biblioteca">Volver a la biblioteca</button><button class="btn ghost" data-v="inicio">Ir al inicio</button></div>`;
  const s = S.ses, ok = s.res.filter(r => r.ok).length, tot = s.res.length, p = Math.round(ok / Math.max(1, tot) * 100);
  const msj = pick(p >= 80 ? MENSAJES.alto : p >= 50 ? MENSAJES.medio : MENSAJES.bajo);
  const fallas = s.res.filter(r => !r.ok).map(r => S.banco.familias[IDX.items[r.id].familia].nombre);
  const prep = preparacion();
  return `<div class="center stack" style="padding-top:4vh">
    <div style="font-size:64px" class="pop">${p >= 80 ? "🏆" : p >= 50 ? "💪" : "🌱"}</div>
    <h1>${s.tipo === "duelo" ? "Duelo terminado" : s.tipo === "estudio" ? "¡Ficha estudiada!" : s.tipo === "lectura" ? "¡Lectura y práctica listas!" : s.tipo === "modulo" ? "Práctica terminada" : "¡Reto terminado!"}</h1>
    <div class="score">${p}%</div><p class="muted">${ok} de ${tot} correctas · +${s.xp} XP${s.bonus ? ` (incluye bono de ${s.bonus})` : ""}</p>
    <div class="chips" style="justify-content:center"><span class="chip fire">🔥 Racha: ${rachaVisible()} ${rachaVisible() === 1 ? "día" : "días"}</span><span class="chip xp">⭐ ${S.estado.perfil.xp} XP</span></div>
    <div class="card" style="text-align:left"><p>${S.estado.perfil.nombre ? esc(S.estado.perfil.nombre) + ", " + esc(msj.charAt(0).toLowerCase() + msj.slice(1)) : esc(msj)}</p>
      <div class="row between small mt"><span>Preparación para la meta (60/100)</span><b>${prep}%</b></div><div class="bar amber"><i style="width:${prep}%"></i></div>
      ${fallas.length ? `<p class="small mt"><b>🧠 Guardado en tu cofre:</b> ${esc([...new Set(fallas)].join(" · "))}. Aparecerán en próximos retos con otros contextos.</p>` : `<p class="small mt">Sin errores para el cofre. 👏</p>`}
    </div>
    ${s.nuevas?.length ? `<div class="card"><h3>Nuevas insignias</h3><div class="badge-grid mt">${s.nuevas.map(b => `<div class="badge on pop"><div class="e">${b.e}</div><b>${esc(b.n)}</b></div>`).join("")}</div></div>` : ""}
    <button class="btn" data-v="inicio">Volver al inicio</button></div>`;
}
function vistaResumenSimulacro() {
  const s = S.ses, r = s.sim, aprueba = r.puntaje >= 60;
  const filas = S.banco.componentes.filter(c => r.porComp[c.id]).map(c => { const x = r.porComp[c.id], p = Math.round(x.ok / x.n * 100);
    return `<div class="comp-row"><span>${c.icono}</span><div><div class="small"><b>${esc(c.nombre)}</b> · ${x.ok}/${x.n}</div><div class="bar ${p < 60 ? "amber" : ""}"><i style="width:${p}%"></i></div></div><b class="small">${p}%</b></div>`; }).join("");
  const errores = s.res.filter(x => !x.ok);
  return `<div class="stack">
    <div class="center"><div style="font-size:60px" class="pop">${aprueba ? "🏆" : "📈"}</div><h1>Resultado del simulacro</h1>
    <div class="score" style="color:${aprueba ? "var(--ok)" : "var(--coral)"}">${r.puntaje.toLocaleString("es-CO",{minimumFractionDigits:2,maximumFractionDigits:2})}</div>
    <p class="muted">Aptitudes y Competencias Básicas (sobre 100) · mínimo aprobatorio para docentes: 60 · ${r.minutos} min</p>
    ${r.psi !== null ? `<p class="small">Psicotécnica (clasificatoria): ${r.psi}% de acierto</p>` : ""}</div>
    <div class="card"><h3>Por componente</h3>${filas}<p class="tiny muted mt">Estimación del entrenamiento: la CNSC califica con puntuación directa o ajustada y puede excluir ítems que no cumplan parámetros psicométricos.</p></div>
    ${errores.length ? `<div class="card"><h3>Revisa tus ${errores.length} errores</h3><p class="small muted">Ya están en tu cofre. Toca uno para ver la justificación.</p>
      <div class="list mt">${errores.map(e => { const it = IDX.items[e.id], o = it.opciones.find(x => x.l === it.clave);
        return `<details><summary class="small"><b>${esc(IDX.casos[it.caso].titulo)}:</b> ${esc(it.enunciado)}…</summary><p class="small"><b>Correcta:</b> ${esc(o.t)}</p><p class="small muted">${esc(o.j)}</p><p class="tiny">💡 ${esc(it.consejo)}</p></details>`; }).join("")}</div></div>` : ""}
    ${s.nuevas?.length ? `<div class="card"><h3>Nuevas insignias</h3><div class="badge-grid mt">${s.nuevas.map(b => `<div class="badge on"><div class="e">${b.e}</div><b>${esc(b.n)}</b></div>`).join("")}</div></div>` : ""}
    <button class="btn" data-v="inicio">Volver al inicio</button></div>`;
}
/* ---------- cuaderno de estudio ---------- */
const CU = { doc: null, lectura: null, sel: null, q: "", flash: null };
const docsDelPlan = () => { const m = {}; (S.banco.plan || []).forEach(l => (m[l.doc] ||= { doc: l.doc, nombre: l.nombre, partes: [] }).partes.push(l)); return Object.values(m); };
const conceptos = () => S.estado.cuaderno.conceptos;
const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
function vistaCuaderno() {
  const c = conceptos(), notas = Object.values(S.estado.cuaderno.notas).filter(x => x && x.trim()).length;
  return `<div class="top"><button class="icon-btn" data-v="inicio">‹</button><h2>Cuaderno de estudio</h2><span style="width:44px"></span></div>
  <p class="muted small">Esta sección es para estudiar sentada y con calma. El reto diario sigue siendo corto, para hacerlo en cualquier parte.</p>
  <button class="node" data-v="docs"><div style="font-size:34px">📚</div><div class="meta"><b>Leer los documentos completos</b><span class="tiny muted">Parte por parte. Toca un párrafo para convertirlo en concepto y escribe tus notas al final.</span></div><span class="muted">›</span></button>
  <button class="node" data-v="conceptos"><div style="font-size:34px">🧠</div><div class="meta"><b>Mis conceptos (${c.length})</b><span class="tiny muted">Tu glosario: el concepto, tu definición y el texto oficial de donde salió.</span></div><span class="muted">›</span></button>
  <button class="node" data-a="flashIni" ${c.length ? "" : "disabled style='opacity:.5'"}><div style="font-size:34px">🔁</div><div class="meta"><b>Repasar mis conceptos</b><span class="tiny muted">${c.length ? "Tarjetas: ves el concepto, lo explicas en voz alta y luego compruebas." : "Aparece cuando guardes tu primer concepto."}</span></div><span class="muted">›</span></button>
  <div class="card mt"><div class="row between"><span class="small"><b>${c.length}</b> conceptos · <b>${notas}</b> lecturas con notas</span>
    <button class="chip" data-a="exportarCuaderno" ${c.length || notas ? "" : "disabled"}>⬇️ Descargar</button></div>
    <p class="tiny muted">Descarga tu cuaderno como archivo de texto para imprimirlo o pasarlo a Word. Todo se guarda también en la nube con tu avance.</p></div>`;
}
function vistaDocs() {
  return `<div class="top"><button class="icon-btn" data-v="cuaderno">‹</button><h2>Documentos</h2><span style="width:44px"></span></div>
  <p class="muted small">Están en el orden de prioridad para la prueba. Las partes que leas aquí también cuentan en tu plan de lectura.</p>
  ${docsDelPlan().map(d => { const ok = d.partes.filter(l => lecturaLeida(l.id)).length, n = Math.round(ok / d.partes.length * 100);
    return `<button class="node" data-a="abrirDoc" data-d="${d.doc}"><div class="ring" style="--p:${n}"><span style="font-size:14px;font-weight:900">${n}%</span></div>
      <div class="meta"><b>${esc(d.nombre)}</b><span class="tiny muted">${ok} de ${d.partes.length} partes leídas</span></div><span class="muted">›</span></button>`; }).join("")}`;
}
function vistaDoc() {
  const d = docsDelPlan().find(x => x.doc === CU.doc); if (!d) return vistaDocs();
  return `<div class="top"><button class="icon-btn" data-v="docs">‹</button><h2 style="font-size:19px">${esc(d.nombre)}</h2><span style="width:44px"></span></div>
  <div class="card list">${d.partes.map(l => { const nota = (S.estado.cuaderno.notas[l.id] || "").trim(), nc = conceptos().filter(c => c.lectura === l.id).length;
    return `<button class="row between ficha-btn" data-a="leerParte" data-l="${l.id}"><span>${lecturaLeida(l.id) ? "✅" : "📄"} Parte ${l.parte} · ${esc(l.titulo)}${nota ? " · 📝" : ""}${nc ? ` · 🧠${nc}` : ""}</span><span class="muted">›</span></button>`; }).join("")}</div>`;
}
function vistaLeer() {
  const L = LECT[CU.lectura]; if (!L) return `<p class="muted">Cargando…</p>`;
  const d = docsDelPlan().find(x => x.doc === L.doc), k = d.partes.findIndex(x => x.id === L.id), ant = d.partes[k - 1], sig = d.partes[k + 1];
  const marcados = new Set(conceptos().filter(c => c.lectura === L.id).map(c => c.parrafo));
  return `<div class="top"><button class="icon-btn" data-a="volverDoc">‹</button><div class="center"><div class="tiny muted">${esc(L.nombre)}</div><b>Parte ${L.parte} de ${L.total}</b></div><span style="width:44px"></span></div>
  <h2>${esc(L.titulo)}</h2>
  <p class="tiny muted">Toca un párrafo para guardarlo como concepto en tu cuaderno.</p>
  <div class="lectura doc leer">${L.parrafos.map((p, i) => `<p data-a="parr" data-k="${i}" class="${CU.sel === i ? "selp" : ""} ${marcados.has(i) ? "marcado" : ""}">${esc(p)}</p>
     ${CU.sel === i ? `<div class="row wrap parr-acc"><button class="btn blue" style="width:auto;min-height:44px" data-a="nuevoConcepto" data-k="${i}">🧠 Crear concepto con este párrafo</button><button class="chip" data-a="parr" data-k="${i}">Cancelar</button></div>` : ""}`).join("")}</div>
  <div class="card mt"><label class="lab" for="notaL">📝 Mis notas de esta parte</label>
    <textarea id="notaL" class="input" rows="5" data-i="nota" placeholder="Ideas clave, dudas, ejemplos para el aula…">${esc(S.estado.cuaderno.notas[L.id] || "")}</textarea>
    <p class="tiny muted">Se guarda solo mientras escribes.</p></div>
  <button class="btn ${lecturaLeida(L.id) ? "sec" : ""} mt" data-a="marcarLeida">${lecturaLeida(L.id) ? "✓ Leída (tocar para desmarcar)" : "Marcar como leída"}</button>
  <div class="row mt">${ant ? `<button class="btn sec" data-a="leerParte" data-l="${ant.id}">‹ Anterior</button>` : ""}${sig ? `<button class="btn sec" data-a="leerParte" data-l="${sig.id}">Siguiente ›</button>` : ""}</div>`;
}
function vistaConceptos() {
  const q = CU.q.trim().toLowerCase(), lista = conceptos().slice().sort((a, b) => a.termino.localeCompare(b.termino, "es"))
    .filter(c => !q || (c.termino + " " + c.def + " " + (c.cita || "")).toLowerCase().includes(q));
  return `<div class="top"><button class="icon-btn" data-v="cuaderno">‹</button><h2>Mis conceptos</h2><button class="icon-btn" data-a="nuevoConcepto" aria-label="Nuevo concepto">＋</button></div>
  <input class="input" data-i="buscar" placeholder="🔎 Buscar en mis conceptos" value="${esc(CU.q)}">
  ${conceptos().length ? "" : `<div class="card mt center"><div style="font-size:44px">🧠</div><p>Aún no tienes conceptos.</p><p class="small muted">Abre un documento, toca un párrafo y guárdalo con tu propia definición. O toca ＋ para escribir uno desde cero.</p><button class="btn blue mt" data-v="docs">Ir a los documentos</button></div>`}
  <div class="mt">${lista.map(c => `<div class="card mt"><div class="row between"><h3>${esc(c.termino)}</h3><div class="row"><button class="chip" data-a="editConcepto" data-id="${c.id}">✏️</button><button class="chip" data-a="borrarConcepto" data-id="${c.id}">🗑️</button></div></div>
    ${c.def ? `<p>${esc(c.def)}</p>` : `<p class="small muted">Sin definición propia todavía.</p>`}
    ${c.cita ? `<details><summary class="tiny muted">📜 Texto oficial · ${esc(c.fuente || "")}</summary><blockquote class="citaC">${esc(c.cita)}</blockquote></details>` : c.fuente ? `<p class="tiny muted">${esc(c.fuente)}</p>` : ""}</div>`).join("")}</div>`;
}
function vistaFlash() {
  const F = CU.flash, c = F && conceptos().find(x => x.id === F.cola[F.i]);
  if (!c) return `<div class="center stack" style="padding-top:8vh"><div style="font-size:60px" class="pop">🎉</div><h1>Repaso terminado</h1>
    <p class="muted">${F ? `${F.ok} de ${F.cola.length} los sabías.` : ""}</p><button class="btn" data-v="cuaderno">Volver al cuaderno</button></div>`;
  return `<div class="qhead"><button class="icon-btn" data-v="cuaderno">✕</button><div class="bar"><i style="width:${F.i / F.cola.length * 100}%"></i></div><span class="tiny muted">${F.i + 1}/${F.cola.length}</span></div>
  <div class="card center flashcard" data-a="voltear"><div class="tiny muted">${F.vuelta ? "Tu definición" : "¿Qué significa?"}</div>
    <h1 class="mt">${esc(c.termino)}</h1>
    ${F.vuelta ? `<p class="mt" style="text-align:left">${esc(c.def || "—")}</p>${c.cita ? `<blockquote class="citaC" style="text-align:left">${esc(c.cita)}</blockquote><p class="tiny muted">${esc(c.fuente || "")}</p>` : ""}` : `<p class="small muted mt">Explícalo en voz alta y luego toca la tarjeta.</p>`}</div>
  ${F.vuelta ? `<div class="row mt"><button class="btn amber" data-a="flashRes" data-ok="0">Repasar otra vez</button><button class="btn" data-a="flashRes" data-ok="1">Lo sabía</button></div>` : `<button class="btn mt" data-a="voltear">Ver respuesta</button>`}`;
}
function modalConcepto(c) {
  const L = c.lectura ? LECT[c.lectura] : null;
  const m = modal(`<h2>${c.id ? "Editar concepto" : "Nuevo concepto"}</h2>
    <label class="lab" for="cT">Concepto</label><input id="cT" class="input" value="${esc(c.termino || "")}" placeholder="Ej.: Ajuste razonable">
    <label class="lab" for="cD">Mi definición (con mis palabras)</label><textarea id="cD" class="input" rows="4" placeholder="Explícalo como se lo dirías a un compañero">${esc(c.def || "")}</textarea>
    ${c.cita ? `<label class="lab">Texto oficial</label><blockquote class="citaC">${esc(c.cita)}</blockquote><p class="tiny muted">${esc(c.fuente || (L ? L.nombre + " · " + L.titulo : ""))}</p>` : ""}
    <button class="btn mt" data-m="ok">Guardar en mi cuaderno</button><button class="btn ghost" data-m="no">Cancelar</button>`);
  setTimeout(() => m.querySelector(c.termino ? "#cD" : "#cT")?.focus(), 250);
  m.querySelector("[data-m=no]").onclick = cerrarModal;
  m.querySelector("[data-m=ok]").onclick = () => {
    const t = m.querySelector("#cT").value.trim(); if (!t) { toast("Escribe el nombre del concepto"); return; }
    const lista = S.estado.cuaderno.conceptos, d = m.querySelector("#cD").value.trim();
    if (c.id) Object.assign(lista.find(x => x.id === c.id), { termino: t, def: d, t: Date.now() });
    else lista.push({ id: uid(), termino: t, def: d, cita: c.cita || "", fuente: c.fuente || "", lectura: c.lectura || null, parrafo: c.parrafo ?? null, t: Date.now() });
    CU.sel = null; guardarLocal(); cerrarModal(); toast("Guardado en tu cuaderno 🧠"); render();
  };
}
function exportarCuaderno() {
  const C = S.estado.cuaderno, plan = S.banco.plan || [];
  let md = `# Mi cuaderno de estudio · Plaza Docente\n\nExportado el ${fechaLarga(hoy())}\n\n## Conceptos\n\n`;
  C.conceptos.slice().sort((a, b) => a.termino.localeCompare(b.termino, "es")).forEach(c => {
    md += `### ${c.termino}\n${c.def || ""}\n${c.cita ? `\n> ${c.cita}\n> — ${c.fuente || ""}\n` : ""}\n`; });
  const notas = plan.filter(l => (C.notas[l.id] || "").trim());
  if (notas.length) { md += `## Notas de lectura\n\n`; notas.forEach(l => md += `### ${l.nombre} · parte ${l.parte}: ${l.titulo}\n${C.notas[l.id].trim()}\n\n`); }
  const blob = new Blob([md], { type: "text/plain;charset=utf-8" }), url = URL.createObjectURL(blob), a = document.createElement("a");
  a.href = url; a.download = `mi-cuaderno-${hoy()}.txt`; a.click(); setTimeout(() => URL.revokeObjectURL(url), 2000);
}
let notaTimer = null;
$app.addEventListener("input", e => {
  const i = e.target.dataset?.i;
  if (i === "nota" && CU.lectura) { S.estado.cuaderno.notas[CU.lectura] = e.target.value; clearTimeout(notaTimer); notaTimer = setTimeout(guardarLocal, 800); }
  else if (i === "buscar") { CU.q = e.target.value; const pos = e.target.selectionStart; render(); const el = document.querySelector("[data-i=buscar]"); el.focus(); el.setSelectionRange(pos, pos); }
});

function vistaBiblioteca() {
  const fs = S.banco.fichas || [];
  return `<div class="top"><button class="icon-btn" data-v="inicio">‹</button><h2>Biblioteca</h2><span style="width:44px"></span></div>
  ${(() => { const pi = planInfo(), sig = lecturaPendiente(), pct = Math.round(pi.leidas / Math.max(1, pi.total) * 100);
    const prox = (S.banco.plan || []).filter(l => !lecturaLeida(l.id)).slice(0, 4);
    const porDoc = {}; (S.banco.plan || []).forEach(l => { const d = porDoc[l.nombre] ||= { n: 0, ok: 0 }; d.n++; if (lecturaLeida(l.id)) d.ok++; });
    return `<div class="card"><div class="row between"><h3>📖 Plan de lectura de los documentos oficiales</h3><b>${pi.leidas}/${pi.total}</b></div>
      <div class="bar mt"><i style="width:${pct}%"></i></div>
      <p class="tiny muted mt">Una lectura corta por día dentro del reto (unos 3 a 4 minutos). Así lees todos los documentos antes de la prueba, empezando por la Guía 30 y las Orientaciones Curriculares.</p>
      ${sig ? `<div class="list mt">${prox.map((l, k) => `<button class="row between ficha-btn" data-a="leerPlan" data-l="${l.id}"><span>${k === 0 ? "▶️" : "📄"} <b>${esc(l.nombre.split(" (")[0])}</b> · ${esc(l.titulo)}</span><span class="muted">›</span></button>`).join("")}</div>
        <p class="tiny muted">¿Te quedó tiempo? Toca la siguiente para adelantar lectura.</p>` : `<p class="small">🎉 ¡Leíste todo el plan!</p>`}
      <details><summary class="small">Avance por documento</summary><table class="t small">${Object.entries(porDoc).map(([n, d]) => `<tr><td>${esc(n)}</td><td style="text-align:right">${d.ok}/${d.n}</td></tr>`).join("")}</table></details></div>
    <h3 class="mt2">📘 Fichas: estudia y responde</h3>`; })()}
  <p class="muted small">Cada ficha explica un tema con palabras sencillas, muestra el texto oficial y luego te pregunta.</p>
  ${S.banco.componentes.map(c => { const lista = fs.filter(f => S.banco.familias[f.familia].componente === c.id); if (!lista.length) return "";
    return `<h3 class="mt2">${c.icono} ${esc(c.nombre)}</h3><div class="card list">${lista.map(f => `<button class="row between ficha-btn" data-a="estudiar" data-f="${f.id}"><span>${fichaLeida(f.id) ? "✅" : "📘"} ${esc(f.titulo)}</span><span class="muted">›</span></button>`).join("")}</div>`; }).join("")}`;
}
function vistaCofre() {
  const c = cofre().sort((a, b) => (a.proxima || "").localeCompare(b.proxima || ""));
  return `<div class="top"><button class="icon-btn" data-v="inicio">‹</button><h2>Cofre de errores</h2><span style="width:44px"></span></div>
  <p class="muted small">Aquí quedan las competencias que fallaste. Vuelven en otro contexto: al día siguiente, luego a los 3 días y después a la semana. Al acertarlas 3 veces seguidas salen del cofre.</p>
  ${c.length ? `<div class="card list">${c.map(x => { const F = S.banco.familias[x.f], comp = IDX.comps[F.componente];
    const est = x.proxima <= hoy() ? `<span class="tag amber">Toca hoy</span>` : `<span class="tag">${fechaLarga(x.proxima)}</span>`;
    return `<div><div class="row between"><b>${comp.icono} ${esc(F.nombre)}</b>${est}</div>
      <div class="row between tiny muted mt"><span>Progreso: ${"●".repeat(Math.min(x.caja, DOMINIO))}${"○".repeat(Math.max(0, DOMINIO - x.caja))} · ${x.fallos} ${x.fallos === 1 ? "fallo" : "fallos"}</span><button class="tag violet" data-a="verLeccion" data-f="${x.f}">Ver lección</button></div></div>`; }).join("")}</div>
    <button class="btn amber mt" data-a="duelo">⚔️ Duelo contra mis errores</button>`
  : `<div class="card center"><div style="font-size:48px">✨</div><p>Tu cofre está vacío.</p></div>`}`;
}
function vistaInsignias() {
  const I = S.estado.perfil.insignias;
  return `<div class="top"><button class="icon-btn" data-v="inicio">‹</button><h2>Insignias</h2><span style="width:44px"></span></div>
  <p class="muted small">${Object.keys(I).length} de ${INSIGNIAS.length} desbloqueadas · Mejor racha: ${S.estado.perfil.mejorRacha} días</p>
  <div class="badge-grid mt">${INSIGNIAS.map(b => `<div class="badge ${I[b.id] ? "on" : ""}"><div class="e">${b.e}</div><b>${esc(b.n)}</b><small>${I[b.id] ? fechaLarga(I[b.id]) : esc(b.d)}</small></div>`).join("")}</div>`;
}
function vistaProgreso() {
  const sims = S.estado.simulacros.slice(-6);
  return `<div class="top"><button class="icon-btn" data-v="inicio">‹</button><h2>Mi progreso</h2><span style="width:44px"></span></div>
  <div class="card"><div class="row between"><span>Preguntas respondidas</span><b>${S.estado.perfil.respondidas}</b></div>
    <div class="row between mt"><span>Banco disponible</span><b>${Object.keys(IDX.items).length} preguntas · ${S.banco.casos.length} casos</b></div>
    <div class="row between mt"><span>Mejor racha</span><b>${S.estado.perfil.mejorRacha} días</b></div></div>
  <div class="card mt"><h3>Precisión por componente</h3>
  ${S.banco.componentes.map(c => { const st = statsComp(c.id), p = st.precision === null ? null : Math.round(st.precision * 100);
    return `<div class="comp-row"><span>${c.icono}</span><div><div class="small"><b>${esc(c.nombre)}</b> <span class="muted">· ${esc(c.prueba)}</span></div><div class="bar ${p !== null && p < 60 ? "amber" : ""}"><i style="width:${p ?? 0}%"></i></div></div><b class="small">${p === null ? "—" : p + "%"}</b></div>`; }).join("")}
  <p class="tiny muted">La barra naranja indica precisión por debajo de 60 %: prioriza ese componente en el mapa.</p></div>
  <div class="card mt"><h3>Simulacros</h3>${sims.length ? sims.map(x => `<div class="row between small mt"><span>${fechaLarga(x.fecha)}</span><b style="color:${x.puntaje >= 60 ? "var(--ok)" : "var(--coral)"}">${x.puntaje.toLocaleString("es-CO",{minimumFractionDigits:2,maximumFractionDigits:2})}</b></div>`).join("") : `<p class="small muted">Aún no has presentado simulacros.</p>`}</div>
  <div class="card mt"><h3>Cómo es la prueba real</h3><p class="small">Proceso de Selección 2026 (Acuerdo 314 de 2026 para Yopal): la <b>Prueba de Aptitudes y Competencias Básicas</b> es eliminatoria (60/100 para docentes, 55 % del puntaje total) e incluye lectura crítica, razonamiento cuantitativo, competencias blandas y conocimientos disciplinares con competencias pedagógicas. La <b>Psicotécnica</b> es clasificatoria (5 %). Las preguntas son casos con un enunciado y tres opciones (formato de juicio situacional).</p></div>`;
}
function vistaAjustes() {
  const P = S.estado.perfil;
  return `<div class="top"><button class="icon-btn" data-v="inicio">‹</button><h2>Ajustes</h2><span style="width:44px"></span></div>
  <div class="card stack"><label class="lab" for="nombre">Nombre</label><input id="nombre" class="input" value="${esc(P.nombre)}">
    <button class="btn sec" data-a="guardarNombre">Guardar nombre</button></div>
  <div class="card mt"><div class="row between"><span>Apariencia</span><div class="row">${[["claro", "☀️ Claro"], ["oscuro", "🌙 Oscuro"], ["auto", "Auto"]].map(([v, n]) => `<button class="chip ${(S.estado.ajustes.tema || "claro") === v ? "xp" : ""}" data-a="tema" data-t="${v}">${n}</button>`).join("")}</div></div>
    <p class="tiny muted">"Auto" sigue el modo claro u oscuro del celular.</p></div>
  <div class="card mt"><div class="row between"><span>Sonidos</span><button class="chip" data-a="sonido">${S.estado.ajustes.sonido ? "🔊 Activados" : "🔇 Desactivados"}</button></div></div>
  <div class="card mt stack"><h3>Respaldo</h3><p class="sync" data-sync>${syncHTML()}</p>
    <button class="btn sec" data-a="syncAhora">☁️ Guardar en la nube ahora</button>
    <button class="btn sec" data-a="exportar">⬇️ Descargar copia de mi avance</button>
    <button class="btn sec" data-a="ics">📅 Recordatorios de simulacros</button></div>
  <div class="card mt stack"><p class="small muted">Banco: ${esc(S.banco.version)} · actualizado ${esc(S.banco.actualizado)} · ${S.banco.lotes || 1} lote(s) · ${Object.keys(IDX.items).length} preguntas · ${(S.banco.fichas || []).length} fichas</p>
    <button class="btn ghost" data-a="salirCuenta">Cerrar sesión en este celular</button></div>`;
}

/* ---------- modales ---------- */
function modal(html) {
  cerrarModal();
  const bg = document.createElement("div"); bg.className = "modal-bg"; bg.innerHTML = `<div class="modal" role="dialog" aria-modal="true">${html}</div>`;
  bg.addEventListener("click", e => { if (e.target === bg) cerrarModal(); });
  document.body.appendChild(bg); document.body.style.overflow = "hidden"; return bg;
}
function cerrarModal() { document.querySelectorAll(".modal-bg").forEach(m => m.remove()); document.body.style.overflow = ""; }
function modalLeccion(fam, onPracticar) {
  const F = S.banco.familias[fam], L = F.leccion, comp = IDX.comps[F.componente];
  const m = modal(`<div class="tag amber">${comp.icono} ${esc(comp.nombre)}</div>
    <h2 class="mt">🛟 ${esc(F.nombre)}</h2><p>${esc(L.idea)}</p>
    <div class="card flat mt"><b>Claves para acertar</b><ul class="small">${L.claves.map(c => `<li>${esc(c)}</li>`).join("")}</ul></div>
    <div class="card flat mt" style="background:var(--coral-soft); border:0"><b>⚠️ La trampa típica</b><p class="small">${esc(L.trampa)}</p></div>
    <p class="src">📚 ${esc(L.fuente)}</p>
    ${onPracticar ? `<button class="btn mt" data-m="practicar">Ponme a prueba con otro caso</button>` : ""}
    <button class="btn ghost" data-m="cerrar">${onPracticar ? "Ahora no" : "Cerrar"}</button>`);
  m.querySelector("[data-m=cerrar]").onclick = cerrarModal;
  if (onPracticar) m.querySelector("[data-m=practicar]").onclick = onPracticar;
}
const DOCS = {
  guia30_mineducacion_2008: "Guía 30 MEN (2008)", orientaciones_tecnologia_2022: "Orientaciones Curriculares Tecnología e Informática (MEN, 2022)",
  decreto_1075_2015: "Decreto 1075 de 2015", decreto_1421_2017: "Decreto 1421 de 2017", decreto_1965_2013: "Decreto 1965 de 2013",
  ley_1620_2013: "Ley 1620 de 2013", ley_115_1994: "Ley 115 de 1994", ley_1098_2006: "Ley 1098 de 2006", decreto_1278_2002: "Decreto 1278 de 2002",
  resolucion_3842_2022_ocr: "Resolución 3842 de 2022 (MEN)", anexo_tecnico_2026: "Anexo Técnico CNSC 2026", acuerdo_314_2026_yopal: "Acuerdo 314 de 2026 (Yopal)",
  guia_orientacion_cnsc_2022: "Guía de orientación al aspirante CNSC 2022"
};
function modalReporte() {
  const s = S.ses, it = IDX.items[s.cola[s.i].id];
  const motivos = ["La respuesta correcta me parece equivocada", "El dato normativo no coincide con la norma", "La pregunta es confusa o tiene dos respuestas", "Error de redacción u ortografía", "Otro"];
  const m = modal(`<h2>🚩 Reportar pregunta ${esc(it.id)}</h2><p class="small muted">Se revisará contra el documento oficial. Si hay error, la pregunta se corrige o se retira del banco.</p>
    <div class="stack mt">${motivos.map((x, k) => `<label class="radio"><input type="radio" name="mot" value="${esc(x)}" ${k === 0 ? "checked" : ""}> ${esc(x)}</label>`).join("")}</div>
    <textarea id="nota" class="input mt" rows="3" placeholder="¿Qué notaste? (opcional)"></textarea>
    <button class="btn mt" data-m="enviar">Enviar reporte</button><button class="btn ghost" data-m="cerrar">Cancelar</button>`);
  m.querySelector("[data-m=cerrar]").onclick = cerrarModal;
  m.querySelector("[data-m=enviar]").onclick = () => {
    const ob = outbox(); ob.reportes.push({ item: it.id, motivo: m.querySelector("input[name=mot]:checked").value, nota: m.querySelector("#nota").value.trim(), lote: S.banco.actualizado, t: new Date().toISOString() });
    setOutbox(ob); cerrarModal(); toast("Gracias. Reporte guardado."); programarSync(200);
  };
}
function modalSinVidas() {
  const s = S.ses, it = IDX.items[s.cola[s.i].id];
  const m = modal(`<div class="center"><div style="font-size:52px">💔</div><h2>Se acabaron los corazones</h2>
    <p>No pasa nada: puedes seguir el reto. Pero una lección de rescate te ayudará a no repetir el error y te devuelve 2 ❤️.</p></div>
    <button class="btn mt" data-m="rescate">🛟 Hacer lección de rescate</button><button class="btn ghost" data-m="seguir">Seguir sin corazones</button>`);
  m.querySelector("[data-m=rescate]").onclick = () => abrirRescate();
  m.querySelector("[data-m=seguir]").onclick = () => { cerrarModal(); siguiente(); };
}
function modalSimulacro() {
  const m = modal(`<h2>⏱️ Simulacro del mes</h2>
    <ul class="small"><li>${CFG.simulacroPreguntas} preguntas en ${CFG.simulacroPreguntas * CFG.minutosPorPregunta} minutos (unos ${CFG.minutosPorPregunta} min por pregunta, ritmo del examen real de 5 horas).</li>
    <li>Sin retroalimentación hasta el final, como el examen.</li><li>Busca un lugar tranquilo, sin celular aparte de esta app, con lápiz y papel para cálculos.</li>
    <li>Al final verás tu puntaje sobre 100 frente al mínimo de 60 y tus errores irán al cofre.</li></ul>
    <button class="btn violet mt" data-m="ok">Comenzar ahora</button><button class="btn ghost" data-m="no">Más tarde</button>`);
  m.querySelector("[data-m=ok]").onclick = () => { cerrarModal(); iniciarSesion("simulacro"); };
  m.querySelector("[data-m=no]").onclick = cerrarModal;
}
function avisoSimulacro() {
  if (!S.clave || !S.estado?.perfil?.nombre || S.vista !== "inicio") return;
  const sim = simulacroInfo(), A = S.estado.ajustes, clave = `${sim.fecha}-${sim.disponible ? 0 : sim.dias}`;
  if (A.avisoSimulacro === clave) return;
  if (sim.disponible || sim.dias === 1 || sim.dias === 7) {
    A.avisoSimulacro = clave; guardarLocal();
    const txt = sim.disponible ? "¡Hoy es tu simulacro del mes! Reserva el tiempo y preséntalo sin interrupciones."
      : sim.dias === 1 ? `Mañana, ${fechaLarga(sim.fecha)}, es tu simulacro. Duerme bien y prepara ${CFG.simulacroPreguntas * CFG.minutosPorPregunta} minutos libres desde las 8:00 a. m.`
      : `En una semana (${fechaLarga(sim.fecha)}) tienes simulacro. Organiza tu sábado desde ya.`;
    const m = modal(`<div class="center"><div style="font-size:52px">🗓️</div><h2>Aviso de simulacro</h2><p>${esc(txt)}</p></div>
      ${sim.disponible ? `<button class="btn violet mt" data-m="ir">Ver simulacro</button>` : `<button class="btn sec mt" data-m="ics">📅 Agregar al calendario</button>`}
      <button class="btn ghost" data-m="cerrar">Entendido</button>`);
    m.querySelector("[data-m=cerrar]").onclick = cerrarModal;
    m.querySelector("[data-m=ics]")?.addEventListener("click", descargarICS);
    m.querySelector("[data-m=ir]")?.addEventListener("click", () => { cerrarModal(); modalSimulacro(); });
  }
}

/* ---------- render y eventos ---------- */
let timerInt = null;
function aplicarTema() {
  const t = S.estado?.ajustes?.tema || "claro";
  const oscuro = t === "oscuro" || (t === "auto" && matchMedia("(prefers-color-scheme: dark)").matches);
  document.documentElement.classList.toggle("oscuro", oscuro);
  document.querySelectorAll('meta[name="theme-color"]').forEach(m => m.content = oscuro ? "#131F24" : "#FFFFFF");
}
function render() {
  clearInterval(timerInt); aplicarTema();
  const v = !S.clave ? vistaLogin() : !S.estado.perfil.nombre ? vistaNombre() : ({
    inicio: vistaInicio, pregunta: vistaPregunta, resumen: vistaResumen, resumenSimulacro: vistaResumenSimulacro,
    cofre: vistaCofre, biblioteca: vistaBiblioteca, cuaderno: vistaCuaderno, docs: vistaDocs, doc: vistaDoc, leer: vistaLeer, conceptos: vistaConceptos, flash: vistaFlash, insignias: vistaInsignias, progreso: vistaProgreso, ajustes: vistaAjustes
  }[S.vista] || vistaInicio)();
  $app.innerHTML = v;
  if (S.vista === "pregunta" && S.ses?.fin) {
    const tick = () => { const el = document.querySelector("[data-timer]"); if (!el) return;
      const ms = S.ses.fin - Date.now(); if (ms <= 0) { clearInterval(timerInt); toast("Se acabó el tiempo"); terminarSesion(); return; }
      const m = Math.floor(ms / 60000), sgs = Math.floor(ms / 1000) % 60; el.textContent = `⏱️ ${m}:${pad(sgs)}`; };
    tick(); timerInt = setInterval(tick, 1000);
  }
}
$app.addEventListener("click", async e => {
  const b = e.target.closest("[data-a],[data-v]"); if (!b) return;
  if (b.dataset.v) { ir(b.dataset.v); return; }
  const a = b.dataset.a;
  if (a === "entrar") {
    const c = document.getElementById("clave").value.trim(); if (!c) return;
    b.disabled = true; b.textContent = "Verificando…";
    try { const h = await sha256(c); const r = await rpc("pd_cargar", { p_clave: h });
      S.clave = h; localStorage.setItem(K.clave, h);
      const local = S.estado; const remoto = r.datos && r.datos.v ? r.datos : null;
      S.estado = remoto && (!local || (remoto.t || 0) >= (local.t || 0)) ? remoto : (local || estadoInicial());
      normalizar(); guardarLocal(); S.sync = { ok: true, msg: "Conectado" }; ir("inicio"); setTimeout(avisoSimulacro, 600);
    } catch (err) { b.disabled = false; b.textContent = "Entrar"; toast(err.message === "clave_invalida" ? "Clave incorrecta" : "Sin conexión. Intenta de nuevo."); }
  }
  else if (a === "guardarNombre") { const n = document.getElementById("nombre").value.trim(); if (!n) return; S.estado.perfil.nombre = n; S.estado.perfil.inicio ||= hoy(); guardarLocal(); toast("Guardado"); ir("inicio"); }
  else if (a === "reto") { b.disabled = true; const L = lecturaPendiente(); if (L) await asegurarLectura(L.id); iniciarSesion("reto"); }
  else if (a === "duelo") iniciarSesion("duelo", { n: 10 });
  else if (a === "modulo") iniciarSesion("modulo", { comp: b.dataset.c, n: 6, sinFicha: true });
  else if (a === "simulacro") modalSimulacro();
  else if (a === "ics") descargarICS();
  else if (a === "sel") { if (S.ses.respondida) return; S.ses.sel = b.dataset.l; render(); }
  else if (a === "responder") responder();
  else if (a === "siguiente") { if (S.ses.tipo !== "simulacro" && S.ses.vidas === 0 && !S.ses.avisoVidas && !S.ses.res[S.ses.res.length - 1].ok) { S.ses.avisoVidas = true; modalSinVidas(); } else siguiente(); }
  else if (a === "rescate") abrirRescate();
  else if (a === "verLeccion") modalLeccion(b.dataset.f, null);
  else if (a === "estudiar") iniciarSesion("estudio", { ficha: b.dataset.f });
  else if (a === "leidoL") { const q = S.ses.cola[S.ses.i]; (S.estado.lecturas ||= {})[q.lectura] = hoy(); guardarLocal(); siguiente(); }
  else if (a === "leerPlan") { b.disabled = true; await asegurarLectura(b.dataset.l); iniciarSesion("lectura", { lectura: b.dataset.l }); }
  else if (a === "leido") { const q = S.ses.cola[S.ses.i]; (S.estado.fichas ||= {})[q.ficha] = hoy(); guardarLocal(); siguiente(); }
  else if (a === "reportar") modalReporte();
  else if (a === "salir") {
    const sim = S.ses?.tipo === "simulacro";
    const m = modal(`<h2>¿Salir ${sim ? "del simulacro" : S.ses?.tipo === "reto" ? "del reto" : "de la práctica"}?</h2><p class="small">${sim ? "Si sales ahora, se calificará lo que alcanzaste a responder." : "Lo que respondiste ya quedó guardado, pero el reto no contará para tu racha."}</p>
      <button class="btn mt" data-m="seguir">Seguir respondiendo</button><button class="btn ghost" data-m="salir">${sim ? "Terminar y calificar" : "Salir"}</button>`);
    m.querySelector("[data-m=seguir]").onclick = cerrarModal;
    m.querySelector("[data-m=salir]").onclick = () => { cerrarModal(); if (sim && S.ses.res.length) terminarSesion(); else { S.ses = null; ir("inicio"); } };
  }
  else if (a === "abrirDoc") { CU.doc = b.dataset.d; ir("doc"); }
  else if (a === "leerParte") { CU.lectura = b.dataset.l; CU.sel = null; CU.doc = (S.banco.plan.find(l => l.id === CU.lectura) || {}).doc; await asegurarLectura(CU.lectura); ir("leer"); }
  else if (a === "volverDoc") { ir("doc"); }
  else if (a === "parr") { const k = +b.dataset.k; CU.sel = CU.sel === k ? null : k; render(); }
  else if (a === "nuevoConcepto") {
    if (b.dataset.k !== undefined && CU.lectura) { const L = LECT[CU.lectura], k = +b.dataset.k;
      modalConcepto({ cita: L.parrafos[k], fuente: `${L.nombre} · parte ${L.parte}: ${L.titulo}`, lectura: L.id, parrafo: k }); }
    else modalConcepto({});
  }
  else if (a === "editConcepto") modalConcepto(conceptos().find(c => c.id === b.dataset.id));
  else if (a === "borrarConcepto") { const c = conceptos().find(x => x.id === b.dataset.id);
    const m = modal(`<h2>¿Borrar «${esc(c.termino)}»?</h2><p class="small muted">Se quitará de tu cuaderno.</p><button class="btn amber mt" data-m="si">Sí, borrar</button><button class="btn ghost" data-m="no">Cancelar</button>`);
    m.querySelector("[data-m=no]").onclick = cerrarModal;
    m.querySelector("[data-m=si]").onclick = () => { S.estado.cuaderno.conceptos = conceptos().filter(x => x.id !== c.id); guardarLocal(); cerrarModal(); render(); }; }
  else if (a === "marcarLeida") { const L = CU.lectura; if (lecturaLeida(L)) delete S.estado.lecturas[L]; else S.estado.lecturas[L] = hoy(); guardarLocal(); render(); }
  else if (a === "flashIni") { if (!conceptos().length) return; CU.flash = { cola: shuffle(conceptos().map(c => c.id)), i: 0, ok: 0, vuelta: false }; ir("flash"); }
  else if (a === "voltear") { if (CU.flash) { CU.flash.vuelta = true; render(); } }
  else if (a === "flashRes") { const F = CU.flash; if (b.dataset.ok === "1") F.ok++; else F.cola.push(F.cola[F.i]); F.i++; F.vuelta = false; if (F.cola.length > 60) F.cola.length = 60; render(); }
  else if (a === "exportarCuaderno") exportarCuaderno();
  else if (a === "tema") { S.estado.ajustes.tema = b.dataset.t; guardarLocal(); render(); }
  else if (a === "sonido") { S.estado.ajustes.sonido = !S.estado.ajustes.sonido; guardarLocal(); render(); }
  else if (a === "syncAhora") { S.sync = { ok: true, msg: "Guardando…" }; pintarSync(); await sincronizar(); toast(S.sync.ok ? "Guardado en la nube" : S.sync.msg); }
  else if (a === "exportar") {
    const blob = new Blob([JSON.stringify(S.estado, null, 1)], { type: "application/json" });
    const url = URL.createObjectURL(blob), l = document.createElement("a"); l.href = url; l.download = `plaza-docente-${hoy()}.json`; l.click(); setTimeout(() => URL.revokeObjectURL(url), 2000);
  }
  else if (a === "salirCuenta") {
    await sincronizar();
    if (!S.sync.ok && !confirm("No se pudo guardar en la nube. Si cierras sesión podrías perder lo más reciente. ¿Cerrar de todas formas?")) return;
    localStorage.removeItem(K.clave); localStorage.removeItem(K.estado); S.clave = null; S.estado = null; render();
  }
});
document.addEventListener("keydown", e => { if (e.key === "Enter" && document.getElementById("clave")) document.querySelector("[data-a=entrar]")?.click(); });

function normalizar() {
  const base = estadoInicial(), E = S.estado;
  for (const k of Object.keys(base)) if (E[k] === undefined) E[k] = base[k];
  E.perfil = { ...base.perfil, ...E.perfil }; E.ajustes = { ...base.ajustes, ...E.ajustes };
  E.cuaderno = { notas: {}, conceptos: [], ...(E.cuaderno || {}) };
  if (!E.perfil.inicio && E.perfil.nombre) E.perfil.inicio = (E.perfil.dias[0] || hoy());
}

/* ---------- arranque ---------- */
(async function init() {
  try {
    S.banco = await cargarBanco(); indexar(S.banco);
    S.clave = localStorage.getItem(K.clave);
    try { S.estado = JSON.parse(localStorage.getItem(K.estado)); } catch { S.estado = null; }
    if (S.clave) {
      if (!S.estado) S.estado = estadoInicial();
      normalizar(); render();
      // trae la versión más reciente de la nube (p. ej., si usó otro dispositivo)
      rpc("pd_cargar", { p_clave: S.clave }).then(r => {
        if (r?.datos?.v && (r.datos.t || 0) > (S.estado.t || 0) && S.vista === "inicio") { S.estado = r.datos; normalizar(); localStorage.setItem(K.estado, JSON.stringify(S.estado)); render(); }
        S.sync = { ok: true, msg: "Sincronizado" }; pintarSync(); if (outbox().intentos.length || outbox().sesiones.length || outbox().reportes.length) programarSync(300);
      }).catch(() => { S.sync = { ok: false, msg: "Sin conexión: tu avance se guarda en el celular" }; pintarSync(); });
      setTimeout(avisoSimulacro, 800);
    } else render();
  } catch (err) { $app.innerHTML = `<div class="card mt2"><h2>Ups</h2><p>${esc(err.message)}</p><button class="btn" onclick="location.reload()">Reintentar</button></div>`; }
  if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
})();
})();
