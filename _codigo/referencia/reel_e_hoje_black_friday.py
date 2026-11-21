#!/usr/bin/env python3
"""Reel 'É HOJE · Black Friday da Star' (feed de sexta 27/11/2026 07h10, 1º dia do presente do câmbio).
Montagem de fotos e b-roll do acervo nunca usados (Fiat Toro IMG_2049, Honda CR-V IMG_1991, Honda Fit IMG_2039 e
IMG_2118, b-roll do cárter com borra IMG_2548.MOV e do filtro sujo x novo IMG_1938.MOV), locução John Edgard
(1 take, 401 créditos, flow HT9VjwBx9Co8fXq75A6J), textões por frase (tempos pelo silencedetect da locução,
porque a transcrição local não instalou nesta sessão), trilha corporativa_m1 e card final com o slogan oficial.
Fontes da locução em 2026-11/fontes/e_hoje/."""
import subprocess, os, sys
W, H, FPS = 1080, 1920, 30
WD = "/home/claude/w2011"; os.makedirs(WD + "/t", exist_ok=True); os.chdir(WD)
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from star_lib import abrir, grade
from reel_lib import cor_video
from PIL import Image, ImageDraw
T = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/Tudo até Outubro 26/"
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_corporativa_m1.mp3"
VOZ = "/home/claude/staroleo-instagram/2026-11/fontes/e_hoje/locucao_e_hoje.mp3"
OUT = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-20/reel_e_hoje_black_friday.mp4"
TAG709 = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
def run(a): subprocess.run(a, check=True)
def enc(out): return ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p", out]

def card(src, name, fy=0.5, fx=0.5, box=None):
    im = grade(abrir(src).convert("RGB"))
    if box: w, h = im.size; im = im.crop((int(box[0]*w), int(box[1]*h), int(box[2]*w), int(box[3]*h)))
    p = f"t/{name}.png"; cover(im, W, H, fy=fy, fx=fx).save(p); return p

def foto(png, d, out, z0=1.0, z1=1.12, cx=0.5, cy=0.5):
    n = int(round(d * FPS))
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", png, "-vf",
         f"scale={W*2}:{H*2},zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw*{cx}-iw/zoom/2':y='ih*{cy}-ih/zoom/2':d={n}:s={W}x{H}:fps={FPS},format=yuv420p,{TAG709}",
         "-frames:v", str(n)] + enc(out))

def broll(src, a, d, out, cx=0.5):
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(d), "-i", src, "-vf",
         f"scale=-2:{H}:flags=lanczos,crop={W}:{H}:(iw-{W})*{cx}:0,fps={FPS},format=yuv420p,{cor_video(src)}",
         "-t", str(d)] + enc(out))

TORO, CRV, FIT3, FIT1 = T + "IMG_2049.HEIC", T + "IMG_1991.HEIC", T + "IMG_2039.HEIC", T + "IMG_2118.HEIC"
VO = 0.3
# (tipo, fonte, dur, textos)
SC = [
  ("f", card(TORO, "toro", fy=0.3, box=(0, 0, 1, 0.62)), 2.75, [("É HOJE", "g"), ("BLACK FRIDAY", "w"), ("DA STAR", "w")], (1.0, 1.10)),
  ("f", card(CRV, "crv", fy=0.3, box=(0, 0, 1, 0.62)), 1.25, [("HOJE E AMANHÃ", "w"), ("27 E 28/11", "g")], (1.08, 1.0)),
  ("b", (T + "IMG_2548.MOV", 0.2, 0.5), 3.15, [("QUEM TROCAR", "w"), ("O ÓLEO DO CÂMBIO", "g")], None),
  ("f", card(FIT3, "fit3", fy=0.3, box=(0, 0, 1, 0.62)), 2.25, [("ATÉ 30% OFF", "g"), ("+ R$ 250", "w"), ("EM SERVIÇOS", "w")], (1.0, 1.08)),
  ("f", card(FIT1, "fit1", fy=0.3, box=(0, 0, 1, 0.62)), 2.35, None, (1.08, 1.0)),
  ("b", (T + "IMG_1938.MOV", 0.6, 0.5), 4.2, [("4 BALANCEAMENTOS", "w"), ("+ ALINHAMENTO", "w"), ("+ HIGIENIZAÇÃO", "g"), ("DO AR", "g")], None),
  ("f", card(CRV, "crv_maq", fy=0.85, box=(0.1, 0.5, 0.95, 1.0)), 3.2, [("TROCA COMPLETA", "w"), ("NA MÁQUINA", "g")], (1.0, 1.10)),
  ("f", card(TORO, "toro_maq", fy=0.85, box=(0.15, 0.5, 0.9, 1.0)), 2.2, [("MANDA O MODELO", "w"), ("NO WHATSAPP", "g")], (1.10, 1.0)),
  ("f", card(FIT3, "fit3_maq", fy=0.85, box=(0.05, 0.5, 0.9, 1.0)), 2.15, [("AQUI NA STAR", "w"), ("A GENTE RESOLVE.", "g")], (1.0, 1.08)),
]
parts, starts, t = [], [], 0.0
for i, (k, src, d, txt, z) in enumerate(SC):
    p = f"t/s{i}.mp4"
    if k == "b": broll(src[0], src[1], d, p, cx=src[2])
    else: foto(src, d, p, z0=z[0], z1=z[1], cy=0.47)
    parts.append(p); starts.append(t); t += d
V_END = t; END = 3.4; TOT = V_END + END

# card final: presente do câmbio com o slogan oficial em 2 linhas
c = Image.new("RGB", (W, H), PRETO); logo(c, 200, (W - 200) // 2, 300); badge(c, 560, tam=1.0)
d = ImageDraw.Draw(c)
ctext(d, W, 680, "HOJE E AMANHÃ", bc(120), WHITE); ctext(d, W, 805, "27 E 28/11", bc(120), GOLD)
faixa(c, 990, ang=-4, alt=74, txt="BLACK FRIDAY")
d = ImageDraw.Draw(c); y = 1110
S1, S2 = "ATÉ 30% OFF + R$ 250 EM SERVIÇOS", "(4 balanceamentos + alinhamento + higienização do ar)"
f1 = bc(80)
while d.textlength(S1, font=f1) > W - 150: f1 = bc(f1.size - 2)
f2 = mrs(36)
while d.textlength(S2, font=f2) > W - 150: f2 = mrs(f2.size - 1)
h = f1.size + f2.size + 74
d.rounded_rectangle((50, y, W - 50, y + h), radius=18, fill=PRETO, outline=GOLD, width=5)
ctext(d, W, y + 22, S1, f1, GOLD); ctext(d, W, y + 36 + f1.size, S2, f2, WHITE); y += h + 30
ctext(d, W, y, "Só na troca do óleo do câmbio automático", mr(36), (225, 226, 228)); y += 80
pill(d, W / 2, y + 30, f"WHATSAPP  {WA}", bc(60), GRAF, GOLD, padx=36, pady=20, center=True)
ctext(d, W, y + 160, "Estr. dos Bandeirantes, 841", mr(36), MUTED); c.save("t/end.png")
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", "t/end.png", "-t", str(END), "-vf", f"fps={FPS},format=yuv420p,{TAG709}"] + enc("t/end.mp4"))
parts.append("t/end.mp4")
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "t/joined.mp4"])

run(["ffmpeg", "-v", "error", "-y", "-i", VOZ, "-af", "loudnorm=I=-16:TP=-2,aresample=48000", "-ac", "2", "t/voz.wav"])
VEND = VO + 23.2
vol = f"volume='if(lt(t,{VEND}),0.16,0.40)':eval=frame"
fc = (f"[0:a]adelay={int(VO*1000)}:all=1[v];[1:a]atrim=0:{TOT},{vol},afade=t=in:d=0.2,afade=t=out:st={TOT-1.0}:d=1.0[m];"
      f"[v][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:{TOT},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
run(["ffmpeg", "-v", "error", "-y", "-i", "t/voz.wav", "-stream_loop", "-1", "-i", MUSIC, "-filter_complex", fc, "-map", "[a]", "-ar", "48000", "t/mix.wav"])

GA = "&H0021C3F0&"
def ts(x): x = max(x, 0); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: W,Barlow Condensed ExtraBold,124,&H00FFFFFF,&H00FFFFFF,&H00090808,&H96000000,0,0,0,0,100,100,1,0,1,8,5,5,0,0,0,1
Style: G,Barlow Condensed ExtraBold,124,{GA},{GA},&H00090808,&H96000000,0,0,0,0,100,100,1,0,1,8,5,5,0,0,0,1
Style: Badge,Barlow Condensed ExtraBold,64,&H00FFFFFF,&H00FFFFFF,&H00090808,&H00090808,0,0,0,0,100,100,2,0,3,18,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
POP = "\\fad(80,100)\\fscx60\\fscy60\\t(0,160,\\fscx106\\fscy106)\\t(160,240,\\fscx100\\fscy100)"
ev = []
for i, (k, src, d, txt, z) in enumerate(SC):
    if txt is None: continue
    a = starts[i]; j2 = i + 1
    while j2 < len(SC) and SC[j2][3] is None: j2 += 1
    b = starts[j2] if j2 < len(SC) else V_END
    n = len(txt); y0 = (1440 if k == "f" else 1000) - (n - 1) * 70
    for j, (ln, col) in enumerate(txt):
        st = a + 0.05 + j * 0.22
        ev.append(f"Dialogue: 1,{ts(st)},{ts(b - 0.03)},{'G' if col == 'g' else 'W'},,0,0,0,,{{\\pos(540,{y0 + j*140}){POP}}}{ln}")
ev.append(f"Dialogue: 2,{ts(0)},{ts(V_END)},Badge,,0,0,0,,{{\\pos(540,300)\\fad(200,0)}}BLACK {{\\c{GA}}}FRIDAY")
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mp4", "-i", "t/mix.wav", "-filter_complex",
     f"[0:v]ass=t/subs.ass,{TAG709}[v]",
     "-map", "[v]", "-map", "1:a", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
     "-profile:v", "high", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT])
print("ok", [round(s, 2) for s in starts], round(V_END, 2), round(TOT, 2))
