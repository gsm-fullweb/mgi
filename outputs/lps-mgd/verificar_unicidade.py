#!/usr/bin/env python3
"""Checa duplicidade e canibalização entre as LPs HTML antes de publicar.

Uso: python3 verificar_unicidade.py <pasta-com-html> [--max-sim 0.30] [--min-palavras 600]
Cada arquivo deve se chamar <slug>.html. Sai com código 1 se houver falha.
"""
import argparse, collections, glob, itertools, os, re, sys
from html import unescape

def texto(html):
    html = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", html)
    return unescape(re.sub(r"(?s)<[^>]+>", " ", html))

def pega(rx, html):
    m = re.search(rx, html, re.I | re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""

def shingles(t, n=5):
    w = re.findall(r"\w+", t.lower())
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}

ap = argparse.ArgumentParser()
ap.add_argument("pasta")
ap.add_argument("--max-sim", type=float, default=0.30)
ap.add_argument("--min-palavras", type=int, default=600)
a = ap.parse_args()

pags = {}
for f in sorted(glob.glob(os.path.join(a.pasta, "*.html"))):
    slug = os.path.basename(f)[:-5]
    h = open(f, encoding="utf-8").read()
    body = pega(r"<body[^>]*>(.*)</body>", h) or h
    pags[slug] = dict(
        title=pega(r"<title>(.*?)</title>", h),
        h1=pega(r"<h1[^>]*>(.*?)</h1>", re.sub(r"(?s)<[^>]+>(?=[^<]*</h1>)", "", h)) or pega(r"<h1[^>]*>(.*?)</h1>", h),
        desc=pega(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', h),
        canon=pega(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', h),
        faq=re.findall(r'"name"\s*:\s*"([^"]+\?)"', h),
        txt=texto(h), sh=None)
    pags[slug]["sh"] = shingles(pags[slug]["txt"])

erros = []
for campo in ("title", "h1", "desc"):
    c = collections.defaultdict(list)
    for s, p in pags.items():
        c[p[campo].lower()].append(s)
    for v, ss in c.items():
        if len(ss) > 1 or not v:
            erros.append(f"{campo.upper()} {'vazio' if not v else 'duplicado'}: {', '.join(ss)}")
for s, p in pags.items():
    if not re.search(rf"/{re.escape(s)}/?$", p["canon"]):
        erros.append(f"CANONICAL não aponta para si mesma em {s}: '{p['canon']}'")
    n = len(re.findall(r"\w+", p["txt"]))
    if n < a.min_palavras:
        erros.append(f"CONTEÚDO FINO em {s}: {n} palavras (mín. {a.min_palavras})")
    if len(p["title"]) > 60:
        erros.append(f"TITLE longo em {s}: {len(p['title'])} caracteres")
# perguntas de FAQ repetidas em mais de 2 páginas = texto de molde
q = collections.defaultdict(list)
for s, p in pags.items():
    for x in p["faq"]:
        q[x.lower()].append(s)
for x, ss in q.items():
    if len(ss) > 2:
        erros.append(f"FAQ repetida em {len(ss)} páginas: '{x}'")
# similaridade de texto (shingles de 5 palavras)
pares = []
for (s1, p1), (s2, p2) in itertools.combinations(pags.items(), 2):
    u = len(p1["sh"] | p2["sh"])
    j = len(p1["sh"] & p2["sh"]) / u if u else 0
    if j > a.max_sim:
        pares.append((j, s1, s2))
for j, s1, s2 in sorted(pares, reverse=True):
    erros.append(f"DUPLICIDADE {j:.0%} entre {s1} e {s2} (limite {a.max_sim:.0%})")

print(f"{len(pags)} páginas analisadas, {len(erros)} problemas")
for e in erros:
    print(" -", e)
sys.exit(1 if erros else 0)
