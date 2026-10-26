#!/usr/bin/env python3
"""Trend 'Out & In My Control' (xícara de café, out/2026) para a Star.
Fora da xícara: o que o motorista não controla. Dentro: o que ele controla. Reel 9:16, ~15 s, sem gravação."""
import sys, os, subprocess, math
REPO = os.path.expanduser("~/staroleo-instagram")
sys.path.insert(0, REPO + "/_codigo")
from star_lib import *
from PIL import Image, ImageDraw, ImageFilter
T = "/tmp/trend_controle"; os.makedirs(T + "/f", exist_ok=True)
OUT = REPO + "/2026-10/trends/reel_trend_controle.mp4"
AUD = REPO + "/_codigo/audio/trilha_corporativa_m1.mp3"
W, H, FPS = 1080, 1920, 30
FORA = [("O TRÂNSITO DA", "BANDEIRANTES", 260, 560), ("O PREÇO DA", "GASOLINA", 820, 560),
        ("BURACO", "NA RUA", 150, 1500), ("O CALOR", "DO RIO", 930, 1500), ("QUEM NÃO", "DÁ SETA", 540, 1650)]
DENTRO = ["TROCAR O ÓLEO", "DO CÂMBIO NO PRAZO", "CALIBRAR OS PNEUS", "CHAMAR A STAR"]
T_FORA = [0.9, 1.6, 2.3, 3.0, 3.7]; T_VIRA = 5.0; T_DENTRO = [5.7, 5.7, 6.7, 7.7]; VE = 10.2; END = 3.4; TOT = VE + END

# xícara (base)
def base():
    c = Image.new("RGB", (W, H), GRAF); d = ImageDraw.Draw(c)
    for r in range(900, 0, -12):  # brilho suave atrás da xícara
        a = int(26 * (1 - r / 900)); d.ellipse((540 - r, 1110 - r, 540 + r, 1110 + r), fill=(17 + a, 18 + a, 20 + a // 2))
    # alça
    d.ellipse((800, 900, 1010, 1180), outline=WHITE, width=34)
    # corpo
    d.rounded_rectangle((230, 820, 850, 1380), radius=70, fill=WHITE)
    d.rectangle((230, 820, 850, 900), fill=WHITE)
    d.ellipse((230, 780, 850, 870), fill=(235, 235, 235)); d.ellipse((250, 790, 830, 860), fill=(70, 42, 22))  # café
    # pires
    d.ellipse((150, 1360, 930, 1440), fill=(225, 225, 225)); d.ellipse((230, 1352, 850, 1400), fill=WHITE)
    # fumaça
    for k, x in enumerate((470, 540, 610)):
        pts = [(x + 16 * math.sin(i / 7 + k), 760 - i * 4) for i in range(32)]
        d.line(pts, fill=(120, 122, 126), width=8, joint="curve")
    return c

BASE = base()
def ease(p): p = max(0, min(1, p)); return 1 - (1 - p) ** 3

def texto_c(d, cx, y, t, f, cor, bg=(24, 25, 27)):
    if len(cor) == 4:  # mistura com o fundo (o texto do PIL não respeita o alfa)
        a = cor[3] / 255
        cor = tuple(int(c * a + b * (1 - a)) for c, b in zip(cor[:3], bg))
    d.text((cx - d.textlength(t, font=f) / 2, y), t, font=f, fill=cor)

def quadro(t):
    c = BASE.copy(); d = ImageDraw.Draw(c, "RGBA")
    # título
    if t < T_VIRA:
        p = ease((t - 0.1) / 0.35)
        if p > 0:
            texto_c(d, 540, 150 - 30 * (1 - p), "O QUE ESTÁ", bc(104), (255, 255, 255, int(255 * p)))
            texto_c(d, 540, 255 - 30 * (1 - p), "FORA DO SEU CONTROLE", bc(104), (229, 57, 53, int(255 * p)))
    else:
        p = ease((t - T_VIRA) / 0.35)
        texto_c(d, 540, 150 - 30 * (1 - p), "O QUE ESTÁ", bc(104), (255, 255, 255, int(255 * p)))
        texto_c(d, 540, 255 - 30 * (1 - p), "NO SEU CONTROLE", bc(104), (240, 195, 33, int(255 * p)))
    # itens fora
    for (l1, l2, cx, y), t0 in zip(FORA, T_FORA):
        p = ease((t - t0) / 0.3)
        if p <= 0: continue
        dim = 1.0 if t < T_VIRA else max(0.35, 1 - (t - T_VIRA) / 0.4 * 0.65)
        a = int(255 * p * dim); f = bc(58)
        yy = y + 24 * (1 - p)
        texto_c(d, cx, yy, l1, f, (255, 255, 255, a)); texto_c(d, cx, yy + 62, l2, f, (255, 255, 255, a))
    # itens dentro da xícara
    ys = [930, 990, 1110, 1230]; cores = [GRAF, GRAF, GRAF, (176, 132, 0)]
    for txt, y, t0, cor in zip(DENTRO, ys, T_DENTRO, cores):
        p = ease((t - t0) / 0.3)
        if p <= 0: continue
        f = bc(60) if txt != "CHAMAR A STAR" else bc(78)
        if txt == "CHAMAR A STAR":
            w = d.textlength(txt, font=f) + 50
            d.rounded_rectangle((540 - w / 2, y - 12, 540 + w / 2, y + 88), radius=14, fill=(17, 18, 20, int(255 * p)))
            texto_c(d, 540, y - 2, txt, f, (240, 195, 33, int(255 * p)), bg=WHITE if p < 1 else GRAF)
        else:
            texto_c(d, 540, y + 20 * (1 - p), txt, f, (17, 18, 20, int(255 * p)), bg=WHITE)
    d.text((540 - d.textlength("@staroleo_rj", font=mrs(34)) / 2, 1820), "@staroleo_rj", font=mrs(34), fill=(166, 168, 171, 255))
    return c

def fechamento(t):
    c = Image.new("RGB", (W, H), GRAF); d = ImageDraw.Draw(c, "RGBA")
    p = ease(t / 0.4); a = int(255 * p)
    l = LOGO.resize((520, round(LOGO.height * 520 / LOGO.width))); l2 = l.copy(); l2.putalpha(l.getchannel("A").point(lambda v: v * p))
    c.paste(l2, (280, 560), l2)
    texto_c(d, 540, 840, "O QUE DEPENDE DE VOCÊ,", bc(100), (255, 255, 255, a))
    texto_c(d, 540, 950, "A STAR RESOLVE.", bc(100), (240, 195, 33, a))
    p2 = ease((t - 0.4) / 0.35); a2 = int(255 * p2)
    if p2 > 0:
        txt = f"WHATSAPP  {WA}"; f = bc(64); w = d.textlength(txt, font=f)
        d.rounded_rectangle((540 - w / 2 - 34, 1130, 540 + w / 2 + 34, 1230), radius=14, fill=(240, 195, 33, a2))
        texto_c(d, 540, 1138, txt, f, (17, 18, 20, a2), bg=GOLD)
        texto_c(d, 540, 1275, ENDERECO, mrs(40), (166, 168, 171, a2))
    return c

n = round(TOT * FPS)
for i in range(n):
    t = i / FPS
    (quadro(t) if t < VE else fechamento(t - VE)).save(f"{T}/f/{i:04d}.png", compress_level=1)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{T}/f/%04d.png", "-i", AUD,
    "-filter_complex", f"[1:a]atrim=0:{TOT},afade=t=in:d=0.2,afade=t=out:st={TOT-0.9}:d=0.9,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
    "-map", "0:v", "-map", "[a]", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT], check=True)
print("ok", OUT, round(TOT, 2))
