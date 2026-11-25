#!/usr/bin/env python3
"""Lote 2026-11-25 (produção da execução de 25/11): stories de 30/11, 02/12 e 03/12.
30/11 (segunda, ÚLTIMO DIA da Black November; o presente do câmbio já acabou em 28/11):
  11h50 story Black "Já passou aqui · Citroën" (Tudo até Outubro 26/IMG_3690.HEIC, Citroën branco (C4 Cactus) no
        elevador com a máquina Motul e os óleos, capa de placa da Star; escrito só a marca).
  17h00 story Black "ÚLTIMO DIA · HOJE, SEGUNDA 30/11" com as 3 condições (fundo IMG_3422.HEIC, Fiat vermelho no elevador).
02/12 (quarta) 11h50 story "Já passou aqui · Toyota Yaris" (Tudo até Outubro 26/IMG_4254.HEIC, Yaris amarelo).
03/12 (quinta) 11h50 story frase de cliente: Ramone (Fiat Cronos, 23/10) "Indico sim." (palavras reais do vídeo).
"""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from star_lib import abrir, story_carro, story_citacao, folha_previa

T = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/Tudo até Outubro 26/"
R = "/home/claude/staroleo-instagram/"
O = R + "2026-11/lote-2026-11-25/"
os.makedirs(O, exist_ok=True)
o = lambda n: O + n

# 30/11 11h50 Citroën (Black)
_im = abrir(T + "IMG_3690.HEIC"); _w, _h = _im.size
_im.crop((0, 0, _w, int(_h * 0.80))).save(o("_ct_crop.jpg"), quality=95)
story_carro(o("_ct_crop.jpg"), "CITROËN", o("_ct.jpg"), fy=0.15)
story_black_carro(o("_ct.jpg"), "CITROËN", o("story_3011_1150_citroen.jpg"))

# 30/11 17h00 último dia da Black November
story_black_cond("ÚLTIMO DIA", "HOJE, SEGUNDA 30/11",
                 "A Black November da Star acaba hoje. Manda o modelo do seu carro no WhatsApp e garante a condição.",
                 o("story_3011_1700_ultimo_dia.jpg"), foto=T + "IMG_3422.HEIC", fy=0.3, tam_grande=230)

# 02/12 11h50 Toyota Yaris (dezembro, sem Black)
_im = abrir(T + "IMG_4254.HEIC"); _w, _h = _im.size
_im.crop((0, 0, _w, int(_h * 0.80))).save(o("_ty_crop.jpg"), quality=95)
story_carro(o("_ty_crop.jpg"), "TOYOTA YARIS", o("story_0212_1150_yaris.jpg"), fy=0.15)

# 03/12 11h50 frase do Ramone
story_citacao(R + "2026-10/fontes/cronos/foto_cronos_elevador_maquina.jpg", "“INDICO", "SIM.”",
              "Ramone, cliente da Star · Fiat Cronos", "Troca do óleo do câmbio automático",
              o("story_0312_1150_frase_ramone.jpg"), fy=0.2)

for n in ["_ct.jpg", "_ct_crop.jpg", "_ty_crop.jpg"]: os.remove(o(n))
folha_previa([o("story_3011_1150_citroen.jpg"), o("story_3011_1700_ultimo_dia.jpg"),
              o("story_0212_1150_yaris.jpg"), o("story_0312_1150_frase_ramone.jpg")],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=420)
print("ok")
