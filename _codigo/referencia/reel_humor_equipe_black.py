#!/usr/bin/env python3
"""Reel Star: vídeo de humor da equipe toda na frente da parede (BD0E5F71...MP4, 21/10) + fechamento Black November.
Fala do Fernando (Scribe): "Se cê tá com depressão, ansiedade, médico diagnosticou que cê tá com essas coisas,
fica dois dia com nós, que cê vai ver se não some isso tudinho que cê tem".
Parede STAR ÓLEO aparece o tempo todo: sem logo por cima; título só no teto (y < 270).
Uso: python3 reel_humor_equipe_black.py <pasta com src.mp4 e words.json (Scribe)> <saída.mp4>"""
import json, subprocess, os, sys
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from reel_lib import cor_video
from black_lib import *
WD, OUT = sys.argv[1], os.path.abspath(sys.argv[2])
os.chdir(WD); os.makedirs("t", exist_ok=True)
W, H, FPS = 1080, 1920, 30
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_trend_feriado.mp3"
GOLD_A = "&H0021C3F0&"; WHITE_A = "&H00FFFFFF&"
A, B = 0.90, 10.75; T_END = B - A; END = 4.0; TOT = T_END + END

# ---------- card final Black ----------
c = Image.new("RGB", (W, H), PRETO); d = ImageDraw.Draw(c)
badge(c, 330, tam=1.1)
y = 520
for ln, cor in (("FICA DOIS DIAS", WHITE), ("COM A GENTE.", GOLD)):
    ctext(d, W, y, ln, bc(140), cor); y += 150
faixa(c, y + 120, ang=-4, alt=80); y += 270
ctext(d, W, y, "SEU CARRO BEM CUIDADO.", bc(80), WHITE); y += 120
y = selo(c, y, letra=LETRA) + 40
y = pill(d, W / 2, y, "WHATSAPP (21) 97544-6417", bc(62), GRAF, GOLD, padx=34, pady=18, center=True) + 30
ctext(d, W, y, "Estr. dos Bandeirantes, 841 · Taquara", mr(40), (200, 201, 204)); y += 80
logo(c, 220, (W - 220) // 2, y + 10)
c.save("t/card.png")

src = "src.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(A), "-to", str(B), "-i", src,
    "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},{cor_video(src)},format=yuv420p",
    "-af", f"highpass=f=90,afftdn=nf=-28,afade=t=in:d=0.05,afade=t=out:st={T_END-0.08:.2f}:d=0.08,aresample=48000",
    "-ac", "2", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-c:a", "pcm_s16le", "t/v0.mov"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", "t/card.png", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
    "-t", str(END), "-vf", "format=yuv420p,fade=t=in:d=0.35", "-c:v", "libx264", "-crf", "14", "-c:a", "pcm_s16le", "t/end.mov"], check=True)
open("t/list.txt", "w").write(f"file '{os.path.abspath('t/v0.mov')}'\nfile '{os.path.abspath('t/end.mov')}'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "14",
    "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "t/joined.mov"], check=True)

vol = f"volume='if(lt(t,{T_END}),0.07,0.45)':eval=frame"
fc = (f"[0:a]loudnorm=I=-16:TP=-2,aresample=48000[s];[1:a]atrim=0:{TOT},{vol},afade=t=in:d=0.4,afade=t=out:st={TOT-1.0}:d=1.0[m];"
      f"[s][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:{TOT},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "t/joined.mov", "-stream_loop", "-1", "-i", MUSIC, "-filter_complex", fc,
    "-map", "[a]", "-ar", "48000", "t/mix.wav"], check=True)

def ts(x): x = max(x, 0); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Barlow Condensed ExtraBold,100,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,7,3,5,40,40,0,1
Style: Title,Barlow Condensed ExtraBold,84,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,6,3,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
def add(st, en, style, x, y, text, layer=1, extra=""):
    ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{{\\pos({x},{y}){extra}}}{text}")
POP = "\\fscx70\\fscy70\\t(0,140,\\fscx104\\fscy104)\\t(140,220,\\fscx100\\fscy100)"
g = lambda s: "{\\c" + GOLD_A + "}" + s + "{\\c" + WHITE_A + "}"
add(0.0, T_END, "Title", 540, 160, "O TRATAMENTO\\N" + g("DA EQUIPE STAR"), extra="\\fad(150,150)")
words = [(w["text"], w["start"] - A, w["end"] - A) for w in json.load(open("words.json")) if w["start"] >= A - 0.05]
groups, cur = [], []
for w in words:
    cur.append(w)
    if w[0][-1] in ".,!?" or len(cur) == 3 or len(" ".join(x[0] for x in cur)) > 16: groups.append(cur); cur = []
if cur: groups.append(cur)
clean = lambda s: s.upper().rstrip(".,!?")
for gi, grp in enumerate(groups):
    nxt = groups[gi + 1][0][1] if gi + 1 < len(groups) else T_END
    for k, w in enumerate(grp):
        st = w[1]; en = grp[k + 1][1] if k + 1 < len(grp) else min(grp[-1][2] + 0.45, nxt - 0.01, T_END)
        txt = " ".join((g(clean(x[0])) if j == k else clean(x[0])) for j, x in enumerate(grp))
        add(st, en, "Cap", 540, 1480, txt, layer=2, extra=POP if k == 0 else "")
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

gimg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = gimg.load()
for yy in range(H):
    a = int(200 * (1 - yy / 330) ** 1.3) if yy < 330 else (int(150 * min(1, (yy - 1250) / 600)) if yy > 1250 else 0)
    for x in range(W): px[x, yy] = (17, 18, 20, a)
gimg.save("t/grad.png")
fc = (f"movie=t/grad.png[gr];[0:v][gr]overlay=0:0:enable='lt(t,{T_END})'[v0];"
      "[v0]ass=t/subs.ass,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mov", "-i", "t/mix.wav", "-filter_complex", fc, "-map", "[v]", "-map", "1:a",
    "-t", f"{TOT:.2f}", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
print("ok", round(T_END, 2), round(TOT, 2))
