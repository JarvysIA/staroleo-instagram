#!/usr/bin/env python3
"""Reel "boneco 3D do Fernando" - Black Friday do câmbio (18/11/2026).
Pedido do Fernando: estilo dos vídeos de IA com apresentador + gráficos (referência N.A-Films).
Caminho B aprovado: boneco 3D gerado a partir do vídeo IMG_6612 (gemini 2K, 918) + a fala REAL do Fernando
(IMG_6628, 14,7 s, sem clonar voz) + HeyGen Avatar 6 turbo (4.545). Condições valem o mês todo (Fernando, 18/11).
Sem os R$ 250 em serviços (Fernando: "não incluir").
Uso: python3 reel_boneco_black_cambio.py boneco_falando.mp4 fala.wav saida.mp4
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from star_lib import *
from black_lib import selo, estrela, PRETO
from reel_lib import HDR, ts, G
from PIL import Image, ImageDraw, ImageFilter

SRC, VOZ, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = 1080, 1920
WD = os.path.join(os.path.dirname(os.path.abspath(OUT)), "tmp_boneco"); os.makedirs(WD, exist_ok=True)
MUSIC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio", "trilha_r15mil.mp3")

FALA = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VOZ],
                            capture_output=True, text=True).stdout)
HOLD = 2.2                    # quadro final congelado com o fechamento
TOT = round(FALA + HOLD, 2)

# ---------- camada fixa do topo: degradê + logo + BLACK FRIDAY + validade ----------
top = Image.new("RGBA", (W, H), (0, 0, 0, 0))
g = Image.new("L", (1, H), 0)
for y in range(H):
    a = 0
    if y < 640: a = int(215 * (1 - y / 640) ** 1.15)
    if y > H - 620: a = max(a, int(230 * min(1, (y - (H - 620)) / 420) ** 1.2))
    g.putpixel((0, y), a)
top.paste(Image.new("RGBA", (W, H), GRAF + (255,)), (0, 0), g.resize((W, H)))
d = ImageDraw.Draw(top)
logo(top, 250, (W - 250) / 2, 52)
f1 = bc(178); f2 = bc(178)
t1, t2 = "BLACK ", "FRIDAY"
w1, w2 = d.textlength(t1, font=f1), d.textlength(t2, font=f2)
x0 = (W - w1 - w2) / 2; yb = 250
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
ds.text((x0 + 6, yb + 8), t1 + t2, font=f1, fill=(0, 0, 0, 200)); sh = sh.filter(ImageFilter.GaussianBlur(8))
top.alpha_composite(sh)
d.text((x0, yb), t1, font=f1, fill=WHITE); d.text((x0 + w1, yb), t2, font=f2, fill=GOLD)
pill(d, W / 2, 462, "NO CÂMBIO AUTOMÁTICO · VÁLIDO ATÉ 30/11", bc(44), GRAF, GOLD, padx=28, pady=10, center=True)
top.save(f"{WD}/topo.png")

# ---------- fechamento (sobre o quadro congelado) ----------
fim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fim.paste(Image.new("RGBA", (W, 760), (8, 8, 9, 236)), (0, H - 760))
dd = ImageDraw.Draw(fim)
y = selo(fim, H - 700, letra=None, conds=["ATÉ 30% OFF", "10X SEM JUROS", "COBRIMOS OFERTAS*"])
y += 40
pill(dd, W / 2, y, f"AGENDE NO WHATSAPP  {WA}", bc(64), GRAF, GOLD, padx=34, pady=16, center=True)
ctext(dd, W, y + 120, ENDERECO, mrs(38), WHITE)
ctext(dd, W, H - 70, "*Mediante apresentação do orçamento. Consulte as condições.", mrs(28), (200, 200, 200))
fim.save(f"{WD}/fim.png")

# ---------- textos animados (tempo de saída = tempo da fala) ----------
POP = "\\fscx70\\fscy70\\t(0,170,\\fscx106\\fscy106)\\t(170,260,\\fscx100\\fscy100)"
STY = HDR.replace("[Events]", "Style: Card,Barlow Condensed ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00141211,&H00000000,0,0,0,0,100,100,1,0,1,6,0,5,0,0,0,1\n"
                  "Style: Box,Barlow Condensed ExtraBold,122,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,26,0,5,0,0,0,1\n"
                  "Style: Nota,Manrope SemiBold,30,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1\n\n[Events]")
YC = 1610
ev = []
def card(a, b, txt, st="Card", y=YC):
    ev.append(f"Dialogue: 2,{ts(a)},{ts(b)},{st},,0,0,0,,{{\\pos(540,{y})\\fad(60,120){POP}}}{txt}")
card(1.30, 4.25, f"TROCA DO ÓLEO DO{G}\\NCÂMBIO AUTOMÁTICO")
card(4.25, 6.55, "ATÉ 30% OFF", "Box")
card(6.55, 8.75, f"10X SEM JUROS{G}\\NNOS CARTÕES")
card(8.75, FALA - 1.95, f"ACHOU MAIS BARATO?{G}\\NCOBRIMOS A OFERTA*")
card(FALA - 1.95, FALA, f"AGENDE AGORA{G}\\NPELO WHATSAPP")
NOTA = "*Mediante apresentação do orçamento. Consulte as condições."
ev.append(f"Dialogue: 3,{ts(8.75)},{ts(FALA)},Nota,,0,0,0,,{{\\pos(540,1850)\\fad(150,0)}}{NOTA}")
ass = f"{WD}/textos.ass"; open(ass, "w").write(STY + "\n".join(ev) + "\n")

# ---------- vídeo: boneco + cor viva + topo + textos + fechamento ----------
fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps=30,"
      f"eq=contrast=1.06:saturation=1.22:gamma=0.98,unsharp=5:5:0.5,"
      f"tpad=stop_mode=clone:stop_duration={HOLD + 1},trim=0:{TOT},setpts=PTS-STARTPTS,format=rgba[bv];"
      f"[bv][1:v]overlay=0:0[v1];[v1]ass={ass}[v2];"
      f"[2:v]format=rgba,fade=t=in:st={FALA - 0.05}:d=0.35:alpha=1[fm];"
      f"[v2][fm]overlay=0:0:enable='gte(t,{FALA - 0.05})',format=yuv420p,"
      f"setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[v];"
      f"[3:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{TOT},volume=1.0[voz];"
      f"[4:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{TOT},volume=0.16,"
      f"afade=t=in:d=0.4,afade=t=out:st={TOT - 0.8}:d=0.8[mus];"
      f"[voz][mus]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC,
                "-loop", "1", "-framerate", "30", "-i", f"{WD}/topo.png",
                "-loop", "1", "-framerate", "30", "-i", f"{WD}/fim.png",
                "-i", VOZ, "-i", MUSIC,
                "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(TOT),
                "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
print(OUT, TOT)
