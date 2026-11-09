#!/usr/bin/env python3
"""Lote 2026-11-08 (produção da noite de 08/11): dias 15/11 e 16/11, Black November.
15/11: feed imagem única "Equipe especializada em câmbio automático" (IMG_6037, câmbio aberto na bancada) ·
       story 11h50 Já passou aqui · Mitsubishi Pajero TR4 · story 17h contagem 12 dias.
16/11: feed reel "Dica do Fernando: mais de 50 mil km?" (reel_dica_50mil_black.py) ·
       story 11h50 Já passou aqui · Hyundai Creta · story 17h contagem 11 dias."""
import sys
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-08/"
o = lambda n: O + n
feed_black(U + "Tudo até Outubro 26/IMG_6037.HEIC", "EQUIPE ESPECIALIZADA", "EM CÂMBIO AUTOMÁTICO",
           "Do diagnóstico à troca completa do óleo na máquina: câmbio automático é a especialidade da Star.",
           o("post_1511_especialista.jpg"), fy=0.5, fx=0.62,
           nota="*Cobrimos ofertas mediante apresentação do orçamento. Consulte as condições.")
story_carro(U + "Câmbio Automático_/Câmbio TR4/IMG_1646.HEIC", "MITSUBISHI PAJERO TR4", o("story_cambio_tr4.jpg"), fy=0.15)
story_black_carro(o("story_cambio_tr4.jpg"), "PAJERO TR4", o("story_1511_1150_tr4.jpg"))
story_black_cond("12 DIAS", "PRA BLACK FRIDAY", "Mas na Star o desconto já está valendo. Manda o modelo do seu carro no WhatsApp.",
                 o("story_1511_1700_contagem.jpg"), foto=U + "Tudo até Outubro 26/IMG_6037.HEIC", fy=0.5)
story_carro(U + "Novembro 26/IMG_6235.HEIC", "HYUNDAI CRETA", o("story_cambio_creta.jpg"), fy=0.12)
story_black_carro(o("story_cambio_creta.jpg"), "HYUNDAI CRETA", o("story_1611_1150_creta.jpg"))
story_black_cond("11 DIAS", "PRA BLACK FRIDAY", "Até 30% de desconto, 10x sem juros e cobrimos ofertas. Chama a Star no WhatsApp.",
                 o("story_1611_1700_contagem.jpg"), foto="/home/claude/staroleo-instagram/2026-10/fontes/cronos/foto_carter_limpo_motul.jpg", fy=0.5)

# Parede STAR ÓLEO aparece no fundo do TR4 -> sem o logo de baixo
from PIL import Image, ImageDraw
for n in ["story_1511_1150_tr4.jpg"]:
    im = Image.open(o(n)); px = im.getpixel((20, 1900))
    ImageDraw.Draw(im).rectangle((300, 1615, 780, 1760), fill=px); im.save(o(n), quality=93)
folha_previa([o(x) for x in ["post_1511_especialista.jpg", "story_1511_1150_tr4.jpg", "story_1511_1700_contagem.jpg",
                             "story_1611_1150_creta.jpg", "story_1611_1700_contagem.jpg"]],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=360)
print("ok")
