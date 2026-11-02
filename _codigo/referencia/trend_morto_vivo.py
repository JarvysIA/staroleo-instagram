#!/usr/bin/env python3
"""Reel trend "Brincadeira do morto-vivo" versão câmbio automático (Star, Black November).
Cortes no tempo exato do reel de referência que o Fernando mandou (01/11/2026). MORTO = óleo velho, cárter sujo,
filtro entupido, câmbio aberto; VIVO = óleo novo, cárter limpo, carro liberado. Monitor cardíaco (UTI do câmbio):
pulsa dourado no VIVO e fica reto vermelho no MORTO. O áudio da trend o Fernando escolhe no app do Instagram;
a versão de prévia leva o áudio do reel de referência só para conferir o sincronismo (não postar)."""
import os, sys, math, subprocess, random
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from PIL import Image, ImageDraw, ImageFilter, ImageOps

os.chdir("/home/claude/vivomorto"); os.makedirs("t", exist_ok=True); os.makedirs("ov", exist_ok=True)
W, H, FPS = 1080, 1920, 30
REN, CRE = "/home/claude/renegade/src/", "/home/claude/creta/src/"
KICKS = "/home/claude/kicks/src/"; FOT = "/home/claude/staroleo-instagram/2026-10/fontes/"
RAD = "/home/claude/staroleo-instagram/2026-10/lote2/reel_dica_radiador.mp4"
GRADE = "curves=preset=strong_contrast,eq=saturation=1.45"
TAG = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
LOOK = {"morto": ",eq=saturation=0.5:brightness=-0.04,colorbalance=rs=0.18:gs=-0.04:bs=-0.06",
        "vivo": ",eq=saturation=1.12:brightness=0.02", "intro": "", "flash": ",eq=saturation=0.4,colorbalance=rs=0.25"}
def run(a): subprocess.run(a, check=True)
def enc(out): return ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p", out]

# (início, fim, tipo, fonte, extra, palavra, legenda)
#  fonte: ("v", arquivo, início) vídeo do iPhone | ("p", foto, (cx, cy, zoom0, zoom1)) | ("r", radiador)
T = [
 (0.0, 2.8, "intro", ("v", REN + "2648.mov", 0.8), None, None, None),
 (2.8, 3.4, "flash", ("p", KICKS + "2_carter_sujo.jpg", (0.5, 0.5, 1.2, 1.3)), None, None, None),
 (3.4, 6.7, "intro", ("v", REN + "4781.mov", 2.0), None, None, None),
 (6.7, 7.1, "flash", ("v", REN + "6285.mov", 21.6), None, None, None),
 (7.1, 9.98, "intro", ("v", CRE + "6224.mov", 0.5), None, None, None),
 (9.98, 12.08, "morto", ("v", REN + "6285.mov", 21.0), None, "ÓLEO VELHO = MORTO", None),
 (12.08, 14.0, "vivo", ("v", REN + "6286.mov", 3.0), None, "ÓLEO NOVO = VIVO", None),
 (14.0, 15.4, "intro", ("v", REN + "6277.mov", 1.0), None, "VALENDO!", None),
 (15.4, 17.3, "morto", ("p", KICKS + "2_carter_sujo.jpg", (0.5, 0.55, 1.0, 1.18)), None, "MORTO", "cárter cheio de borra"),
 (17.3, 19.3, "vivo", ("v", CRE + "6239.mov", 2.0), None, "VIVO", "óleo novo entrando"),
 (19.3, 21.0, "vivo", ("v", CRE + "6242.mov", 10.0), None, "VIVO", "Creta liberado"),
 (21.0, 23.1, "morto", ("v", REN + "6285.mov", 23.0), None, "MORTO", "óleo velho saindo"),
 (23.1, 24.1, "vivo", ("p", FOT + "cronos/foto_carter_limpo_motul.jpg", (0.55, 0.4, 1.05, 1.18)), None, "VIVO", "cárter limpinho"),
 (24.1, 25.07, "morto", ("p", KICKS + "4_filtros.jpg", (0.66, 0.42, 1.55, 1.7)), None, "MORTO", "filtro entupido"),
 (25.07, 26.07, "vivo", ("v", REN + "6288.mov", 5.0), None, "VIVO", "óleo novo no visor"),
 (26.07, 27.07, "morto", ("r", RAD, 5.7), None, "MORTO", "água misturada com óleo"),
 (27.07, 27.57, "vivo", ("v", REN + "6286.mov", 5.5), None, "VIVO", None),
 (27.57, 28.1, "morto", ("v", REN + "2648.mov", 18.6), None, "MORTO", None),
 (28.1, 28.6, "vivo", ("p", KICKS + "4_filtros.jpg", (0.36, 0.42, 1.55, 1.65)), None, "VIVO", None),
 (28.6, 29.0, "morto", ("v", CRE + "6225.mov", 3.0), None, "MORTO", None),
 (29.0, 30.0, "vivooo", ("v", REN + "2650.mov", 19.4), None, "VIVOOOO", "Renegade liberada"),
]
END0, TOT = 30.0, 34.0

def seg_video(src, a, d, look, out, zoom=(1.0, 1.06)):
    z = f"({zoom[0]}+({zoom[1]}-{zoom[0]})*t/{d})"
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},format=yuv420p,{TAG},{GRADE}{look},"
          f"scale=w='trunc({W}*{z}/2)*2':h=-2:eval=frame,crop={W}:{H}")
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", src, "-t", f"{d:.3f}", "-vf", vf] + enc(out))

def seg_radiador(src, a, d, look, out):
    # reel já editado (SDR): pega só a área do vídeo 4:5 (sem textos) e amplia para 9:16
    vf = (f"crop=1080:1100:0:330,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p,{TAG}{look}")
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", src, "-t", f"{d:.3f}", "-vf", vf] + enc(out))

def seg_foto(path, params, d, look, out):
    cx, cy, z0, z1 = params
    im = carregar(path)
    s = max(W / im.width, H / im.height) * z1 * 1.02
    big = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    n = max(1, int(round(d * FPS))); os.makedirs("t/f", exist_ok=True)
    for i in range(n):
        z = z0 + (z1 - z0) * i / max(1, n - 1)
        # recorte: janela W*k x H*k na imagem ampliada, k = z1/z
        k = z1 / z * 1.0
        ww, hh = W * k * 1.02, H * k * 1.02
        x0 = min(max(cx * big.width - ww / 2, 0), big.width - ww); y0 = min(max(cy * big.height - hh / 2, 0), big.height - hh)
        big.crop((int(x0), int(y0), int(x0 + ww), int(y0 + hh))).resize((W, H), Image.LANCZOS).save(f"t/f/{i:04d}.jpg", quality=92)
    run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", "t/f/%04d.jpg", "-vf", f"format=yuv420p,{TAG}{look}",
         "-frames:v", str(n)] + enc(out))
    for f in os.listdir("t/f"): os.remove("t/f/" + f)

parts = []
for i, (a, b, kind, src, _, _, _) in enumerate(T):
    d = b - a; out = f"t/s{i:02d}.mp4"; look = LOOK["vivo" if kind == "vivooo" else kind]
    if not (os.environ.get("REUSE") and os.path.exists(out)):
        if src[0] == "v": seg_video(src[1], src[2], d, look, out, zoom=(1.0, 1.08) if kind in ("intro", "vivooo") else (1.04, 1.12))
        elif src[0] == "r": seg_radiador(src[1], src[2], d, look, out)
        else: seg_foto(src[1], src[2], d, look, out)
    parts.append(out)
run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x080809:s={W}x{H}:r={FPS}:d={TOT-END0}"] + enc("t/end.mp4"))
parts.append("t/end.mp4")
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "t/joined.mp4"])

# ---------------- camada gráfica (PIL, quadro a quadro) ----------------
RED = (229, 57, 53); GREEN = (64, 220, 120)
fW = bc(170); fWbig = bc(200); fSub = mr(44); fTit = bc(118); fTit2 = bc(62)

def sparkle(d, cx, cy, r, cor=GOLD):
    pts = []
    for k in range(8):
        a = -math.pi / 2 + k * math.pi / 4; rr = r if k % 2 == 0 else r * 0.22
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=cor)

def texto_sombra(img, xy, txt, font, fill, sombra=(0, 0, 0), raio=10, anchor="mm", glow=None):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.text(xy, txt, font=font, fill=(glow or sombra) + (230,), anchor=anchor, stroke_width=8, stroke_fill=(glow or sombra) + (230,))
    lay = lay.filter(ImageFilter.GaussianBlur(raio)); img.alpha_composite(lay)
    ImageDraw.Draw(img).text(xy, txt, font=font, fill=fill, anchor=anchor, stroke_width=3, stroke_fill=(20, 18, 17))

def ecg(img, t, modo, y0=1440, h=170, cor=None):
    d = ImageDraw.Draw(img, "RGBA"); x0, x1 = 60, W - 60
    d.rounded_rectangle((x0, y0, x1, y0 + h), radius=18, fill=(5, 10, 8, 175), outline=(255, 255, 255, 40), width=2)
    for gx in range(x0 + 30, x1, 40): d.line([(gx, y0 + 8), (gx, y0 + h - 8)], fill=(80, 255, 140, 18), width=1)
    for gy in range(y0 + 20, y0 + h, 30): d.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(80, 255, 140, 18), width=1)
    mid = y0 + h * 0.58; pts = []; L = x1 - 200 - (x0 + 20)
    cor = cor or (GOLD if modo != "morto" else RED)
    for i in range(0, L, 3):
        x = x0 + 20 + i
        if modo == "morto": y = mid + math.sin(i * 0.9 + t * 40) * 1.2
        else:
            ph = ((i / L) * 3.2 - t * 2.4) % 1.0      # ~2,4 batidas por segundo correndo pra esquerda
            if 0.40 < ph < 0.44: y = mid + (ph - 0.40) / 0.04 * 18
            elif 0.44 < ph < 0.47: y = mid + 18 - (ph - 0.44) / 0.03 * (h * 0.62 + 18)
            elif 0.47 < ph < 0.51: y = mid - h * 0.62 + (ph - 0.47) / 0.04 * (h * 0.62 + 26)
            elif 0.51 < ph < 0.54: y = mid + 26 - (ph - 0.51) / 0.03 * 26
            elif 0.62 < ph < 0.72: y = mid - math.sin((ph - 0.62) / 0.10 * math.pi) * 14
            else: y = mid
        pts.append((x, y))
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).line(pts, fill=cor + (200,), width=12)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(img, "RGBA"); d.line(pts, fill=cor + (255,), width=5)
    bpm = "0" if modo == "morto" else str(118 + int(6 * math.sin(t * 3)))
    d.text((x1 - 100, y0 + 52), "BPM", font=bcb(34), fill=(255, 255, 255, 170), anchor="mm")
    d.text((x1 - 100, y0 + 112), bpm, font=bc(78), fill=cor, anchor="mm")

grad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gp = grad.load()
for y in range(H):
    a = 0
    if y < 420: a = int(160 * (1 - y / 420) ** 1.4)
    if y > 1000: a = max(a, int(200 * min(1, (y - 1000) / 700) ** 1.3))
    for x in range(W): gp[x, y] = (8, 8, 9, a)
LOGO_S = LOGO.resize((190, round(LOGO.height * 190 / LOGO.width)), Image.LANCZOS)

# fechamento (fundo fixo)
endbg = Image.new("RGBA", (W, H), (8, 8, 9, 255)); badge(endbg, 300, tam=0.95); de = ImageDraw.Draw(endbg)
ctext(de, W, 470, "CÂMBIO MORTO?", bc(132), WHITE); ctext(de, W, 610, "NA STAR ELE", bc(132), GOLD); ctext(de, W, 745, "VOLTA A VIVER.", bc(132), GOLD)
yy = selo(endbg, 1180, letra=None); de = ImageDraw.Draw(endbg)
pill(de, W / 2, yy + 40, f"WHATSAPP  {WA}", bc(60), GRAF, GOLD, padx=36, pady=20, center=True)
ctext(de, W, yy + 170, ENDERECO, mr(36), MUTED); logo(endbg, 220, (W - 220) // 2, 1640)

def kind_at(t):
    for a, b, k, *_ in T:
        if a <= t < b: return a, b, k
    return None

n = int(TOT * FPS)
for fi in range(n):
    t = fi / FPS; img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if t >= END0:
        img = endbg.copy(); ecg(img, t, "vivo", y0=930, h=200)
        a = min(1, (t - END0) / 0.25); img.putalpha(Image.eval(img.getchannel("A"), lambda v: int(v * a)))
        img.save(f"ov/{fi:04d}.png"); continue
    img.alpha_composite(grad)
    a, b, k = kind_at(t); row = [r for r in T if r[0] == a][0]; word, sub = row[5], row[6]; dt = t - a
    if t < 15.4:
        # título da brincadeira
        d = ImageDraw.Draw(img)
        texto_sombra(img, (W / 2, 175), "BRINCADEIRA DO", fTit2, WHITE)
        texto_sombra(img, (W / 2, 265), "MORTO-VIVO", fTit, GOLD)
        texto_sombra(img, (W / 2, 350), "versão câmbio automático", mr(40), WHITE, raio=8)
        if 3.4 <= t < 6.7:
            texto_sombra(img, (W / 2, 1320), "REGRA DO CHEFE:", bc(96), WHITE)
            texto_sombra(img, (W / 2, 1420), "ESCUTA O QUE EU DIGO", bc(72), GOLD)
        if word:
            col = RED if "MORTO" in word else GOLD
            sc = min(1, 0.6 + dt / 0.15 * 0.4)
            f = bc(int(112 * sc)) if word != "VALENDO!" else bc(int(170 * sc))
            texto_sombra(img, (W / 2, 1250), word, f, WHITE if word == "VALENDO!" else col, glow=(0, 0, 0))
            if word != "VALENDO!": ecg(img, t, "morto" if "MORTO" in word else "vivo")
    else:
        img.alpha_composite(LOGO_S, ((W - LOGO_S.width) // 2, 150))
        sc = 0.55 + 0.45 * min(1, dt / 0.12); sc = sc * (1 + 0.06 * max(0, 1 - abs(dt - 0.12) / 0.1))
        if k == "morto":
            texto_sombra(img, (W / 2, 1230), "MORTO", bc(int(190 * sc)), WHITE, glow=RED, raio=16)
        else:
            txt = word; f = bc(int((200 if k == "vivooo" else 190) * sc))
            texto_sombra(img, (W / 2, 1230), txt, f, WHITE, glow=(200, 150, 0), raio=16)
            d = ImageDraw.Draw(img); tw = d.textlength(txt, font=f)
            tw_ = 0.6 + 0.4 * abs(math.sin(t * 9))
            sparkle(d, W / 2 - tw / 2 - 60, 1205, 34 * sc * tw_); sparkle(d, W / 2 + tw / 2 + 60, 1205, 34 * sc * (1.6 - tw_))
            sparkle(d, W / 2 + tw / 2 + 25, 1150, 16 * sc)
        if sub: texto_sombra(img, (W / 2, 1345), sub, mr(46), (235, 235, 235), raio=8)
        ecg(img, t, "morto" if k == "morto" else "vivo")
        # clarão vermelho no início de cada MORTO
        if k == "morto" and dt < 0.10:
            fl = Image.new("RGBA", (W, H), RED + (int(110 * (1 - dt / 0.10)),)); img.alpha_composite(fl)
    if k == "flash":
        fl = Image.new("RGBA", (W, H), (255, 255, 255, 60)); img.alpha_composite(fl)
    img.save(f"ov/{fi:04d}.png")

run(["ffmpeg", "-v", "error", "-y", "-i", "t/joined.mp4", "-framerate", str(FPS), "-i", "ov/%04d.png",
     "-filter_complex", f"[0:v][1:v]overlay=0:0:format=auto,format=yuv420p,{TAG}[v]", "-map", "[v]", "-t", str(TOT),
     "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
     "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "t/video.mp4"])
# versão para postar (áudio mudo: o Fernando escolhe o áudio da trend no Instagram)
run(["ffmpeg", "-v", "error", "-y", "-i", "t/video.mp4", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest",
     "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "reel_vivo_morto_POSTAR_sem_audio.mp4"])
# prévia com o áudio do reel de referência (só para conferir o ritmo)
run(["ffmpeg", "-v", "error", "-y", "-i", "t/video.mp4", "-i", "ref/trend.mp4", "-map", "0:v", "-map", "1:a", "-shortest",
     "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "previa_com_musica_da_trend.mp4"])
print("ok")
