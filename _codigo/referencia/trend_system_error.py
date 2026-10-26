#!/usr/bin/env python3
"""Trend 'System Error' (post retrô de erro de sistema, out/2026) para a Star: janela antiga do Windows
com a foto do Fernando no balcão e um aviso de erro do câmbio. Feed 1080x1350."""
import sys, os, random
REPO = os.path.expanduser("~/staroleo-instagram")
sys.path.insert(0, REPO + "/_codigo")
from star_lib import *
from PIL import Image, ImageDraw, ImageFilter
OUT = REPO + "/2026-10/trends/post_trend_system_error.jpg"
W, H = 1080, 1350
CINZA = (198, 198, 198); CLARO = (255, 255, 255); ESCURO = (90, 90, 90); AZUL = (17, 18, 20)

def bisel(d, b, dentro=False):
    x0, y0, x1, y1 = b; a, z = (ESCURO, CLARO) if dentro else (CLARO, ESCURO)
    d.rectangle(b, fill=CINZA); d.line((x0, y0, x1, y0), fill=a, width=4); d.line((x0, y0, x0, y1), fill=a, width=4)
    d.line((x0, y1, x1, y1), fill=z, width=4); d.line((x1, y0, x1, y1), fill=z, width=4)

def botao_x(d, x, y, s=40):
    bisel(d, (x, y, x + s, y + s)); d.line((x + 11, y + 11, x + s - 11, y + s - 11), fill=(0, 0, 0), width=5)
    d.line((x + s - 11, y + 11, x + 11, y + s - 11), fill=(0, 0, 0), width=5)

# fundo dourado com grade de pontos (retrô)
c = Image.new("RGB", (W, H), GOLD); d = ImageDraw.Draw(c)
for y in range(0, H, 28):
    for x in range(0, W, 28): d.ellipse((x, y, x + 4, y + 4), fill=(222, 178, 20))

# janela 1: foto
wx0, wy0, wx1, wy1 = 70, 70, 1010, 830
bisel(d, (wx0, wy0, wx1, wy1)); d.rectangle((wx0 + 8, wy0 + 8, wx1 - 8, wy0 + 64), fill=AZUL)
d.text((wx0 + 24, wy0 + 14), "STAR_OLEO.EXE", font=bc(44), fill=GOLD); botao_x(d, wx1 - 60, wy0 + 16)
foto = carregar(REPO + "/2026-10/fontes/fernando_balcao.jpg")
fw, fh = wx1 - wx0 - 40, wy1 - wy0 - 104
foto = cover(foto, fw, fh, fy=0.32)
# efeito vintage: menos cor, grão e linhas
foto = Image.blend(foto, foto.convert("L").convert("RGB"), 0.25)
random.seed(4); g = Image.effect_noise((fw, fh), 22).convert("RGB"); foto = Image.blend(foto, g, 0.07)
fd = ImageDraw.Draw(foto)
for y in range(0, fh, 4): fd.line((0, y, fw, y), fill=(0, 0, 0), width=1)
foto = Image.blend(foto, cover(carregar(REPO + "/2026-10/fontes/fernando_balcao.jpg"), fw, fh, fy=0.32), 0.72)
c.paste(foto, (wx0 + 20, wy0 + 84)); d.rectangle((wx0 + 20, wy0 + 84, wx0 + 20 + fw, wy0 + 84 + fh), outline=ESCURO, width=3)

# janela 2: erro
ex0, ey0, ex1, ey1 = 120, 700, 960, 1180
sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rectangle((ex0 + 16, ey0 + 16, ex1 + 16, ey1 + 16), fill=150)
c.paste(Image.new("RGB", (W, H), (60, 48, 6)), (0, 0), sh.filter(ImageFilter.GaussianBlur(10))); d = ImageDraw.Draw(c)
bisel(d, (ex0, ey0, ex1, ey1)); d.rectangle((ex0 + 8, ey0 + 8, ex1 - 8, ey0 + 64), fill=(229, 57, 53))
d.text((ex0 + 24, ey0 + 12), "ERRO DO SISTEMA", font=bc(46), fill=CLARO); botao_x(d, ex1 - 60, ey0 + 16)
# ícone de alerta
tx, ty = ex0 + 50, ey0 + 110
d.polygon([(tx + 60, ty), (tx + 120, ty + 104), (tx, ty + 104)], fill=GOLD, outline=(0, 0, 0))
d.line([(tx + 60, ty), (tx + 120, ty + 104), (tx, ty + 104), (tx + 60, ty)], fill=(0, 0, 0), width=4)
d.text((tx + 48, ty + 22), "!", font=bc(80), fill=(0, 0, 0))
d.text((ex0 + 200, ey0 + 96), "ÓLEO DO CÂMBIO", font=bc(64), fill=(0, 0, 0))
d.text((ex0 + 200, ey0 + 160), "NÃO ENCONTRADO.", font=bc(64), fill=(229, 57, 53))
y = ey0 + 250
for ln in ["Você não lembra quando foi a última troca?",
           "Tranco na troca de marcha é o primeiro aviso."]:
    d.text((ex0 + 50, y), ln, font=mrs(31), fill=(20, 20, 20)); y += 46
# botões
b1 = (ex0 + 50, ey1 - 112, ex0 + 330, ey1 - 40); b2 = (ex0 + 360, ey1 - 112, ex1 - 50, ey1 - 40)
bisel(d, b1); f = bcb(42)
t = "IGNORAR"; d.text(((b1[0] + b1[2] - d.textlength(t, font=f)) / 2, b1[1] + 12), t, font=f, fill=(140, 140, 140))
d.line((b1[0] + 40, (b1[1] + b1[3]) // 2 + 4, b1[2] - 40, (b1[1] + b1[3]) // 2 + 4), fill=(140, 140, 140), width=4)
d.rectangle(b2, fill=AZUL); d.rectangle((b2[0] + 6, b2[1] + 6, b2[2] - 6, b2[3] - 6), outline=GOLD, width=3)
t = "CHAMAR A STAR"; f = bc(46); d.text(((b2[0] + b2[2] - d.textlength(t, font=f)) / 2, b2[1] + 9), t, font=f, fill=GOLD)

# rodapé
d.rectangle((0, H - 130, W, H), fill=AZUL)
logo(c, 190, 60, H - 112)
t = f"WHATSAPP {WA}"; f = bc(52); d.text((W - 60 - d.textlength(t, font=f), H - 118), t, font=f, fill=GOLD)
t = ENDERECO; f = mrs(28); d.text((W - 60 - d.textlength(t, font=f), H - 58), t, font=f, fill=MUTED)
os.makedirs(os.path.dirname(OUT), exist_ok=True); c.save(OUT, quality=93); print(OUT)
