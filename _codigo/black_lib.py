#!/usr/bin/env python3
"""BLACK NOVEMBER STAR (01 a 30/11/2026). Pedido do Fernando em 29/10/2026: novembro inteiro em promoção.
Condições confirmadas: até 30% de desconto em produtos e serviços (varia por item, o valor exato sai no orçamento),
10x sem juros e cobrimos ofertas, que podem ir juntos no mesmo post.
EXCEÇÃO: peça com o preço do pneu (a partir de R$ 199,90 no pix) NÃO leva o 10x nem o "até 30% off" (o preço já é a oferta):
use o selo PNEU = ["MONTAGEM GRÁTIS", "COBRIMOS OFERTAS"].

Visual: preto e dourado (cores da Star) + faixa inclinada "BLACK NOVEMBER ★" e selo com as 3 condições.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from star_lib import *
from PIL import Image, ImageDraw, ImageFilter

PRETO = (8, 8, 9)
CONDS = ["ATÉ 30% OFF", "10X SEM JUROS", "COBRIMOS OFERTAS"]
PNEU = ["MONTAGEM GRÁTIS", "COBRIMOS OFERTAS"]
LETRA = "em produtos e serviços · consulte no WhatsApp"

def faixa(c, y, ang=-4, txt="BLACK NOVEMBER", alt=86, fundo=GOLD, cor=GRAF):
    """Faixa inclinada atravessando a peça, com o texto repetido."""
    W = c.width; L = int(W * 1.5)
    band = Image.new("RGBA", (L, alt), fundo + (255,)); d = ImageDraw.Draw(band)
    f = bc(int(alt * 0.72)); x = 10; r = alt * 0.24
    while x < L:
        d.text((x, alt * 0.5), txt, font=f, fill=cor, anchor="lm"); x += d.textlength(txt, font=f) + 30 + r
        estrela(d, x, alt * 0.5, r, cor); x += r + 30
    band = band.rotate(ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", band.size, (0, 0, 0, 0)); sh.putalpha(band.getchannel("A").point(lambda v: int(v * 0.55)))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    x0 = (W - band.width) // 2; y0 = int(y - band.height / 2)
    c.paste(sh, (x0, y0 + 14), sh); c.paste(band, (x0, y0), band)

def estrela(d, cx, cy, r, cor):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=cor)

def selo(c, y, sem_10x=False, larg=None, letra=LETRA, escala=1.0, conds=None):
    """Três caixas lado a lado com as condições da Black. Retorna o y de baixo."""
    W = c.width; larg = larg or W - 80; d = ImageDraw.Draw(c)
    conds = conds or [x for x in CONDS if not (sem_10x and "10X" in x)]
    gap = 14; bw = (larg - gap * (len(conds) - 1)) / len(conds); bh = int(112 * escala)
    x = (W - larg) / 2
    for i, t in enumerate(conds):
        fill = GOLD if i == 0 else None
        d.rounded_rectangle((x, y, x + bw, y + bh), radius=12, fill=fill, outline=GOLD, width=4)
        f = bc(int(48 * escala))
        while d.textlength(t, font=f) > bw - 24: f = bc(f.size - 2)
        d.text((x + bw / 2, y + bh / 2), t, font=f, fill=GRAF if fill else GOLD, anchor="mm"); x += bw + gap
    y += bh
    if letra:
        y += 20; ctext(d, W, y, letra, mrs(int(30 * escala)), MUTED); y += int(42 * escala)
    return y

def badge(c, y, tam=1.0):
    """Etiqueta 'BLACK NOVEMBER' (preto com borda dourada) centralizada no topo."""
    d = ImageDraw.Draw(c); W = c.width; f = bc(int(78 * tam))
    t1, t2 = "BLACK ", "NOVEMBER"; w1, w2 = d.textlength(t1, font=f), d.textlength(t2, font=f)
    pad = int(34 * tam); h = int(104 * tam); x0 = (W - w1 - w2) / 2
    d.rounded_rectangle((x0 - pad, y, x0 + w1 + w2 + pad, y + h), radius=int(14 * tam), fill=PRETO, outline=GOLD, width=max(3, int(4 * tam)))
    d.text((x0, y + h / 2), t1, font=f, fill=WHITE, anchor="lm"); d.text((x0 + w1, y + h / 2), t2, font=f, fill=GOLD, anchor="lm")
    return y + h

def marca(c, y, tam=1.0):
    """Lockup BLACK / NOVEMBER (branco e dourado), centralizado."""
    d = ImageDraw.Draw(c); W = c.width
    f1 = bc(int(150 * tam)); f2 = bc(int(76 * tam))
    d.text((W / 2, y), "BLACK", font=f1, fill=WHITE, anchor="mt")
    y += int(140 * tam)
    tw = d.textlength("NOVEMBER", font=f2); sp = int(10 * tam)
    # NOVEMBER espaçado
    letras = list("NOVEMBER"); tot = sum(d.textlength(l, font=f2) for l in letras) + sp * (len(letras) - 1)
    x = (W - tot) / 2
    for l in letras: d.text((x, y), l, font=f2, fill=GOLD); x += d.textlength(l, font=f2) + sp
    return y + int(84 * tam)

def foto_de_story(path, corte=1150):
    """Parte de cima (sem texto) de um story antigo da Star, já tratada."""
    return Image.open(path).convert("RGB").crop((0, 0, 1080, corte))

def story_black_carro(story_antigo, modelo, out, titulo="O SEU É O PRÓXIMO.", sem_10x=False):
    """Story 'Já passou aqui' na versão Black: foto do carro do story antigo + faixa + condições."""
    c = Image.new("RGB", (SW, SH), PRETO); c.paste(foto_de_story(story_antigo), (0, 0))
    c = grad(c, top=380, top_a=200, bot=1080, bot_a=255, full=0.30)
    badge(c, 240, tam=0.9)
    faixa(c, 1035, ang=-4, alt=78)
    d = ImageDraw.Draw(c); y = 1135
    y = pill(d, SW / 2, y, "JÁ PASSOU AQUI", bc(42), GRAF, WHITE, padx=30, pady=12, center=True) + 16
    f = bc(118) if d.textlength(modelo, font=bc(118)) < 1000 else bc(96)
    ctext(d, SW, y, modelo, f, WHITE); y += 124
    ctext(d, SW, y, titulo, bc(64), GOLD); y += 96
    y = selo(c, y, sem_10x=sem_10x)
    logo(c, 170, (SW - 170) // 2, y + 18)
    c.save(out, quality=93); return out

# ---------------- FEED 1080x1350 ----------------
def _fundo(foto, w=FW, h=FH, escuro=0.62, fy=0.3, fx=0.5):
    if foto is None: return Image.new("RGB", (w, h), PRETO)
    return Image.blend(cover(carregar(foto), w, h, fy=fy, fx=fx), Image.new("RGB", (w, h), PRETO), escuro)

def seta(d, x, y, h, cor=GRAF):
    for dx in (0, 22): d.polygon([(x + dx, y + 18), (x + dx + 20, y + h / 2), (x + dx, y + h - 18)], fill=cor)

def capa_black(foto, linha1, linha2, out, chamada="ARRASTA PRO LADO", fy=0.3, fx=0.5):
    """Capa de carrossel Black: lockup grande, 2 linhas de chamada, faixa e botão arrasta."""
    c = _fundo(foto, escuro=0.55, fy=fy, fx=fx); c = grad(c, top=420, top_a=200, bot=700, bot_a=250)
    y = marca(c, 120, tam=1.55)
    d = ImageDraw.Draw(c); y += 40
    ctext(d, FW, y, linha1, bc(96), WHITE); ctext(d, FW, y + 100, linha2, bc(96), GOLD)
    faixa(c, 905, ang=-4, alt=80)
    d = ImageDraw.Draw(c)
    if chamada:
        yb = pill(d, FW / 2 - 30, 1070, chamada, bc(48), GRAF, GOLD, padx=34, pady=16, center=True)
        tw = d.textlength(chamada, font=bc(48)); x0 = FW / 2 - 30 + tw / 2 + 34
        d.rounded_rectangle((x0 - 12, 1070, x0 + 62, yb), radius=10, fill=GOLD); seta(d, x0, 1070, yb - 1070)
    logo(c, 170, (FW - 170) // 2, 1210)
    c.save(out, quality=93); return out

def slide_black(foto, grande, titulo, corpo, num, total, out, fy=0.3, fx=0.5, cor_grande=GOLD, tam_grande=250):
    """Slide com um número/palavra gigante (ex.: 30%), título e texto curto."""
    c = _fundo(foto, escuro=0.74, fy=fy, fx=fx); d = ImageDraw.Draw(c)
    d.text((52, 58), f"{num}/{total}", font=bcb(40), fill=MUTED); badge(c, 52, tam=0.62)
    d = ImageDraw.Draw(c)
    f = bc(tam_grande)
    while d.textlength(grande, font=f) > FW - 100: f = bc(f.size - 6)
    ctext(d, FW, 300, grande, f, cor_grande); y = 300 + f.size + 30
    for ln in quebrar(d, titulo, bc(96), FW - 120): ctext(d, FW, y, ln, bc(96), WHITE); y += 100
    y += 30
    for ln in quebrar(d, corpo, mr(42), FW - 160): ctext(d, FW, y, ln, mr(42), (225, 226, 228)); y += 60
    c.save(out, quality=93); return out

def cta_black(titulo1, titulo2, out, itens=None, sem_10x=False, foto=None):
    c = _fundo(foto, escuro=0.82); d = ImageDraw.Draw(c)
    badge(c, 70, tam=0.8); d = ImageDraw.Draw(c)
    ctext(d, FW, 230, titulo1, bc(130), WHITE); ctext(d, FW, 360, titulo2, bc(130), GOLD); y = 540
    if itens:
        for t in itens:
            estrela(d, 200, y + 26, 16, GOLD); d.text((236, y), t, font=mr(42), fill=WHITE); y += 70
    y = max(y + 20, 830)
    y = selo(c, y, sem_10x=sem_10x, letra=None) + 40
    d = ImageDraw.Draw(c)
    pill(d, FW / 2, y, f"CHAME NO WHATSAPP  {WA}", bc(52), GRAF, GOLD, padx=36, pady=20, center=True)
    ctext(d, FW, y + 120, ENDERECO, mr(34), MUTED)
    c.save(out, quality=93); return out

def story_black_cond(grande, titulo, corpo, out, foto=None, fy=0.3, sem_10x=False, tam_grande=300, cor_grande=GOLD, mostrar_selo=True, conds=None):
    """Story de condição (ex.: ATÉ 30% OFF, 10X, COBRIMOS OFERTAS, contagem para a Black Friday)."""
    c = _fundo(foto, SW, SH, escuro=0.72, fy=fy)
    c = grad(c, top=420, top_a=160, bot=900, bot_a=230)
    badge(c, 250, tam=0.9); faixa(c, 520, ang=-4, alt=70)
    d = ImageDraw.Draw(c); f = bc(tam_grande)
    while d.textlength(grande, font=f) > SW - 100: f = bc(f.size - 6)
    y = 650; ctext(d, SW, y, grande, f, cor_grande); y += f.size + 20
    for ln in quebrar(d, titulo, bc(104), SW - 120): ctext(d, SW, y, ln, bc(104), WHITE); y += 108
    y += 24
    for ln in quebrar(d, corpo, mr(44), SW - 170): ctext(d, SW, y, ln, mr(44), (225, 226, 228)); y += 62
    if mostrar_selo: y = selo(c, max(y + 40, 1330), sem_10x=sem_10x, letra=None, conds=conds)
    logo(c, 170, (SW - 170) // 2, min(max(y + 40, 1460), 1560))
    c.save(out, quality=93); return out

def feed_black(foto, linha1, linha2, apoio, out, fy=0.3, fx=0.5, sem_10x=False, nota=None, foto_img=None, conds=None):
    """Post único de oferta (1080x1350): foto + título em 2 linhas + apoio + selo."""
    base = foto_img if foto_img is not None else cover(carregar(foto), FW, FH, fy=fy, fx=fx)
    c = grad(base, top=260, top_a=190, bot=760, bot_a=252, full=0.5)
    badge(c, 56, tam=0.75); d = ImageDraw.Draw(c); y = 760
    ctext(d, FW, y, linha1, bc(112), WHITE); ctext(d, FW, y + 112, linha2, bc(112), GOLD); y += 250
    if apoio:
        for ln in quebrar(d, apoio, mr(36), FW - 140): ctext(d, FW, y, ln, mr(36), (225, 226, 228)); y += 50
    y = selo(c, max(y + 18, 1140), sem_10x=sem_10x, letra=None, escala=0.9, conds=conds)
    if nota: ctext(ImageDraw.Draw(c), FW, y + 14, nota, mrs(26), MUTED)
    c.save(out, quality=93); return out
