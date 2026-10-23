#!/usr/bin/env python3
"""Trend 'A Star vai abrir no feriado?': foto real + 6 cenas geradas, cortes na batida da trilha."""
import subprocess, os
from PIL import Image, ImageOps
os.chdir("/home/claude/ref"); os.makedirs("t", exist_ok=True)
W, H, FPS = 1080, 1920, 30
CUTS = [0.0, 2.41, 4.11, 5.83, 7.55, 9.26, 10.98, 12.70]   # fortes da trilha (librosa)
END = 15.9
CENAS = [("orig", None), ("1_apagao", "NO APAGÃO"), ("2_enchente", "NA ENCHENTE"), ("3_alien", "NA INVASÃO\\NALIENÍGENA"),
         ("4_natal", "NO NATAL"), ("5_anonovo", "NO ANO NOVO"), ("6_fimdomundo", "NO FIM\\NDO MUNDO")]

# imagens 1080x1920 (com folga para o zoom)
o = ImageOps.exif_transpose(Image.open("/home/claude/staroleo-instagram/2026-10/fontes/fernando_balcao.jpg")).convert("RGB")
cw = round(o.height * 9 / 16); x0 = max(0, min(o.width - cw, 970 - cw // 2))
o.crop((x0, 0, x0 + cw, o.height)).resize((W, H), Image.LANCZOS).save("t/orig.png")
for n, _ in CENAS[1:]:
    Image.open(f"{n}.png").convert("RGB").resize((W, H), Image.LANCZOS).save(f"t/{n}.png")

# cada cena: punch-in no corte (1.12 -> 1.02 rápido) e depois zoom lento
parts = []
for i, (n, _) in enumerate(CENAS):
    a = CUTS[i]; b = CUTS[i + 1] if i + 1 < len(CUTS) else None
    d = (b - a) if b else None
    frames = round(d * FPS)
    z = "if(lte(on,7),1.12-0.10*on/7,1.02+0.025*(on-7)/%d)" % max(1, frames - 7)
    if i == 0: z = "1.0+0.04*on/%d" % frames
    out = f"t/seg{i}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"t/{n}.png", "-vf",
        f"scale={W*2}:{H*2},zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},format=yuv420p",
        "-frames:v", str(frames), "-c:v", "libx264", "-crf", "16", "-preset", "fast", out], check=True)
    parts.append(out)
# fechamento grafite
endd = END - CUTS[-1]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x111214:s={W}x{H}:r={FPS}:d={endd}",
    "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "t/end.mp4"], check=True)
parts.append("t/end.mp4")
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "16",
    "-pix_fmt", "yuv420p", "t/joined.mp4"], check=True)

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Barlow Condensed ExtraBold,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,7,4,5,40,40,0,1
Style: Cap,Barlow Condensed ExtraBold,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,8,4,5,40,40,0,1
Style: Handle,Manrope ExtraLight Bold,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,3,1,5,0,0,0,1
Style: Big,Barlow Condensed ExtraBold,112,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Info,Manrope ExtraLight SemiBold,42,&H00ABA8A6,&H00ABA8A6,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Btn,Barlow Condensed ExtraBold,62,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,24,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
G = "{\\c&H0021C3F0&}"; WH = "{\\c&H00FFFFFF&}"
POP = "\\fscx70\\fscy70\\t(0,120,\\fscx106\\fscy106)\\t(120,200,\\fscx100\\fscy100)"
ev = [f"Dialogue: 1,{ts(0.15)},{ts(CUTS[1])},Hook,,0,0,0,,{{\\pos(540,330)\\fad(150,0){POP}}}A STAR VAI ABRIR\\N{G}NO FERIADO?"]
for i in range(1, len(CENAS)):
    a = CUTS[i]; b = CUTS[i + 1] if i + 1 < len(CUTS) else CUTS[-1]
    ev.append(f"Dialogue: 1,{ts(a + 0.04)},{ts(b)},Cap,,0,0,0,,{{\\pos(540,330){POP}}}{CENAS[i][1]}")
ev.append(f"Dialogue: 1,{ts(0)},{ts(CUTS[-1])},Handle,,0,0,0,,{{\\pos(540,1540)}}@staroleo_rj")
E0 = CUTS[-1]
ev.append(f"Dialogue: 1,{ts(E0+0.35)},{ts(END)},Big,,0,0,0,,{{\\pos(540,900)\\fad(250,0)}}FERIADO OU NÃO,")
ev.append(f"Dialogue: 1,{ts(E0+0.5)},{ts(END)},Big,,0,0,0,,{{\\pos(540,1015)\\fad(250,0)}}{G}CHAMA A STAR.")
ev.append(f"Dialogue: 1,{ts(E0+0.8)},{ts(END)},Btn,,0,0,0,,{{\\pos(540,1185)\\fad(250,0){POP}}}WHATSAPP  (21) 97544-6417")
ev.append(f"Dialogue: 1,{ts(E0+1.0)},{ts(END)},Info,,0,0,0,,{{\\pos(540,1310)\\fad(250,0)}}Estr. dos Bandeirantes, 841 · Taquara")
open("t/trend.ass", "w").write(hdr + "\n".join(ev) + "\n")

# flash branco curto em cada corte (cenas 1..6)
flashes = "+".join(f"between(t,{c:.2f},{c+0.10:.2f})" for c in CUTS[1:-1])
logo = "/home/claude/staroleo-instagram/_codigo/logo.png"
fc = (f"[0:v]eq=brightness='0.55*({flashes})':eval=frame[f];"
      f"[1:v]format=rgba,scale=520:-1,fade=t=in:st={E0+0.05}:d=0.4:alpha=1[lb];"
      f"[f][lb]overlay=x=(W-w)/2:y=560:enable='gte(t,{E0})'[v2];[v2]ass=t/trend.ass[v];"
      f"[2:a]atrim=0:{END},afade=t=out:st={END-0.8}:d=0.8,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "t/joined.mp4", "-loop", "1", "-framerate", str(FPS), "-i", logo,
    "-i", "musica.mp3", "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(END),
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart", "reel_trend_feriado.mp4"], check=True)
print("ok")
