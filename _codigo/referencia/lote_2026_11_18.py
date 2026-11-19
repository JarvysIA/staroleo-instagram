#!/usr/bin/env python3
"""Lote 2026-11-18 (produção da noite de 18/11): stories de 25/11 (quarta), 2 dias pra Black Friday.
11h50 story Black: Já passou aqui · Renault (Tudo até Outubro 26/IMG_1989.HEIC, Sandero/Logan prata no elevador com a
      máquina Höche/Motul e os Mobil, capa de placa da Star; recorte da esquerda tira as letras da parede STAR ÓLEO;
      modelo exato não confirmado -> só a marca).
17h00 story: 2 dias pra Black Friday + presente do câmbio (fundo IMG_2248.HEIC, cárter/filtro velho x novo nas mãos).
caixa_slogan copiada do lote de 13/11."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from star_lib import abrir, story_carro
from PIL import Image, ImageDraw

U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
T = U + "Tudo até Outubro 26/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-18/"
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


# 11h50 story Renault: carro no centro-esquerda, parede STAR ÓLEO no alto à direita -> recorta a esquerda
_im = abrir(T + "IMG_1989.HEIC"); _w, _h = _im.size
_im.crop((0, int(_h * 0.06), int(_w * 0.60), int(_h * 0.86))).save(o("_rn_crop.jpg"), quality=95)
story_carro(o("_rn_crop.jpg"), "RENAULT", o("_rn.jpg"), fy=0.2)
story_black_carro(o("_rn.jpg"), "RENAULT", o("story_2511_1150_renault.jpg"))
for n in ["_rn.jpg", "_rn_crop.jpg"]: os.remove(o(n))

# 17h00 contagem 2 dias + presente
c = Image.blend(cover(abrir(T + "IMG_2248.HEIC"), SW, SH, fy=0.45), Image.new("RGB", (SW, SH), PRETO), 0.74)
c = grad(c, top=420, top_a=160, bot=900, bot_a=230)
badge(c, 250, tam=0.9); faixa(c, 520, ang=-4, alt=70, txt="BLACK FRIDAY")
d = ImageDraw.Draw(c)
y = 640; ctext(d, SW, y, "2 DIAS", bc(280), GOLD); y += 300
ctext(d, SW, y, "PRA BLACK FRIDAY", bc(104), WHITE); y += 130
for ln in quebrar(d, "Sexta 27 e sábado 28/11, quem trocar o óleo do câmbio na Star leva:", mr(44), SW - 170):
    ctext(d, SW, y, ln, mr(44), (225, 226, 228)); y += 62
y = caixa_slogan(c, y + 26, SW, escala=1.05) + 34
d = ImageDraw.Draw(c)
ctext(d, SW, y, "Garante o seu horário no WhatsApp", bcb(50), GOLD); y += 80
logo(c, 170, (SW - 170) // 2, min(y + 10, 1490))
c.save(o("story_2511_1700_contagem_presente.jpg"), quality=93)

folha_previa([o("story_2511_1150_renault.jpg"), o("story_2511_1700_contagem_presente.jpg")],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=480)
print("ok")
