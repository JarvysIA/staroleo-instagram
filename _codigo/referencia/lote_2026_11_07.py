#!/usr/bin/env python3
"""Lote 2026-11-07 (produção de 07/11): dia 14/11 inteiro, Black November.
Feed 07h10: carrossel educativo "Troca parcial ou completa?" (6 slides). Story 11h50: Já passou aqui · Citroën C4 Pallas.
Story 17h: contagem 13 dias pra Black Friday."""
import sys
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
T = U + "Tudo até Outubro 26/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-07/"
o = lambda n: O + n
N = 6
capa_black(T + "IMG_2611.HEIC", "TROCA PARCIAL", "OU COMPLETA?", o("tp_01.jpg"), fy=0.55)
slide_black(T + "IMG_5989.HEIC", "PARCIAL", "SÓ ESCOA O QUE SAI",
            "Abre o bujão, sai uma parte do óleo e o resto continua no câmbio, misturado com o novo.", 2, N, o("tp_02.jpg"), fy=0.5, cor_grande=(229, 57, 53))
slide_black(T + "IMG_3232.HEIC", "COMPLETA", "NA MÁQUINA ESPECIALIZADA",
            "A máquina tira o óleo velho do sistema e coloca o óleo novo homologado pelo fabricante.", 3, N, o("tp_03.jpg"), fy=0.75)
slide_black(T + "IMG_2549.HEIC", "FILTRO", "CÁRTER LIMPO",
            "Quando o câmbio tem filtro, o cárter desce: limpeza, filtro novo e junta nova.", 4, N, o("tp_04.jpg"), fy=0.5)
slide_black(T + "IMG_3066.HEIC", "50 MIL KM", "E NUNCA TROCOU?",
            "Tá na hora. Tranco, demora para engatar e patinada são avisos do câmbio.", 5, N, o("tp_05.jpg"), fy=0.5, tam_grande=230)
cta_black("TROCA COMPLETA", "COM DESCONTO.", o("tp_06.jpg"),
          itens=["Máquina especializada", "Óleo homologado pelo fabricante", "Filtro e cárter quando o câmbio tem"],
          foto=T + "IMG_0849.HEIC")
story_carro(U + "Câmbio Automático_/Câmbio C4 Pallas/IMG_0599.HEIC", "CITROËN C4 PALLAS", o("story_cambio_c4.jpg"), fy=0.15)
story_black_carro(o("story_cambio_c4.jpg"), "CITROËN C4 PALLAS", o("story_1411_1150_c4.jpg"))
story_black_cond("13 DIAS", "PRA BLACK FRIDAY", "Mas o desconto da Star já está valendo. Manda o modelo do seu carro no WhatsApp.",
                 o("story_1411_1700_contagem.jpg"), foto=U + "Novembro 26/IMG_6161.HEIC", fy=0.5)
folha_previa([o(f"tp_0{i}.jpg") for i in range(1, 7)] + [o("story_1411_1150_c4.jpg"), o("story_1411_1700_contagem.jpg")],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=360)
print("ok")

# Nota obrigatória do "cobrimos ofertas" no feed
from PIL import Image, ImageDraw
im = Image.open(o("tp_06.jpg")); d = ImageDraw.Draw(im)
ctext(d, FW, 1270, "*Cobrimos ofertas mediante apresentação do orçamento. Consulte as condições.", mrs(26), MUTED)
im.save(o("tp_06.jpg"), quality=93)
