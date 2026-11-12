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
  items: {}, familias: {}, sesiones: [], simulacros: [], retoHoy: null,
  ajustes: { sonido: true, avisoSimulacro: null }
});
const INTERVALOS = [0, 1, 3, 7, 14, 30]; // días según la caja de repaso
const DOMINIO = 3; // caja desde la cual la familia se considera dominada

function guardarLocal() {
  S.estado.t = Date.now();
  localStorage.setItem(K.estado, JSON.stringify(S.estado));
  programarSync();
}
const outbox = () => { try { return JSON.parse(localStorage.getItem(K.outbox)) || { intentos: [], sesiones: [] }; } catch { return { intentos: [], sesiones: [] }; } };
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
  const items = {}, casos = {}, porFam = {}, porComp = {}, porCaso = {};
  b.casos.forEach(c => casos[c.id] = c);
  b.items.forEach(it => {
    it.comp = b.familias[it.familia].componente;
    items[it.id] = it;
    (porFam[it.familia] ||= []).push(it.id);
    (porComp[it.comp] ||= []).push(it.id);
    (porCaso[it.caso] ||= []).push(it.id);
  });
  const comps = {}; b.componentes.forEach(c => comps[c.id] = c);
  IDX = { items, casos, porFam, porComp, porCaso, comps };
}
async function cargarBanco() {
  try {
    const r = await fetch(CFG.bancoUrl, { cache: "no-cache" });
    const b = await r.json(); localStorage.setItem(K.banco, JSON.stringify(b)); return b;
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

function armarCola(tipo, opts = {}) {
  const n = opts.n || CFG.preguntasPorReto, cola = [], usados = new Set();
  const add = (id, extra = {}) => { if (id && !usados.has(id)) { usados.add(id); cola.push({ id, ...extra }); } };

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
    let pool = Object.keys(IDX.items).filter(id => !usados.has(id) && (!opts.comp || IDX.items[id].comp === opts.comp));
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
  const q = S.ses.cola[S.ses.i]; const it = IDX.items[q.id];
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
      <div class="big">${hecho ? "¡Cumplido! ✓" : "10 preguntas"}</div>
      <div class="small" style="opacity:.92">${hecho ? "Tu racha está a salvo. Puedes seguir practicando." : venc ? `Incluye ${Math.min(venc, CFG.maxRepasoPorReto)} de repaso: misma competencia, otro contexto` : "Unos 10 minutos · casos tipo CNSC"}</div></div>
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

  <h2 class="mt2">Mapa de estudio</h2>
  <p class="small muted">Todos los módulos están abiertos. Toca uno para practicarlo.</p>
  <div class="map">${S.banco.componentes.map(c => { const st = statsComp(c.id);
    return `<button class="node" data-a="modulo" data-c="${c.id}"><div class="ring" style="--p:${st.avance}"><span>${c.icono}</span></div>
      <div class="meta"><b>${esc(c.nombre)}</b><span class="tiny muted">${st.dom}/${st.fams} competencias dominadas · ${st.vistos}/${st.total} preguntas</span></div><span class="muted">›</span></button>`; }).join("")}</div>
  <p class="sync center mt" data-sync>${syncHTML()}</p>`;
}

function vistaPregunta() {
  const s = S.ses, q = s.cola[s.i], it = IDX.items[q.id], caso = IDX.casos[it.caso], comp = IDX.comps[it.comp];
  const sim = s.tipo === "simulacro";
  const prev = s.i > 0 ? IDX.items[s.cola[s.i - 1].id].caso : null;
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
      <div class="just">${just}</div>
      <div class="tip">💡 <b>Clave CNSC:</b> ${esc(it.consejo)}</div>
      <div class="src">📚 ${esc(it.fuente)}</div>
    </div>`;
  }
  const tablaHTML = caso.tabla ? `<table class="t"><tr>${caso.tabla.encabezado.map(h => `<th>${esc(h)}</th>`).join("")}</tr>${caso.tabla.filas.map(f => `<tr>${f.map(c => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</table>` : "";
  return `
  <div class="qhead"><button class="icon-btn" data-a="salir" aria-label="Salir">✕</button>
    <div class="bar"><i style="width:${(s.i / s.cola.length) * 100}%"></i></div>
    <span class="tiny muted">${s.i + 1}/${s.cola.length}</span>${vidas}${reloj}</div>
  ${etiqueta}
  <div class="chips" style="margin-bottom:10px">
    <span class="tag">${esc(comp.prueba.split(" (")[0])}</span>
    <span class="tag amber">${comp.icono} ${esc(comp.oficial)}</span>
    <span class="tag blue">${esc(it.competencia)}</span>
  </div>
  <details class="case" ${abierto ? "open" : ""}><summary><span>📄 Caso: ${esc(caso.titulo)}</span><span class="muted tiny">ver/ocultar</span></summary>
    <div class="txt">${esc(caso.texto)}</div>
    ${caso.lectura ? `<blockquote>${esc(caso.lectura)}</blockquote>` : ""}
    ${caso.codigo ? `<pre>${esc(caso.codigo)}</pre>` : ""}${tablaHTML}
  </details>
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
  const s = S.ses, ok = s.res.filter(r => r.ok).length, tot = s.res.length, p = Math.round(ok / Math.max(1, tot) * 100);
  const msj = pick(p >= 80 ? MENSAJES.alto : p >= 50 ? MENSAJES.medio : MENSAJES.bajo);
  const fallas = s.res.filter(r => !r.ok).map(r => S.banco.familias[IDX.items[r.id].familia].nombre);
  const prep = preparacion();
  return `<div class="center stack" style="padding-top:4vh">
    <div style="font-size:64px" class="pop">${p >= 80 ? "🏆" : p >= 50 ? "💪" : "🌱"}</div>
    <h1>${s.tipo === "duelo" ? "Duelo terminado" : "¡Reto terminado!"}</h1>
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
  <div class="card mt"><div class="row between"><span>Sonidos</span><button class="chip" data-a="sonido">${S.estado.ajustes.sonido ? "🔊 Activados" : "🔇 Desactivados"}</button></div></div>
  <div class="card mt stack"><h3>Respaldo</h3><p class="sync" data-sync>${syncHTML()}</p>
    <button class="btn sec" data-a="syncAhora">☁️ Guardar en la nube ahora</button>
    <button class="btn sec" data-a="exportar">⬇️ Descargar copia de mi avance</button>
    <button class="btn sec" data-a="ics">📅 Recordatorios de simulacros</button></div>
  <div class="card mt stack"><p class="small muted">Banco: ${esc(S.banco.version)} (${esc(S.banco.actualizado)}) · ${Object.keys(IDX.items).length} preguntas</p>
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
function render() {
  clearInterval(timerInt);
  const v = !S.clave ? vistaLogin() : !S.estado.perfil.nombre ? vistaNombre() : ({
    inicio: vistaInicio, pregunta: vistaPregunta, resumen: vistaResumen, resumenSimulacro: vistaResumenSimulacro,
    cofre: vistaCofre, insignias: vistaInsignias, progreso: vistaProgreso, ajustes: vistaAjustes
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
  else if (a === "reto") iniciarSesion("reto");
  else if (a === "duelo") iniciarSesion("duelo", { n: 10 });
  else if (a === "modulo") iniciarSesion("modulo", { comp: b.dataset.c, n: 6 });
  else if (a === "simulacro") modalSimulacro();
  else if (a === "ics") descargarICS();
  else if (a === "sel") { if (S.ses.respondida) return; S.ses.sel = b.dataset.l; render(); }
  else if (a === "responder") responder();
  else if (a === "siguiente") { if (S.ses.tipo !== "simulacro" && S.ses.vidas === 0 && !S.ses.avisoVidas && !S.ses.res[S.ses.res.length - 1].ok) { S.ses.avisoVidas = true; modalSinVidas(); } else siguiente(); }
  else if (a === "rescate") abrirRescate();
  else if (a === "verLeccion") modalLeccion(b.dataset.f, null);
  else if (a === "salir") {
    const sim = S.ses?.tipo === "simulacro";
    const m = modal(`<h2>¿Salir ${sim ? "del simulacro" : "del reto"}?</h2><p class="small">${sim ? "Si sales ahora, se calificará lo que alcanzaste a responder." : "Lo que respondiste ya quedó guardado, pero el reto no contará para tu racha."}</p>
      <button class="btn mt" data-m="seguir">Seguir respondiendo</button><button class="btn ghost" data-m="salir">${sim ? "Terminar y calificar" : "Salir"}</button>`);
    m.querySelector("[data-m=seguir]").onclick = cerrarModal;
    m.querySelector("[data-m=salir]").onclick = () => { cerrarModal(); if (sim && S.ses.res.length) terminarSesion(); else { S.ses = null; ir("inicio"); } };
  }
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
        S.sync = { ok: true, msg: "Sincronizado" }; pintarSync(); if (outbox().intentos.length || outbox().sesiones.length) programarSync(300);
      }).catch(() => { S.sync = { ok: false, msg: "Sin conexión: tu avance se guarda en el celular" }; pintarSync(); });
      setTimeout(avisoSimulacro, 800);
    } else render();
  } catch (err) { $app.innerHTML = `<div class="card mt2"><h2>Ups</h2><p>${esc(err.message)}</p><button class="btn" onclick="location.reload()">Reintentar</button></div>`; }
  if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
})();
})();
