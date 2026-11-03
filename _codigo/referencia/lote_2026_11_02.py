#!/usr/bin/env python3
"""Lote 2026-11-02 (stories de 09, 10 e 11/11, Black November). Material novo da pasta 'Novembro 26'."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
N = U + "Novembro 26/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-02/"
o = lambda n: O + n

# Já passou aqui (story antigo -> versão Black)
story_carro(N + "IMG_6199.HEIC", "CHEVROLET SPIN", o("story_cambio_spin.jpg"), fy=0.18)
story_black_carro(o("story_cambio_spin.jpg"), "CHEVROLET SPIN", o("story_0911_1150_spin.jpg"))
story_carro(N + "IMG_6203.HEIC", "MITSUBISHI", o("story_cambio_mitsubishi.jpg"), fy=0.18)
story_black_carro(o("story_cambio_mitsubishi.jpg"), "MITSUBISHI", o("story_1011_1150_mitsubishi.jpg"))
story_carro(U + "Tudo até Outubro 26/IMG_2114.HEIC", "SANDERO STEPWAY", o("story_cambio_stepway.jpg"), fy=0.18)
story_black_carro(o("story_cambio_stepway.jpg"), "SANDERO STEPWAY", o("story_1111_1150_stepway.jpg"))

# Contagem
story_black_cond("18 DIAS", "PRA BLACK FRIDAY", "Mas na Star o desconto já está valendo. Não espera o dia 27.",
                 o("story_0911_1700_contagem.jpg"), foto=N + "IMG_6204.HEIC", fy=0.5)
story_black_cond("16 DIAS", "PRA BLACK FRIDAY", "Manda o modelo do seu carro no WhatsApp e garante o desconto antes.",
                 o("story_1111_1700_contagem.jpg"), foto=N + "IMG_6207.HEIC", fy=0.5)

# Bastidor: filtro velho x novo (foto nítida em cima, texto e selo embaixo)
def story_bastidor(foto, linha1, linha2, corpo, out, fy=0.45):
    c = Image.new("RGB", (SW, SH), PRETO)
    c.paste(cover(carregar(foto), SW, 1250, fy=fy), (0, 0))
    c = grad(c, top=380, top_a=190, bot=980, bot_a=255, full=0.35)
    badge(c, 240, tam=0.9)
    d = ImageDraw.Draw(c); y = 1090
    y = pill(d, SW / 2, y, "BASTIDOR DA STAR", bc(42), GRAF, GOLD, padx=30, pady=12, center=True) + 18
    ctext(d, SW, y, linha1, bc(104), WHITE); y += 106
    ctext(d, SW, y, linha2, bc(104), GOLD); y += 120
    for ln in quebrar(d, corpo, mr(38), SW - 170): ctext(d, SW, y, ln, mr(38), (225, 226, 228)); y += 52
    y = selo(c, y + 24, letra=None)
    logo(c, 150, (SW - 150) // 2, min(y + 20, 1740))
    c.save(out, quality=93); return out

story_bastidor(N + "4a8b2f76-885c-4338-82b6-308d7c15e2ac.JPG", "FILTRO NOVO", "x FILTRO VELHO",
               "Na troca completa do câmbio, o filtro também sai.", o("story_1011_1700_filtro.jpg"), fy=0.55)
folha_previa([o(x) for x in ["story_0911_1150_spin.jpg", "story_0911_1700_contagem.jpg", "story_1011_1150_mitsubishi.jpg",
              "story_1011_1700_filtro.jpg", "story_1111_1150_stepway.jpg", "story_1111_1700_contagem.jpg"]],
             "/tmp/claude-0/-home-claude-staroleo-instagram/ffbe48f7-64a9-511b-bd77-ab5da0aaac23/scratchpad/previa_stories.jpg", larg=360)
print("ok")

# Stepway: a parede STAR ÓLEO aparece na foto -> sem o logo de baixo
from PIL import Image, ImageDraw
im = Image.open(o("story_1111_1150_stepway.jpg")); px = im.getpixel((20, 1900))
ImageDraw.Draw(im).rectangle((300, 1615, 780, 1760), fill=px); im.save(o("story_1111_1150_stepway.jpg"), quality=93)
