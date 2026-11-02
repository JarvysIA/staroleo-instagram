#!/usr/bin/env python3
"""Trend 'How to avoid stress' (meme, Your Social Team, out/2026) na versão Star + Black November.
Post único 1080x1350, sem gravação, 0 crédito: 'Como evitar o estresse na viagem de fim de ano:' + foto da Renegade
no elevador com a máquina + legenda de meme 'trocar o óleo do câmbio antes de pegar a estrada' + selo da Black."""
import os, sys
REPO = os.path.expanduser("~/staroleo-instagram"); sys.path.insert(0, REPO + "/_codigo")
from black_lib import *
from PIL import Image, ImageDraw
OUT = REPO + "/2026-11/trends/post_trend_evitar_estresse.jpg"
FOTO = REPO + "/2026-10/fontes/renegade/foto_renegade_maquina.jpg"

c = Image.new("RGB", (FW, FH), GRAF); d = ImageDraw.Draw(c)
badge(c, 40, tam=0.62); d = ImageDraw.Draw(c)
ctext(d, FW, 128, "COMO EVITAR O ESTRESSE", bc(104), WHITE)
ctext(d, FW, 236, "NA VIAGEM DE FIM DE ANO:", bc(84), GOLD)
# foto em moldura (meme)
PX0, PY0, PX1, PY1 = 40, 345, FW - 40, 1150
ft = cover(carregar(FOTO), PX1 - PX0, PY1 - PY0, fy=0.62, fx=0.5)
ft = grad(ft, bot=300, bot_a=235, full=0.9)
c.paste(ft, (PX0, PY0)); d = ImageDraw.Draw(c)
d.rounded_rectangle((PX0 - 4, PY0 - 4, PX1 + 4, PY1 + 4), radius=10, outline=GOLD, width=5)
def meme(y, t, f):
    w = d.textlength(t, font=f)
    d.text(((FW - w) / 2, y), t, font=f, fill=WHITE, stroke_width=7, stroke_fill=GRAF)
meme(PY1 - 205, "TROCAR O ÓLEO DO CÂMBIO", bc(92))
meme(PY1 - 110, "ANTES DE PEGAR A ESTRADA", bc(76))
pill(d, PX0 + 24, PY0 + 24, "A SOLUÇÃO:", bc(44), GRAF, GOLD, padx=22, pady=10)
y = selo(c, 1172, letra=None, escala=0.82)
ctext(ImageDraw.Draw(c), FW, y + 12, "*Cobrimos ofertas mediante apresentação do orçamento. Consulte as condições.", mrs(24), MUTED)
c.save(OUT, quality=93); print(OUT)
