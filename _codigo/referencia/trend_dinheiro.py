#!/usr/bin/env python3
"""Trend 'Dinheiro não compra felicidade, mas...' com o b-roll limpo do vídeo do CR-V (10 a 27 s)."""
import subprocess, os
os.chdir("/home/claude/trend2"); os.makedirs("t", exist_ok=True)
SRC = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/Câmbio Automático_/Vídeos_/Star - CRV oléo do câmbio.MP4"
AUD = "/home/claude/staroleo-instagram/_codigo/audio/trilha_r15mil.mp3"
LOGO = "/home/claude/staroleo-instagram/_codigo/logo.png"
W, H, FPS = 1080, 1920, 30
SEG = [(10.2, 11.9), (13.3, 15.4), (17.3, 18.9), (20.4, 21.6), (23.4, 25.8)]
END = 3.2
parts = []
for i, (a, b) in enumerate(SEG):
    p = f"t/s{i}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", SRC, "-t", str(b - a), "-an",
        "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS},eq=contrast=1.06:saturation=1.10,format=yuv420p",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast", p], check=True)
    parts.append(p)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x111214:s={W}x{H}:r={FPS}:d={END}",
    "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "t/end.mp4"], check=True)
parts.append("t/end.mp4")
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264",
    "-crf", "16", "-pix_fmt", "yuv420p", "t/joined.mp4"], check=True)
VE = sum(b - a for a, b in SEG); TOT = VE + END

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Barlow Condensed ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,7,4,5,60,60,0,1
Style: Handle,Manrope ExtraLight Bold,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,3,1,5,0,0,0,1
Style: Big,Barlow Condensed ExtraBold,112,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Info,Manrope ExtraLight SemiBold,42,&H00ABA8A6,&H00ABA8A6,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Btn,Barlow Condensed ExtraBold,62,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,24,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
G = "{\\c&H0021C3F0&}"
POP = "\\fscx80\\fscy80\\t(0,140,\\fscx104\\fscy104)\\t(140,220,\\fscx100\\fscy100)"
T1 = 3.3
ev = [f"Dialogue: 1,{ts(0.1)},{ts(T1)},Cap,,0,0,0,,{{\\pos(540,360)\\fad(120,100){POP}}}DINHEIRO NÃO COMPRA\\NFELICIDADE…",
      f"Dialogue: 1,{ts(T1)},{ts(VE)},Cap,,0,0,0,,{{\\pos(540,380)\\fad(100,0){POP}}}…MAS COMPRA A TROCA\\N{G}DO ÓLEO DO CÂMBIO\\N{{\\c&H00FFFFFF&}}E O CARRO AGRADECE.",
      f"Dialogue: 1,{ts(0)},{ts(VE)},Handle,,0,0,0,,{{\\pos(540,1560)}}@staroleo_rj",
      f"Dialogue: 1,{ts(VE+0.35)},{ts(TOT)},Big,,0,0,0,,{{\\pos(540,900)\\fad(250,0)}}SEU CÂMBIO",
      f"Dialogue: 1,{ts(VE+0.5)},{ts(TOT)},Big,,0,0,0,,{{\\pos(540,1015)\\fad(250,0)}}{G}BEM CUIDADO.",
      f"Dialogue: 1,{ts(VE+0.8)},{ts(TOT)},Btn,,0,0,0,,{{\\pos(540,1185)\\fad(250,0){POP}}}WHATSAPP  (21) 97544-6417",
      f"Dialogue: 1,{ts(VE+1.0)},{ts(TOT)},Info,,0,0,0,,{{\\pos(540,1310)\\fad(250,0)}}Até 10x sem juros · Taquara"]
open("t/d.ass", "w").write(hdr + "\n".join(ev) + "\n")
fc = (f"[1:v]format=rgba,scale=520:-1,fade=t=in:st={VE+0.05}:d=0.4:alpha=1[lb];"
      f"[0:v][lb]overlay=x=(W-w)/2:y=560:enable='gte(t,{VE})'[v2];[v2]ass=t/d.ass[v];"
      f"[2:a]atrim=0:{TOT},afade=t=in:d=0.2,afade=t=out:st={TOT-0.8}:d=0.8,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "t/joined.mp4", "-loop", "1", "-framerate", str(FPS), "-i", LOGO,
    "-i", AUD, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow",
    "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
    "reel_trend_dinheiro.mp4"], check=True)
print("ok", round(TOT, 2))
