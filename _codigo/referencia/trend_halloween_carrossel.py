#!/usr/bin/env python3
"""Carrossel trend 'aviso de conteúdo assustador' (Halloween 31/10) para a Star."""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from star_lib import *
from PIL import Image, ImageDraw, ImageFilter
os.chdir("/home/claude/trend2"); os.makedirs("hw", exist_ok=True)
P = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
W, H = 1080, 1350

def fundo_borrado(path, fy=0.5):
    im = cover(carregar(path), W, H, fy=fy).filter(ImageFilter.GaussianBlur(48))
    return Image.blend(im, Image.new("RGB", (W, H), GRAF), 0.45)

def olho_riscado(d, cx, cy, r=70, cor=WHITE, w=9):
    d.ellipse((cx - r, cy - r * 0.62, cx + r, cy + r * 0.62), outline=cor, width=w)
    d.ellipse((cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3), outline=cor, width=w)
    d.line((cx - r * 0.95, cy + r * 0.85, cx + r * 0.95, cy - r * 0.85), fill=cor, width=w + 2)

def bloco(d, y, linhas, f, cor, gap):
    for ln in linhas: ctext(d, W, y, ln, f, cor); y += gap
    return y

# 1) aviso
c = fundo_borrado(P + "IMG_6037.HEIC"); d = ImageDraw.Draw(c)
olho_riscado(d, W // 2, 380)
ctext(d, W, 500, "CONTEÚDO ASSUSTADOR", bc(96), WHITE)
y = bloco(d, 640, quebrar(d, "Este post mostra o que acontece dentro do câmbio automático quando o óleo não é trocado. Pode assustar donos de carro.", mr(40), 860), mr(40), WHITE, 58)
d.line((90, y + 50, W - 90, y + 50), fill=(255, 255, 255), width=2)
ctext(d, W, y + 85, "Arraste para ver mesmo assim", bcb(56), WHITE)
d.text((52, 58), "1/4", font=bcb(40), fill=MUTED)
c.save("hw/halloween_01.jpg", quality=93)

# 2) tem certeza?
c = fundo_borrado(P + "IMG_6037.HEIC", fy=0.3); d = ImageDraw.Draw(c)
d.rounded_rectangle((110, 330, W - 110, 1020), radius=36, fill=(28, 29, 32))
ctext(d, W, 400, "TEM CERTEZA?", bc(118), WHITE)
bloco(d, 560, quebrar(d, "Depois que você vê, não dá para desver. E nunca mais esquece de trocar o óleo do câmbio.", mr(38), 740), mr(38), MUTED, 56)
d.line((110, 820, W - 110, 820), fill=(60, 61, 64), width=2)
d.line((W // 2, 820, W // 2, 1020), fill=(60, 61, 64), width=2)
ctext_x = lambda t, f, cx, yy, cor: d.text((cx - d.textlength(t, font=f) / 2, yy), t, font=f, fill=cor)
ctext_x("VOLTAR", bcb(54), W / 4 + 55, 890, MUTED)
ctext_x("VER  >>", bc(58), 3 * W / 4 - 55, 888, GOLD)
d.text((52, 58), "2/4", font=bcb(40), fill=MUTED)
c.save("hw/halloween_02.jpg", quality=93)

# 3) BOO! (filtro novo em cima, filtro que saiu do câmbio embaixo)
im = carregar(P + "1899b1c7-6987-4ac6-9a7a-402b3e152283.JPG")
c = grad(cover(im, W, H, fy=0.55), top=330, top_a=235, bot=330, bot_a=235); d = ImageDraw.Draw(c)
d.text((52, 58), "3/4", font=bcb(40), fill=MUTED)
ctext(d, W, 70, "BOO!", bc(210), GOLD)
pill(d, 880, 360, "NOVO", bc(46), GRAF, WHITE)
pill(d, 70, 560, "O QUE SAIU DO CÂMBIO", bc(46), WHITE, (229, 57, 53))
ctext(d, W, 1150, "Óleo vencido vira borra e entope o filtro.", mr(40), WHITE)
ctext(d, W, 1205, "O câmbio sente primeiro: trancos e patinadas.", mrs(34), MUTED)
c.save("hw/halloween_03.jpg", quality=93)

# 4) CTA
carrossel_cta("SEM TERROR", "NO SEU CÂMBIO.", "hw/halloween_04.jpg",
              bullets=["Troca completa com máquina especializada", "Óleo homologado pelo fabricante", "Parcelamos em até 10x sem juros"])
folha_previa([f"hw/halloween_0{i}.jpg" for i in range(1, 5)], "hw/previa.jpg")
print("ok")
