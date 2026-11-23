#!/usr/bin/env python3
"""Trend "It's NO-vember" (New Engen, 20/11/2026) na versão Star, em carrossel (sem gravação):
"É NÃO-VEMBRO." e uma lista de NÃOs, fechando a Black November no último dia (segunda 30/11).
Capa: cena de IA do Fernando no balcão balançando o dedo (2026-11/fontes/trend_nao_sim/nao.jpg, já paga).
Fotos dos slides: parte de cima (sem texto) de stories antigos de outubro (Captur, Fit, F-Pace, filtro, 208).
Fechamento "Aqui na Star a gente resolve." + selo das 3 condições + WhatsApp + nota do cobrimos ofertas.
Endereço sem o bairro (regra de 18/11). Uso: python3 trend_novembro_nao.py"""
import os, sys
REPO = os.path.expanduser("~/staroleo-instagram"); sys.path.insert(0, REPO + "/_codigo")
from black_lib import *
from PIL import Image, ImageDraw
O = REPO + "/2026-11/trends/"; T = "/tmp/trend_naovembro"; os.makedirs(T, exist_ok=True)
W, H = 1080, 1350
END = "Estr. dos Bandeirantes, 841"
L24 = REPO + "/2026-10/lote-2026-10-24/"
NAO_IMG = REPO + "/2026-11/fontes/trend_nao_sim/nao.jpg"
SLIDES = [  # (story antigo, frase do NÃO, apoio)
    (L24 + "story_cambio_captur.jpg", "deixar o óleo do câmbio pra dezembro", "A Black November acaba hoje."),
    (REPO + "/2026-10/lote1/story_cambio_208.jpg", "pagar tudo de uma vez", "Aqui é em até 10x sem juros."),
    (L24 + "story_cambio_fpace.jpg", "pagar mais caro", "Achou mais barato? Traz o orçamento que a gente cobre.*"),
    (L24 + "story_bastidor_filtro.jpg", "troca pela metade", "Troca completa na máquina, com filtro novo e cárter limpo."),
    (L24 + "story_cambio_fit.jpg", "deixar pra amanhã", "Até 30% off em produtos e serviços só até hoje, 30/11."),
]
def rodape(c, n=None):
    logo(c, 140, (W - 140) // 2, H - 88)
def capa():
    c = Image.new("RGB", (W, H), GRAF)
    c.paste(cover(carregar(NAO_IMG), W, 900, fy=0.36), (0, 0))
    c = grad(c, top=0, top_a=0, bot=760, bot_a=255, full=0.3)
    badge(c, 46, tam=0.8); d = ImageDraw.Draw(c)
    y = 860
    ctext(d, W, y, "É NÃO-VEMBRO.", bc(170), GOLD); y += 190
    ctext(d, W, y, "Último dia da Black November", bc(62), WHITE); y += 78
    ctext(d, W, y, "Arrasta pro lado e vê a lista de NÃOs", mrs(36), (225, 226, 228))
    rodape(c); return c
def slide(i, src, frase, apoio):
    c = Image.new("RGB", (W, H), GRAF)
    ph = foto_de_story(src, 1150).crop((0, 140, 1080, 1100)).resize((1080, 960))
    c.paste(ph, (0, 0))
    c = grad(c, top=0, top_a=0, bot=620, bot_a=255, full=0.2)
    d = ImageDraw.Draw(c)
    pill(d, W / 2, 40, f"NÃO-VEMBRO  {i}/5", bc(42), GRAF, GOLD, padx=26, pady=10, center=True)
    y = 780
    ctext(d, W, y, "NÃO", bc(200), GOLD); y += 200
    f = bc(78)
    for ln in quebrar(d, frase.upper(), f, W - 110):
        ctext(d, W, y, ln, f, WHITE); y += 84
    y += 10
    for ln in quebrar(d, apoio, mr(36), W - 140):
        ctext(d, W, y, ln, mr(36), (225, 226, 228)); y += 46
    return c  # parede STAR ÓLEO aparece nas fotos: sem logo por cima
def cta():
    c = Image.new("RGB", (W, H), GRAF)
    l = LOGO.resize((280, round(LOGO.height * 280 / LOGO.width))); c.paste(l, ((W - 280) // 2, 110), l)
    d = ImageDraw.Draw(c); y = 330
    ctext(d, W, y, "PRO SEU CÂMBIO,", bc(110), WHITE); y += 112
    ctext(d, W, y, "SÓ UM SIM.", bc(150), GOLD); y += 175
    y = pill(d, W / 2, y, "ÚLTIMO DIA · SEGUNDA 30/11", bc(50), GRAF, GOLD, padx=30, pady=12, center=True) + 34
    y = selo(c, y, escala=0.9) + 40; d = ImageDraw.Draw(c)
    ctext(d, W, y, "Aqui na Star a gente resolve.", bc(64), WHITE); y += 92
    y = pill(d, W / 2, y, f"WHATSAPP  {WA}", bc(60), GRAF, GOLD, padx=36, pady=16, center=True) + 22
    ctext(d, W, y, END, mr(36), MUTED); y += 54
    ctext(d, W, y, "*Cobrimos ofertas mediante apresentação do orçamento. Consulte as condições.", mrs(24), MUTED)
    return c
if __name__ == "__main__":
    pecas = [capa()] + [slide(i, *s) for i, s in enumerate(SLIDES, 1)] + [cta()]
    arqs = []
    for i, p in enumerate(pecas, 1):
        a = O + f"naovembro_{i:02d}.jpg"; p.save(a, quality=93); arqs.append(a)
    folha_previa(arqs, T + "/previa.jpg")
    print("ok", len(arqs))
