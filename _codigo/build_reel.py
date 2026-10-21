#!/usr/bin/env python3
"""Reel piloto: corte do depoimento do João (cliente que achou a Star no Instagram)."""
import subprocess, os
os.chdir("/home/claude/piloto"); os.makedirs("tmp", exist_ok=True)
SRC = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/Câmbio Automático_/Vídeos_/Star 1F.MP4"
SEG = [(0.0, 5.10, "CLIENTE QUE CHEGOU\\NPELA INTERNET"), (9.25, 19.10, "ELE ACHOU A STAR\\NNO INSTAGRAM"), (19.10, 27.65, "TEVE PEGADINHA\\NNO PREÇO?")]
END = 3.0
W, H = 1080, 1920; VH = 1350; VY = 250

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"

# 1) cortes do vídeo original (com o áudio), cada um com micro fade de áudio
parts = []
for i, (a, b, _) in enumerate(SEG):
    d = b - a; out = f"tmp/seg{i}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", SRC, "-t", str(d),
        "-vf", f"scale={W}:{VH}:flags=lanczos,pad={W}:{H}:0:{VY}:color=0x111214,fps=30,format=yuv420p",
        "-af", f"afade=t=in:d=0.04,afade=t=out:st={d-0.06}:d=0.06,aresample=48000",
        "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-c:a", "aac", "-b:a", "192k", out], check=True)
    parts.append((out, d))
# endcard em branco (grafite) com silêncio
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x111214:s={W}x{H}:r=30:d={END}",
    "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo", "-t", str(END), "-c:v", "libx264", "-crf", "16",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "tmp/end.mp4"], check=True)
parts.append(("tmp/end.mp4", END))
open("tmp/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p, _ in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "tmp/list.txt",
    "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "tmp/joined.mp4"], check=True)

# 2) textos (ASS)
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Barlow Condensed ExtraBold,84,&H00FFFFFF,&H00FFFFFF,&H00141211,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,30,30,0,1
Style: Tag,Barlow Condensed ExtraBold,44,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,14,0,5,0,0,0,1
Style: Big,Barlow Condensed ExtraBold,112,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Info,Manrope ExtraLight SemiBold,42,&H00ABA8A6,&H00ABA8A6,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Btn,Barlow Condensed ExtraBold,62,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,24,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
G = "{\\c&H0021C3F0&}"; Wc = "{\\c&H00FFFFFF&}"
POP = "\\fscx80\\fscy80\\t(0,160,\\fscx103\\fscy103)\\t(160,240,\\fscx100\\fscy100)"
ev = []; t = 0
for i, (a, b, hook) in enumerate(SEG):
    d = b - a
    l1, l2 = hook.split("\\N")
    ev.append(f"Dialogue: 1,{ts(t)},{ts(t+d)},Hook,,0,0,0,,{{\\pos(540,128)\\fad(120,80){POP}}}{l1}\\N{G}{l2}")
    t += d
VE = t
ev.append(f"Dialogue: 1,{ts(0)},{ts(VE)},Tag,,0,0,0,,{{\\pos(540,1722)}}CLIENTE REAL DA STAR")
ev.append(f"Dialogue: 1,{ts(VE+0.45)},{ts(VE+END)},Big,,0,0,0,,{{\\pos(540,930)\\fad(250,0)}}SEU CARRO")
ev.append(f"Dialogue: 1,{ts(VE+0.6)},{ts(VE+END)},Big,,0,0,0,,{{\\pos(540,1045)\\fad(250,0)}}{G}BEM CUIDADO.")
ev.append(f"Dialogue: 1,{ts(VE+0.9)},{ts(VE+END)},Btn,,0,0,0,,{{\\pos(540,1215)\\fad(250,0){POP}}}CHAME NO WHATSAPP  (21) 97544-6417")
ev.append(f"Dialogue: 1,{ts(VE+1.1)},{ts(VE+END)},Info,,0,0,0,,{{\\pos(540,1340)\\fad(250,0)}}Estr. dos Bandeirantes, 841 · Taquara")
open("tmp/reel.ass", "w").write(hdr + "\n".join(ev) + "\n")

# 3) logo: pequeno embaixo no depoimento, grande no fechamento; loudnorm
fc = ("[1:v]format=rgba,split=2[a][b];[a]scale=210:-1[ls];[b]scale=520:-1,"
      f"fade=t=in:st={VE+0.05}:d=0.4:alpha=1[lb];"
      f"[0:v][ls]overlay=x=(W-w)/2:y=1795:enable='lt(t,{VE})'[v1];"
      f"[v1][lb]overlay=x=(W-w)/2:y=600:enable='gte(t,{VE})'[v2];[v2]ass=tmp/reel.ass[v];"
      "[0:a]loudnorm=I=-14:TP=-1.5:LRA=9[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "tmp/joined.mp4", "-loop", "1", "-framerate", "30", "-i", "/home/claude/kicks/logo.png",
    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(VE + END), "-c:v", "libx264", "-preset", "slow", "-crf", "18",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "out/reel_depoimento_joao.mp4"], check=True)
print("ok", round(VE + END, 2))
