#!/usr/bin/env python3
"""Lote 2026-11-22 (produção da noite de 22/11): domingo 29/11, último fim de semana da Black November (acaba 30/11;
o presente do câmbio já acabou em 28/11: só até 30%, 10x e cobrimos ofertas).
11h50 story Black: Já passou aqui · Peugeot (Tudo até Outubro 26/IMG_2979.HEIC, Peugeot branco (308/408) no elevador com a
      máquina Motul e os Shell, capa de placa da Star; escrito só a marca; sem parede STAR ÓLEO).
17h00 story "SÓ ATÉ AMANHÃ" Black November (fundo Tudo até Outubro 26/IMG_4437.HEIC, tampa do filtro do câmbio nova x velha).
O reel do feed 07h10 está em reel_cafe_com_leite_compass_black.py."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from star_lib import abrir, story_carro

T = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/Tudo até Outubro 26/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-22/"
o = lambda n: O + n

_im = abrir(T + "IMG_2979.HEIC"); _w, _h = _im.size
_im.crop((0, 0, _w, int(_h * 0.80))).save(o("_pg_crop.jpg"), quality=95)
story_carro(o("_pg_crop.jpg"), "PEUGEOT", o("_pg.jpg"), fy=0.15)
story_black_carro(o("_pg.jpg"), "PEUGEOT", o("story_2911_1150_peugeot.jpg"))
for n in ["_pg.jpg", "_pg_crop.jpg"]: os.remove(o(n))

story_black_cond("SÓ ATÉ", "AMANHÃ, SEGUNDA 30/11",
                 "Último fim de semana da Black November na Star. Manda o modelo do seu carro no WhatsApp e garante a condição.",
                 o("story_2911_1700_so_ate_amanha.jpg"), foto=T + "IMG_4437.HEIC", fy=0.4, tam_grande=260)

folha_previa([o("story_2911_1150_peugeot.jpg"), o("story_2911_1700_so_ate_amanha.jpg")],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=480)
print("ok")
