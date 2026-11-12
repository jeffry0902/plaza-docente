# Descarga una norma de la Secretaría del Senado y la guarda como texto plano (la ejecuta GitHub Actions).
import sys, re, html, urllib.request
url, salida, encabezado = sys.argv[1], sys.argv[2], sys.argv[3]
raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
for enc in ("utf-8", "latin-1"):
    try: t = raw.decode(enc); break
    except UnicodeDecodeError: pass
t = re.sub(r"(?is)<(script|style).*?</\1>", "", t)
t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h\d>|</tr>|</li>", "\n", t)
t = html.unescape(re.sub(r"<[^>]+>", "", t))
lines = [re.sub(r"\s+", " ", l).strip() for l in t.split("\n")]
lines = [l for l in lines if l]
ini = next(i for i, l in enumerate(lines) if re.match(r"ART[ÍI]CULO 1o?\.", l))
fin = next((i for i, l in enumerate(lines) if i > ini and re.match(r"(?i)el presidente del honorable senado", l)), len(lines))
cuerpo = [l for l in lines[ini:fin] if l != "Notas de Vigencia" and not l.startswith("- Modificado") and not l.startswith("- Numeral") and not l.startswith("- Parágrafo")]
open(salida, "w", encoding="utf-8").write(encabezado + "\n\n" + "\n".join(cuerpo) + "\n")
print(len(cuerpo), "líneas")
