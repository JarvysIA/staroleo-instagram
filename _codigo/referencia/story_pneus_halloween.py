#!/usr/bin/env python3
"""Story Halloween dos pneus Crystone (31/10/2026, 15h). Pedido do Fernando em 28/10: "preço de assustar a concorrência",
R$ 199,90 no pix e montagem grátis. Fundo = foto dos pneus do story de 24/10 (parte de cima, sem texto), com clima de
Halloween (tom laranja, vinheta, teias) e o avatar abóbora do reel num círculo."""
import sys, math, random
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from star_lib import *
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUT = "/home/claude/halloween/story_pneus_halloween.jpg"
ORANGE = (255, 140, 26); RED = (229, 57, 53)
SRC = "/home/claude/staroleo-instagram/2026-10/lote-2026-10-24/story_pneus_crystone.jpg"
AV = "/home/claude/halloween/avatar.png"

# fundo: só a parte da foto sem texto (até y=1150), esticada para cobrir a tela
foto = Image.open(SRC).convert("RGB").crop((0, 0, 1080, 1150))
bg = Image.new("RGB", (SW, SH), GRAF); bg.paste(foto, (0, 0))   # sem ampliar: foto nítida
bg = ImageEnhance.Color(bg).enhance(0.75)
r, g, b = bg.split()
bg = Image.merge("RGB", (r.point(lambda v: min(255, int(v * 1.08 + 6))), g.point(lambda v: int(v * 0.92)), b.point(lambda v: int(v * 0.72))))
# vinheta
vig = Image.new("L", (SW, SH), 0); dv = ImageDraw.Draw(vig)
for i in range(60):
    a = int(200 * (i / 60) ** 2.2)
    dv.rectangle((i * 9, i * 13, SW - i * 9, SH - i * 13), outline=255 - a, width=14)
vig = vig.filter(ImageFilter.GaussianBlur(60))
bg = Image.composite(bg, Image.new("RGB", bg.size, (8, 6, 6)), vig)
c = grad(bg, top=360, top_a=170, bot=1240, bot_a=255, full=0.33)
d = ImageDraw.Draw(c, "RGBA")

# teias nos cantos de cima
def teia(cx, cy, sx, sy, raio, n=7, aneis=6):
    angs = [math.radians(a) for a in [i * 90 / (n - 1) for i in range(n)]]
    pts = [(cx + sx * raio * math.cos(a), cy + sy * raio * math.sin(a)) for a in angs]
    for p in pts: d.line([(cx, cy), p], fill=(255, 255, 255, 70), width=2)
    for k in range(1, aneis + 1):
        f = k / aneis; ring = [(cx + (p[0] - cx) * f, cy + (p[1] - cy) * f) for p in pts]
        for j in range(len(ring) - 1):
            a, b2 = ring[j], ring[j + 1]; m = ((a[0] + b2[0]) / 2 - sx * 6 * f, (a[1] + b2[1]) / 2 - sy * 6 * f)
            d.line([a, m, b2], fill=(255, 255, 255, 55), width=2)
teia(0, 0, 1, 1, 330); teia(SW, 0, -1, 1, 260)

# morcegos simples
def morcego(x, y, s, a=210):
    w = [(0, 0), (-0.5, -0.35), (-1.0, -0.2), (-1.25, -0.5), (-1.5, -0.05), (-1.15, 0.05), (-0.95, 0.3), (-0.65, 0.1),
         (-0.3, 0.32), (0, 0.15), (0.3, 0.32), (0.65, 0.1), (0.95, 0.3), (1.15, 0.05), (1.5, -0.05), (1.25, -0.5),
         (1.0, -0.2), (0.5, -0.35)]
    d.polygon([(x + px * s, y + py * s) for px, py in w], fill=(10, 8, 8, a))
    d.ellipse((x - 0.18 * s, y - 0.32 * s, x + 0.18 * s, y + 0.2 * s), fill=(10, 8, 8, a))

# topo
y = pill(d, SW / 2, 250, "ESPECIAL HALLOWEEN", bc(50), GRAF, ORANGE, padx=34, pady=14, center=True)

# avatar abóbora num círculo com aro laranja
av = Image.open(AV).convert("RGB"); R = 210
av = av.crop((768 - R, 1235 - R, 768 + R, 1235 + R)).resize((300, 300), Image.LANCZOS)
m = Image.new("L", (300, 300), 0); ImageDraw.Draw(m).ellipse((0, 0, 299, 299), fill=255)
glow = Image.new("RGBA", (380, 380), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((20, 20, 360, 360), fill=(255, 120, 0, 150))
glow = glow.filter(ImageFilter.GaussianBlur(22)); AX, AY = 735, 470
c.paste(glow, (AX - 40, AY - 40), glow)
d = ImageDraw.Draw(c, "RGBA"); d.ellipse((AX - 9, AY - 9, AX + 309, AY + 309), fill=ORANGE)
c.paste(av, (AX, AY), m)

# texto
d = ImageDraw.Draw(c, "RGBA"); y = 985
ctext(d, SW, y, "PREÇO DE ASSUSTAR", bc(118), WHITE); y += 122
ctext(d, SW, y, "A CONCORRÊNCIA", bc(118), ORANGE); y += 150
ctext(d, SW, y, "Pneus Crystone a partir de", mr(42), WHITE); y += 52
f = bc(190); preco = "R$ 199,90"; tw = d.textlength(preco, font=f)
d.text(((SW - tw) / 2 - 40, y), preco, font=f, fill=GOLD)
d.text(((SW + tw) / 2 - 20, y + 118), "no pix", font=bcb(48), fill=WHITE); y += 222
y = pill(d, SW / 2, y, "+ MONTAGEM GRÁTIS", bc(54), GRAF, GOLD, padx=34, pady=14, center=True) + 22
ctext(d, SW, y, "Consulte a medida do seu carro no WhatsApp", mr(32), MUTED)
logo(c, 190, (SW - 190) // 2, y + 56)
c.save(OUT, quality=94); print(OUT, y)
