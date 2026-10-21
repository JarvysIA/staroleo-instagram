#!/usr/bin/env python3
"""Biblioteca de peças da Star Óleo (@staroleo_rj) no padrão aprovado pelo Fernando em 21/10/2026.

Uso:  import sys; sys.path.insert(0, "<repo>/_codigo"); from star_lib import *
Antes, rode uma vez:  bash <repo>/_codigo/setup.sh   (fontes, pillow-heif)

Todas as funções recebem caminhos de arquivo e salvam JPG prontos para o Instagram.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter
try:
    import pillow_heif; pillow_heif.register_heif_opener()
except Exception:
    pass

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, "fonts")
LOGO_PATH = os.path.join(AQUI, "logo.png")
GOLD = (240, 195, 33); GRAF = (17, 18, 20); WHITE = (255, 255, 255); MUTED = (166, 168, 171)
WA = "(21) 97544-6417"
ENDERECO = "Estr. dos Bandeirantes, 841 · Taquara"

def _f(nome, s): return ImageFont.truetype(os.path.join(FONTES, nome), s)
bc = lambda s: _f("barlow-condensed-latin-800-normal.ttf", s)    # títulos
bcb = lambda s: _f("barlow-condensed-latin-700-normal.ttf", s)   # subtítulos
mr = lambda s: _f("manrope-latin-700-normal.ttf", s)             # texto
mrs = lambda s: _f("manrope-latin-600-normal.ttf", s)            # texto leve
LOGO = Image.open(LOGO_PATH).convert("RGBA")

# ---------------- utilidades ----------------
def abrir(path):
    """Abre JPG/PNG/HEIC já na orientação certa."""
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")

def grade(im):
    """Tratamento padrão: contraste, cor, nitidez e tira o azul da luz fluorescente."""
    im = ImageOps.autocontrast(im, cutoff=0.5)
    im = ImageEnhance.Contrast(im).enhance(1.10); im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Sharpness(im).enhance(1.3)
    r, g, b = im.split(); r = r.point(lambda v: min(255, int(v * 1.03))); b = b.point(lambda v: int(v * 0.96))
    return Image.merge("RGB", (r, g, b))

def carregar(path): return grade(abrir(path))

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

def borrar(im, caixas, raio=28):
    """Borra regiões (placas, rostos de terceiros). caixas = [(x0,y0,x1,y1)] em pixels da imagem original."""
    im = im.copy()
    for b in caixas:
        reg = im.crop(b).filter(ImageFilter.GaussianBlur(raio)); im.paste(reg, b[:2])
    return im

def logo(c, w, x, y):
    l = LOGO.resize((w, round(LOGO.height * w / LOGO.width)), Image.LANCZOS); c.paste(l, (int(x), int(y)), l)

def ctext(d, W, y, t, f, fill): d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)

def pill(d, x, y, t, f, fg, bg, padx=26, pady=12, center=False):
    tw = d.textlength(t, font=f); b = f.getbbox(t); h = b[3] - b[1]
    if center: x = x - (tw + 2 * padx) / 2
    d.rounded_rectangle((x, y, x + tw + 2 * padx, y + h + 2 * pady), radius=10, fill=bg)
    d.text((x + padx, y + pady - b[1]), t, font=f, fill=fg); return y + h + 2 * pady

def quebrar(d, texto, fonte, largura):
    linhas, cur = [], ""
    for w in texto.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fonte) <= largura: cur = t
        else: linhas.append(cur); cur = w
    linhas.append(cur); return linhas

# ---------------- STORIES 1080x1920 (deixar 250 px em cima e 340 embaixo livres) ----------------
SW, SH = 1080, 1920

def story_carro(foto, modelo, out, fy=0.2, selo="JÁ PASSOU AQUI",
                servico="TROCA DO ÓLEO DO CÂMBIO AUTOMÁTICO", rodape="Parcelamos em até 10x sem juros", caixas_borrar=()):
    """Carro no elevador. A parede STAR ÓLEO já aparece na foto, então sem logo por cima."""
    im = carregar(foto)
    if caixas_borrar: im = borrar(im, caixas_borrar)
    c = grad(cover(im, SW, SH, fy=fy), top=300, top_a=150, bot=980, bot_a=250)
    d = ImageDraw.Draw(c); y = 1180
    y = pill(d, SW / 2, y, selo, bc(46), GRAF, GOLD, padx=34, pady=16, center=True) + 22
    f = bc(124) if d.textlength(modelo, font=bc(124)) < 1000 else bc(100)
    ctext(d, SW, y, modelo, f, WHITE); y += 132
    ctext(d, SW, y, servico, bcb(50), GOLD); y += 80
    if rodape: ctext(d, SW, y, rodape, mr(36), WHITE)
    c.save(out, quality=93); return out

def story_citacao(foto, linha1, linha2, autor, apoio, out, fy=0.15, fx=0.5):
    """Frase de cliente. SÓ use palavras que o cliente disse de verdade no vídeo."""
    im = carregar(foto)
    c = Image.new("RGB", (SW, SH), GRAF)
    c.paste(cover(im, SW, SH, fy=fy, fx=fx).crop((0, 0, SW, SH - 200)), (0, 200))
    c = grad(c, bot=1000, bot_a=250); d = ImageDraw.Draw(c)
    d.rectangle((0, 192, SW, 200), fill=GOLD); d.rectangle((70, 1190, 82, 1450), fill=GOLD)
    d.text((110, 1170), linha1, font=bc(150), fill=WHITE); d.text((110, 1315), linha2, font=bc(150), fill=GOLD)
    d.text((74, 1490), autor, font=mr(40), fill=WHITE); d.text((74, 1546), apoio, font=mrs(34), fill=MUTED)
    c.save(out, quality=93); return out

def story_oferta(foto, etiqueta, preco, sufixo, rodape, out, fy=0.3, antes="a partir de"):
    """Oferta com preço (ex.: pneus Crystone a partir de R$ 199,90 no pix). Só preço confirmado pelo Fernando."""
    c = grad(cover(carregar(foto), SW, SH, fy=fy), top=300, top_a=150, bot=900, bot_a=250)
    d = ImageDraw.Draw(c); y = 1170
    y = pill(d, SW / 2, y, etiqueta, bc(50), GRAF, GOLD, padx=34, pady=16, center=True) + 26
    if antes: ctext(d, SW, y, antes, mr(42), WHITE); y += 58
    f = bc(190); tw = d.textlength(preco, font=f)
    d.text(((SW - tw) / 2 - 40, y), preco, font=f, fill=GOLD)
    if sufixo: d.text(((SW + tw) / 2 - 20, y + 118), sufixo, font=bcb(48), fill=WHITE)
    y += 220; ctext(d, SW, y, rodape, mr(34), MUTED); logo(c, 200, (SW - 200) // 2, y + 70)
    c.save(out, quality=93); return out

def story_texto(titulo1, titulo2, corpo, out, foto=None, fy=0.2):
    """Story de dica/aviso só com texto (com ou sem foto de fundo bem escurecida)."""
    if foto: c = Image.blend(cover(carregar(foto), SW, SH, fy=fy), Image.new("RGB", (SW, SH), GRAF), 0.72)
    else: c = Image.new("RGB", (SW, SH), GRAF)
    d = ImageDraw.Draw(c); logo(c, 240, (SW - 240) // 2, 300)
    y = 700; d.text((80, y), titulo1, font=bc(130), fill=WHITE); y += 135
    d.text((80, y), titulo2, font=bc(130), fill=GOLD); y += 180
    for ln in quebrar(d, corpo, mr(44), SW - 160): d.text((80, y), ln, font=mr(44), fill=(225, 226, 228)); y += 62
    c.save(out, quality=93); return out

# ---------------- FEED 1080x1350 ----------------
FW, FH = 1080, 1350

def feed_foto(foto, titulo1, titulo2, apoio, out, fy=0.3, fx=0.5, zoom=1.0):
    c = grad(cover(carregar(foto), FW, FH, fy=fy, fx=fx, zoom=zoom), top=200, top_a=120, bot=520, bot_a=245)
    d = ImageDraw.Draw(c); y = 960
    d.text((52, y), titulo1, font=bc(120), fill=WHITE); d.text((52, y + 118), titulo2, font=bc(120), fill=GOLD)
    d.text((52, y + 255), apoio, font=mrs(34), fill=MUTED)
    c.save(out, quality=93); return out

def carrossel_capa_mosaico(fotos4, titulo1, titulo2, sub1, sub2, out, chamada="ARRASTA PRO LADO"):
    c = Image.new("RGB", (FW, FH), GRAF)
    for i, p in enumerate(fotos4[:4]):
        t = cover(carregar(p), FW // 2 - 3, FH // 2 - 3, fy=0.15)
        c.paste(t, ((i % 2) * (FW // 2 + 3), (i // 2) * (FH // 2 + 3)))
    c = Image.blend(c, Image.new("RGB", (FW, FH), GRAF), 0.58); d = ImageDraw.Draw(c)
    ctext(d, FW, 430, titulo1, bc(170), WHITE); ctext(d, FW, 600, titulo2, bc(170), GOLD)
    ctext(d, FW, 815, sub1, mr(42), WHITE); ctext(d, FW, 868, sub2, mr(42), WHITE)
    yb = pill(d, FW / 2 - 30, 1010, chamada, bc(48), GRAF, GOLD, padx=34, pady=16, center=True)
    tw = d.textlength(chamada, font=bc(48)); x0 = FW / 2 - 30 + tw / 2 + 34
    d.rounded_rectangle((x0 - 12, 1010, x0 + 62, yb), radius=10, fill=GOLD)
    for dx in (0, 22): d.polygon([(x0 + dx, 1030), (x0 + dx + 20, (1010 + yb) / 2), (x0 + dx, yb - 20)], fill=GRAF)
    c.save(out, quality=93); return out

def carrossel_carro(foto, marca, modelo, num, total, out, fy=0.12, selo="JÁ PASSOU AQUI",
                    apoio="Troca do óleo do câmbio automático"):
    c = grad(cover(carregar(foto), FW, FH, fy=fy), top=260, top_a=170, bot=560, bot_a=245)
    d = ImageDraw.Draw(c); d.text((52, 58), f"{num}/{total}", font=bcb(40), fill=MUTED)
    y = pill(d, 52, 1000, selo, bc(36), GRAF, GOLD) + 18
    d.text((52, y - 6), marca, font=bcb(50), fill=GOLD); d.text((52, y + 42), modelo, font=bc(138), fill=WHITE)
    d.text((52, y + 196), apoio, font=mrs(34), fill=MUTED)
    c.save(out, quality=93); return out

def carrossel_capa_texto(foto, linhas, apoio, out, fy=0.25):
    """Capa de carrossel educativo. linhas = [(texto, 'w' ou 'g')]."""
    c = grad(Image.blend(cover(carregar(foto), FW, FH, fy=fy), Image.new("RGB", (FW, FH), GRAF), 0.55), bot=700, bot_a=245)
    d = ImageDraw.Draw(c); logo(c, 220, 52, 60); y = 640
    for t, cor in linhas: d.text((52, y), t, font=bc(128), fill=GOLD if cor == "g" else WHITE); y += 132
    d.text((52, y + 20), apoio, font=mrs(36), fill=MUTED)
    c.save(out, quality=93); return out

def carrossel_item(foto, numero, titulo, corpo, num, total, out, fy=0.15):
    c = Image.blend(cover(carregar(foto), FW, FH, fy=fy), Image.new("RGB", (FW, FH), GRAF), 0.72)
    d = ImageDraw.Draw(c); d.text((52, 58), f"{num}/{total}", font=bcb(40), fill=MUTED)
    d.text((52, 360), numero, font=bc(230), fill=GOLD); y = 640
    for ln in quebrar(d, titulo, bc(110), FW - 104): d.text((52, y), ln, font=bc(110), fill=WHITE); y += 112
    y += 30
    for ln in quebrar(d, corpo, mr(42), FW - 104): d.text((52, y), ln, font=mr(42), fill=(225, 226, 228)); y += 60
    c.save(out, quality=93); return out

def carrossel_cta(titulo1, titulo2, out, bullets=None, frase=None):
    c = Image.new("RGB", (FW, FH), GRAF); d = ImageDraw.Draw(c)
    d.rectangle((0, 0, FW, 12), fill=GOLD); logo(c, 300, (FW - 300) // 2, 120)
    ctext(d, FW, 390, titulo1, bc(150), WHITE); ctext(d, FW, 540, titulo2, bc(150), GOLD); y = 760
    if bullets:
        for t in bullets: d.ellipse((150, y + 14, 170, y + 34), fill=GOLD); d.text((196, y), t, font=mr(40), fill=WHITE); y += 74
    if frase:
        for ln in quebrar(d, frase, mr(40), 900): ctext(d, FW, y, ln, mr(40), WHITE); y += 58
    pill(d, FW / 2, 1035, f"CHAME NO WHATSAPP  {WA}", bc(52), GRAF, GOLD, padx=36, pady=20, center=True)
    ctext(d, FW, 1180, ENDERECO, mr(34), MUTED)
    c.save(out, quality=93); return out

def folha_previa(arquivos, out, larg=270):
    """Junta várias peças numa imagem só, para conferir e mandar de prévia."""
    ims = [Image.open(a).convert("RGB") for a in arquivos]
    ims = [i.resize((larg, round(larg * i.height / i.width))) for i in ims]
    H = max(i.height for i in ims); s = Image.new("RGB", (len(ims) * (larg + 10) - 10, H), (0, 0, 0))
    for k, i in enumerate(ims): s.paste(i, (k * (larg + 10), 0))
    s.save(out, quality=85); return out
