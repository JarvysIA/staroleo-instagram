#!/usr/bin/env python3
"""Reel 'Olha o que saiu desse câmbio' (VW na Star, material de 05/11/2026 gravado pela equipe, Black November).
Ordem aprovada pelo Fernando em 05/11. Locução aprovada, mas a nuvem não baixa áudio da ElevenLabs (403),
então o texto da locução virou textões na tela. Trilha corporativa_m1 (paga), card final Black."""
import subprocess, os, sys
W, H, FPS = 1080, 1920, 30
WD = "/home/claude/v1105"; os.makedirs(WD + "/t", exist_ok=True); os.chdir(WD)
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from reel_lib import cor_video
S = WD + "/src/"
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_corporativa_m1.mp3"
OUT = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-05/reel_cambio_vw_black_voz.mp4"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
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

def broll(src, a, d, out, lento=1.0):
    # lento=2: clipe de 60 fps em câmera lenta (cada quadro vira um quadro de 30 fps)
    pre = f"setpts={lento}*PTS," if lento != 1 else ""
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(d / lento), "-i", src, "-vf",
         f"{pre}scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},format=yuv420p,{cor_video(src)}",
         "-t", str(d)] + enc(out))

# cenas: (tipo, fonte, dur, textos, zoom/lento); textos None = continua o texto da cena anterior
SC = [
  ("b", (S + "34bc0e4e-IMG_4849.MOV", 2.9), 2.6, None, 2.0),
  ("b", (S + "IMG_4850.MOV", 33.8), 1.8, None, 1.0),
  ("b", (S + "IMG_4850.MOV", 36.6), 1.0, None, 1.0),
  ("b", (S + "IMG_4851.MOV", 59.4), 1.2, None, 1.0),
  ("b", (S + "ceb9a521-IMG_4841.MOV", 0.2), 1.2, None, 1.0),
  ("b", (S + "IMG_4848.MOV", 39.0), 1.1, None, 1.0),
  ("f", card(S + "IMG_4853.jpg", "filtros", fy=0.5), 1.0, None, (1.0, 1.06)),
  ("b", (S + "IMG_4854.MOV", 2.0), 1.0, None, 1.0),
  ("b", (S + "IMG_4855.MOV", 15.0), 1.0, None, 1.0),
  ("f", card(S + "IMG_4856.jpg", "carter_limpo", fy=0.5), 1.4, None, (1.08, 1.0)),
  ("b", (S + "e1e7efac-IMG_4872.MP4", 6.5), 1.2, None, 1.0),
  ("b", (S + "0f804601-IMG_4873.MP4", 9.4), 1.1, None, 1.0),
  ("b", (S + "IMG_4850.MOV", 25.2), 2.6, [("ATÉ 30%", "g"), ("DE DESCONTO", "w")], 1.0),
  ("b", (S + "IMG_4851.MOV", 17.4), 1.6, [("10X", "g"), ("SEM JUROS", "w")], 1.0),
  ("b", (S + "IMG_4848.MOV", 7.2), 1.6, [("COBRIMOS", "w"), ("OFERTAS", "g")], 1.0),
]
parts, starts, t = [], [], 0.0
for i, (k, src, d, txt, z) in enumerate(SC):
    p = f"t/s{i}.mp4"
    if k == "b": broll(src[0], src[1], d, p, lento=z)
    else: foto(src, d, p, z0=z[0], z1=z[1], cy=0.47)
    parts.append(p); starts.append(t); t += d
V_END = t; END = 3.0; TOT = V_END + END; VO = 0.3

# card final Black (mesmo dos reels de novembro)
c = Image.new("RGB", (W, H), PRETO); badge(c, 560, tam=1.0); d = ImageDraw.Draw(c)
ctext(d, W, 700, "O SEU DESCONTO", bc(116), WHITE); ctext(d, W, 820, "TÁ NO WHATSAPP.", bc(116), GOLD)
faixa(c, 1030, ang=-4, alt=78); y = selo(c, 1140, letra=None); d = ImageDraw.Draw(c)
pill(d, W / 2, y + 40, f"WHATSAPP  {WA}", bc(60), GRAF, GOLD, padx=36, pady=20, center=True)
ctext(d, W, y + 170, ENDERECO, mr(36), MUTED); logo(c, 200, (W - 200) // 2, 300); c.save("t/end.png")
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", "t/end.png", "-t", str(END), "-vf", f"fps={FPS},format=yuv420p,{TAG709}"] + enc("t/end.mp4"))
parts.append("t/end.mp4")
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "t/joined.mp4"])

run(["ffmpeg", "-v", "error", "-y", "-i", "voz/voz.mp3", "-af", "loudnorm=I=-16:TP=-2,aresample=48000", "-ac", "2", "t/voz.wav"])
vol = f"volume='if(lt(t,{VO+22.7}),0.18,0.40)':eval=frame"
fc = (f"[0:a]adelay={int(VO*1000)}:all=1[v];[1:a]atrim=0:{TOT},{vol},afade=t=in:d=0.2,afade=t=out:st={TOT-1.0}:d=1.0[m];"
      f"[v][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:{TOT},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
run(["ffmpeg", "-v", "error", "-y", "-i", "t/voz.wav", "-i", MUSIC, "-filter_complex", fc, "-map", "[a]", "-ar", "48000", "t/mix.wav"])

GA = "&H0021C3F0&"
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
Style: Cap,Barlow Condensed ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,7,3,5,40,40,0,1
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
    for j, (ln, col) in enumerate(txt):
        st = a + 0.05 + j * 0.25
        ev.append(f"Dialogue: 1,{ts(st)},{ts(b - 0.03)},{'G' if col == 'g' else 'W'},,0,0,0,,{{\\pos(540,{860 + j*150}){POP}}}{ln}")
import json
words = json.load(open("voz/words_raw.json"))
ws = []
for w, a, b in words:
    if w == "%": ws[-1][0] += "%"; ws[-1][2] = b; continue
    ws.append([{"Olho": "Óleo"}.get(w, w), a, b])
groups, cur = [], []
for w in ws:
    cur.append(w)
    if w[0][-1] in ".,!?" or len(cur) == 3 or len(" ".join(x[0] for x in cur)) > 16:
        groups.append(cur); cur = []
if cur: groups.append(cur)
GOLDC = "&H0021C3F0&"; g = lambda x: "{\\c" + GOLDC + "}" + x + "{\\c&H00FFFFFF&}"
clean = lambda x: x.upper().rstrip(".,!?")
BLK = starts[12]
for gi, grp in enumerate(groups):
    gs = grp[0][1] + VO
    if gs >= BLK - 0.05: break
    nxt = groups[gi + 1][0][1] + VO if gi + 1 < len(groups) else 999
    for k, w in enumerate(grp):
        st = w[1] + VO if k else gs
        en = (grp[k + 1][1] + VO) if k + 1 < len(grp) else min(grp[-1][2] + VO + 0.15, nxt - 0.01)
        ps = [(g(clean(x[0])) if j == k else clean(x[0])) for j, x in enumerate(grp)]
        ev.append(f"Dialogue: 2,{ts(st)},{ts(min(en, BLK))},Cap,,0,0,0,,{{\\pos(540,1480)}}" + " ".join(ps))
ev.append(f"Dialogue: 2,{ts(0)},{ts(V_END)},Badge,,0,0,0,,{{\\pos(540,300)\\fad(200,0)}}BLACK {{\\c{GA}}}NOVEMBER")
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mp4", "-i", "t/mix.wav", "-filter_complex",
     f"[0:v]drawbox=x=0:y=0:w={W}:h={H}:color=black@0.40:t=fill:enable='between(t,{starts[12]},{V_END})',ass=t/subs.ass,{TAG709}[v]",
     "-map", "[v]", "-map", "1:a", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
     "-profile:v", "high", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT])
print("ok", [round(s, 2) for s in starts], round(V_END, 2), round(TOT, 2))
