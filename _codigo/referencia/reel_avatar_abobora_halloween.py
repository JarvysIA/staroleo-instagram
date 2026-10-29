#!/usr/bin/env python3
"""Reel Star: Especial Halloween (31/10/2026). Avatar abóbora (Kling 2.5 a partir da foto gerada da oficina) +
locução Nassif (ElevenLabs v4) + cortes reais da Renegade (óleo velho, máquina, visor) + foto do filtro novo x velho.
Trilha: drone sintetizado (suspense) até "Quer dormir tranquilo?", depois trilha corporativa (alívio)."""
import subprocess, os, json
os.chdir("/home/claude/halloween"); os.makedirs("t", exist_ok=True)
W, H, FPS = 1080, 1920, 30
LOGO = "/home/claude/staroleo-instagram/_codigo/logo.png"
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_corporativa_m1.mp3"
REN = "/home/claude/renegade/src"
FILTRO = "/home/claude/staroleo-instagram/2026-10/fontes/cronos/foto_filtro_novo_x_velho.jpg"
GOLD = "&H0021C3F0&"; WHITE = "&H00FFFFFF&"; RED = "&H003539E5&"; ORANGE = "&H001A8CFF&"
GRADE = "curves=preset=strong_contrast,eq=saturation=1.45"          # iPhone HLG (regra 26/10)
TAG709 = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
VO = 0.3                                                             # locução começa em 0,3 s
END = 3.3

def run(a): subprocess.run(a, check=True)
def enc(out): return ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p", out]

# ---------- segmentos ----------
def avatar(a, d, out, zoom0=1.0, zoom1=1.12, rev=False, shake=()):
    """Clipe do Kling (1072x1928, 24 fps): push-in lento centrado na abóbora; rev=True toca de trás pra frente."""
    if os.environ.get("REUSE") and os.path.exists(out): return
    z = f"({zoom0}+({zoom1}-{zoom0})*t/{d})"
    sh = "+".join(f"between(t,{s},{e})*22*sin(t*90)" for s, e in shake) or "0"
    vf = (f"trim=start={a}:duration={d},setpts=PTS-STARTPTS," + ("reverse," if rev else "") +
          f"fps={FPS},scale=w='trunc(1140*{z}/2)*2':h=-2:eval=frame:flags=lanczos,"
          f"crop={W}:{H}:x='(iw-{W})/2+({sh})':y='(ih-{H})*0.42+({sh})*0.6',format=yuv420p,{TAG709}")
    run(["ffmpeg", "-v", "error", "-y", "-i", "avatar_kling.mp4", "-vf", vf, "-t", str(d)] + enc(out))

def broll(n, a, d, out):
    if os.environ.get("REUSE") and os.path.exists(out): return
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", f"{REN}/{n}.mov", "-t", str(d),
         "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},format=yuv420p,{TAG709},{GRADE}"] + enc(out))

def filtro(d, out):
    """Foto filtro novo x velho: fundo desfocado + foto na largura, etiquetas NOVO/VELHO, zoom lento no filtro velho."""
    from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont
    im = ImageOps.exif_transpose(Image.open(FILTRO)).convert("RGB")
    bg = im.resize((W, int(im.height * W / im.width) * 2 // 1)).resize((W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (17, 18, 20)), 0.55)
    fg = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS); fy = (H - fg.height) // 2
    bg.paste(fg, (0, fy)); d0 = ImageDraw.Draw(bg)
    f = ImageFont.truetype("/home/claude/staroleo-instagram/_codigo/fonts/barlow-condensed-latin-800-normal.ttf", 54)
    for txt, cx, cy, col, tc in (("NOVO", 0.28, 0.31, (240, 195, 33), (20, 18, 17)), ("VELHO", 0.73, 0.29, (229, 57, 53), (255, 255, 255))):
        x, y = int(cx * W), fy + int(cy * fg.height); bb = d0.textbbox((0, 0), txt, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d0.rectangle([x - tw // 2 - 18, y - th // 2 - 14, x + tw // 2 + 18, y + th // 2 + 18], fill=col)
        d0.text((x - tw // 2 - bb[0], y - th // 2 - bb[1]), txt, font=f, fill=tc)
    bg.save("t/filtro_card.png")
    n = int(d * FPS); cx, cy = 0.68 * W, fy + 0.40 * fg.height
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", "t/filtro_card.png", "-vf",
         f"scale={W*2}:{H*2},zoompan=z='1+0.22*on/{n}':x='{cx*2}*(1-1/zoom)*0.9':y='{cy*2}*(1-1/zoom)*0.9':d={n}:s={W}x{H}:fps={FPS},format=yuv420p,{TAG709}",
         "-frames:v", str(n)] + enc(out))

SEGS = [("A1", 8.9), ("B1", 1.65), ("B2", 2.95), ("A2", 4.9), ("B3", 1.5), ("B4", 2.3), ("B5", 1.8), ("A3", 2.9)]
avatar(0.0, 8.9, "t/A1.mp4", 1.0, 1.14)
broll("6285", 21.0, 1.65, "t/B1.mp4")
filtro(2.95, "t/B2.mp4")
avatar(5.1, 4.9, "t/A2.mp4", 1.22, 1.30, rev=True, shake=((0.10, 0.45), (0.70, 1.05)))
broll("2650", 19.4, 1.5, "t/B3.mp4")
broll("6286", 3.0, 2.3, "t/B4.mp4")
broll("6288", 5.0, 1.8, "t/B5.mp4")
avatar(1.0, 2.9, "t/A3.mp4", 1.38, 1.48)
starts, t = {}, 0.0
for k, d in SEGS: starts[k] = t; t += d
V_END = t; TOT = V_END + END
# fundo do fechamento: último quadro do avatar escurecido e desfocado
run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", "t/A3.mp4", "-frames:v", "1", "t/last.png"])
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", "t/last.png", "-t", str(END), "-vf",
     f"gblur=sigma=26,eq=brightness=-0.22:saturation=0.8,fps={FPS},format=yuv420p,{TAG709}"] + enc("t/end.mp4"))
parts = [f"t/{k}.mp4" for k, _ in SEGS] + ["t/end.mp4"]
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "14",
     "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "t/joined.mp4"])

# ---------- áudio ----------
CALM = starts["B3"]                     # "Quer dormir tranquilo?" -> sai o suspense, entra a trilha
HITS = [VO + 0.0, VO + 12.52, VO + 13.32, VO + 13.92]   # Buuu, terror, tranco, patinada
drone = ("aevalsrc=exprs='0.20*sin(2*PI*55*t)*(0.65+0.35*sin(2*PI*0.23*t))+0.11*sin(2*PI*82.41*t+2.5*sin(2*PI*0.4*t))"
         "+0.07*sin(2*PI*77.78*t)*(0.5+0.5*sin(2*PI*0.31*t))+0.05*sin(2*PI*233.08*t)*(0.5+0.5*sin(2*PI*0.17*t))':s=48000:d=" + f"{CALM+1.0}")
run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", drone, "-af",
     f"lowpass=f=700,afade=t=in:d=0.4,afade=t=out:st={CALM-0.4}:d=1.2,aformat=channel_layouts=stereo", "t/drone.wav"])
run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anoisesrc=c=brown:a=0.9:d=1.6:r=48000", "-f", "lavfi",
     "-i", "aevalsrc=exprs='0.9*sin(2*PI*48*t*(1-0.35*t))*exp(-3.2*t)':s=48000:d=1.6", "-filter_complex",
     "[0:a]lowpass=f=900,afade=t=out:st=0:d=1.5:curve=exp[n];[n][1:a]amix=inputs=2:normalize=0,aformat=channel_layouts=stereo[a]",
     "-map", "[a]", "t/hit.wav"])
run(["ffmpeg", "-v", "error", "-y", "-i", "voz.mp3", "-af", "loudnorm=I=-16:TP=-2,aresample=48000", "-ac", "2", "t/voz.wav"])
ins = ["-i", "t/voz.wav", "-i", "t/drone.wav", "-stream_loop", "-1", "-i", MUSIC] + sum([["-i", "t/hit.wav"] for _ in HITS], [])
fc = f"[0:a]adelay={int(VO*1000)}:all=1[v];[1:a]volume=0.55[d];"
fc += (f"[2:a]atrim=0:{TOT-CALM},asetpts=PTS-STARTPTS,volume='if(lt(t,{V_END-CALM}),0.22,0.45)':eval=frame,"
       f"afade=t=in:d=0.8,afade=t=out:st={TOT-CALM-1.0}:d=1.0,adelay={int(CALM*1000)}:all=1[m];")
for i, h in enumerate(HITS):
    fc += f"[{3+i}:a]volume={0.55 if i else 0.75},adelay={int(h*1000)}:all=1[h{i}];"
fc += "[v][d][m]" + "".join(f"[h{i}]" for i in range(len(HITS))) + f"amix=inputs={3+len(HITS)}:normalize=0:duration=longest,atrim=0:{TOT},loudnorm=I=-14:TP=-1.5:LRA=11[a]"
run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", fc, "-map", "[a]", "-ar", "48000", "t/mix.wav"])

# ---------- legendas ----------
def ts(x): x = max(x, 0); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Barlow Condensed ExtraBold,100,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,7,3,5,40,40,0,1
Style: TagO,Barlow Condensed ExtraBold,50,&H00141211,&H00141211,{ORANGE},{ORANGE},0,0,0,0,100,100,3,0,3,14,0,5,0,0,0,1
Style: TagG,Barlow Condensed ExtraBold,50,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,3,0,3,14,0,5,0,0,0,1
Style: TagR,Barlow Condensed ExtraBold,50,&H00FFFFFF,&H00FFFFFF,{RED},{RED},0,0,0,0,100,100,3,0,3,14,0,5,0,0,0,1
Style: Big,Barlow Condensed ExtraBold,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Info,Manrope ExtraLight SemiBold,42,&H00D0CCCA,&H00D0CCCA,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Btn,Barlow Condensed ExtraBold,62,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,24,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
def add(st, en, style, x, y, text, layer=1, extra=""):
    ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{{\\pos({x},{y}){extra}}}{text}")
POP = "\\fscx70\\fscy70\\t(0,140,\\fscx104\\fscy104)\\t(140,220,\\fscx100\\fscy100)"
FD = "\\fad(200,150)"
col = lambda c, s: "{\\c" + c + "}" + s + "{\\c" + WHITE + "}"
SCARY = {"TERROR", "TRANCO", "PATINADA", "BORRA", "VENCIDO", "BUUU"}

words = json.load(open("words.json"))
FIX = {"Bum!": "Buuu...", "conceito": "conserto"}
words = [[FIX.get(w, w), a, b] for w, a, b in words]
groups, cur = [], []
for w in words:
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
        ps = []
        for j, x in enumerate(grp):
            c = clean(x[0])
            ps.append(col(ORANGE if c in SCARY else GOLD, c) if j == k else c)
        add(st, en, "Cap", 540, 1450, " ".join(ps), layer=2, extra=POP if k == 0 else "")

add(0.15, V_END, "TagO", 540, 330, "ESPECIAL HALLOWEEN", extra=FD)
add(starts["B1"], starts["B2"], "TagR", 540, 420, "ÓLEO VELHO DO CÂMBIO", extra=FD)
add(starts["B2"], starts["A2"], "TagR", 540, 420, "FILTRO DO CÂMBIO ENTUPIDO", extra=FD)
add(starts["B4"], starts["A3"], "TagG", 540, 420, "TROCA COMPLETA NA MÁQUINA", extra=FD)
D = "\\fad(300,0)"
add(V_END + 0.3, TOT, "Big", 540, 880, "SEM TERROR", extra=D)
add(V_END + 0.45, TOT, "Big", 540, 1000, col(GOLD, "NO SEU CÂMBIO."), extra=D)
add(V_END + 0.75, TOT, "Btn", 540, 1175, "WHATSAPP  (21) 97544-6417", extra=D + POP)
add(V_END + 0.95, TOT, "Info", 540, 1300, "Até 10x sem juros", extra=D)
add(V_END + 1.05, TOT, "Info", 540, 1360, "Estr. dos Bandeirantes, 841 · Taquara", extra=D)
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

from PIL import Image
g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = g.load()
for y in range(H):
    a = 0
    if y < 620: a = int(170 * (1 - y / 620) ** 1.3)
    if y > 1150: a = max(a, int(190 * min(1, (y - 1150) / 600) ** 1.2))
    for x in range(W): px[x, y] = (17, 18, 20, a)
g.save("t/grad.png")

# clarões vermelhos nos sustos
flash = ",".join(f"drawbox=x=0:y=0:w={W}:h={H}:color=0xE53935@0.38:t=fill:enable='between(t,{h},{h+0.12})'" for h in HITS[1:])
fc = ("[1:v]format=rgba,scale=210:-1:flags=lanczos,split=2[ls][lb0];[lb0]scale=520:-1:flags=lanczos[lb];"
      f"[lb]fade=t=in:st={V_END+0.05}:d=0.45:alpha=1[lbf];"
      f"movie=t/grad.png[gr];[0:v][gr]overlay=0:0:enable='lt(t,{V_END})'[v0];"
      f"[v0][ls]overlay=x=(W-w)/2:y=150:enable='lt(t,{V_END})'[v1];"
      f"[v1][lbf]overlay=x=(W-w)/2:y=430:enable='gte(t,{V_END})'[v2];[v2]{flash},vignette=angle=0.55:enable='lt(t,{CALM})',"
      f"ass=t/subs.ass,{TAG709}[v]")
run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mp4", "-loop", "1", "-framerate", str(FPS), "-i", LOGO, "-i", "t/mix.wav",
     "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
     "-profile:v", "high", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "reel_halloween_abobora.mp4"])
print("ok", {k: round(v, 2) for k, v in starts.items()}, round(V_END, 2), round(TOT, 2))
