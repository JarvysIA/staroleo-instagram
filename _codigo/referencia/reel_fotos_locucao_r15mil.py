#!/usr/bin/env python3
"""Reel 'R$ 15 mil' – Star Óleo. Gancho, 3 exigências, risco, montagem de 20 carros, fechamento."""
import json, subprocess, os
from PIL import Image, ImageFilter
os.chdir("/home/claude/r15")
os.makedirs("tmp", exist_ok=True)

W, H, FPS = 1080, 1920, 30
OFF = 0.6            # atraso da locução
MUS_SKIP = 0.3       # corta início da música (alinha batida forte com o fechamento)
SPL = 22.36          # ponto da música onde repetimos 16 batidas (estica a montagem)
DUP = round(22.36 - 16.51, 3)
END = round(28.8 + DUP, 2)
E0 = round(23.3 + DUP, 2)  # fechamento (cai na batida forte)
VO_SPLIT = 22.70     # locução: "Star Óleo..." entra depois da montagem
GOLD, GRAF, WHITE, RED, MUTED = "&H0021C3F0&", "&H00141211&", "&H00FFFFFF&", "&H003539E5&", "&H00ABA8A6&"

def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode: raise SystemExit(r.stderr[-2000:])

# ---------------- cenas ----------------
# (foto, inicio, fim, z0, z1, foco_x, foco_y, efeito)
S = []
hook = ["01", "15", "13", "08"]
for i, f in enumerate(hook):
    S.append((f, i * 1.5, (i + 1) * 1.5 if i < 3 else 5.95, 1.18, 1.04, .5, .42, "shake"))
S += [
    ("12", 5.95, 8.2, 1.0, 1.10, .5, .45, "flash"),
    ("10", 8.2, 9.88, 1.15, 1.55, .40, .47, ""),     # mecânico
    ("17", 9.88, 11.72, 1.15, 1.65, .27, .74, ""),   # máquina
    ("20", 11.72, 14.75, 1.2, 1.75, .62, .67, ""),   # óleos
    ("07", 14.75, 17.95, 1.0, 1.15, .5, .40, "flash,red,shake2"),
]
mont = [("02", "FORD KA"), ("03", "RENAULT CAPTUR"), ("15", "MERCEDES-BENZ"), ("06", "HONDA FIT"),
        ("04", "PEUGEOT 2008"), ("11", "HONDA CR-V"), ("09", "HYUNDAI HB20"), ("01", "JEEP COMPASS"),
        ("16", "FIAT CRONOS"), ("05", "VOLKSWAGEN"), ("13", "TOYOTA COROLLA"), ("14", "FORD ECOSPORT"),
        ("18", "CITROËN"), ("08", "SUBARU IMPREZA")]
mont += [("19", "VOLKSWAGEN"), ("17", "HONDA CIVIC"), ("20", "HONDA HR-V"), ("12", "FIAT TORO"),
         ("07", "TOYOTA ETIOS"), ("10", "RENAULT SANDERO")]
beats = [0.77,1.14,1.51,1.88,2.23,2.6,2.97,3.34,3.69,4.06,4.44,4.81,5.15,5.53,5.9,6.27,6.62,6.99,7.36,7.73,8.08,8.45,8.82,9.2,9.57,9.91,10.29,10.66,11.01,11.38,11.75,12.12,12.49,12.84,13.21,13.58,13.93,14.3,14.68,15.05,15.42,15.77,16.14,16.51,16.88,17.23,17.6,17.97,18.34,18.69,19.06,19.44,19.81,20.18,20.53,20.9,21.27,21.64,21.99,22.36,22.73,23.1,23.45,23.82,24.2,24.57,24.92,25.29,25.66,26.03,26.38,26.75,27.12,27.49,27.84,28.21,28.58]
hb = sorted(set(beats + [(a + b) / 2 for a, b in zip(beats, beats[1:])]))
grid = [r - MUS_SKIP for r in hb if r < SPL] + [r - MUS_SKIP + DUP for r in hb if r >= SPL - DUP]
grid = [g for g in grid if 18.35 < g < E0 - 0.3][::3]
cuts = [17.95] + grid + [E0]
MONT = []
for k in range(len(cuts) - 1):
    f, name = mont[k % len(mont)]
    MONT.append((cuts[k], cuts[k + 1], name))
    S.append((f, cuts[k], cuts[k + 1], 1.12, 1.02, .5, .40, "flash" if k == 0 else ""))
print("montagem:", len(MONT), "cortes, média", round((E0 - 17.95) / len(MONT), 2), "s")
S.append(("END", E0, END, 1.0, 1.05, .5, .5, "flash"))

# fundo do fechamento
bg = Image.open("src/15.jpg").convert("RGB").resize((1440, 1920)).crop((180, 0, 1260, 1920)).filter(ImageFilter.GaussianBlur(30))
Image.blend(bg, Image.new("RGB", bg.size, (17, 18, 20)), 0.82).save("tmp/end_bg.jpg", quality=92)

clips = []
REUSE = os.path.exists('tmp/base.mp4')
for i, (f, a, b, z0, z1, px, py, fx) in enumerate(S):
    # alinhar aos quadros
    fa, fb = round(a * FPS), round(b * FPS)
    n = fb - fa
    src = "tmp/end_bg.jpg" if f == "END" else f"src/{f}.jpg"
    z = f"{z0}+({z1}-{z0})*on/{max(n-1,1)}"
    xexp = f"max(0,min(iw-iw/zoom,{px}*iw-iw/zoom/2))"
    yexp = f"max(0,min(ih-ih/zoom,{py}*ih-ih/zoom/2))"
    vf = (f"scale=2880:3840:force_original_aspect_ratio=increase,crop=2880:3840,"
          f"zoompan=z='{z}':x='{xexp}':y='{yexp}':d={n}:s=1440x1920:fps={FPS},")
    if "shake" in fx:
        vf += "crop=1080:1920:x='180+if(lt(t,0.3),28*sin(t*110)*(1-t/0.3),0)':y=0,"
    elif "shake2" in fx:
        vf += "crop=1080:1920:x='180+if(between(t,1.65,2.1),40*sin((t-1.65)*95)*(1-(t-1.65)/0.45),0)':y=0,"
    else:
        vf += "crop=1080:1920,"
    if "red" in fx:
        vf += "eq=saturation=0.15:contrast=1.15:brightness=-0.06,colorbalance=rs=0.35:rm=0.15,"
    if "flash" in fx:
        vf += "fade=t=in:st=0:d=0.2:color=white,"
    vf += "format=yuv420p"
    out = f"tmp/c{i:02d}.mp4"
    if not REUSE: run(["ffmpeg", "-y", "-loop", "1", "-i", src, "-vf", vf, "-frames:v", str(n), "-r", str(FPS),
         "-c:v", "libx264", "-preset", "fast", "-crf", "16", out])
    clips.append(out)
open("tmp/list.txt", "w").write("".join(f"file '{os.path.basename(c)}'\n" for c in clips))
if not REUSE: run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "tmp/list.txt", "-c", "copy", "tmp/base.mp4"])

# ---------------- textos ----------------
def ts(t): t = max(t, 0); return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Barlow Condensed ExtraBold,108,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,7,3,5,40,40,0,1
Style: Title,Barlow Condensed ExtraBold,98,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,5,3,5,40,40,0,1
Style: Huge,Barlow Condensed ExtraBold,250,&H0021C3F0,&H0021C3F0,&H00141211,&HA0000000,0,0,0,0,100,100,2,0,1,9,6,5,0,0,0,1
Style: Sub,Barlow Condensed,56,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,4,0,1,4,2,5,40,40,0,1
Style: Badge,Barlow Condensed ExtraBold,112,&H00FFFFFF,&H00FFFFFF,&H003539E5,&H003539E5,0,0,0,0,100,100,8,0,3,22,0,5,0,0,0,1
Style: BadgeR,Barlow Condensed ExtraBold,120,&H00FFFFFF,&H00FFFFFF,&H003539E5,&H003539E5,0,0,0,0,100,100,4,0,3,20,0,5,0,0,0,1
Style: Splash,Barlow Condensed ExtraBold,250,&H00FFFFFF,&H00FFFFFF,&H003539E5,&H003539E5,0,0,0,0,100,100,3,0,3,30,0,5,0,0,0,1
Style: Full,Barlow Condensed,10,&H003539E5,&H003539E5,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Item,Barlow Condensed ExtraBold,74,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,4,2,4,0,0,0,1
Style: Box,Barlow Condensed,10,&H40141211,&H40141211,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: TagG,Barlow Condensed ExtraBold,62,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,3,0,3,16,0,5,0,0,0,1
Style: Brow,Barlow Condensed,46,&H0021C3F0,&H0021C3F0,&H00000000,&H00000000,0,0,0,0,100,100,5,0,1,0,0,5,0,0,0,1
Style: Big,Barlow Condensed ExtraBold,128,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Info,Manrope ExtraLight SemiBold,44,&H00ABA8A6,&H00ABA8A6,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Btn,Barlow Condensed ExtraBold,64,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,26,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
def add(st, en, style, x, y, text, layer=1, extra=""):
    ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{{\\pos({x},{y}){extra}}}{text}")
POP = "\\fscx70\\fscy70\\t(0,140,\\fscx106\\fscy106)\\t(140,220,\\fscx100\\fscy100)"
SLAM = "\\fscx160\\fscy160\\t(0,120,\\fscx96\\fscy96)\\t(120,200,\\fscx100\\fscy100)"
FADE = "\\fad(150,120)"
c = lambda col, t: "{\\c" + col + "}" + t + "{\\c" + WHITE + "}"
TY = 395

# 1) gancho
PULSE = "".join(f"\\t({a},{a+250},\\fscx108\\fscy108)\\t({a+250},{a+500},\\fscx100\\fscy100)" for a in range(300, 5600, 500))
add(0.0, 5.9, "Badge", 540, 360, "ATENÇÃO", extra=SLAM + PULSE)
add(0.10, 5.9, "Sub", 540, 495, "ERRO NA TROCA DO ÓLEO DO CÂMBIO", extra=FADE)
add(0.15, 4.25, "Huge", 540, 690, "R$ 15 MIL", extra=SLAM)
add(4.28, 5.9, "Huge", 540, 690, "R$ 15 MIL", extra=SLAM + "\\fad(0,120)")
add(0.45, 5.9, "BadgeR", 540, 955, "DE PREJUÍZO", extra=SLAM + "\\frz-3")

# 2) três exigências (painel)
box = "{\\p1}m 0 0 l 920 0 920 490 0 490{\\p0}"
add(6.4, 14.7, "Box", 80, 300, box, layer=0, extra="\\fad(200,150)")
add(6.4, 14.7, "Title", 540, 370, "3 EXIGÊNCIAS", extra=FADE + POP)
items = [(8.2, "PROFISSIONAL CAPACITADO"), (9.88, "MÁQUINA ESPECIALIZADA"), (11.72, "ÓLEO HOMOLOGADO")]
for k, (t, txt) in enumerate(items):
    add(t, 14.7, "Item", 140, 480 + k * 88, "{\\fnInter Display Black\\c" + GOLD + "}✓{\\fnBarlow Condensed ExtraBold\\c" + WHITE + "}  " + txt,
        extra="\\fad(120,150)\\fscx80\\fscy80\\t(0,150,\\fscx100\\fscy100)")
add(12.6, 14.7, "Sub", 540, 742, c(GOLD, "PELO FABRICANTE DO SEU CARRO"), extra=FADE)

# 3) risco
add(14.85, 17.9, "Title", 540, TY, "PROCEDIMENTO ERRADO", extra=FADE + POP)
add(16.4, 16.75, "Full", 0, 0, "{\\p1}m 0 0 l 1080 0 1080 1920 0 1920{\\p0}", layer=3, extra="\\alpha&H40&\\t(0,350,\\alpha&HFF&)")
BIG = "\\fscx260\\fscy260\\t(0,140,\\fscx94\\fscy94)\\t(140,230,\\fscx100\\fscy100)\\frz-6"
add(16.4, 17.93, "Splash", 540, 860, "CÂMBIO", layer=4, extra=BIG)
add(16.55, 17.93, "Splash", 540, 1110, "CONDENADO", layer=4, extra=BIG + "\\fs200")

# 4) montagem
add(17.95, 19.0, "Title", 540, TY, "NÃO " + c(GOLD, "ARRISQUE."), extra=POP)
add(19.0, E0 - 0.05, "Title", 540, TY, "NACIONAIS " + c(GOLD, "E IMPORTADOS"), extra=POP)
for a, b, name in MONT:
    add(a, b, "TagG", 540, 1180, name, extra="\\fscx85\\fscy85\\t(0,90,\\fscx100\\fscy100)")

# legenda palavra a palavra
words = [[w, a + (DUP if a >= VO_SPLIT else 0), b + (DUP if a >= VO_SPLIT else 0)] for w, a, b in json.load(open("words.json"))]
groups, cur = [], []
for w in words:
    cur.append(w)
    if w[0][-1] in ".,:!?" or len(cur) == 3 or len(" ".join(x[0] for x in cur)) > 16:
        groups.append(cur); cur = []
if cur: groups.append(cur)
for gi, grp in enumerate(groups):
    gs, ge = grp[0][1] + OFF, grp[-1][2] + OFF
    nxt = groups[gi + 1][0][1] + OFF if gi + 1 < len(groups) else 99
    cy = 1640 if gs >= E0 - 0.1 else 1400
    for k, w in enumerate(grp):
        st = w[1] + OFF if k else gs
        en = (grp[k + 1][1] + OFF) if k + 1 < len(grp) else min(ge + 0.12, nxt - 0.01)
        parts = [(c(GOLD, x[0].upper().rstrip(".,:")) if j == k else x[0].upper().rstrip(".,:")) for j, x in enumerate(grp)]
        add(st, en, "Cap", 540, cy, " ".join(parts), layer=2, extra=POP if k == 0 else "")

# 5) fechamento
D = "\\fad(300,0)"
add(E0 + 0.35, END, "Brow", 540, 760, "———  ESPECIALISTA EM CÂMBIO AUTOMÁTICO  ———", extra=D)
add(E0 + 0.55, END, "Big", 540, 880, "NACIONAIS E IMPORTADOS.", extra=D + "\\fscx88\\fscy88\\t(0,300,\\fscx100\\fscy100)")
add(E0 + 0.75, END, "Big", 540, 1005, c(GOLD, "SEU CÂMBIO EM BOAS MÃOS."), extra=D + "\\fscx88\\fscy88\\t(0,300,\\fscx100\\fscy100)")
add(E0 + 1.0, END, "Info", 540, 1135, "Estr. dos Bandeirantes, 841 · Taquara – RJ", extra=D)
add(E0 + 1.3, END, "Btn", 540, 1265, "AGENDE PELO WHATSAPP  (21) 97544-6417", extra=D + POP)
add(E0 + 1.6, END, "Info", 540, 1395, c(GOLD, "★★★★★") + "{\\c" + MUTED + "}  4,9 no Google · Delivery Car leva e traz", extra=D)
open("tmp/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

# ---------------- áudio ----------------
run(["ffmpeg", "-y", "-f", "lavfi", "-i",
     "aevalsrc='0.9*sin(2*PI*(38+110*exp(-9*t))*t)*exp(-3.2*t)':s=48000:d=1.6", "-f", "lavfi", "-i",
     "anoisesrc=d=1.6:c=brown:a=0.9:r=48000", "-filter_complex",
     "[1:a]lowpass=f=900,volume='exp(-9*t)':eval=frame[n];[0:a][n]amix=inputs=2:normalize=0,alimiter=limit=0.95,aformat=channel_layouts=stereo",
     "tmp/boom.wav"])
hits = [0.08, 4.25, 16.38]
a1 = int(OFF * 1000)
run(["ffmpeg", "-y", "-i", "vo.mp3", "-filter_complex",
     f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=7,aresample=48000,asplit=2[x][y];"
     f"[x]atrim=0:{VO_SPLIT},adelay={a1}|{a1}[p];[y]atrim=start={VO_SPLIT},asetpts=PTS-STARTPTS,adelay={int((OFF+VO_SPLIT+DUP)*1000)}|{int((OFF+VO_SPLIT+DUP)*1000)}[q];"
     f"[p][q]amix=inputs=2:normalize=0:duration=longest,apad=whole_dur={END}",
     "-ac", "2", "-ar", "48000", "-t", str(END), "tmp/vo.wav"])
run(["ffmpeg", "-y", "-i", "music.mp3", "-filter_complex",
     f"[0:a]aresample=48000,asplit=2[m1][m2];[m1]atrim={MUS_SKIP}:{SPL},asetpts=PTS-STARTPTS[a];"
     f"[m2]atrim=start={SPL-DUP},asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=0.03:c1=tri:c2=tri,"
     f"volume=0.6,afade=t=in:d=0.3,atrim=0:{END},afade=t=out:st={END-2.0}:d=2.0,apad=whole_dur={END}",
     "-ac", "2", "-ar", "48000", "-t", str(END), "tmp/mus.wav"])
sfx_in, sfx_f = [], []
for k, h in enumerate(hits):
    sfx_in += ["-i", "tmp/boom.wav"]
    sfx_f.append(f"[{k+2}:a]adelay={int(h*1000)}|{int(h*1000)},volume=0.55[s{k}]")
run(["ffmpeg", "-y", "-i", "tmp/vo.wav", "-i", "tmp/mus.wav", *sfx_in, "-filter_complex",
     ";".join(sfx_f) + ";[0:a]asplit=2[vo][sc];[1:a][sc]sidechaincompress=threshold=0.04:ratio=7:attack=20:release=350[duck];"
     f"[vo][duck]{''.join(f'[s{k}]' for k in range(len(hits)))}amix=inputs={2+len(hits)}:duration=first:normalize=0,alimiter=limit=0.9",
     "-t", str(END), "tmp/mix.wav"])

# ---------------- composição final ----------------
fc = ("[1:v]format=rgba,scale=230:-1:flags=lanczos,split=2[ls][lb0];[lb0]scale=600:-1:flags=lanczos[lb];"
      f"[ls]fade=t=out:st={E0-0.3}:d=0.3:alpha=1[lsf];[lb]fade=t=in:st={E0+0.05}:d=0.45:alpha=1[lbf];"
      "movie=/home/claude/kicks/tmp/grad.png[gr];[0:v][gr]overlay=0:0[v0];"
      f"[v0][lsf]overlay=x=(W-w)/2:y=135:enable='lt(t,{E0+0.05})'[v1];"
      f"[v1][lbf]overlay=x=(W-w)/2:y=330:enable='gte(t,{E0})'[v2];[v2]ass=tmp/subs.ass[v]")
run(["ffmpeg", "-y", "-i", "tmp/base.mp4", "-loop", "1", "-framerate", "30", "-i", "/home/claude/kicks/logo.png",
     "-i", "tmp/mix.wav", "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", str(END),
     "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "reel_15mil_cambio_v2.mp4"])
print("ok")
