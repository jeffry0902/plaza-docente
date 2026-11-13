// Recordatorios estilo Duolingo para Plaza Docente.
// Lo llama pg_cron cada 15 minutos (encabezado x-cron-secret) o la app para una notificación de prueba ({clave, prueba:true}).
import { createClient } from "npm:@supabase/supabase-js@2";
import webpush from "npm:web-push@3.6.7";

const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const URL_APP = "https://jeffry0902.github.io/plaza-docente/";
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "content-type, apikey, authorization, x-client-info", "Access-Control-Allow-Methods": "POST, OPTIONS" };

// Franjas (hora de Bogotá): se envía una vez por día y franja si aún no hizo el reto
const FRANJAS = [
  { id: "tarde", desde: 17 * 60 + 30, hasta: 18 * 60 + 30 },
  { id: "noche", desde: 20 * 60, hasta: 21 * 60 },
  { id: "ultima", desde: 21 * 60 + 45, hasta: 22 * 60 + 45 },
];
function bogota() {
  const p = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Bogota", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).formatToParts(new Date());
  const g = (t: string) => p.find(x => x.type === t)!.value;
  return { dia: `${g("year")}-${g("month")}-${g("day")}`, min: +g("hour") * 60 + +g("minute") };
}
function ayer(dia: string) { const d = new Date(dia + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() - 1); return d.toISOString().slice(0, 10); }
const elegir = <T,>(a: T[]) => a[Math.floor(Math.random() * a.length)];

function mensaje(franja: string, nombre: string, racha: number) {
  const n = nombre || "Hola";
  if (franja === "tarde") return racha > 0
    ? elegir([{ t: `🔥 ${racha} ${racha === 1 ? "día" : "días"} de racha`, b: `${n}, tu reto de hoy te espera: lectura corta y 10 preguntas. ¡Sigue sumando!` },
              { t: "📚 Es hora de tu reto diario", b: `${n}, 15 minutos hoy te acercan a la plaza. ¿Lo hacemos?` }])
    : elegir([{ t: "📚 Tu plaza docente se gana de a poquitos", b: `${n}, empieza hoy una racha nueva: solo 15 minutos.` },
              { t: "🌱 Hoy es un buen día para empezar", b: `${n}, una lectura corta y unas preguntas. ¡Tú puedes!` }]);
  if (franja === "noche") return racha > 0
    ? { t: `⚠️ Tu racha de ${racha} ${racha === 1 ? "día" : "días"} está en riesgo`, b: `${n}, todavía estás a tiempo. Haz el reto antes de dormir y mantén el fuego 🔥` }
    : { t: "⏰ Aún no haces el reto de hoy", b: `${n}, 15 minutos y quedas al día. ¡Vamos!` };
  return racha > 0
    ? { t: `🔥 Última oportunidad para tu racha`, b: `${n}, si no lo haces hoy, tu racha de ${racha} ${racha === 1 ? "día" : "días"} vuelve a cero. ¡Un último esfuerzo!` }
    : { t: "🌙 Último recordatorio del día", b: `${n}, aunque sea el reto corto: cada día cuenta para la prueba.` };
}

async function enviar(subs: any[], payload: unknown) {
  let ok = 0;
  for (const s of subs) {
    try { await webpush.sendNotification(s.sub, JSON.stringify(payload), { TTL: 3600, urgency: "high" }); ok++; }
    catch (e: any) {
      if (e?.statusCode === 404 || e?.statusCode === 410) await sb.from("push_subs").update({ activo: false }).eq("id", s.id);
      console.error("push error", e?.statusCode, e?.body);
    }
  }
  return ok;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  const { data: cfg } = await sb.rpc("pd_config_privada");
  webpush.setVapidDetails(URL_APP, cfg.vapid_public, cfg.vapid_private);
  const body = await req.json().catch(() => ({}));

  // Notificación de prueba desde la app
  if (body.prueba && body.clave) {
    const { data: c } = await sb.from("cuentas").select("id, nombre").eq("clave_hash", await sha256(body.clave)).maybeSingle();
    if (!c) return json({ error: "clave_invalida" }, 401);
    const { data: subs } = await sb.from("push_subs").select("id, sub").eq("cuenta_id", c.id).eq("activo", true);
    const n = await enviar(subs || [], { title: "✅ ¡Recordatorios activados!", body: "Así te avisaré cuando no hayas hecho tu reto del día.", url: URL_APP });
    return json({ ok: true, enviados: n });
  }

  if (req.headers.get("x-cron-secret") !== cfg.cron_secret) return json({ error: "no autorizado" }, 401);
  const { dia, min } = bogota();
  const franja = FRANJAS.find(f => min >= f.desde && min < f.hasta);
  if (!franja) return json({ ok: true, nada: "fuera de franja", min });

  const { data: subs } = await sb.from("push_subs").select("id, cuenta_id, sub").eq("activo", true);
  const porCuenta = new Map<string, any[]>();
  (subs || []).forEach(s => porCuenta.set(s.cuenta_id, [...(porCuenta.get(s.cuenta_id) || []), s]));
  let total = 0;
  for (const [cuenta, lista] of porCuenta) {
    const { data: ya } = await sb.from("push_log").select("id").eq("cuenta_id", cuenta).eq("dia", dia).eq("franja", franja.id).maybeSingle();
    if (ya) continue;
    const { data: est } = await sb.from("estado").select("datos").eq("cuenta_id", cuenta).maybeSingle();
    const P = est?.datos?.perfil || {};
    if (P.ultimoDia === dia) continue;                                       // ya hizo el reto hoy
    const racha = P.ultimoDia === ayer(dia) ? (P.racha || 0) : 0;
    const m = mensaje(franja.id, P.nombre || "", racha);
    const n = await enviar(lista, { title: m.t, body: m.b, url: URL_APP, tag: "reto-" + dia });
    await sb.from("push_log").insert({ cuenta_id: cuenta, dia, franja: franja.id, enviados: n });
    total += n;
  }
  return json({ ok: true, franja: franja.id, enviados: total });
});

async function sha256(t: string) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join("");
}
function json(o: unknown, status = 200) { return new Response(JSON.stringify(o), { status, headers: { ...CORS, "Content-Type": "application/json" } }); }
