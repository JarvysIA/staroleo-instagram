#!/usr/bin/env python3
"""Black November da Star: peças da semana 1 (01 a 07/11/2026)."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
R = "/home/claude/staroleo-instagram/2026-10/"
F = R + "fontes/"
OUT = "/home/claude/staroleo-instagram/2026-11/black-semana1/"; os.makedirs(OUT, exist_ok=True)
o = lambda n: OUT + n
car = lambda n: [p for p in __import__("glob").glob(R + f"*/story_cambio_{n}.jpg")][0]
NOTA_COBRE = "*Mediante apresentação do orçamento. Consulte as condições."

# ---- 01/11 carrossel de lançamento ----
capa_black(F + "renegade/foto_renegade_maquina.jpg", "O MÊS INTEIRO", "EM OFERTA NA STAR", o("lanc_01.jpg"), fy=0.25)
slide_black(F + "cronos/foto_cronos_elevador_maquina.jpg", "ATÉ 30%", "DE DESCONTO",
            "Em produtos e serviços. O desconto de cada item sai no orçamento pelo WhatsApp.", 2, 5, o("lanc_02.jpg"))
slide_black(F + "fernando_balcao.jpg", "10X", "SEM JUROS", "Em todos os produtos e serviços da Star.", 3, 5, o("lanc_03.jpg"), fy=0.2)
slide_black(F + "cronos/foto_carter_limpo_motul.jpg", "COBRIMOS", "OFERTAS",
            "Achou mais barato em outro lugar? Traz o orçamento e fala com a gente.", 4, 5, o("lanc_04.jpg"), tam_grande=200)
cta_black("APROVEITA", "O MÊS INTEIRO", o("lanc_05.jpg"), itens=["Troca do óleo do câmbio automático",
          "Troca de óleo do motor e filtros", "Pneus e suspensão", "Radiador e arrefecimento"])

# ---- feed 02 a 05/11 ----
feed_black(F + "cronos/foto_cronos_elevador_maquina.jpg", "VOLTOU DA ESTRADA?", "PASSA NA STAR.",
           "Depois do feriadão, confere óleo, câmbio, pneus e arrefecimento com desconto de Black.", o("feed_0211_estrada.jpg"), fy=0.35)
feed_black(F + "renegade/foto_renegade_maquina.jpg", "ÓLEO DO CÂMBIO", "COM ATÉ 30% OFF",
           "Troca completa com máquina especializada e óleo homologado pelo fabricante.", o("feed_0311_cambio.jpg"), fy=0.55)
pn = Image.new("RGB", (FW, FH), PRETO); pn.paste(Image.open(R + "lote-2026-10-24/story_pneus_crystone.jpg").convert("RGB").crop((0, 60, 1080, 1150)), (0, 0))
feed_black(None, "PNEUS CRYSTONE", "A PARTIR DE R$ 199,90", "No pix. Consulte a medida do seu carro no WhatsApp.",
           o("feed_0411_pneus.jpg"), foto_img=pn, conds=PNEU)
feed_black(F + "fernando_balcao.jpg", "ACHOU MAIS BARATO?", "TRAZ O ORÇAMENTO.",
           "Na Black November a Star cobre a oferta. Manda o orçamento no WhatsApp.", o("feed_0511_cobrimos.jpg"), fy=0.18, nota=NOTA_COBRE)

# ---- 07/11 carrossel "já passaram aqui" ----
def foto_carro_feed(n):
    im = Image.open(car(n)).convert("RGB").crop((0, 0, 1080, 1150))
    return cover(im, FW, FH, fy=0.0)
CARROS7 = [("compass", "JEEP", "COMPASS"), ("crv", "HONDA", "CR-V"), ("c200", "MERCEDES", "C200"), ("kicks", "NISSAN", "KICKS")]
mos = Image.new("RGB", (FW, FH), PRETO)
for i, (n, _, _) in enumerate(CARROS7):
    t = cover(Image.open(car(n)).convert("RGB").crop((0, 0, 1080, 1150)), FW // 2 - 3, FH // 2 - 3, fy=0.2)
    mos.paste(t, ((i % 2) * (FW // 2 + 3), (i // 2) * (FH // 2 + 3)))
mos.save(o("_mosaico.jpg"))
capa_black(o("_mosaico.jpg"), "ESSES JÁ PASSARAM.", "O SEU É O PRÓXIMO.", o("jp_01.jpg"))
for k, (n, m1, m2) in enumerate(CARROS7):
    c = grad(foto_carro_feed(n), top=260, top_a=170, bot=560, bot_a=250)
    d = ImageDraw.Draw(c); d.text((52, 58), f"{k + 2}/6", font=bcb(40), fill=MUTED); badge(c, 52, tam=0.62)
    d = ImageDraw.Draw(c); y = pill(d, 52, 1000, "JÁ PASSOU AQUI", bc(36), GRAF, WHITE) + 18
    d.text((52, y - 6), m1, font=bcb(50), fill=GOLD); d.text((52, y + 42), m2, font=bc(138), fill=WHITE)
    d.text((52, y + 196), "Troca do óleo do câmbio automático", font=mrs(34), fill=MUTED)
    c.save(o(f"jp_0{k + 2}.jpg"), quality=93)
cta_black("O SEU", "É O PRÓXIMO.", o("jp_06.jpg"), itens=["Troca do óleo do câmbio automático", "Máquina especializada",
          "Óleo homologado pelo fabricante"])

# ---- stories 11h50: "já passou aqui" Black ----
ST1 = [("0111", "compass", "JEEP COMPASS"), ("0211", "creta", "HYUNDAI CRETA"), ("0311", "etios", "TOYOTA ETIOS"),
       ("0411", "fpace", "JAGUAR F-PACE"), ("0511", "corolla", "TOYOTA COROLLA"), ("0611", "hrv", "HONDA HR-V"),
       ("0711", "q5", "AUDI Q5")]
for dia, n, m in ST1: story_black_carro(car(n), m, o(f"story_{dia}_1150_{n}.jpg"))

# ---- stories 17h: condições ----
Image.open(R + "lote-2026-10-24/story_pneus_crystone.jpg").convert("RGB").crop((0, 0, 1080, 1150)).save("/home/claude/black/_pneu_topo.jpg")
story_black_cond("COMEÇOU", "A BLACK DA STAR", "Novembro inteiro com oferta em produtos e serviços.", o("story_0111_1700_comecou.jpg"),
                 foto=F + "renegade/foto_renegade_maquina.jpg", fy=0.3, tam_grande=230)
story_black_cond("ATÉ 30%", "DE DESCONTO", "Em produtos e serviços. Pede o seu orçamento no WhatsApp.", o("story_0211_1700_30off.jpg"),
                 foto=F + "cronos/foto_cronos_elevador_maquina.jpg")
story_black_cond("10X", "SEM JUROS", "Em todos os produtos e serviços da Star.", o("story_0311_1700_10x.jpg"),
                 foto=F + "fernando_balcao.jpg", fy=0.15)
story_black_cond("R$ 199,90", "PNEUS CRYSTONE NO PIX", "Preço a partir de. Consulte a medida do seu carro no WhatsApp.", o("story_0411_1700_pneus.jpg"),
                 foto="/home/claude/black/_pneu_topo.jpg", fy=0.0, conds=PNEU, tam_grande=230)
story_black_cond("COBRIMOS", "OFERTAS", "Achou mais barato? Manda o orçamento no WhatsApp e consulte as condições.", o("story_0511_1700_cobrimos.jpg"),
                 foto=F + "cronos/foto_carter_limpo_motul.jpg", tam_grande=230)
story_black_cond("21 DIAS", "PRA BLACK FRIDAY", "Mas na Star a oferta já começou. Não espera o dia 27.", o("story_0611_1700_contagem.jpg"),
                 foto=F + "renegade/foto_renegade_maquina.jpg", fy=0.6, tam_grande=260)
story_black_cond("TROCA DO ÓLEO", "DO CÂMBIO COM DESCONTO", "Máquina especializada e óleo homologado. Até 30% off em novembro.",
                 o("story_0711_1700_cambio.jpg"), foto=F + "cronos/foto_cronos_elevador_maquina.jpg", tam_grande=150, cor_grande=WHITE)

import glob
fs = sorted(glob.glob(OUT + "[!_]*.jpg")); print(len(fs))
folha_previa([f for f in fs if "/lanc" in f or "/feed" in f or "/jp" in f], "/home/claude/black/folha_feed.jpg", larg=300)
folha_previa([f for f in fs if "/story" in f], "/home/claude/black/folha_stories.jpg", larg=220)
