-- Cargo por cuenta (docente_ti | coordinador) y creación de cuentas desde el panel de administración.
-- La clave nueva llega cifrada con sha256 desde el navegador y aquí se vuelve a cifrar, igual que las demás.
alter table public.cuentas add column if not exists cargo text not null default 'docente_ti';
alter table public.cuentas drop constraint if exists cuentas_cargo_chk;
alter table public.cuentas add constraint cuentas_cargo_chk check (cargo in ('docente_ti','coordinador'));

create or replace function public.pd_cargar(p_clave text)
 returns jsonb language plpgsql security definer set search_path to 'public','extensions'
as $function$
declare v uuid; r record;
begin
  v := public._cuenta(p_clave);
  if v is null then raise exception 'clave_invalida'; end if;
  select datos, version, actualizado into r from public.estado where cuenta_id = v;
  return jsonb_build_object(
    'nombre', (select nombre from public.cuentas where id = v),
    'cargo', (select cargo from public.cuentas where id = v),
    'datos', coalesce(r.datos, '{}'::jsonb),
    'version', coalesce(r.version, 0),
    'actualizado', r.actualizado);
end $function$;

create or replace function public.pd_admin(p_clave text)
 returns jsonb language plpgsql stable security definer set search_path to 'public','extensions'
as $function$
declare v uuid; res jsonb;
begin
  v := public._cuenta(p_clave);
  if v is null or not exists (select 1 from public.cuentas where id = v and es_admin) then raise exception 'clave_invalida'; end if;
  select jsonb_agg(x order by x->>'creado') into res from (
    select jsonb_build_object(
      'id', c.id, 'nombre', c.nombre, 'creado', c.creado, 'admin', c.es_admin, 'cargo', c.cargo,
      'estado', coalesce(e.datos, '{}'::jsonb), 'actualizado', e.actualizado,
      'dias', (select coalesce(jsonb_agg(d order by d->>'dia'), '[]') from (
          select jsonb_build_object('dia', (i.creado at time zone 'America/Bogota')::date, 'n', count(*), 'ok', count(*) filter (where i.correcta),
                 'min', round(sum(coalesce(i.ms,0)) / 60000.0, 1)) d
          from public.intentos i where i.cuenta_id = c.id and i.creado > now() - interval '120 days'
          group by (i.creado at time zone 'America/Bogota')::date) t),
      'familias', (select coalesce(jsonb_agg(f), '[]') from (
          select jsonb_build_object('familia', i.familia, 'componente', i.componente, 'n', count(*), 'ok', count(*) filter (where i.correcta),
                 'n7', count(*) filter (where i.creado > now() - interval '7 days'), 'ok7', count(*) filter (where i.correcta and i.creado > now() - interval '7 days')) f
          from public.intentos i where i.cuenta_id = c.id group by i.familia, i.componente) t),
      'sesiones', (select coalesce(jsonb_agg(s order by s->>'creado' desc), '[]') from (
          select jsonb_build_object('tipo', s.tipo, 'total', s.total, 'ok', s.correctas, 'xp', s.xp, 'creado', s.creado) s
          from public.sesiones s where s.cuenta_id = c.id order by s.creado desc limit 60) t),
      'ultimo', (select max(i.creado) from public.intentos i where i.cuenta_id = c.id),
      'reportes', (select coalesce(jsonb_agg(jsonb_build_object('item', r.item_id, 'motivo', r.motivo, 'nota', r.nota, 'estado', r.estado, 'resolucion', r.resolucion, 'creado', r.creado) order by r.creado desc), '[]')
          from public.reportes r where r.cuenta_id = c.id)
    ) x
    from public.cuentas c left join public.estado e on e.cuenta_id = c.id
  ) q;
  return jsonb_build_object('ahora', now(), 'cuentas', coalesce(res, '[]'));
end $function$;

create or replace function public.pd_admin_crear_cuenta(p_clave text, p_nombre text, p_cargo text, p_clave_nueva text)
 returns jsonb language plpgsql security definer set search_path to 'public','extensions'
as $function$
declare v uuid; nuevo uuid; h text;
begin
  v := public._cuenta(p_clave);
  if v is null or not exists (select 1 from public.cuentas where id = v and es_admin) then raise exception 'clave_invalida'; end if;
  if coalesce(trim(p_nombre), '') = '' then raise exception 'nombre_vacio'; end if;
  if p_cargo not in ('docente_ti','coordinador') then raise exception 'cargo_invalido'; end if;
  if p_clave_nueva !~ '^[0-9a-f]{64}$' then raise exception 'clave_mal_formada'; end if;
  h := encode(extensions.digest(p_clave_nueva, 'sha256'), 'hex');
  if exists (select 1 from public.cuentas where clave_hash = h) then raise exception 'clave_en_uso'; end if;
  insert into public.cuentas (clave_hash, nombre, cargo, es_admin) values (h, trim(p_nombre), p_cargo, false) returning id into nuevo;
  return jsonb_build_object('id', nuevo, 'nombre', trim(p_nombre), 'cargo', p_cargo);
end $function$;
revoke all on function public.pd_admin_crear_cuenta(text,text,text,text) from public;
grant execute on function public.pd_admin_crear_cuenta(text,text,text,text) to anon, authenticated;
