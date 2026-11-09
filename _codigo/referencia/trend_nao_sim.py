#!/usr/bin/env python3
"""Trend 'No, No, No… Yes!' (3 cortes rápidos com NÃO e o último com SIM; New Engen, nov/2026) na versão Star + Black.
Reel 9:16 sem gravação: 2 cenas de IA do Fernando no balcão (gemini-3.1-flash-image 2K, 918 créditos cada, editadas
de 2026-10/fontes/fernando_balcao.jpg; arquivos em 2026-11/fontes/trend_nao_sim/) + foto do Cronos com a máquina.
NÃO: deixar o óleo do câmbio pra depois / esperar o câmbio dar tranco / troca só pelo bujão.
SIM: troca completa na Star, na máquina, com até 30% off na Black. Fechamento Black com WhatsApp. Trilha paga r15mil."""
import os, sys, subprocess, math
REPO = os.path.expanduser("~/staroleo-instagram"); sys.path.insert(0, REPO + "/_codigo")
from black_lib import *
from PIL import Image, ImageDraw
T = "/tmp/trend_nao_sim"; os.makedirs(T + "/f", exist_ok=True)
OUT = REPO + "/2026-11/trends/reel_trend_nao_sim.mp4"
AUD = REPO + "/_codigo/audio/trilha_r15mil.mp3"
FN = REPO + "/2026-11/fontes/trend_nao_sim/"
W, H, FPS = 1080, 1920, 30
RED = (229, 57, 53)
# (ini, fim, foto, fy, fx, zoom0, zoom1, rótulo, cor do rótulo, linha1, linha2, tremer)
CENAS = [
 (0.0, 2.5, FN + "nao.jpg", 0.40, 0.50, 1.00, 1.06, "NÃO", RED, "DEIXAR O ÓLEO DO CÂMBIO", "PRA DEPOIS", True),
 (2.5, 5.0, FN + "nao.jpg", 0.36, 0.48, 1.18, 1.24, "NÃO", RED, "ESPERAR O CÂMBIO", "DAR TRANCO", True),
 (5.0, 7.5, FN + "nao.jpg", 0.34, 0.47, 1.36, 1.42, "NÃO", RED, "TROCA PARCIAL,", "SÓ PELO BUJÃO", True),
 (7.5, 9.9, FN + "sim.jpg", 0.40, 0.52, 1.08, 1.00, "SIM!", GOLD, "TROCA COMPLETA", "NA STAR", False),
 (9.9, 12.0, REPO + "/2026-10/fontes/cronos/foto_cronos_elevador_maquina.jpg", 0.62, 0.5, 1.0, 1.08, "SIM!", GOLD,
  "NA MÁQUINA ESPECIALIZADA", "COM ATÉ 30% OFF", False),
]
VE = 12.0; END = 3.6; TOT = VE + END
FOTOS = {}
def foto(p, fy, fx):
    k = (p, fy, fx)
    if k not in FOTOS: FOTOS[k] = cover(carregar(p), int(W * 1.5), int(H * 1.5), fy=fy, fx=fx)
    return FOTOS[k]
def ease(p): p = max(0, min(1, p)); return 1 - (1 - p) ** 3
def contorno(d, y, t, f, cor, a=255):
    while d.textlength(t, font=f) > W - 80: f = bc(f.size - 4)
    w = d.textlength(t, font=f)
    d.text(((W - w) / 2, y), t, font=f, fill=cor + (a,), stroke_width=8, stroke_fill=(17, 18, 20, a))
def quadro(t):
    for (t0, t1, p, fy, fx, z0, z1, rot, cor, l1, l2, tremer) in CENAS:
        if t0 <= t < t1: break
    k = (t - t0) / (t1 - t0); z = z0 + (z1 - z0) * k
    base = foto(p, fy, fx); bw, bh = base.size
    cw, ch = int(bw / z), int(bh / z)
    cw, ch = min(cw, bw), min(ch, bh)
    dx = 0
    if tremer and (t - t0) < 0.9: dx = int(26 * math.sin((t - t0) * 2 * math.pi * 3.2) * (1 - (t - t0) / 0.9))
    x0 = (bw - cw) // 2 + dx; y0 = (bh - ch) // 2
    x0 = max(0, min(bw - cw, x0))
    c = base.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BICUBIC)
    c = grad(c, top=200, top_a=110, bot=820, bot_a=235)
    d = ImageDraw.Draw(c, "RGBA")
    p0 = ease((t - t0) / 0.22); p1 = ease((t - t0 - 0.25) / 0.3); p2 = ease((t - t0 - 0.55) / 0.3)
    if p0 > 0:  # rótulo NÃO / SIM! carimbado
        f = bc(int(230 * (1.25 - 0.25 * p0))); tw = d.textlength(rot, font=f)
        d.rounded_rectangle(((W - tw) / 2 - 40, 1205, (W + tw) / 2 + 40, 1205 + f.size * 1.02), radius=22,
                            fill=cor + (int(240 * p0),))
        d.text((W / 2, 1205 + f.size * 0.52), rot, font=f, fill=(GRAF if cor == GOLD else WHITE) + (int(255 * p0),), anchor="mm")
    if p1 > 0: contorno(d, 1500 - 18 * (1 - p1), l1, bc(92), WHITE, int(255 * p1))
    if p2 > 0: contorno(d, 1600 - 18 * (1 - p2), l2, bc(104), GOLD, int(255 * p2))
    d.text((W / 2, 1860), "@staroleo_rj", font=mrs(32), fill=(220, 221, 223, 220), anchor="mm")
    if t - t0 < 0.07 and t0 > 0: c = Image.blend(c, Image.new("RGB", (W, H), WHITE), 0.35)
    return c
def fechamento(t):
    c = Image.new("RGB", (W, H), GRAF); p = ease(t / 0.4)
    l = LOGO.resize((420, round(LOGO.height * 420 / LOGO.width)))
    c.paste(l, ((W - 420) // 2, 330), l)
    badge(c, 610, tam=0.85); d = ImageDraw.Draw(c)
    ctext(d, W, 760, "SIM PRA TROCA", bc(118), WHITE)
    ctext(d, W, 885, "COMPLETA. CHAMA A STAR.", bc(96), GOLD)
    y = selo(c, 1060, letra=None)
    d = ImageDraw.Draw(c)
    pill(d, W / 2, y + 60, f"WHATSAPP  {WA}", bc(64), GRAF, GOLD, padx=36, pady=18, center=True)
    ctext(d, W, y + 200, ENDERECO, mr(40), MUTED)
    ctext(d, W, y + 270, "*Cobrimos ofertas mediante orçamento. Consulte as condições.", mrs(28), MUTED)
    if p < 1: c = Image.blend(Image.new("RGB", (W, H), GRAF), c, p)
    return c
if __name__ == "__main__":
    n = round(TOT * FPS)
    for i in range(n):
        t = i / FPS
        (quadro(t) if t < VE else fechamento(t - VE)).save(f"{T}/f/{i:04d}.png", compress_level=1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{T}/f/%04d.png", "-i", AUD,
        "-filter_complex", f"[1:a]atrim=0:{TOT},afade=t=in:d=0.2,afade=t=out:st={TOT-1.0}:d=1.0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
        "-map", "0:v", "-map", "[a]", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT], check=True)
    print("ok", OUT, round(TOT, 2))
