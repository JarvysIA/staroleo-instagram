#!/usr/bin/env python3
"""Anúncio Star Óleo – vídeo do Fernando (Taquara/Zona Oeste). Cortes secos, punch-ins, B-roll, legendas, CTA."""
import subprocess, os, json
from PIL import Image, ImageFilter
os.chdir("/home/claude/ad"); os.makedirs("tmp", exist_ok=True)
W, H, FPS = 1080, 1920, 30
GOLD, GRAF, WHITE, RED, MUTED = "&H0021C3F0&", "&H00141211&", "&H00FFFFFF&", "&H003539E5&", "&H00ABA8A6&"
fr = lambda t: round(t * FPS) / FPS

def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode: raise SystemExit(" ".join(cmd)[:300] + "\n" + r.stderr[-2500:])

# ---------- cortes (tempo do vídeo original) e zoom de cada trecho ----------
# (início, fim, zoom)
SEG = [(8.06, 10.53, 1.88), (10.67, 12.21, 1.55), (12.39, 13.32, 1.50), (13.32, 14.78, 1.90),
       (15.03, 16.39, 1.60), (16.63, 18.99, 1.85), (19.17, 21.55, 1.55)]
SEG = [(fr(a), fr(b), z) for a, b, z in SEG]
FX, FY = 0.495, 0.47          # posição do rosto no quadro original
def out_t(raw):               # tempo original -> tempo no vídeo editado
    o = 0
    for a, b, _ in SEG:
        if raw < a: return o
        if raw <= b: return o + raw - a
        o += b - a
    return o
TALK = sum(b - a for a, b, _ in SEG)
ENDLEN = 3.0
END = fr(TALK + ENDLEN)
print("fala:", round(TALK, 2), "s  total:", END, "s")

# ---------- vídeo do Fernando com punch-ins ----------
parts = []
for i, (a, b, z) in enumerate(SEG):
    n = round((b - a) * FPS)
    push = 0.035 / max(n, 1)
    xexp = f"max(0,min(iw-iw/zoom,{FX}*iw-iw/zoom/2))"
    yexp = f"max(0,min(ih-ih/zoom,{FY}*ih-0.30*ih/zoom))"
    vf = (f"fps={FPS},scale=2160:3840:flags=lanczos,"
          f"zoompan=z='{z}+{push}*on':x='{xexp}':y='{yexp}':d=1:s={W}x{H}:fps={FPS},"
          f"eq=contrast=1.06:saturation=1.12:brightness=0.01,unsharp=5:5:0.6,format=yuv420p")
    out = f"tmp/p{i}.mp4"
    run(["ffmpeg", "-y", "-ss", f"{a:.4f}", "-t", f"{b-a:.4f}", "-i", "raw.mov", "-an", "-vf", vf,
         "-frames:v", str(n), "-c:v", "libx264", "-preset", "fast", "-crf", "15", out])
    parts.append(out)
# fechamento: último quadro desfocado e escurecido
run(["ffmpeg", "-y", "-sseof", "-0.1", "-i", "tmp/p6.mp4", "-frames:v", "1", "-update", "1", "tmp/last.png"])
im = Image.open("tmp/last.png").convert("RGB").filter(ImageFilter.GaussianBlur(26))
Image.blend(im, Image.new("RGB", im.size, (17, 18, 20)), 0.80).save("tmp/end_bg.png")
n = round(ENDLEN * FPS)
run(["ffmpeg", "-y", "-loop", "1", "-i", "tmp/end_bg.png", "-vf",
     f"zoompan=z='1+0.0008*on':d={n}:s={W}x{H}:fps={FPS},fade=t=in:st=0:d=0.25:color=white,format=yuv420p",
     "-frames:v", str(n), "-c:v", "libx264", "-preset", "fast", "-crf", "15", "tmp/pend.mp4"])
parts.append("tmp/pend.mp4")
open("tmp/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "tmp/list.txt", "-c", "copy", "tmp/base.mp4"])

# ---------- B-roll (fotos da Star) ----------
BR = [  # (foto, início editado, fim editado, z0, z1, foco x, foco y)
    ("/home/claude/r15/src/12.jpg", out_t(13.86), out_t(14.78), 1.55, 1.85, .30, .72),   # máquina
    ("/home/claude/r15/src/20.jpg", out_t(16.84), out_t(18.04), 1.6, 1.95, .62, .67),   # fluido homologado
]
for k, (src, a, b, z0, z1, px, py) in enumerate(BR):
    a, b = fr(a), fr(b); BR[k] = (src, a, b)
    n = round((b - a) * FPS)
    vf = (f"scale=2880:3840:force_original_aspect_ratio=increase,crop=2880:3840,"
          f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='max(0,min(iw-iw/zoom,{px}*iw-iw/zoom/2))':"
          f"y='max(0,min(ih-ih/zoom,{py}*ih-ih/zoom/2))':d={n}:s=1440x1920:fps={FPS},crop={W}:{H},"
          f"eq=contrast=1.05:saturation=1.1,format=yuv420p")
    run(["ffmpeg", "-y", "-loop", "1", "-i", src, "-vf", vf, "-frames:v", str(n),
         "-c:v", "libx264", "-preset", "fast", "-crf", "15", f"tmp/b{k}.mp4"])

# ---------- legendas ----------
def ts(t): t = max(t, 0); return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Barlow Condensed ExtraBold,104,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,7,4,5,30,30,0,1
Style: Pin,Barlow Condensed ExtraBold,66,&H00FFFFFF,&H00FFFFFF,&H00141211,&H00141211,0,0,0,0,100,100,3,0,3,18,0,5,0,0,0,1
Style: Shape,Barlow Condensed,10,&H0021C3F0,&H0021C3F0,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Brow,Barlow Condensed,46,&H0021C3F0,&H0021C3F0,&H00000000,&H00000000,0,0,0,0,100,100,5,0,1,0,0,5,0,0,0,1
Style: Big,Barlow Condensed ExtraBold,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Info,Manrope ExtraLight SemiBold,44,&H00ABA8A6,&H00ABA8A6,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Btn,Barlow Condensed ExtraBold,66,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,28,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
def add(st, en, style, x, y, text, layer=1, extra=""):
    ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{{\\pos({x},{y}){extra}}}{text}")
POP = "\\fscx72\\fscy72\\t(0,130,\\fscx106\\fscy106)\\t(130,210,\\fscx100\\fscy100)"
c = lambda col, t: "{\\c" + col + "}" + t + "{\\c" + WHITE + "}"

# selo de localização fixo (pino desenhado + texto)
PIN = "{\\p1}m 0 -26 b 15 -26 26 -15 26 0 b 26 16 6 30 0 44 b -6 30 -26 16 -26 0 b -26 -15 -15 -26 0 -26{\\p0}"
DOT = "{\\p1}m 0 -9 b 5 -9 9 -5 9 0 b 9 5 5 9 0 9 b -5 9 -9 5 -9 0 b -9 -5 -5 -9 0 -9{\\p0}"
STK = TALK - 0.05
add(0.0, STK, "Pin", 575, 300, "TAQUARA  ·  ZONA OESTE", extra="\\fad(0,150)" + POP)
add(0.0, STK, "Shape", 292, 290, PIN, layer=2, extra="\\fad(0,150)")
add(0.0, STK, "Shape", 292, 290, DOT, layer=3, extra="\\c" + GRAF + "\\fad(0,150)")

# palavras (tempo original) – texto corrigido; KEY = destaque dourado
W_ = [("VOCÊ", 8.13, 8.42), ("NÃO", 8.42, 8.68), ("PRECISA", 8.68, 9.16), ("ATRAVESSAR*", 9.16, 9.66), ("A*", 9.66, 9.78),
      ("CIDADE*", 9.78, 9.94), ("INTEIRA", 9.94, 10.47), ("PARA", 10.73, 10.95), ("TROCAR", 10.95, 11.1), ("O", 11.1, 11.18),
      ("ÓLEO*", 11.18, 11.3), ("DE*", 11.3, 11.4), ("CÂMBIO*", 11.4, 11.6), ("DO", 11.6, 11.7), ("SEU", 11.7, 11.78), ("CARRO", 11.78, 12.15),
      ("AQUI", 12.44, 12.62), ("NA", 12.62, 12.9), ("STAR*", 12.9, 13.32), ("NÓS", 13.34, 13.5), ("TEMOS", 13.5, 13.86),
      ("A", 13.86, 14.0), ("MÁQUINA*", 14.0, 14.3), ("ESPECIALIZADA*", 14.3, 14.72),
      ("PROFISSIONAIS*", 15.09, 15.6), ("CAPACITADOS*", 15.6, 16.33),
      ("E", 16.69, 16.8), ("O", 16.8, 16.9), ("ADITIVO*", 16.9, 17.4), ("HOMOLOGADO*", 17.4, 18.02), ("PARA", 18.02, 18.22),
      ("O", 18.22, 18.34), ("SEU", 18.34, 18.42), ("VEÍCULO", 18.42, 18.93),
      ("ENTRE", 19.23, 19.4), ("EM", 19.4, 19.48), ("CONTATO", 19.48, 19.72), ("COM", 19.72, 19.8), ("A", 19.8, 19.84), ("GENTE", 19.84, 20.0),
      ("AGORA", 20.0, 20.18), ("MESMO", 20.18, 20.5), ("E", 20.5, 20.64), ("AGENDE*", 20.64, 20.95), ("SUA", 20.95, 21.08), ("TROCA*", 21.08, 21.48)]
GROUPS = [[0, 1, 2], [3, 4, 5], [6], [7, 8], [9, 10, 11, 12], [13, 14, 15], [16, 17, 18], [19, 20, 21], [22], [23],
          [24], [25], [26, 27, 28], [29], [30, 31, 32, 33], [34, 35, 36], [37, 38, 39], [40, 41], [42, 43], [44, 45]]
CAP_Y = 1330
for gi, g in enumerate(GROUPS):
    words = [W_[i] for i in g]
    gs = out_t(words[0][1])
    nxt = out_t(W_[GROUPS[gi + 1][0]][1]) if gi + 1 < len(GROUPS) else TALK
    for k, (wd, a, b) in enumerate(words):
        st = out_t(a) if k else gs
        en = out_t(words[k + 1][1]) if k + 1 < len(words) else min(out_t(b) + 0.15, nxt - 0.01)
        parts_ = []
        for j, (w2, _, _) in enumerate(words):
            key, t = w2.endswith("*"), w2.rstrip("*")
            if j == k:
                parts_.append("{\\c" + GOLD + "\\fscx112\\fscy112}" + t + "{\\fscx100\\fscy100\\c" + WHITE + "}")
            else:
                parts_.append(c(GOLD, t) if key else t)
        add(st, en, "Cap", 540, CAP_Y, " ".join(parts_), layer=4, extra=POP if k == 0 else "")

# fechamento
E0 = TALK
D = "\\fad(250,0)"
add(E0 + 0.30, END, "Brow", 540, 760, "———  ESPECIALISTA EM CÂMBIO AUTOMÁTICO  ———", extra=D)
add(E0 + 0.45, END, "Big", 540, 875, "ÓLEO DO CÂMBIO", extra=D + POP)
add(E0 + 0.60, END, "Big", 540, 995, c(GOLD, "PERTINHO DE VOCÊ."), extra=D + POP)
add(E0 + 0.85, END, "Info", 540, 1120, "Estr. dos Bandeirantes, 841 · Taquara – RJ", extra=D)
add(E0 + 1.05, END, "Btn", 540, 1250, "AGENDE PELO WHATSAPP", extra=D + POP)
add(E0 + 1.35, END, "Info", 540, 1385, c(GOLD, "★★★★★") + "{\\c" + MUTED + "}  4,9 no Google · Delivery Car leva e traz", extra=D)
open("tmp/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

# ---------- áudio ----------
pieces, flt = [], []
for i, (a, b, _) in enumerate(SEG):
    flt.append(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={b-a-0.012:.4f}:d=0.012[s{i}]")
flt.append("".join(f"[s{i}]" for i in range(len(SEG))) + f"concat=n={len(SEG)}:v=0:a=1,"
           "highpass=f=85,afftdn=nf=-28,acompressor=threshold=0.08:ratio=3:attack=8:release=120:makeup=1.6,"
           f"loudnorm=I=-14:TP=-1.2:LRA=6,aresample=48000,apad=whole_dur={END}[v]")
run(["ffmpeg", "-y", "-i", "raw.mov", "-filter_complex", ";".join(flt), "-map", "[v]", "-ac", "2", "-t", str(END), "tmp/voice.wav"])
# whoosh sintetizado para entradas do B-roll
run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anoisesrc=d=0.5:c=pink:a=0.6:r=48000", "-af",
     "highpass=f=400,lowpass=f=6000,volume='sin(PI*t/0.5)':eval=frame,aformat=channel_layouts=stereo", "tmp/whoosh.wav"])
wh = [BR[0][1] - 0.15, BR[0][2] - 0.15, BR[1][1] - 0.15, BR[1][2] - 0.15, E0 - 0.15]
sfx_in, sfx_f = [], []
for k, h in enumerate(wh):
    sfx_in += ["-i", "tmp/whoosh.wav"]
    sfx_f.append(f"[{k+2}:a]adelay={int(h*1000)}|{int(h*1000)},volume=0.35[w{k}]")
run(["ffmpeg", "-y", "-i", "tmp/voice.wav", "-i", "/home/claude/kicks/m1.mp3", *sfx_in, "-filter_complex",
     ";".join(sfx_f) + ";"
     f"[1:a]aresample=48000,atrim=0:{END},volume=0.42,afade=t=in:d=0.4,afade=t=out:st={END-1.2}:d=1.2[m];"
     "[0:a]asplit=2[vo][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=9:attack=15:release=300[duck];"
     f"[vo][duck]{''.join(f'[w{k}]' for k in range(len(wh)))}amix=inputs={2+len(wh)}:duration=first:normalize=0,alimiter=limit=0.92",
     "-t", str(END), "tmp/mix.wav"])

# ---------- composição ----------
fc = ("[3:v]format=rgba,scale=210:-1:flags=lanczos,split=2[ls][lb0];[lb0]scale=600:-1:flags=lanczos[lb];"
      f"[ls]fade=t=out:st={E0-0.25}:d=0.25:alpha=1[lsf];[lb]fade=t=in:st={E0+0.05}:d=0.4:alpha=1[lbf];"
      f"[1:v]setpts=PTS-STARTPTS+{BR[0][1]}/TB,fade=t=in:st={BR[0][1]}:d=0.12:alpha=1[b0];"
      f"[2:v]setpts=PTS-STARTPTS+{BR[1][1]}/TB,fade=t=in:st={BR[1][1]}:d=0.12:alpha=1[b1];"
      f"[0:v][b0]overlay=0:0:eof_action=pass[v0];[v0][b1]overlay=0:0:eof_action=pass[v1];"
      "movie=/home/claude/kicks/tmp/grad.png[gr];[v1][gr]overlay=0:0[v2];"
      f"[v2][lsf]overlay=x=(W-w)/2:y=118:enable='lt(t,{E0+0.05})'[v3];"
      f"[v3][lbf]overlay=x=(W-w)/2:y=330:enable='gte(t,{E0})'[v4];[v4]ass=tmp/subs.ass[v]")
run(["ffmpeg", "-y", "-i", "tmp/base.mp4", "-i", "tmp/b0.mp4", "-i", "tmp/b1.mp4",
     "-loop", "1", "-framerate", str(FPS), "-i", "/home/claude/kicks/logo.png", "-i", "tmp/mix.wav",
     "-filter_complex", fc, "-map", "[v]", "-map", "4:a", "-t", str(END), "-r", str(FPS),
     "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "anuncio_star_taquara.mp4"])
print("ok")
