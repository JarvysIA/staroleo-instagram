#!/usr/bin/env python3
"""Trend 'Keep Me In Your Thoughts' (lembrete bem-humorado do seu serviço; Scott Social, out/2026) na versão Star + Black.
Reel 9:16 sem gravação, 0 crédito: fotos do repositório com zoom lento + frases no ritmo:
'Me guarda no seu pensamento…' -> '…pra quando o câmbio começar a dar tranco' -> '…pra quando descobrir que nunca
trocou o óleo dele' -> '…e pra trocar com até 30% off' -> fechamento Black com WhatsApp. Trilha já paga (trend_feriado)."""
import os, sys, subprocess
REPO = os.path.expanduser("~/staroleo-instagram"); sys.path.insert(0, REPO + "/_codigo")
from black_lib import *
from PIL import Image, ImageDraw, ImageFilter
T = "/tmp/trend_pensamento"; os.makedirs(T + "/f", exist_ok=True)
OUT = REPO + "/2026-11/trends/reel_trend_pensamento.mp4"
AUD = REPO + "/_codigo/audio/trilha_trend_feriado.mp3"
F = REPO + "/2026-10/fontes/"
W, H, FPS = 1080, 1920, 30
# (início, fim, foto, fy, linha1, linha2 dourada, zoom0, zoom1)
CENAS = [
 (0.0, 3.2, F + "fernando_balcao.jpg", 0.45, "ME GUARDA NO SEU", "PENSAMENTO…", 1.0, 1.08),
 (3.2, 6.0, F + "cronos/foto_cronos_elevador_maquina.jpg", 0.4, "…PRA QUANDO O CÂMBIO", "COMEÇAR A DAR TRANCO", 1.12, 1.02),
 (6.0, 8.8, F + "cronos/foto_filtro_novo_x_velho.jpg", 0.45, "…PRA QUANDO DESCOBRIR QUE", "NUNCA TROCOU O ÓLEO DELE", 1.0, 1.1),
 (8.8, 11.6, F + "cronos/foto_carter_limpo_motul.jpg", 0.45, "…E PRA TROCAR NA BLACK", "COM ATÉ 30% OFF", 1.1, 1.0),
]
VE = 11.6; END = 3.6; TOT = VE + END
FOTOS = {}
def foto(p, fy):
    if p not in FOTOS:
        im = cover(carregar(p), int(W * 1.15), int(H * 1.15), fy=fy)
        FOTOS[p] = im
    return FOTOS[p]
def ease(p): p = max(0, min(1, p)); return 1 - (1 - p) ** 3
def contorno(d, y, t, f, cor, a=255):
    w = d.textlength(t, font=f)
    while w > W - 70: f = bc(f.size - 4); w = d.textlength(t, font=f)
    d.text(((W - w) / 2, y), t, font=f, fill=cor + (a,), stroke_width=8, stroke_fill=(17, 18, 20, a))
    return f.size
def quadro(t):
    for (t0, t1, p, fy, l1, l2, z0, z1) in CENAS:
        if t0 <= t < t1: break
    k = (t - t0) / (t1 - t0); z = z0 + (z1 - z0) * k
    base = foto(p, fy); bw, bh = base.size
    cw, ch = int(W * 1.15 / z), int(H * 1.15 / z)
    x0 = (bw - cw) // 2; y0 = (bh - ch) // 2
    c = base.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BICUBIC)
    c = grad(c, top=760, top_a=200, full=0.8)
    d = ImageDraw.Draw(c, "RGBA")
    p1 = ease((t - t0 - 0.05) / 0.3); p2 = ease((t - t0 - 0.45) / 0.3)
    if p1 > 0: contorno(d, 290 - 20 * (1 - p1), l1, bc(96), WHITE, int(255 * p1))
    if p2 > 0: contorno(d, 400 - 20 * (1 - p2), l2, bc(112), GOLD, int(255 * p2))
    if t0 < 0.1 and k > 0: pass
    d.text((W / 2, 1830), "@staroleo_rj", font=mrs(34), fill=(220, 221, 223, 230), anchor="mm")
    # flash curto na troca de cena
    if t - t0 < 0.08 and t0 > 0: c = Image.blend(c, Image.new("RGB", (W, H), WHITE), 0.35)
    return c
def fechamento(t):
    c = Image.new("RGB", (W, H), GRAF); p = ease(t / 0.4)
    l = LOGO.resize((420, round(LOGO.height * 420 / LOGO.width)))
    c.paste(l, ((W - 420) // 2, 330), l)
    badge(c, 610, tam=0.85); d = ImageDraw.Draw(c)
    ctext(d, W, 760, "JÁ ME GUARDOU?", bc(118), WHITE)
    ctext(d, W, 885, "ENTÃO CHAMA A STAR.", bc(104), GOLD)
    y = selo(c, 1060, letra=None)
    d = ImageDraw.Draw(c)
    pill(d, W / 2, y + 60, f"WHATSAPP  {WA}", bc(64), GRAF, GOLD, padx=36, pady=18, center=True)
    ctext(d, W, y + 200, ENDERECO, mr(40), MUTED)
    ctext(d, W, y + 270, "*Cobrimos ofertas mediante orçamento. Consulte as condições.", mrs(28), MUTED)
    if p < 1: c = Image.blend(Image.new("RGB", (W, H), GRAF), c, p)
    return c
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
