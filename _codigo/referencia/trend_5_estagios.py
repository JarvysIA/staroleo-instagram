#!/usr/bin/env python3
"""Trend '5 stages of being...' (Later, 13/11/2026) na versão Star, em carrossel (0 crédito, sem gravação):
'Os 5 estágios de quem nunca trocou o óleo do câmbio' — negação, raiva, negociação, tristeza, aceitação — e CTA com o
PRESENTE DO CÂMBIO da Black Friday (slogan oficial em 2 linhas) + selo das 3 condições + nota do cobrimos ofertas.
Fotos: quadros limpos (faixa do meio, sem legenda) dos reels de serviço já publicados (VW, Renegade, Cronos)."""
import os, sys, subprocess
REPO = os.path.expanduser("~/staroleo-instagram"); sys.path.insert(0, REPO + "/_codigo")
from black_lib import *
from PIL import Image, ImageDraw
O = REPO + "/2026-11/trends/"; T = "/tmp/trend_5est"; os.makedirs(T, exist_ok=True)
W, H = 1080, 1350
C = REPO + "/2026-10/lote-2026-10-23/reel_cronos_ramone_v2.mp4"
V = REPO + "/2026-11/lote-2026-11-05/reel_cambio_vw_black_voz.mp4"
R = REPO + "/2026-10/lote-2026-10-28/reel_renegade_preventiva.mp4"
SLOGAN1 = "ATÉ 30% OFF + R$ 250 EM SERVIÇOS"
SLOGAN2 = "(4 balanceamentos + alinhamento + higienização do ar)"
def quadro(src, t, nome):
    p = f"{T}/{nome}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src, "-frames:v", "1", "-vf", "crop=1080:787:0:480", p], check=True)
    return Image.open(p).convert("RGB")
ESTAGIOS = [
 (1, "NEGAÇÃO", (C, 3.0), "“Tranco? Impressão sua.”", "O carro já tá avisando faz tempo."),
 (2, "RAIVA", (V, 3.2), "“Logo agora esse tranco?!”", "Óleo vencido não escolhe hora."),
 (3, "NEGOCIAÇÃO", (R, 31.8), "“E se eu só completar o nível?”", "Completar não tira o óleo velho nem a borra."),
 (4, "TRISTEZA", (C, 9.0), "“Olha o que saiu do meu câmbio…”", "Borra no cárter e filtro saturado."),
 (5, "ACEITAÇÃO", (R, 33.2), "“Troca completa na Star.”", "Cárter limpo, filtro novo e óleo homologado na máquina."),
]
def rodape(c):
    logo(c, 150, (W - 150) // 2, H - 92)
def capa():
    ph = quadro(V, 0.8, "capa")
    c = Image.new("RGB", (W, H), GRAF); c.paste(ph, (0, 0))
    c = grad(c, top=0, top_a=0, bot=700, bot_a=255, full=0.25)
    d = ImageDraw.Draw(c)
    badge(c, 50, tam=0.8); d = ImageDraw.Draw(c)
    y = 700; ctext(d, W, y, "OS 5 ESTÁGIOS", bc(150), WHITE); y += 150
    ctext(d, W, y, "DE QUEM NUNCA TROCOU", bc(84), WHITE); y += 92
    ctext(d, W, y, "O ÓLEO DO CÂMBIO", bc(110), GOLD); y += 150
    ctext(d, W, y, "Em qual você está? Arrasta pro lado", mrs(38), (225, 226, 228))
    rodape(c); return c
def estagio(n, nome, src, frase, apoio):
    c = Image.new("RGB", (W, H), GRAF); d = ImageDraw.Draw(c)
    pill(d, W / 2, 46, f"ESTÁGIO {n} DE 5", bc(46), GRAF, GOLD, padx=28, pady=12, center=True)
    ctext(d, W, 120, nome, bc(150), WHITE if n < 5 else GOLD)
    ph = quadro(src[0], src[1], f"e{n}"); c.paste(ph, (0, 300))
    d = ImageDraw.Draw(c)
    f = bc(64); y = 300 + 787 + 26
    for ln in quebrar(d, frase, f, W - 100):
        ctext(d, W, y, ln, f, GOLD if n == 5 else WHITE); y += 70
    ctext(d, W, y + 4, apoio, mr(36), MUTED)
    rodape(c); return c
def cta():
    c = Image.new("RGB", (W, H), GRAF)
    l = LOGO.resize((300, round(LOGO.height * 300 / LOGO.width))); c.paste(l, ((W - 300) // 2, 50), l)
    d = ImageDraw.Draw(c); y = 250
    ctext(d, W, y, "PULA DIRETO", bc(130), WHITE); y += 128
    ctext(d, W, y, "PRO ESTÁGIO 5", bc(130), GOLD); y += 165
    y = pill(d, W / 2, y, "BLACK FRIDAY · 27 E 28/11", bc(50), GRAF, GOLD, padx=30, pady=12, center=True) + 22
    d = ImageDraw.Draw(c); f1 = bc(76)
    while d.textlength(SLOGAN1, font=f1) > W - 150: f1 = bc(f1.size - 2)
    f2 = mrs(34)
    while d.textlength(SLOGAN2, font=f2) > W - 150: f2 = mrs(f2.size - 1)
    h = f1.size + f2.size + 70
    d.rounded_rectangle((50, y, W - 50, y + h), radius=18, fill=PRETO, outline=GOLD, width=5)
    ctext(d, W, y + 22, SLOGAN1, f1, GOLD); ctext(d, W, y + 36 + f1.size, SLOGAN2, f2, WHITE); y += h + 18
    ctext(d, W, y, "Presente só na troca do óleo do câmbio, dias 27 e 28/11", mr(30), (225, 226, 228)); y += 58
    y = selo(c, y, letra=None, escala=0.85) + 30; d = ImageDraw.Draw(c)
    y = pill(d, W / 2, y, f"WHATSAPP  {WA}", bc(60), GRAF, GOLD, padx=36, pady=16, center=True) + 20
    ctext(d, W, y, ENDERECO, mr(36), MUTED); y += 52
    ctext(d, W, y, "*Cobrimos ofertas mediante apresentação do orçamento. Consulte as condições.", mrs(24), MUTED)
    return c
if __name__ == "__main__":
    pecas = [capa()] + [estagio(*e) for e in ESTAGIOS] + [cta()]
    for i, p in enumerate(pecas, 1): p.save(O + f"estagios_{i:02d}.jpg", quality=93)
    folha_previa([O + f"estagios_{i:02d}.jpg" for i in range(1, 8)], T + "/previa.jpg") if "folha_previa" in globals() else None
    print("ok")
