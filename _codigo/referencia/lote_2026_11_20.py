#!/usr/bin/env python3
"""Lote 2026-11-20 (produção da noite de 20/11): sexta 27/11, 1º dia do PRESENTE DO CÂMBIO (Black Friday).
11h50 story Black: Já passou aqui · Jeep Renegade (Novembro 26/IMG_6259.HEIC, Renegade cinza no elevador com a
      máquina Motul, Mobil e Paraflu, capa de placa da Star; liberado a partir de 27/11).
17h00 story "É HOJE" + presente do câmbio (fundo Tudo até Outubro 26/IMG_1829.HEIC, tampa do filtro velha x nova nas mãos).
O reel do feed 07h10 está em reel_e_hoje_black_friday.py. caixa_slogan copiada do lote de 13/11."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from star_lib import abrir, story_carro
from PIL import Image, ImageDraw

U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
T = U + "Tudo até Outubro 26/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-20/"
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


# 11h50 story Renegade (carro centralizado, sem parede STAR ÓLEO na foto)
_im = abrir(U + "Novembro 26/IMG_6259.HEIC"); _w, _h = _im.size
_im.crop((0, 0, _w, int(_h * 0.80))).save(o("_rg_crop.jpg"), quality=95)
story_carro(o("_rg_crop.jpg"), "JEEP RENEGADE", o("_rg.jpg"), fy=0.15)
story_black_carro(o("_rg.jpg"), "JEEP RENEGADE", o("story_2711_1150_renegade.jpg"))
for n in ["_rg.jpg", "_rg_crop.jpg"]: os.remove(o(n))

# 17h00 É HOJE + presente
c = Image.blend(cover(abrir(T + "IMG_1829.HEIC"), SW, SH, fy=0.6), Image.new("RGB", (SW, SH), PRETO), 0.72)
c = grad(c, top=420, top_a=160, bot=900, bot_a=230)
badge(c, 250, tam=0.9); faixa(c, 520, ang=-4, alt=70, txt="BLACK FRIDAY")
d = ImageDraw.Draw(c)
y = 650; ctext(d, SW, y, "É HOJE", bc(250), GOLD); y += 270
ctext(d, SW, y, "HOJE E AMANHÃ (28/11)", bc(84), WHITE); y += 118
for ln in quebrar(d, "Quem trocar o óleo do câmbio na Star leva:", mr(44), SW - 170):
    ctext(d, SW, y, ln, mr(44), (225, 226, 228)); y += 62
y = caixa_slogan(c, y + 26, SW, escala=1.05) + 34
d = ImageDraw.Draw(c)
ctext(d, SW, y, "Garante o seu horário no WhatsApp", bcb(50), GOLD); y += 80
logo(c, 170, (SW - 170) // 2, min(y + 10, 1490))
c.save(o("story_2711_1700_e_hoje_presente.jpg"), quality=93)

folha_previa([o("story_2711_1150_renegade.jpg"), o("story_2711_1700_e_hoje_presente.jpg")],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=480)
print("ok")
