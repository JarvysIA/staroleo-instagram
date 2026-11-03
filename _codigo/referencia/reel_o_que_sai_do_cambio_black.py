#!/usr/bin/env python3
"""Reel 'O que sai do câmbio' (11/11/2026, Black November). Fotos novas da pasta 'Novembro 26' (cárter sujo,
filtro velho x novo, cárter limpo, Spin e Mitsubishi na máquina) + 2 s do vídeo IMG_6155 (Motul Multi CVTF).
Sem locução: a voz foi gerada (364 créditos), mas a nuvem não conseguiu baixar o áudio (elevenlabsusercontent.com bloqueado).
Textões no centro, selo BLACK NOVEMBER no topo, trilha r15mil, card final Black."""
import subprocess, os, sys
W, H, FPS = 1080, 1920, 30
WD = "/home/claude/reel1111"; os.makedirs(WD + "/t", exist_ok=True); os.chdir(WD)
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from reel_lib import cor_video
N = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/Novembro 26/"
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_r15mil.mp3"
OUT = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-02/reel_o_que_sai_do_cambio.mp4"
TAG709 = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
def run(a): subprocess.run(a, check=True)
def enc(out): return ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p", out]

def card(src, name, fy=0.5, fx=0.5):
    im = grade(abrir(src).convert("RGB")); p = f"t/{name}.png"
    cover(im, W, H, fy=fy, fx=fx).save(p); return p

def foto(png, d, out, z0=1.0, z1=1.12, cx=0.5, cy=0.5):
    n = int(round(d * FPS))
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", png, "-vf",
         f"scale={W*2}:{H*2},zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw*{cx}-iw/zoom/2':y='ih*{cy}-ih/zoom/2':d={n}:s={W}x{H}:fps={FPS},format=yuv420p,{TAG709}",
         "-frames:v", str(n)] + enc(out))

def broll(src, a, d, out):
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", src, "-t", str(d), "-vf",
         f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},format=yuv420p,{cor_video(src)}"] + enc(out))

# cenas: (tipo, fonte, dur, textos [(linha, cor)])
SC = [
  ("f", card(N + "IMG_6204.HEIC", "carter_sujo", fy=0.5), 2.4, [("SABE O QUE SAI", "w"), ("DO SEU CÂMBIO?", "g")], (1.18, 1.04)),
  ("f", card(N + "IMG_6205.HEIC", "filtros_carter", fy=0.45), 2.2, [("ÓLEO VELHO", "w"), ("E BORRA NO CÁRTER", "g")], (1.0, 1.12)),
  ("f", card(N + "4a8b2f76-885c-4338-82b6-308d7c15e2ac.JPG", "filtro", fy=0.55), 2.2, [("FILTRO VELHO", "w"), ("SAI. ENTRA O NOVO.", "g")], (1.12, 1.0)),
  ("f", card(N + "IMG_6207.HEIC", "carter_limpo", fy=0.5), 2.0, [("CÁRTER", "w"), ("LIMPO", "g")], (1.0, 1.1)),
  ("b", (N + "IMG_6155.MOV", 0.3), 2.0, [("ÓLEO HOMOLOGADO", "w"), ("PELO FABRICANTE", "g")], None),
  ("f", card(N + "IMG_6199.HEIC", "spin", fy=0.5), 2.2, [("TROCA COMPLETA", "w"), ("NA MÁQUINA", "g")], (1.0, 1.1)),
  ("f", card(N + "IMG_6203.HEIC", "mitsubishi", fy=0.5), 2.0, [("NACIONAIS", "w"), ("E IMPORTADOS", "g")], (1.1, 1.0)),
]
parts, starts, t = [], [], 0.0
for i, (k, src, d, txt, z) in enumerate(SC):
    p = f"t/s{i}.mp4"
    if k == "b": broll(src[0], src[1], d, p)
    else: foto(src, d, p, z0=z[0], z1=z[1], cy=0.45)
    parts.append(p); starts.append(t); t += d
V_END = t; END = 3.4; TOT = V_END + END

# card final Black
c = Image.new("RGB", (W, H), PRETO); badge(c, 560, tam=1.0); d = ImageDraw.Draw(c)
ctext(d, W, 700, "O SEU DESCONTO", bc(116), WHITE); ctext(d, W, 820, "TÁ NO WHATSAPP.", bc(116), GOLD)
faixa(c, 1030, ang=-4, alt=78); y = selo(c, 1140, letra=None); d = ImageDraw.Draw(c)
pill(d, W / 2, y + 40, f"WHATSAPP  {WA}", bc(60), GRAF, GOLD, padx=36, pady=20, center=True)
ctext(d, W, y + 170, ENDERECO, mr(36), MUTED); logo(c, 200, (W - 200) // 2, 300); c.save("t/end.png")
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", "t/end.png", "-t", str(END), "-vf", f"fps={FPS},format=yuv420p,{TAG709}"] + enc("t/end.mp4"))
parts.append("t/end.mp4")
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "t/joined.mp4"])

# áudio: trilha + loudnorm
run(["ffmpeg", "-v", "error", "-y", "-i", MUSIC, "-af",
     f"atrim=0:{TOT},afade=t=in:d=0.2,afade=t=out:st={TOT-1.2}:d=1.2,loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", "t/mix.wav"])

# textos ASS
GA = "&H0021C3F0&"; WA_ = "&H00FFFFFF&"
def ts(x): x = max(x, 0); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: W,Barlow Condensed ExtraBold,128,&H00FFFFFF,&H00FFFFFF,&H00090808,&H96000000,0,0,0,0,100,100,1,0,1,8,5,5,0,0,0,1
Style: G,Barlow Condensed ExtraBold,128,{GA},{GA},&H00090808,&H96000000,0,0,0,0,100,100,1,0,1,8,5,5,0,0,0,1
Style: Badge,Barlow Condensed ExtraBold,64,&H00FFFFFF,&H00FFFFFF,&H00090808,&H00090808,0,0,0,0,100,100,2,0,3,18,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
POP = "\\fad(80,100)\\fscx60\\fscy60\\t(0,160,\\fscx106\\fscy106)\\t(160,240,\\fscx100\\fscy100)"
ev = []
for i, (k, src, d, txt, z) in enumerate(SC):
    a, b = starts[i], starts[i] + d
    for j, (ln, col) in enumerate(txt):
        st = a + 0.05 + j * 0.25
        ev.append(f"Dialogue: 1,{ts(st)},{ts(b - 0.03)},{'G' if col == 'g' else 'W'},,0,0,0,,{{\\pos(540,{1300 + j*140}){POP}}}{ln}")
ev.append(f"Dialogue: 2,{ts(0)},{ts(V_END)},Badge,,0,0,0,,{{\\pos(540,300)\\fad(200,0)}}BLACK {{\\c{GA}}}NOVEMBER")
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

# escurece a parte de baixo (leitura) e queima os textos
run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mp4", "-i", "t/mix.wav", "-filter_complex",
     f"[0:v]drawbox=x=0:y=1150:w={W}:h=560:color=black@0.35:t=fill:enable='lt(t,{V_END})',ass=t/subs.ass,{TAG709}[v]",
     "-map", "[v]", "-map", "1:a", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
     "-profile:v", "high", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT])
print("ok", [round(s, 2) for s in starts], round(V_END, 2), round(TOT, 2))
