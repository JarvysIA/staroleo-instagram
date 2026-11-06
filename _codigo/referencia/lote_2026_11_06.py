#!/usr/bin/env python3
"""Lote 2026-11-06 (produção da noite de 05/11): stories de 12/11 e 13/11, Black November."""
import sys
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-06/"
o = lambda n: O + n
story_carro(U + "Câmbio Automático_/Câmbio BMW X1/IMG_0644.HEIC", "BMW X1", o("story_cambio_x1.jpg"), fy=0.18)
story_black_carro(o("story_cambio_x1.jpg"), "BMW X1", o("story_1211_1150_x1.jpg"))
story_carro(U + "Câmbio Automático_/Câmbio Audi Q3/IMG_0796.HEIC", "AUDI Q3", o("story_cambio_q3.jpg"), fy=0.18)
story_black_carro(o("story_cambio_q3.jpg"), "AUDI Q3", o("story_1311_1150_q3.jpg"))
story_black_cond("15 DIAS", "PRA BLACK FRIDAY", "Na Star a Black já começou. Manda o modelo do seu carro no WhatsApp.",
                 o("story_1211_1700_contagem.jpg"), foto=U + "Novembro 26/IMG_6162.HEIC", fy=0.5)
story_black_cond("R$ 199,90", "PNEUS CRYSTONE NO PIX", "Preço a partir de. Manda a medida do seu pneu no WhatsApp.",
                 o("story_1311_1700_pneus.jpg"), foto=U + "Pneus Crystone/IMG_0294.HEIC", fy=0.45, conds=PNEU, tam_grande=230)
folha_previa([o(x) for x in ["story_1211_1150_x1.jpg", "story_1211_1700_contagem.jpg", "story_1311_1150_q3.jpg", "story_1311_1700_pneus.jpg"]],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=360)
print("ok")

# X1 e Q3: a parede STAR ÓLEO aparece no fundo -> sem o logo de baixo (igual ao Stepway)
from PIL import Image, ImageDraw
for n in ["story_1211_1150_x1.jpg", "story_1311_1150_q3.jpg"]:
    im = Image.open(o(n)); px = im.getpixel((20, 1900))
    ImageDraw.Draw(im).rectangle((300, 1615, 780, 1760), fill=px); im.save(o(n), quality=93)
