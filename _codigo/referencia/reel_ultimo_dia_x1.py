#!/usr/bin/env python3
"""Reel Star (feed de sábado 28/11/2026 07h10, ÚLTIMO DIA do presente do câmbio): Fernando na frente da BMW X1 no elevador,
com a máquina Höche, os Mobil e o filtro WFC (Câmbio BMW X1/IMG_0650.MOV 0,85 a 12,85 s: "Troca de óleo de câmbio automático
é aqui na Star Serviços Automotivos. Trabalhamos com excelência, produtos de primeira linha, máquina especializada... parcelamos
em dez vezes sem juros" + IMG_0647.MOV 8,55 a 11,95 s: "Vem pra cá, cuida do seu câmbio quem entende do assunto. Vem pra melhor,
vem pra Star.") + card final ÚLTIMO DIA com o slogan oficial. Ficaram de fora "melhor preço da região" e "clique no botão abaixo".
Palavras do Scribe na linha do tempo de 2026-11/fontes/dica_x1/audio_x1_0647_0650_0651.mp3 (0647 em 0 s, 0650 em 12,938 s, 0651 em 29,343 s).
Mesmo formato do reel de 22/11 (reel_dica_mercedes_black.py).
Uso: python3 reel_ultimo_dia_x1.py <pasta de trabalho> <saída.mp4>"""
import json, subprocess, os, sys
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from reel_lib import cor_video
from black_lib import *
WD, OUT = sys.argv[1], os.path.abspath(sys.argv[2])
os.makedirs(WD, exist_ok=True); os.chdir(WD); os.makedirs("t", exist_ok=True)
U = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/Câmbio Automático_/Câmbio BMW X1/"
WORDS = "/home/claude/staroleo-instagram/2026-11/fontes/dica_x1/words_scribe.json"
W, H, FPS = 1080, 1920, 30
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_corporativa_m1.mp3"
GOLD_A = "&H0021C3F0&"; WHITE_A = "&H00FFFFFF&"
CLIPS = [(U + "IMG_0650.MOV", 0.85, 12.85, 12.938), (U + "IMG_0647.MOV", 8.55, 11.95, 0.0)]
END = 3.6

# card final: ÚLTIMO DIA + slogan oficial em 2 linhas
c = Image.new("RGB", (W, H), PRETO); logo(c, 200, (W - 200) // 2, 280); badge(c, 540, tam=1.0)
d = ImageDraw.Draw(c)
ctext(d, W, 660, "ÚLTIMO DIA", bc(150), GOLD); ctext(d, W, 820, "HOJE, SÁBADO 28/11", bc(84), WHITE)
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
ctext(d, W, y + 160, "Estr. dos Bandeirantes, 841", mr(36), MUTED)
c.save("t/card.png")

parts, words, off = [], [], 0.0
for i, (src, a, b, j) in enumerate(CLIPS):
    dur = b - a
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", src,
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},{cor_video(src)},format=yuv420p",
        "-af", f"highpass=f=90,afftdn=nf=-28,afade=t=in:d=0.05,afade=t=out:st={dur-0.08:.2f}:d=0.08,aresample=48000",
        "-ac", "2", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-c:a", "pcm_s16le", f"t/v{i}.mov"], check=True)
    parts.append(f"t/v{i}.mov")
    for w in json.load(open(WORDS)):
        if j + a - 0.05 <= w["start"] < j + b:
            words.append((w["text"], w["start"] - j - a + off, w["end"] - j - a + off))
    off += dur
T_END = off; TOT = T_END + END
subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", "t/card.png", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
    "-t", str(END), "-vf", "format=yuv420p,fade=t=in:d=0.35", "-c:v", "libx264", "-crf", "14", "-c:a", "pcm_s16le", "t/end.mov"], check=True)
parts.append("t/end.mov")
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
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
Style: Cap,Barlow Condensed ExtraBold,104,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,7,3,5,40,40,0,1
Style: TagG,Barlow Condensed ExtraBold,46,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,3,0,3,14,0,5,0,0,0,1
Style: TagB,Barlow Condensed ExtraBold,40,&H0021C3F0,&H0021C3F0,&H00141211,&H00141211,0,0,0,0,100,100,3,0,3,12,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
def add(st, en, style, x, y, text, layer=1, extra=""):
    ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{{\\pos({x},{y}){extra}}}{text}")
POP = "\\fscx70\\fscy70\\t(0,140,\\fscx104\\fscy104)\\t(140,220,\\fscx100\\fscy100)"
g = lambda s: "{\\c" + GOLD_A + "}" + s + "{\\c" + WHITE_A + "}"
add(0.0, T_END, "TagG", 540, 1255, "DICA DO FERNANDO", extra="\\fad(150,150)")
add(0.0, T_END, "TagB", 540, 1560, "BLACK FRIDAY ★ ÚLTIMO DIA", extra="\\fad(150,150)")
groups, cur = [], []
for w in words:
    cur.append(w)
    if w[0][-1] in ".,!?" or len(cur) == 3 or len(" ".join(x[0] for x in cur)) > 16: groups.append(cur); cur = []
if cur: groups.append(cur)
clean = lambda s: s.upper().rstrip(".,!") if not s.endswith("?") else s.upper()
for gi, grp in enumerate(groups):
    nxt = groups[gi + 1][0][1] if gi + 1 < len(groups) else T_END
    for k, w in enumerate(grp):
        st = w[1]; en = grp[k + 1][1] if k + 1 < len(grp) else min(grp[-1][2] + 0.45, nxt - 0.01, T_END)
        txt = " ".join((g(clean(x[0])) if j == k else clean(x[0])) for j, x in enumerate(grp))
        add(st, en, "Cap", 540, 1410, txt, layer=2, extra=POP if k == 0 else "")
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

gimg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = gimg.load()
for yy in range(H):
    a = int(170 * min(1, (yy - 1100) / 500)) if yy > 1100 else 0
    for x in range(W): px[x, yy] = (17, 18, 20, a)
gimg.save("t/grad.png")
fc = (f"movie=t/grad.png[gr];[0:v][gr]overlay=0:0:enable='lt(t,{T_END})'[v0];"
      "[v0]ass=t/subs.ass,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mov", "-i", "t/mix.wav", "-filter_complex", fc, "-map", "[v]", "-map", "1:a",
    "-t", f"{TOT:.2f}", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
print("ok", round(T_END, 2), round(TOT, 2))
