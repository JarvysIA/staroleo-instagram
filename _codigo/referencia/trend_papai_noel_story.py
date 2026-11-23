#!/usr/bin/env python3
"""Trend "Dear Santa, I'm a size..." (Later e New Engen, 20/11/2026) na versão Star, em story (sem gravação):
"Querido Papai Noel, eu sou tamanho…" e, escrito na carta: "…TROCA COMPLETA DO ÓLEO DO CÂMBIO".
Cena de IA: foto do Fernando no balcão (2026-10/fontes/fernando_balcao.jpg) editada com gemini-3.1-flash-image
9:16 2K (gorro de Papai Noel + carta em branco nas mãos), 918 créditos, flow FRYhgoJ6vqYIMRL6Lsu9;
arquivo em 2026-11/fontes/trend_papai_noel/carta.jpg (reaproveitável em dezembro).
Story 1080x1920 com os 250 px de cima e os 340 px de baixo livres. Só 10x sem juros (condição confirmada).
Uso: python3 trend_papai_noel_story.py"""
import os, sys
REPO = os.path.expanduser("~/staroleo-instagram"); sys.path.insert(0, REPO + "/_codigo")
from star_lib import *
from PIL import Image, ImageDraw
SRC = REPO + "/2026-11/fontes/trend_papai_noel/carta.jpg"
OUT = REPO + "/2026-11/trends/story_trend_papai_noel.jpg"
SW, SH = 1080, 1920
INK = (28, 30, 34)

def main():
    im = Image.open(SRC).convert("RGB")
    k = SW / im.width; im = im.resize((SW, round(im.height * k)), Image.LANCZOS)
    top = (im.height - SH) // 2; im = im.crop((0, top, SW, top + SH))
    c = grad(im, top=520, top_a=235, bot=560, bot_a=245, full=0.45)
    ov = Image.new("RGBA", (SW, SH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle((90, 252, SW - 90, 478), radius=26, fill=(17, 18, 20, 215))
    od.rounded_rectangle((120, 1410, SW - 120, 1468), radius=16, fill=(17, 18, 20, 190))
    c = Image.alpha_composite(c.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(c)
    # topo (abaixo dos 250 px livres)
    y = 270
    ctext(d, SW, y, "Querido Papai Noel,", bc(92), WHITE); y += 104
    ctext(d, SW, y, "eu sou tamanho…", bc(92), GOLD)
    # escrito na carta (papel em ~x 373..726, y 905..1380)
    px0, px1, py0 = 383, 716, 950
    fx = bc(58); yy = py0
    for ln in ["TROCA", "COMPLETA", "DO ÓLEO", "DO CÂMBIO"]:
        f = fx
        while d.textlength(ln, font=f) > (px1 - px0 - 20): f = bc(f.size - 2)
        w = d.textlength(ln, font=f); d.text(((px0 + px1) / 2 - w / 2, yy), ln, font=f, fill=INK); yy += f.size + 6
    yy += 14
    for ln in ["com filtro novo", "e cárter limpo"]:
        f = mrs(30); w = d.textlength(ln, font=f)
        d.text(((px0 + px1) / 2 - w / 2, yy), ln, font=f, fill=(150, 110, 10)); yy += 40
    # embaixo (acaba antes dos 340 px livres: y < 1580)
    y = 1418
    ctext(d, SW, y, "Aqui na Star a gente resolve. Em até 10x sem juros.", mrs(32), WHITE); y += 52
    pill(d, SW / 2, y, f"WHATSAPP  {WA}", bc(58), GRAF, GOLD, padx=34, pady=14, center=True)
    c.save(OUT, quality=93)
    print("ok", OUT)

if __name__ == "__main__":
    main()
