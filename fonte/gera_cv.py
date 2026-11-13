"""
Gera curriculo (PT) e resume (EN) em HTML A4 e imprime em PDF pelo Edge.

O conteudo fica em dados_cv.py; os PDFs saem na raiz do repositorio.
Uso: python fonte/gera_cv.py
"""
import subprocess
from pathlib import Path

AQUI = Path(__file__).parent
DEST = AQUI.parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
@page { size: A4; margin: 14mm 15mm 14mm 15mm; }
* { box-sizing: border-box; }
body { margin: 0; font-family: "Segoe UI", Arial, sans-serif; font-size: 9.6pt; line-height: 1.42; color: #1f2a30; }
header { display: grid; grid-template-columns: 1fr auto; gap: 6mm; align-items: end; border-bottom: 2px solid #0f6e6b; padding-bottom: 4mm; }
h1 { font-size: 22pt; margin: 0; letter-spacing: .01em; color: #0c2e33; font-weight: 700; }
.cargo { font-size: 11.5pt; color: #0f6e6b; font-weight: 600; margin-top: 1mm; }
.contato { text-align: right; font-size: 8.8pt; color: #3d4b51; line-height: 1.55; }
.contato a { color: #3d4b51; text-decoration: none; }
h2 { font-size: 10pt; text-transform: uppercase; letter-spacing: .12em; color: #0f6e6b; margin: 5mm 0 2mm; font-weight: 700; }
p { margin: 0 0 1.6mm; }
.perfil { font-size: 9.8pt; color: #2a363b; }
.comp { display: grid; grid-template-columns: 34mm 1fr; gap: 1.2mm 4mm; }
.comp b { color: #0c2e33; font-weight: 600; }
.job { margin-bottom: 3.2mm; break-inside: avoid; }
.job .topo { display: flex; justify-content: space-between; gap: 4mm; align-items: baseline; }
.job h3 { font-size: 10.4pt; margin: 0; color: #0c2e33; }
.job h3 span { font-weight: 400; color: #3d4b51; }
.job .per { font-size: 8.8pt; color: #5b6a70; white-space: nowrap; }
.job .cli { font-size: 8.8pt; color: #5b6a70; margin: .3mm 0 1mm; }
ul { margin: 0; padding-left: 4.2mm; }
li { margin: 0 0 .8mm; }
.duas { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
a { color: #0f6e6b; }
.proj b { color: #0c2e33; }
table.ant { border-collapse: collapse; width: 100%; font-size: 8.9pt; }
table.ant td { padding: 1mm 2mm 1mm 0; vertical-align: top; border-bottom: 1px solid #e3eaec; }
table.ant td:first-child { white-space: nowrap; color: #5b6a70; width: 20mm; }
table.ant td:nth-child(2) { white-space: nowrap; width: 38mm; }
table.ant b { color: #0c2e33; font-weight: 600; }
"""

from dados_cv import T  # noqa: E402

CERT = ["Scrum Foundation Professional Certificate (SFPC)", "IBM Certified Administrator — Cognos 10 BI",
        "IBM Certified Designer — Cognos 10 BI Reports", "IBM Certified Developer — Cognos 10 BI OLAP Models",
        "IBM Certified Administrator — Cognos TM1 10.1", "IBM Certified Specialist — Cognos TM1 10.1 Data Analysis",
        "IBM Certified Developer — Cognos TM1 10.1"]


def html(t):
    h = t["h"]
    jobs = "".join(
        f'<div class="job"><div class="topo"><h3>{c} <span>· {e}</span></h3><span class="per">{p}</span></div>'
        + (f'<div class="cli">{cli}</div>' if cli else "")
        + "<ul>" + "".join(f"<li>{b}</li>" for b in bs) + "</ul></div>"
        for c, e, p, cli, bs in t["jobs"])
    ant = "".join(f"<tr><td>{p}</td><td><b>{e}</b></td><td>{d}</td></tr>" for p, e, d in t["ant"])
    proj = "".join(f'<p class="proj"><b>{n}</b> · <a href="https://{u}">{u}</a><br>{d}</p>' for n, u, d in t["proj"])
    comp = "".join(f"<b>{a}</b><span>{b}</span>" for a, b in t["comp"])
    return f"""<!doctype html><html lang="{t['lang']}"><head><meta charset="utf-8"><title>Alexandre Manzo</title><style>{CSS}</style></head><body>
<header><div><h1>Alexandre Manzo</h1><div class="cargo">{t['cargo']}</div></div>
<div class="contato">{t['local']}<br><a href="mailto:alexandrermanzo@gmail.com">alexandrermanzo@gmail.com</a><br>
<a href="https://www.linkedin.com/in/alexandremanzo/">linkedin.com/in/alexandremanzo</a><br><a href="https://github.com/alexandremanzo">github.com/alexandremanzo</a></div></header>
<h2>{h[0]}</h2><p class="perfil">{t['perfil']}</p>
<h2>{h[1]}</h2><div class="comp">{comp}</div>
<h2>{h[2]}</h2>{jobs}
<h2>{h[3]}</h2><table class="ant">{ant}</table>
<h2>{h[4]}</h2>{proj}
<div class="duas"><div><h2>{h[5]}</h2>{''.join(f'<p>{f}</p>' for f in t['form'])}</div>
<div><h2>{h[6]}</h2><ul>{''.join(f'<li>{c}</li>' for c in CERT)}</ul></div></div>
</body></html>"""


for k, t in T.items():
    src = AQUI / f"{t['arquivo']}.html"
    src.write_text(html(t), encoding="utf-8")
    pdf = DEST / f"{t['arquivo']}.pdf"
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True)
    print(pdf, pdf.stat().st_size)
