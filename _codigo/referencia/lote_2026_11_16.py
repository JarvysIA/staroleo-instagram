#!/usr/bin/env python3
"""Lote 2026-11-16 (produção da noite de 16/11): stories de 23/11 (segunda), 4 dias pra Black Friday.
11h50 story Black: Já passou aqui · Ford EcoSport (Tudo até Outubro 26/4aec0096...JPG; recorte da esquerda tira a parede STAR ÓLEO).
17h00 story: 4 dias pra Black Friday + presente do câmbio (fundo 12fb0de7...jpg, filtro velho x novo nas mãos).
caixa_slogan copiada do lote de 13/11."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from star_lib import abrir, story_carro
from PIL import Image, ImageDraw

U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
T = U + "Tudo até Outubro 26/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-16/"
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


# 11h50 story EcoSport: carro no centro-esquerda, parede STAR ÓLEO à direita -> recorta a esquerda
_im = abrir(T + "4aec0096-e1b0-445c-8c0f-926cb994eb01.JPG"); _w, _h = _im.size
_im.crop((0, int(_h * 0.06), int(_w * 0.60), _h)).save(o("_eco_crop.jpg"), quality=95)
story_carro(o("_eco_crop.jpg"), "FORD ECOSPORT", o("_eco.jpg"), fy=0.15)
story_black_carro(o("_eco.jpg"), "FORD ECOSPORT", o("story_2311_1150_ecosport.jpg"))
for n in ["_eco.jpg", "_eco_crop.jpg"]: os.remove(o(n))

# 17h00 contagem 4 dias + presente
c = Image.blend(cover(carregar(T + "12fb0de7-4c9c-435b-bc28-2d48c113370c.jpg"), SW, SH, fy=0.45), Image.new("RGB", (SW, SH), PRETO), 0.74)
c = grad(c, top=420, top_a=160, bot=900, bot_a=230)
badge(c, 250, tam=0.9); faixa(c, 520, ang=-4, alt=70, txt="BLACK FRIDAY")
d = ImageDraw.Draw(c)
y = 640; ctext(d, SW, y, "4 DIAS", bc(280), GOLD); y += 300
ctext(d, SW, y, "PRA BLACK FRIDAY", bc(104), WHITE); y += 130
for ln in quebrar(d, "Sexta 27 e sábado 28/11, quem trocar o óleo do câmbio na Star leva:", mr(44), SW - 170):
    ctext(d, SW, y, ln, mr(44), (225, 226, 228)); y += 62
y = caixa_slogan(c, y + 26, SW, escala=1.05) + 34
d = ImageDraw.Draw(c)
ctext(d, SW, y, "Garante o seu horário no WhatsApp", bcb(50), GOLD); y += 80
logo(c, 170, (SW - 170) // 2, min(y + 10, 1490))
c.save(o("story_2311_1700_contagem_presente.jpg"), quality=93)

folha_previa([o("story_2311_1150_ecosport.jpg"), o("story_2311_1700_contagem_presente.jpg")],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=480)
print("ok")
