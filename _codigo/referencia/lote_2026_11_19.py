#!/usr/bin/env python3
"""Lote 2026-11-19 (produção da noite de 19/11): story de 26/11 (quinta) 17h00, véspera da Black Friday.
"AMANHÃ" + presente do câmbio. Fundo: foto NOVA de 19/11 (Fotos Star/foto_2026-11-19_12-46-21.jpg, Renault Fluence
no elevador com Mobil CVT e a máquina Motul), recortada só no carrinho com os óleos e na máquina (sem o carro, porque
teve story Renault em 25/11). caixa_slogan copiada do lote de 13/11."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from star_lib import abrir, story_carro
from PIL import Image, ImageDraw

U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
T = U + "Tudo até Outubro 26/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-19/"
o = lambda n: O + n
SLOGAN1 = "ATÉ 30% OFF + R$ 250 EM SERVIÇOS"
SLOGAN2 = "(4 balanceamentos + alinhamento + higienização do ar)"


def caixa_slogan(c, y, W, escala=1.0):
    d = ImageDraw.Draw(c)
    f1 = bc(int(76 * escala))
    while d.textlength(SLOGAN1, font=f1) > W - 150: f1 = bc(f1.size - 2)
    f2 = mrs(int(34 * escala))
    while d.textlength(SLOGAN2, font=f2) > W - 150: f2 = mrs(f2.size - 1)
    h = f1.size + f2.size + int(70 * escala)
    d.rounded_rectangle((50, y, W - 50, y + h), radius=18, fill=PRETO, outline=GOLD, width=5)
    ctext(d, W, y + int(22 * escala), SLOGAN1, f1, GOLD)
    ctext(d, W, y + int(22 * escala) + f1.size + int(14 * escala), SLOGAN2, f2, WHITE)
    return y + h



F = "/mnt/user-data/uploads/Fotos Star/foto_2026-11-19_12-46-21.jpg"
_im = abrir(F); _w, _h = _im.size
bg = _im.crop((int(_w*0.22), int(_h*0.60), int(_w*0.92), _h))
c = Image.blend(cover(bg, SW, SH, fy=0.5), Image.new("RGB", (SW, SH), PRETO), 0.70)
c = grad(c, top=420, top_a=160, bot=900, bot_a=230)
badge(c, 250, tam=0.9); faixa(c, 520, ang=-4, alt=70, txt="BLACK FRIDAY")
d = ImageDraw.Draw(c)
y = 650; ctext(d, SW, y, "É AMANHÃ", bc(230), GOLD); y += 250
ctext(d, SW, y, "SEXTA 27 E SÁBADO 28/11", bc(84), WHITE); y += 118
for ln in quebrar(d, "Quem trocar o óleo do câmbio na Star leva:", mr(44), SW - 170):
    ctext(d, SW, y, ln, mr(44), (225, 226, 228)); y += 62
y = caixa_slogan(c, y + 26, SW, escala=1.05) + 34
d = ImageDraw.Draw(c)
ctext(d, SW, y, "Garante o seu horário no WhatsApp", bcb(50), GOLD); y += 80
logo(c, 170, (SW - 170) // 2, min(y + 10, 1490))
c.save(o("story_2611_1700_amanha_presente.jpg"), quality=93)
folha_previa([o("story_2611_1700_amanha_presente.jpg")], sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=540)
print("ok")
