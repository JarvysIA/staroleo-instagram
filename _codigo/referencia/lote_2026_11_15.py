#!/usr/bin/env python3
"""Lote 2026-11-15 (produção da noite de 15/11): dia 22/11 (domingo), 5 dias pra Black Friday.
07h10 feed: reel "Dica do Fernando: nacionais e importados" (IMG_0881, script reel_dica_mercedes_black.py).
11h50 story Black: Já passou aqui · Hyundai HB20 (Tudo até Outubro 26/IMG_1935; recorte da esquerda tira a parede STAR ÓLEO).
17h00 story: 5 dias pra Black Friday + presente do câmbio (fundo 0fc3c6aa...JPG, filtro velho x novo na mão).
caixa_slogan copiada do lote de 13/11."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from star_lib import abrir, story_carro
from PIL import Image, ImageDraw

U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
T = U + "Tudo até Outubro 26/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-15/"
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


# 11h50 story HB20: carro à esquerda, parede STAR ÓLEO no alto à direita -> recorta a esquerda
_im = abrir(T + "IMG_1935.HEIC"); _w, _h = _im.size
_im.crop((0, int(_h * 0.03), int(_w * 0.60), _h)).save(o("_hb20_crop.jpg"), quality=95)
story_carro(o("_hb20_crop.jpg"), "HYUNDAI HB20", o("_hb20.jpg"), fy=0.12)
story_black_carro(o("_hb20.jpg"), "HYUNDAI HB20", o("story_2211_1150_hb20.jpg"))
for n in ["_hb20.jpg", "_hb20_crop.jpg"]: os.remove(o(n))

# 17h00 contagem 5 dias + presente
c = Image.blend(cover(carregar(T + "0fc3c6aa-0d74-44c7-9765-57acfc3a893b.JPG"), SW, SH, fy=0.3), Image.new("RGB", (SW, SH), PRETO), 0.74)
c = grad(c, top=420, top_a=160, bot=900, bot_a=230)
badge(c, 250, tam=0.9); faixa(c, 520, ang=-4, alt=70, txt="BLACK FRIDAY")
d = ImageDraw.Draw(c)
y = 640; ctext(d, SW, y, "5 DIAS", bc(280), GOLD); y += 300
ctext(d, SW, y, "PRA BLACK FRIDAY", bc(104), WHITE); y += 130
for ln in quebrar(d, "Sexta 27 e sábado 28/11, quem trocar o óleo do câmbio na Star leva:", mr(44), SW - 170):
    ctext(d, SW, y, ln, mr(44), (225, 226, 228)); y += 62
y = caixa_slogan(c, y + 26, SW, escala=1.05) + 34
d = ImageDraw.Draw(c)
ctext(d, SW, y, "Garante o seu horário no WhatsApp", bcb(50), GOLD); y += 80
logo(c, 170, (SW - 170) // 2, min(y + 10, 1490))
c.save(o("story_2211_1700_contagem_presente.jpg"), quality=93)

folha_previa([o("story_2211_1150_hb20.jpg"), o("story_2211_1700_contagem_presente.jpg")],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=480)
print("ok")
