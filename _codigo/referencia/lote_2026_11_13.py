#!/usr/bin/env python3
"""Lote 2026-11-13 (produção da noite de 13/11): dia 20/11 (sexta, feriado da Consciência Negra; nada dizendo que abre).
Começa a divulgação do PRESENTE DO CÂMBIO da Black Friday (27 e 28/11), com o slogan oficial em 2 linhas.
07h10 feed: teaser "Dia 27 tem presente" com o Fernando na prateleira de óleos (Tudo até Outubro 26/IMG_5950).
11h50 story Black: Já passou aqui · Honda Civic (Tudo até Outubro 26/IMG_3251, capa de placa da Star).
17h00 story: 7 dias pra Black Friday + presente do câmbio (fundo IMG_2654, cárter limpo)."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from PIL import Image, ImageDraw

U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/Tudo até Outubro 26/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-13/"
os.makedirs(O, exist_ok=True)
o = lambda n: O + n
SLOGAN1 = "ATÉ 30% OFF + R$ 250 EM SERVIÇOS"
SLOGAN2 = "(4 balanceamentos + alinhamento + higienização do ar)"


def caixa_slogan(c, y, W, escala=1.0):
    """Caixa preta com borda dourada e o slogan oficial em 2 linhas. Retorna o y de baixo."""
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


# ---------- 07h10 feed teaser ----------
base = cover(carregar(U + "IMG_5950.HEIC"), FW, FH, fy=0.22, fx=0.5)
c = grad(base, top=300, top_a=210, bot=620, bot_a=252, full=0.35)
d = ImageDraw.Draw(c)
y = 54
y = pill(d, FW / 2, y, "BLACK FRIDAY · 27 E 28/11", bc(54), GRAF, GOLD, padx=34, pady=14, center=True)
y = 790
ctext(d, FW, y, "DIA 27 TEM PRESENTE", bc(118), WHITE); y += 122
ctext(d, FW, y, "PRA QUEM TROCAR O ÓLEO DO CÂMBIO", bc(62), GOLD); y += 88
y = caixa_slogan(c, y, FW) + 26
d = ImageDraw.Draw(c)
ctext(d, FW, y, "Só 27 e 28/11 · só na troca do óleo do câmbio · já agenda no WhatsApp", mr(30), (225, 226, 228))
logo(c, 140, (FW - 140) // 2, FH - 112)
c.save(o("post_2011_presente_cambio.jpg"), quality=93)

# ---------- 11h50 story Já passou aqui · Honda Civic ----------
story_carro(U + "IMG_3251.HEIC", "HONDA CIVIC", o("_civic.jpg"), fy=0.10)
story_black_carro(o("_civic.jpg"), "HONDA CIVIC", o("story_2011_1150_civic.jpg"))
os.remove(o("_civic.jpg"))

# ---------- 17h00 story contagem + presente ----------
c = Image.blend(cover(carregar(U + "IMG_2654.HEIC"), SW, SH, fy=0.5), Image.new("RGB", (SW, SH), PRETO), 0.74)
c = grad(c, top=420, top_a=160, bot=900, bot_a=230)
badge(c, 250, tam=0.9); faixa(c, 520, ang=-4, alt=70, txt="BLACK FRIDAY")
d = ImageDraw.Draw(c)
y = 640; ctext(d, SW, y, "7 DIAS", bc(280), GOLD); y += 300
ctext(d, SW, y, "PRA BLACK FRIDAY", bc(104), WHITE); y += 130
for ln in quebrar(d, "Dias 27 e 28/11, quem trocar o óleo do câmbio na Star leva:", mr(44), SW - 170):
    ctext(d, SW, y, ln, mr(44), (225, 226, 228)); y += 62
y = caixa_slogan(c, y + 26, SW, escala=1.05) + 34
d = ImageDraw.Draw(c)
ctext(d, SW, y, "Já agenda o seu horário no WhatsApp", bcb(50), GOLD); y += 80
logo(c, 170, (SW - 170) // 2, min(y + 10, 1490))
c.save(o("story_2011_1700_contagem_presente.jpg"), quality=93)

folha_previa([o(x) for x in ["post_2011_presente_cambio.jpg", "story_2011_1150_civic.jpg", "story_2011_1700_contagem_presente.jpg"]],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=420)
print("ok")
