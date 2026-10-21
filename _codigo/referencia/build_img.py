#!/usr/bin/env python3
"""Lote piloto Star: carrossel 'Seu carro é desses?', post equipe, 2 stories. Identidade do site."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter
import os
os.chdir("/home/claude/piloto"); os.makedirs("out", exist_ok=True)
GOLD = (240, 195, 33); GRAF = (17, 18, 20); WHITE = (255, 255, 255); MUTED = (166, 168, 171)
F = "/root/.fonts/"
bc = lambda s: ImageFont.truetype(F + "barlow-condensed-latin-800-normal.ttf", s)
bcb = lambda s: ImageFont.truetype(F + "barlow-condensed-latin-700-normal.ttf", s)
mr = lambda s: ImageFont.truetype(F + "manrope-latin-700-normal.ttf", s)
mrs = lambda s: ImageFont.truetype(F + "manrope-latin-600-normal.ttf", s)
LOGO = Image.open("/home/claude/kicks/logo.png").convert("RGBA")
WA = "(21) 97544-6417"

def grade(im):
    im = ImageOps.autocontrast(im, cutoff=0.5)
    im = ImageEnhance.Contrast(im).enhance(1.10); im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Sharpness(im).enhance(1.3)
    r, g, b = im.split(); r = r.point(lambda v: min(255, int(v * 1.03))); b = b.point(lambda v: int(v * 0.96))
    return Image.merge("RGB", (r, g, b))

def load(name): return grade(Image.open(f"src/{name}.jpg").convert("RGB"))

def cover(im, w, h, fy=0.5, fx=0.5, zoom=1.0):
    s = max(w / im.width, h / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))

def grad(base, top=0, top_a=0, bot=0, bot_a=0, full=0.55):
    W, H = base.size; g = Image.new("L", (1, H), 0)
    for y in range(H):
        a = 0
        if top and y < top: a = int(top_a * (1 - y / top) ** 1.2)
        if bot and y > H - bot: a = max(a, int(bot_a * min(1, (y - (H - bot)) / (bot * full)) ** 1.1))
        g.putpixel((0, y), a)
    return Image.composite(Image.new("RGB", base.size, GRAF), base, g.resize(base.size))

def logo(c, w, x, y):
    l = LOGO.resize((w, round(LOGO.height * w / LOGO.width)), Image.LANCZOS); c.paste(l, (x, y), l)

def ctext(d, W, y, t, f, fill):
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)

def pill(d, x, y, t, f, fg, bg, padx=26, pady=12, center=False):
    tw = d.textlength(t, font=f); b = f.getbbox(t); h = b[3] - b[1]
    if center: x = x - (tw + 2 * padx) / 2
    d.rounded_rectangle((x, y, x + tw + 2 * padx, y + h + 2 * pady), radius=10, fill=bg)
    d.text((x + padx, y + pady - b[1]), t, font=f, fill=fg); return y + h + 2 * pady

# ================= CARROSSEL 1080x1350 =================
W, H = 1080, 1350
cars = [("c200", "MERCEDES-BENZ", "C200", 0.12), ("x1", "BMW", "X1", 0.12), ("q5", "AUDI", "Q5", 0.10),
        ("hrv", "HONDA", "HR-V", 0.05), ("tr4", "MITSUBISHI", "PAJERO TR4", 0.12), ("renegade", "JEEP", "RENEGADE", 0.04),
        ("208", "PEUGEOT", "208", 0.12)]
n = len(cars) + 2
# capa: mosaico 2x2
c = Image.new("RGB", (W, H), GRAF)
for i, nm in enumerate(["c200", "x1", "q5", "renegade"]):
    t = cover(load(nm), W // 2 - 3, H // 2 - 3, fy=0.15)
    c.paste(t, ((i % 2) * (W // 2 + 3), (i // 2) * (H // 2 + 3)))
dark = Image.new("RGB", (W, H), GRAF); c = Image.blend(c, dark, 0.58)
d = ImageDraw.Draw(c)
ctext(d, W, 430, "SEU CARRO", bc(170), WHITE)
ctext(d, W, 600, "É DESSES?", bc(170), GOLD)
ctext(d, W, 815, "Olha quem já trocou o óleo do", mr(42), WHITE)
ctext(d, W, 868, "câmbio automático aqui na Star", mr(42), WHITE)
yb = pill(d, W / 2 - 30, 1010, "ARRASTA PRO LADO", bc(48), GRAF, GOLD, padx=34, pady=16, center=True)
tw = d.textlength("ARRASTA PRO LADO", font=bc(48)); x0 = W / 2 - 30 + tw / 2 + 34
d.rounded_rectangle((x0 - 12, 1010, x0 + 62, yb), radius=10, fill=GOLD)
for dx in (0, 22): d.polygon([(x0 + dx, 1010 + 20), (x0 + dx + 20, (1010 + yb) / 2), (x0 + dx, yb - 20)], fill=GRAF)
c.save("out/carrossel_01.jpg", quality=93)

for k, (nm, brand, model, fy) in enumerate(cars):
    c = grad(cover(load(nm), W, H, fy=fy), top=260, top_a=170, bot=560, bot_a=245)
    d = ImageDraw.Draw(c)
    d.text((52, 58), f"{k + 2}/{n}", font=bcb(40), fill=MUTED)
    y = 1000
    y = pill(d, 52, y, "JÁ PASSOU AQUI", bc(36), GRAF, GOLD) + 18
    d.text((52, y - 6), brand, font=bcb(50), fill=GOLD)
    d.text((52, y + 42), model, font=bc(138), fill=WHITE)
    d.text((52, y + 196), "Troca do óleo do câmbio automático", font=mrs(34), fill=MUTED)
    c.save(f"out/carrossel_{k + 2:02d}.jpg", quality=93)

c = Image.new("RGB", (W, H), GRAF); d = ImageDraw.Draw(c)
d.rectangle((0, 0, W, 12), fill=GOLD)
logo(c, 300, (W - 300) // 2, 130)
ctext(d, W, 390, "O SEU É O", bc(150), WHITE)
ctext(d, W, 540, "PRÓXIMO.", bc(150), GOLD)
y = 760
for t in ["Máquina especializada na troca do câmbio", "Óleo homologado pelo fabricante", "Parcelamos em até 10x sem juros"]:
    d.ellipse((150, y + 14, 170, y + 34), fill=GOLD); d.text((196, y), t, font=mr(40), fill=WHITE); y += 74
pill(d, W / 2, 1035, f"CHAME NO WHATSAPP  {WA}", bc(52), GRAF, GOLD, padx=36, pady=20, center=True)
ctext(d, W, 1180, "Estr. dos Bandeirantes, 841 · Taquara", mr(34), MUTED)
c.save(f"out/carrossel_{n:02d}.jpg", quality=93)

# ================= POST EQUIPE 1080x1350 =================
c = grad(cover(load("equipe"), W, H, fy=0.35), bot=470, bot_a=245)
d = ImageDraw.Draw(c)
y = 980
d.text((52, y), "QUEM CUIDA", font=bc(120), fill=WHITE)
d.text((52, y + 118), "DO SEU CARRO", font=bc(120), fill=GOLD)
d.text((52, y + 255), "Time Star · Taquara, Rio de Janeiro", font=mrs(34), fill=MUTED)
c.save("out/post_equipe.jpg", quality=93)

# ================= STORIES 1080x1920 =================
SW, SH = 1080, 1920
# story câmbio
c = grad(cover(load("c200"), SW, SH, fy=0.2), top=300, top_a=150, bot=980, bot_a=250)
d = ImageDraw.Draw(c)
y = 1180
y = pill(d, SW / 2, y, "JÁ PASSOU AQUI", bc(46), GRAF, GOLD, padx=34, pady=16, center=True) + 22
ctext(d, SW, y, "MERCEDES C200", bc(124), WHITE); y += 132
ctext(d, SW, y, "TROCA DO ÓLEO DO CÂMBIO AUTOMÁTICO", bcb(50), GOLD); y += 80
ctext(d, SW, y, "Parcelamos em até 10x sem juros", mr(36), WHITE)
c.save("out/story_cambio_c200.jpg", quality=93)

# story pneus
c = grad(cover(load("pneu1"), SW, SH, fy=0.3), top=300, top_a=150, bot=900, bot_a=250)
d = ImageDraw.Draw(c)
y = 1170
y = pill(d, SW / 2, y, "PNEUS CRYSTONE", bc(50), GRAF, GOLD, padx=34, pady=16, center=True) + 26
ctext(d, SW, y, "a partir de", mr(42), WHITE); y += 58
pr = "R$ 199,90"; f = bc(190); tw = d.textlength(pr, font=f)
d.text(((SW - tw) / 2 - 40, y), pr, font=f, fill=GOLD)
d.text(((SW + tw) / 2 - 20, y + 118), "no pix", font=bcb(48), fill=WHITE); y += 220
ctext(d, SW, y, f"Consulte sua medida no WhatsApp {WA}", mr(34), MUTED)
logo(c, 200, (SW - 200) // 2, y + 70)
c.save("out/story_pneus.jpg", quality=93)
print("ok")
