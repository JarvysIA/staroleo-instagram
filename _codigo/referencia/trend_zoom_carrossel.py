#!/usr/bin/env python3
"""Trend 'Girl, zoom in…' (carrossel de zoom nos detalhes, New Engen, nov/2026) na versão Star + Black November.
Carrossel 1080x1350, sem gravação, 0 crédito: capa com a foto do Cronos no elevador ('DÁ UM ZOOM…', tem um recado
escondido na foto) -> zoom na máquina -> zoom no óleo -> zoom no recado escondido (etiqueta 'ATÉ 30% OFF' pendurada
no carrinho) -> CTA Black com a nota do cobrimos ofertas. A etiqueta é desenhada na foto em resolução cheia,
então os zooms saem nítidos."""
import os, sys, math
REPO = os.path.expanduser("~/staroleo-instagram"); sys.path.insert(0, REPO + "/_codigo")
from black_lib import *
from PIL import Image, ImageDraw, ImageFilter
OUTD = REPO + "/2026-11/trends"; os.makedirs(OUTD, exist_ok=True)
FOTO = REPO + "/2026-10/fontes/cronos/foto_cronos_elevador_maquina.jpg"
NOTA = "*Cobrimos ofertas mediante apresentação do orçamento. Consulte as condições."

base = carregar(FOTO).convert("RGB")  # 1932x2576, já com o tratamento de cor da Star

# --- etiqueta escondida, pendurada na prateleira de baixo do carrinho (coords da foto original)
tag = Image.new("RGBA", (330, 190), (0, 0, 0, 0)); td = ImageDraw.Draw(tag)
td.rounded_rectangle((8, 30, 322, 182), radius=16, fill=GOLD + (255,), outline=GRAF + (255,), width=5)
td.ellipse((150, 40, 180, 70), fill=GRAF + (255,))
td.text((165, 112), "ATÉ 30% OFF", font=bc(56), fill=GRAF, anchor="mm")
td.text((165, 158), "BLACK NOVEMBER", font=bc(30), fill=GRAF, anchor="mm")
tag = tag.rotate(-7, expand=True, resample=Image.BICUBIC)
TX, TY = 1150, 2045
d0 = ImageDraw.Draw(base)
d0.line((1238, 2022, TX + 175, TY + 55), fill=(30, 30, 30), width=5)  # barbante
sh = Image.new("RGBA", tag.size, (0, 0, 0, 0)); sh.putalpha(tag.getchannel("A").point(lambda v: int(v * 0.45)))
sh = sh.filter(ImageFilter.GaussianBlur(10))
base.paste(sh, (TX + 10, TY + 14), sh); base.paste(tag, (TX, TY), tag)

def zoom(x0, y0, w):
    h = int(w * FH / FW)
    return base.crop((x0, y0, x0 + w, y0 + h)).resize((FW, FH), Image.LANCZOS)

def lupa(d, cx, cy, r, cor=GOLD):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=cor, width=9)
    a = math.radians(45); x1 = cx + r * math.cos(a); y1 = cy + r * math.sin(a)
    d.line((x1, y1, x1 + r * 0.9, y1 + r * 0.9), fill=cor, width=16)

def contorno(d, y, t, f, cor):
    while d.textlength(t, font=f) > FW - 80: f = bc(f.size - 4)
    w = d.textlength(t, font=f)
    d.text(((FW - w) / 2, y), t, font=f, fill=cor, stroke_width=7, stroke_fill=GRAF)

def contador(d, n, tot=5):
    d.rounded_rectangle((FW - 150, 40, FW - 40, 92), radius=26, fill=(17, 18, 20, 200))
    d.text((FW - 95, 66), f"{n}/{tot}", font=bc(36), fill=WHITE, anchor="mm")

saidas = []
# 1) capa
c = cover(base, FW, FH, fy=0.55)
c = grad(c, top=520, top_a=225, bot=260, bot_a=150)
badge(c, 40, tam=0.62); d = ImageDraw.Draw(c, "RGBA")
contorno(d, 128, "DÁ UM ZOOM…", bc(150), WHITE)
contorno(d, 292, "TEM UM RECADO ESCONDIDO", bc(70), GOLD)
contorno(d, 368, "NESSA FOTO", bc(70), GOLD)
pill(d, FW / 2, 1240, "ARRASTA PRO LADO  >>", bc(46), GRAF, GOLD, padx=30, pady=14, center=True)
contador(d, 1)
saidas.append(f"{OUTD}/zoom_01.jpg"); c.save(saidas[-1], quality=93)

def slide(img, n, etiqueta, l1, l2, corpo):
    c = grad(img, top=240, top_a=120, bot=560, bot_a=245)
    d = ImageDraw.Draw(c, "RGBA")
    lupa(d, 92, 92, 36); d.text((150, 92), etiqueta, font=bc(48), fill=WHITE, anchor="lm", stroke_width=4, stroke_fill=GRAF)
    contador(d, n)
    y = 905
    contorno(d, y, l1, bc(100), WHITE); contorno(d, y + 102, l2, bc(100), GOLD); y += 232
    for ln in quebrar(d, corpo, mr(38), FW - 140):
        d.text((FW / 2, y), ln, font=mr(38), fill=(232, 233, 235), anchor="ma", stroke_width=3, stroke_fill=GRAF); y += 52
    return c

# 2) zoom na máquina
c = slide(zoom(480, 1500, 520), 2, "ZOOM 1", "A MÁQUINA", "ESPECIALIZADA",
          "Troca completa: o óleo velho sai do câmbio e o novo entra na medida certa.")
saidas.append(f"{OUTD}/zoom_02.jpg"); c.save(saidas[-1], quality=93)
# 3) zoom no óleo
c = slide(zoom(1010, 1520, 580), 3, "ZOOM 2", "O ÓLEO CERTO", "PRA CADA CÂMBIO",
          "Óleo homologado pelo fabricante do seu carro, nada de óleo genérico.")
saidas.append(f"{OUTD}/zoom_03.jpg"); c.save(saidas[-1], quality=93)
# 4) zoom no recado
c = slide(zoom(1010, 1880, 540), 4, "ZOOM 3", "ACHOU", "O RECADO?",
          "Na Black November da Star: até 30% de desconto, 10x sem juros e cobrimos ofertas*.")
saidas.append(f"{OUTD}/zoom_04.jpg"); c.save(saidas[-1], quality=93)
# 5) CTA
out = f"{OUTD}/zoom_05.jpg"
cta_black("AGORA É O", "SEU CARRO", out, itens=["Troca completa na máquina", "Óleo homologado pelo fabricante",
          "Nacionais e importados"], foto=FOTO)
c = Image.open(out).convert("RGB"); d = ImageDraw.Draw(c)
ctext(d, FW, 1290, NOTA, mrs(24), MUTED); c.save(out, quality=93); saidas.append(out)
folha_previa(saidas, "/tmp/zoom_previa.jpg")
print("\n".join(saidas))
