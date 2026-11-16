#!/usr/bin/env python3
"""Trend 'Lately on my SD card' (New Engen, nov/2026): gráfico de cartão SD + 'ultimamente no meu cartão de memória' +
despejo rápido dos clipes recentes. Versão Star, 0 crédito, sem gravação: 12 cortes de 0,7 s tirados dos reels de
serviço já publicados (Cronos, VW, Creta, Renegade), só a faixa do meio (y 480 a 1267), que não tem legenda,
dentro de um visor de câmera (REC, tempo, cantoneiras). Fechamento com o PRESENTE DO CÂMBIO da Black Friday
(slogan oficial em 2 linhas). Trilha já paga (trend_feriado). Saída 1080x1920, 30 fps, -14 LUFS."""
import os, sys, subprocess, glob
REPO = os.path.expanduser("~/staroleo-instagram"); sys.path.insert(0, REPO + "/_codigo")
from black_lib import *
from PIL import Image, ImageDraw
T = "/tmp/trend_cartao"; os.makedirs(T + "/f", exist_ok=True); os.makedirs(T + "/c", exist_ok=True)
OUT = REPO + "/2026-11/trends/reel_trend_cartao_memoria.mp4"
AUD = REPO + "/_codigo/audio/trilha_trend_feriado.mp3"
W, H, FPS = 1080, 1920, 30
SLOGAN1 = "ATÉ 30% OFF + R$ 250 EM SERVIÇOS"
SLOGAN2 = "(4 balanceamentos + alinhamento + higienização do ar)"
C = REPO + "/2026-10/lote-2026-10-23/reel_cronos_ramone_v2.mp4"
V = REPO + "/2026-11/lote-2026-11-05/reel_cambio_vw_black_voz.mp4"
R = REPO + "/2026-10/lote-2026-10-28/reel_renegade_preventiva.mp4"
K = REPO + "/2026-10/lote-2026-10-26/reel_creta_tampa_frontal.mp4"
# (vídeo, início, nome do arquivo no "cartão")
CLIPES = [(C, 0.5, "FILTRO_CRONOS"), (V, 4.4, "BORRA_VW"), (K, 6.2, "CORPO_VALVULA_CRETA"), (R, 6.2, "RENEGADE"),
          (C, 10.4, "MOTUL_CVTF"), (K, 21.2, "MAQUINA_STAR"), (V, 6.1, "VIRTUS"), (R, 30.2, "OLEO_VELHO"),
          (C, 13.6, "OLEO_SAINDO_LIMPO"), (V, 12.0, "CARTER_LIMPO"), (R, 36.0, "NIVEL_OK"), (R, 0.3, "FERNANDO")]
DUR = 0.7; NF = round(DUR * FPS)
WY, WH = 470, 787           # janela do visor
INTRO = 1.1; VE = INTRO + len(CLIPES) * DUR; END = 3.8; TOT = VE + END
# extrai os quadros de cada corte (só a faixa do meio, sem legenda)
for i, (src, t0, _) in enumerate(CLIPES):
    if not glob.glob(f"{T}/c/{i:02d}_*.png"):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0), "-i", src, "-frames:v", str(NF),
                        "-vf", f"fps={FPS},crop=1080:{WH}:0:480", f"{T}/c/{i:02d}_%03d.png"], check=True)
def ease(p): p = max(0, min(1, p)); return 1 - (1 - p) ** 3
def cartao_sd(d, cx, cy, s=1.0, a=255):
    w, h, n = 300 * s, 380 * s, 70 * s
    x0, y0 = cx - w / 2, cy - h / 2
    pts = [(x0, y0 + n), (x0 + n, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    d.polygon(pts, fill=(30, 31, 34, a), outline=GOLD + (a,), width=max(3, int(8 * s)))
    for k in range(5):  # contatos
        xx = x0 + n + 18 * s + k * 38 * s
        d.rectangle((xx, y0 + 22 * s, xx + 22 * s, y0 + 80 * s), fill=GOLD + (a,))
    f = bc(int(150 * s)); tw = d.textlength("SD", font=f)
    d.text((cx - tw / 2, y0 + 120 * s), "SD", font=f, fill=WHITE + (a,))
    f2 = bcb(int(40 * s)); t2 = "STAR · 64GB"; tw = d.textlength(t2, font=f2)
    d.text((cx - tw / 2, y0 + 300 * s), t2, font=f2, fill=GOLD + (a,))
def cantos(d, x0, y0, x1, y1, L=60, w=6):
    for (x, y, dx, dy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        d.line((x, y, x + dx * L, y), fill=WHITE, width=w); d.line((x, y, x, y + dy * L), fill=WHITE, width=w)
def titulo(d, a=255, dy=0):
    f1 = bc(92); f2 = bc(104)
    for (y, t, f, cor) in [(200 + dy, "ULTIMAMENTE NO CARTÃO", f1, WHITE), (300 + dy, "DE MEMÓRIA DA STAR", f2, GOLD)]:
        w = d.textlength(t, font=f)
        d.text(((W - w) / 2, y), t, font=f, fill=cor + (a,), stroke_width=6, stroke_fill=GRAF + (a,))
def quadro(t):
    c = Image.new("RGB", (W, H), GRAF); d = ImageDraw.Draw(c, "RGBA")
    titulo(d, int(255 * ease(t / 0.35)), int(-20 * (1 - ease(t / 0.35))))
    x0, y0, x1, y1 = 0, WY, W, WY + WH
    if t < INTRO:
        d.rectangle((x0, y0, x1, y1), fill=(24, 25, 28))
        p = ease(t / 0.45); cartao_sd(d, W / 2, y0 + WH / 2 + 120 * (1 - p), 1.15, int(255 * p))
        if t > 0.6:
            f = mrs(34); tx = "lendo cartão" + "." * (1 + int((t - 0.6) / 0.15) % 3)
            d.text((W / 2 - d.textlength("lendo cartão...", font=f) / 2, y1 - 80), tx, font=f, fill=MUTED)
        nome, k = "", 0
    else:
        k = min(int((t - INTRO) / DUR), len(CLIPES) - 1); j = min(int(((t - INTRO) - k * DUR) * FPS), NF - 1)
        fr = sorted(glob.glob(f"{T}/c/{k:02d}_*.png")); im = Image.open(fr[min(j, len(fr) - 1)]).convert("RGB")
        c.paste(im, (0, WY)); d = ImageDraw.Draw(c, "RGBA")
        if j < 2: d.rectangle((x0, y0, x1, y1), fill=(255, 255, 255, 90))  # flash do corte
        nome = CLIPES[k][2]
    # visor da câmera
    cantos(d, 40, y0 + 34, W - 40, y1 - 34)
    if int(t * 2) % 2 == 0: d.ellipse((76, y0 + 66, 106, y0 + 96), fill=(229, 57, 53))
    d.text((120, y0 + 60), "REC", font=bc(44), fill=WHITE, stroke_width=2, stroke_fill=GRAF)
    s = int(t); fr_ = int((t - s) * FPS)
    tc = f"00:00:{s:02d}:{fr_:02d}"; f = bcb(40)
    d.text((W - 80 - d.textlength(tc, font=f), y1 - 100), tc, font=f, fill=WHITE, stroke_width=2, stroke_fill=GRAF)
    bx = W - 160; by = y0 + 66  # bateria
    d.rectangle((bx, by, bx + 70, by + 32), outline=WHITE, width=4); d.rectangle((bx + 70, by + 9, bx + 78, by + 23), fill=WHITE)
    d.rectangle((bx + 8, by + 8, bx + 52, by + 24), fill=GOLD)
    # nome do arquivo e contador
    if nome:
        lab = f"DCIM/STAR/{nome}.MP4"; f = mrs(34)
        d.text(((W - d.textlength(lab, font=f)) / 2, y1 + 34), lab, font=f, fill=(225, 226, 228))
        cnt = f"{k + 1:02d}/{len(CLIPES):02d}"; f = bcb(40)
        d.text(((W - d.textlength(cnt, font=f)) / 2, y1 + 92), cnt, font=f, fill=GOLD)
        bw = 760; bx0 = (W - bw) / 2; prog = (t - INTRO) / (VE - INTRO)
        d.rounded_rectangle((bx0, y1 + 156, bx0 + bw, y1 + 166), radius=5, fill=(60, 62, 66))
        d.rounded_rectangle((bx0, y1 + 156, bx0 + bw * prog, y1 + 166), radius=5, fill=GOLD)
    pill(d, W / 2, 1530, "BLACK FRIDAY · 27 E 28/11", bc(46), GRAF, GOLD, padx=30, pady=12, center=True)
    d.text((W / 2, 1830), "@staroleo_rj", font=mrs(34), fill=(220, 221, 223, 230), anchor="mm")
    return c
def caixa_slogan(c, y):
    d = ImageDraw.Draw(c); f1 = bc(76)
    while d.textlength(SLOGAN1, font=f1) > W - 150: f1 = bc(f1.size - 2)
    f2 = mrs(34)
    while d.textlength(SLOGAN2, font=f2) > W - 150: f2 = mrs(f2.size - 1)
    h = f1.size + f2.size + 70
    d.rounded_rectangle((50, y, W - 50, y + h), radius=18, fill=PRETO, outline=GOLD, width=5)
    ctext(d, W, y + 22, SLOGAN1, f1, GOLD); ctext(d, W, y + 36 + f1.size, SLOGAN2, f2, WHITE)
    return y + h
FECH = None
def fechamento(t):
    global FECH
    if FECH is None:
        c = Image.new("RGB", (W, H), GRAF)
        l = LOGO.resize((380, round(LOGO.height * 380 / LOGO.width))); c.paste(l, ((W - 380) // 2, 300), l)
        d = ImageDraw.Draw(c)
        y = 560; y = pill(d, W / 2, y, "BLACK FRIDAY · 27 E 28/11", bc(54), GRAF, GOLD, padx=34, pady=14, center=True)
        y = 700; ctext(d, W, y, "O PRÓXIMO ARQUIVO", bc(110), WHITE); y += 112
        ctext(d, W, y, "PODE SER O SEU CARRO", bc(96), GOLD); y += 140
        y = caixa_slogan(c, y) + 30; d = ImageDraw.Draw(c)
        ctext(d, W, y, "Só na troca do óleo do câmbio · 10x sem juros e cobrimos ofertas*", mr(30), (225, 226, 228)); y += 80
        pill(d, W / 2, y, f"WHATSAPP  {WA}", bc(64), GRAF, GOLD, padx=36, pady=18, center=True)
        ctext(d, W, y + 130, ENDERECO, mr(40), MUTED)
        ctext(d, W, y + 195, "*Mediante apresentação do orçamento. Consulte as condições.", mrs(28), MUTED)
        FECH = c
    p = ease(t / 0.35)
    return FECH if p >= 1 else Image.blend(Image.new("RGB", (W, H), GRAF), FECH, p)
if __name__ == "__main__":
    n = round(TOT * FPS)
    for i in range(n):
        t = i / FPS
        (quadro(t) if t < VE else fechamento(t - VE)).save(f"{T}/f/{i:04d}.png", compress_level=1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{T}/f/%04d.png", "-i", AUD,
        "-filter_complex", f"[1:a]atrim=0:{TOT},afade=t=in:d=0.2,afade=t=out:st={TOT-1.0}:d=1.0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
        "-map", "0:v", "-map", "[a]", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "16",
        "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT], check=True)
    print("ok", OUT, round(TOT, 2))
