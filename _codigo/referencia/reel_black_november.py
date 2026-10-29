#!/usr/bin/env python3
"""Reel Black November da Star (06/11/2026). Locução John Edgard aprovada pelo Fernando em 29/10.
Cortes reais (Renegade 27/10, Creta 26/10) + fotos (Fernando no balcão, pneus) + textões das condições + fechamento Black."""
import subprocess, os, json, sys
os.chdir("/home/claude/blackreel"); os.makedirs("t", exist_ok=True)
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
W, H, FPS = 1080, 1920, 30
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_r15mil.mp3"
LOGO = "/home/claude/staroleo-instagram/_codigo/logo.png"
REN, CRE = "/home/claude/renegade/src", "/home/claude/creta/src"
FOT = "/home/claude/staroleo-instagram/2026-10/fontes/"
GOLD = "&H0021C3F0&"; WHITE = "&H00FFFFFF&"
GRADE = "curves=preset=strong_contrast,eq=saturation=1.45"
TAG709 = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
VO = 0.2; END = 3.4

def run(a): subprocess.run(a, check=True)
def enc(out): return ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p", out]

def broll(src, a, d, out, escuro=0.0):
    if os.environ.get("REUSE") and os.path.exists(out): return
    ex = f",eq=brightness=-{escuro}" if escuro else ""
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", src, "-t", str(d), "-vf",
         f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},format=yuv420p,{TAG709},{GRADE}{ex}"] + enc(out))

def foto(card_png, d, out, zoom=0.12, cx=0.5, cy=0.45):
    n = int(round(d * FPS))
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", card_png, "-vf",
         f"scale={W*2}:{H*2},zoompan=z='1+{zoom}*on/{n}':x='iw*{cx}-iw/zoom/2':y='ih*{cy}-ih/zoom/2':d={n}:s={W}x{H}:fps={FPS},format=yuv420p,{TAG709}",
         "-frames:v", str(n)] + enc(out))

# cartões das fotos
from black_lib import *
from PIL import ImageFilter
fb = cover(carregar(FOT + "fernando_balcao.jpg"), W, H, fy=0.2, fx=0.38); fb.save("t/card_fernando.png")
pn = Image.open("/home/claude/staroleo-instagram/2026-10/lote-2026-10-24/story_pneus_crystone.jpg").convert("RGB").crop((0, 0, 1080, 1150))
bg = pn.resize((W, H)).filter(ImageFilter.GaussianBlur(40)); bg = Image.blend(bg, Image.new("RGB", (W, H), (8, 8, 9)), 0.5)
bg.paste(pn, (0, (H - 1150) // 2 - 120)); bg.save("t/card_pneu.png")

# fechamento (PNG estático, com selo da Black)
c = Image.new("RGB", (W, H), PRETO); badge(c, 560, tam=1.0)
d = ImageDraw.Draw(c)
ctext(d, W, 700, "O SEU DESCONTO", bc(116), WHITE); ctext(d, W, 820, "TÁ NO WHATSAPP.", bc(116), GOLD)
faixa(c, 1030, ang=-4, alt=78)
y = selo(c, 1140, letra=None)
d = ImageDraw.Draw(c); pill(d, W / 2, y + 40, f"WHATSAPP  {WA}", bc(60), GRAF, GOLD, padx=36, pady=20, center=True)
ctext(d, W, y + 170, ENDERECO, mr(36), MUTED); logo(c, 200, (W - 200) // 2, 300)
c.save("t/end.png")

# ---------- linha do tempo (s de saída) ----------
SEGS = [
  ("b", (REN + "/2650.mov", 19.4), 1.75, 0.18),   # Black November na Star!
  ("b", (CRE + "/6239.mov", 2.3), 2.2, 0),        # Novembro inteiro, até 30%
  ("b", (CRE + "/6242.mov", 10.0), 2.35, 0),      # de desconto em produtos e serviços
  ("b", (REN + "/6286.mov", 3.0), 2.0, 0),        # troca do óleo do câmbio automático
  ("b", (REN + "/6288.mov", 5.0), 0.95, 0),       # óleo do motor
  ("f", "t/card_pneu.png", 1.55, 0),               # pneus, suspensão
  ("b", (CRE + "/6232.mov", 2.9), 2.3, 0),        # tudo em até 10x sem juros
  ("f", "t/card_fernando.png", 4.6, 0),            # achou mais barato... cobre a oferta
  ("b", (REN + "/2650.mov", 21.0), 2.9, 0),       # chama a Star no WhatsApp
]
parts, starts, t = [], [], 0.0
for i, (k, src, d, esc) in enumerate(SEGS):
    p = f"t/s{i}.mp4"
    if k == "b": broll(src[0], src[1], d, p, esc)
    else: foto(src, d, p, cx=0.5 if "pneu" in src else 0.45, cy=0.4)
    parts.append(p); starts.append(t); t += d
V_END = t; TOT = V_END + END
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", "t/end.png", "-t", str(END), "-vf", f"fps={FPS},format=yuv420p,{TAG709}"] + enc("t/end.mp4"))
parts.append("t/end.mp4")
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "t/joined.mp4"])

# ---------- áudio ----------
run(["ffmpeg", "-v", "error", "-y", "-i", "voz.mp3", "-af", "loudnorm=I=-16:TP=-2,aresample=48000", "-ac", "2", "t/voz.wav"])
vol = f"volume='if(lt(t,{V_END}),0.20,0.42)':eval=frame"
fc = (f"[0:a]adelay={int(VO*1000)}:all=1[v];[1:a]atrim=0:{TOT},{vol},afade=t=in:d=0.2,afade=t=out:st={TOT-1.0}:d=1.0[m];"
      f"[v][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:{TOT},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
run(["ffmpeg", "-v", "error", "-y", "-i", "t/voz.wav", "-i", MUSIC, "-filter_complex", fc, "-map", "[a]", "-ar", "48000", "t/mix.wav"])

# ---------- legendas ----------
LOGO = "/home/claude/staroleo-instagram/_codigo/logo.png"
GOLD = "&H0021C3F0&"; WHITE = "&H00FFFFFF&"   # cores ASS (o import do black_lib troca por tuplas)
def ts(x): x = max(x, 0); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Barlow Condensed ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,7,3,5,40,40,0,1
Style: Mega,Barlow Condensed ExtraBold,230,{GOLD},{GOLD},&H00090808,&H96000000,0,0,0,0,100,100,1,0,1,10,6,5,0,0,0,1
Style: MegaW,Barlow Condensed ExtraBold,120,&H00FFFFFF,&H00FFFFFF,&H00090808,&H96000000,0,0,0,0,100,100,1,0,1,8,5,5,0,0,0,1
Style: Badge,Barlow Condensed ExtraBold,64,&H00FFFFFF,&H00FFFFFF,&H00090808,&H00090808,0,0,0,0,100,100,2,0,3,18,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
def add(st, en, style, x, y, text, layer=1, extra=""):
    ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{{\\pos({x},{y}){extra}}}{text}")
POP = "\\fscx60\\fscy60\\t(0,160,\\fscx106\\fscy106)\\t(160,240,\\fscx100\\fscy100)"
g = lambda s: "{\\c" + GOLD + "}" + s + "{\\c" + WHITE + "}"

words = json.load(open("words.json"))
FIX = {(3, "30"): "30%", (32, "100"): "sem", (46, "cobra"): "cobre", (48, "alfeta."): "oferta."}
ws = []
for i, (w, a, b) in enumerate(words):
    if w == "%": ws[-1][2] = b; continue
    ws.append([FIX.get((len(ws), w), {"30": "30%", "100": "sem", "cobra": "cobre", "alfeta.": "oferta."}.get(w, w)), a, b])
# "cobra e alfeta" -> "cobre a oferta"
for i in range(len(ws) - 1):
    if ws[i][0] == "cobre" and ws[i + 1][0] == "e": ws[i + 1][0] = "a"
groups, cur = [], []
for w in ws:
    cur.append(w)
    if w[0][-1] in ".,!?:" or len(cur) == 3 or len(" ".join(x[0] for x in cur)) > 16:
        groups.append(cur); cur = []
if cur: groups.append(cur)
clean = lambda s: s.upper().rstrip(".,!?:")
for gi, grp in enumerate(groups):
    gs, ge = grp[0][1] + VO, grp[-1][2] + VO
    nxt = groups[gi + 1][0][1] + VO if gi + 1 < len(groups) else 999
    for k, w in enumerate(grp):
        st = w[1] + VO if k else gs
        en = (grp[k + 1][1] + VO) if k + 1 < len(grp) else min(ge + 0.15, nxt - 0.01)
        ps = [(g(clean(x[0])) if j == k else clean(x[0])) for j, x in enumerate(grp)]
        add(st, min(en, V_END), "Cap", 540, 1480, " ".join(ps), layer=2, extra=POP if k == 0 else "")

# textões
B = "\\fad(120,120)"
add(0.05, starts[1], "MegaW", 540, 760, "BLACK", extra=B + POP)
add(0.25, starts[1], "Mega", 540, 920, "NOVEMBER", extra=B + POP)
add(VO + 2.9, starts[3], "Mega", 540, 820, "ATÉ 30%", extra=B + POP)
add(VO + 4.0, starts[3], "MegaW", 540, 990, "DE DESCONTO", extra=B)
add(VO + 10.6, starts[7], "Mega", 540, 820, "10X", extra=B + POP)
add(VO + 11.3, starts[7], "MegaW", 540, 990, "SEM JUROS", extra=B)
add(VO + 14.8, starts[8], "MegaW", 540, 400, "COBRIMOS", extra=B + POP)
add(VO + 15.0, starts[8], "Mega", 540, 560, "OFERTAS", extra=B + POP)
add(starts[1], V_END, "Badge", 540, 300, "BLACK " + "{\\c" + GOLD + "}NOVEMBER", extra="\\fad(200,0)")
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

fc = (f"[1:v]format=rgba,scale=200:-1:flags=lanczos[ls];[0:v][ls]overlay=x=(W-w)/2:y=150:enable='lt(t,{starts[1]})'[v1];"
      f"[v1]ass=t/subs.ass,{TAG709}[v]")
run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mp4", "-loop", "1", "-framerate", str(FPS), "-i", LOGO, "-i", "t/mix.wav",
     "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
     "-profile:v", "high", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "reel_black_november.mp4"])
print("ok", [round(s, 2) for s in starts], round(V_END, 2), round(TOT, 2))
