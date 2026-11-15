#!/usr/bin/env python3
"""Lote 2026-11-14 (produção da noite de 14/11): dia 21/11 (sábado), 6 dias pra Black Friday.
07h10 feed: carrossel "Presente do câmbio: como funciona" (5 slides) com o slogan oficial em 2 linhas.
11h50 story Black: Já passou aqui · Fiat Cronos (Novembro 26/IMG_6163, capa de placa da Star).
17h00 story: 6 dias pra Black Friday + presente do câmbio (fundo IMG_2246, filtro velho x novo)."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from black_lib import _fundo
from PIL import Image, ImageDraw

U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
T = U + "Tudo até Outubro 26/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-14/"
o = lambda n: O + n
SLOGAN1 = "ATÉ 30% OFF + R$ 250 EM SERVIÇOS"
SLOGAN2 = "(4 balanceamentos + alinhamento + higienização do ar)"
NOTA = "*Cobrimos ofertas mediante apresentação do orçamento. Consulte as condições."


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


def numero(c, num, total=5):
    d = ImageDraw.Draw(c); d.text((52, 58), f"{num}/{total}", font=bcb(40), fill=MUTED)
    pill(d, FW - 52 - 330, 52, "BLACK FRIDAY", bc(40), PRETO, GOLD, padx=26, pady=10)


# 1/5 capa
c = cover(carregar(T + "IMG_3594.HEIC"), FW, FH, fy=0.42)
c = Image.blend(c, Image.new("RGB", (FW, FH), PRETO), 0.35); c = grad(c, top=720, top_a=235, bot=640, bot_a=252, full=0.30)
d = ImageDraw.Draw(c)
y = pill(d, FW / 2, 60, "BLACK FRIDAY · 27 E 28/11", bc(52), GRAF, GOLD, padx=34, pady=14, center=True) + 40
ctext(d, FW, y, "PRESENTE", bc(170), WHITE); y += 168
ctext(d, FW, y, "DO CÂMBIO", bc(170), GOLD); y += 190
ctext(d, FW, y, "como funciona", mr(44), (225, 226, 228))
faixa(c, 905, ang=-4, alt=80, txt="BLACK FRIDAY")
d = ImageDraw.Draw(c); chamada = "ARRASTA PRO LADO"
yb = pill(d, FW / 2 - 30, 1070, chamada, bc(48), GRAF, GOLD, padx=34, pady=16, center=True)
tw = d.textlength(chamada, font=bc(48)); x0 = FW / 2 - 30 + tw / 2 + 34
d.rounded_rectangle((x0 - 12, 1070, x0 + 62, yb), radius=10, fill=GOLD); seta(d, x0, 1070, yb - 1070)
logo(c, 170, (FW - 170) // 2, 1210)
c.save(o("pc_01.jpg"), quality=93)

# 2/5 quando
c = _fundo(T + "IMG_5992.HEIC", escuro=0.74, fy=0.45); numero(c, 2)
d = ImageDraw.Draw(c)
ctext(d, FW, 260, "27 E 28/11", bc(230), GOLD); y = 520
ctext(d, FW, y, "SEXTA E SÁBADO", bc(104), WHITE); y += 140
for ln in quebrar(d, "O presente vale só nesses dois dias, na Black Friday da Star.", mr(44), FW - 170):
    ctext(d, FW, y, ln, mr(44), (225, 226, 228)); y += 62
logo(c, 150, (FW - 150) // 2, FH - 190)
c.save(o("pc_02.jpg"), quality=93)

# 3/5 pra quem
c = _fundo(T + "IMG_3902.HEIC", escuro=0.74, fy=0.4); numero(c, 3)
d = ImageDraw.Draw(c)
ctext(d, FW, 240, "SÓ PRA QUEM", bc(120), WHITE)
ctext(d, FW, 370, "TROCAR O ÓLEO", bc(150), GOLD)
ctext(d, FW, 530, "DO CÂMBIO", bc(150), GOLD); y = 740
for ln in quebrar(d, "Câmbio automático, troca completa na máquina especializada, com óleo homologado pelo fabricante.", mr(44), FW - 170):
    ctext(d, FW, y, ln, mr(44), (225, 226, 228)); y += 62
y += 30
ctext(d, FW, y, "Não vale para outros serviços.", mrs(38), MUTED)
logo(c, 150, (FW - 150) // 2, FH - 190)
c.save(o("pc_03.jpg"), quality=93)

# 4/5 o que leva
c = _fundo(T + "IMG_4236.HEIC", escuro=0.80, fy=0.4); numero(c, 4)
d = ImageDraw.Draw(c)
ctext(d, FW, 200, "VOCÊ LEVA", bc(150), WHITE)
y = caixa_slogan(c, 400, FW, escala=1.0) + 70
d = ImageDraw.Draw(c)
for t in ["4 balanceamentos", "Alinhamento", "Higienização do ar-condicionado"]:
    estrela(d, 190, y + 30, 20, GOLD); d.text((232, y), t, font=mr(50), fill=WHITE); y += 92
y += 30
for ln in quebrar(d, "Tudo junto com o desconto da troca do óleo do câmbio.", mr(40), FW - 170):
    ctext(d, FW, y, ln, mr(40), (225, 226, 228)); y += 58
logo(c, 150, (FW - 150) // 2, FH - 190)
c.save(o("pc_04.jpg"), quality=93)

# 5/5 CTA
cta_black("JÁ AGENDA", "O SEU HORÁRIO.", o("pc_05.jpg"),
          itens=["Sexta 27 ou sábado 28/11", "Manda o modelo do carro no WhatsApp", "10x sem juros e cobrimos ofertas*"],
          foto=T + "IMG_2116.HEIC")
im = Image.open(o("pc_05.jpg")); d = ImageDraw.Draw(im)
ctext(d, FW, 1270, NOTA, mrs(26), MUTED); im.save(o("pc_05.jpg"), quality=93)

# 11h50 story Cronos
story_carro(U + "Novembro 26/IMG_6163.HEIC", "FIAT CRONOS", o("_cronos.jpg"), fy=0.12)
story_black_carro(o("_cronos.jpg"), "FIAT CRONOS", o("story_2111_1150_cronos.jpg"))
os.remove(o("_cronos.jpg"))

# 17h00 contagem 6 dias + presente
c = Image.blend(cover(carregar(T + "IMG_2246.HEIC"), SW, SH, fy=0.5), Image.new("RGB", (SW, SH), PRETO), 0.74)
c = grad(c, top=420, top_a=160, bot=900, bot_a=230)
badge(c, 250, tam=0.9); faixa(c, 520, ang=-4, alt=70, txt="BLACK FRIDAY")
d = ImageDraw.Draw(c)
y = 640; ctext(d, SW, y, "6 DIAS", bc(280), GOLD); y += 300
ctext(d, SW, y, "PRA BLACK FRIDAY", bc(104), WHITE); y += 130
for ln in quebrar(d, "Dias 27 e 28/11, quem trocar o óleo do câmbio na Star leva:", mr(44), SW - 170):
    ctext(d, SW, y, ln, mr(44), (225, 226, 228)); y += 62
y = caixa_slogan(c, y + 26, SW, escala=1.05) + 34
d = ImageDraw.Draw(c)
ctext(d, SW, y, "Garante o seu horário no WhatsApp", bcb(50), GOLD); y += 80
logo(c, 170, (SW - 170) // 2, min(y + 10, 1490))
c.save(o("story_2111_1700_contagem_presente.jpg"), quality=93)

folha_previa([o(f"pc_0{i}.jpg") for i in range(1, 6)] + [o("story_2111_1150_cronos.jpg"), o("story_2111_1700_contagem_presente.jpg")],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=360)
print("ok")
