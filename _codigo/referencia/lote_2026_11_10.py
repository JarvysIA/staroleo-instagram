#!/usr/bin/env python3
"""Lote 2026-11-10 (produção da noite de 10/11): stories de 17, 18 e 19/11, Black November.
17/11: 11h50 Já passou aqui · Subaru (IMG_1836) · 17h contagem 10 dias (fundo IMG_5990, filtro novo x sujo).
18/11: 11h50 Já passou aqui · Chevrolet (Câmbio Chevrolet/IMG_2235, parede STAR ÓLEO: sem logo de baixo) ·
       17h dica rápida "Tranco na troca de marcha?" (fundo IMG_2550, máquina).
19/11: 11h50 Já passou aqui · Toyota Corolla (Novembro 26/IMG_6208) · 17h contagem 8 dias."""
import sys
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from PIL import Image, ImageDraw
U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-10/"
R = "/home/claude/staroleo-instagram/2026-10/fontes/"
import os; os.makedirs(O, exist_ok=True)
o = lambda n: O + n

story_carro(U + "Tudo até Outubro 26/IMG_1836.HEIC", "SUBARU", o("story_cambio_subaru.jpg"), fy=0.15)
story_black_carro(o("story_cambio_subaru.jpg"), "SUBARU", o("story_1711_1150_subaru.jpg"))
story_black_cond("10 DIAS", "PRA BLACK FRIDAY", "Filtro sujo assim não espera a Black. Manda o modelo do seu carro no WhatsApp.",
                 o("story_1711_1700_contagem.jpg"), foto=U + "Tudo até Outubro 26/IMG_5990.HEIC", fy=0.4)

# carro fora do centro e parede STAR ÓLEO no alto à direita: recorta os 66% da esquerda para centrar o carro
from star_lib import abrir
_im = abrir(U + "Câmbio Automático_/Câmbio Chevrolet/IMG_2235.HEIC"); _w, _h = _im.size
_im.crop((0, int(_h * 0.06), int(_w * 0.66), _h)).save(o("_chev_crop.jpg"), quality=95)
story_carro(o("_chev_crop.jpg"), "CHEVROLET", o("story_cambio_chevrolet.jpg"), fy=0.10)
story_black_carro(o("story_cambio_chevrolet.jpg"), "CHEVROLET", o("story_1811_1150_chevrolet.jpg"))
story_black_cond("TRANCO?", "NA TROCA DE MARCHA", "Demora pra engatar e tranco podem ser o óleo do câmbio vencido. Antes de virar conserto, chama a Star.",
                 o("story_1811_1700_dica_tranco.jpg"), foto=U + "Tudo até Outubro 26/IMG_2550.HEIC", fy=0.75, tam_grande=260)

story_carro(U + "Novembro 26/IMG_6208.HEIC", "TOYOTA COROLLA", o("story_cambio_corolla.jpg"), fy=0.12)
story_black_carro(o("story_cambio_corolla.jpg"), "TOYOTA COROLLA", o("story_1911_1150_corolla.jpg"))
story_black_cond("8 DIAS", "PRA BLACK FRIDAY", "Até 30% de desconto, 10x sem juros e cobrimos ofertas. Chama a Star no WhatsApp.",
                 o("story_1911_1700_contagem.jpg"), foto=R + "cronos/foto_filtro_novo_x_velho.jpg", fy=0.5)

# Chevrolet: com o recorte a parede STAR ÓLEO fica quase toda fora do quadro, então o logo de baixo fica
for n in ["story_cambio_subaru.jpg", "story_cambio_chevrolet.jpg", "story_cambio_corolla.jpg", "_chev_crop.jpg"]:
    os.remove(o(n))
folha_previa([o(x) for x in ["story_1711_1150_subaru.jpg", "story_1711_1700_contagem.jpg", "story_1811_1150_chevrolet.jpg",
                             "story_1811_1700_dica_tranco.jpg", "story_1911_1150_corolla.jpg", "story_1911_1700_contagem.jpg"]],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=360)
print("ok")
