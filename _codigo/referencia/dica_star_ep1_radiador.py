#!/usr/bin/env python3
"""DICA DA STAR #1 - "Completou o radiador só com água?" (18/11/2026).
Série aprovada pelo Fernando em 18/11: boneco 3D do Fernando apresenta (HeyGen Avatar 6 turbo, só abertura e
fechamento), narração com a voz clonada "Fernando Star" (Aq4ptfe9mjbOI01Sq8d3), meio com imagens de IA + imagem real
do reel do radiador (café com leite), marca d'água @staroleo_rj flutuando, fechamento "Aqui na Star a gente resolve."
REGRA: nunca citar o bairro na fala/chamada (Fernando, 18/11).
Uso: python3 dica_star_ep1_radiador.py <pasta_fontes> <saida.mp4>
  pasta_fontes: narracao_ep1_radiador.mp3, boneco_falas_ep1.mp4 (HeyGen), ferrugem.png, aditivo.png
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from star_lib import *
from black_lib import estrela
from reel_lib import HDR, ts, G
from PIL import Image, ImageDraw, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H, FPS = 1080, 1920, 30
WD = os.path.join(os.path.dirname(os.path.abspath(OUT)), "tmp_ep1"); os.makedirs(WD, exist_ok=True)
NARR = f"{SRC}/narracao_ep1_radiador.mp3"
BON = f"{SRC}/boneco_falas_ep1.mp4"
RAD = f"{REPO}/2026-10/lote2/reel_dica_radiador.mp4"
MUSIC = f"{REPO}/_codigo/audio/trilha_r15mil.mp3"
FIM = 2.4
NARR_END = 21.55
TOT = round(NARR_END + FIM, 2)
ENC = ["-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p", "-an"]
COR = "eq=contrast=1.06:saturation=1.22,unsharp=5:5:0.4"

def run(a): subprocess.run(a, check=True)

def kenburns(img, dur, out, z0=1.0, z1=1.12, fx0=0.5, fy0=0.5, fx1=0.5, fy1=0.5):
    """Imagem parada -> vídeo com zoom/pan suave (0 crédito)."""
    n = int(round(dur * FPS))
    zexp = f"{z0}+({z1}-{z0})*on/{n}"
    xexp = f"(iw-iw/zoom)*({fx0}+({fx1}-{fx0})*on/{n})"
    yexp = f"(ih-ih/zoom)*({fy0}+({fy1}-{fy0})*on/{n})"
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", img, "-vf",
         f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
         f"zoompan=z='{zexp}':x='{xexp}':y='{yexp}':d={n}:s={W}x{H}:fps={FPS},{COR},format=yuv420p",
         "-frames:v", str(n), *ENC, out])

# ---------- cortes ----------
segs = []
# 1) boneco, abertura (0 a 3,40 s do clipe HeyGen)
run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-t", "3.40", "-i", BON, "-vf",
     f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},{COR},format=yuv420p", *ENC, f"{WD}/s1.mp4"])
segs.append((f"{WD}/s1.mp4", 3.40))
# 2) ferrugem: zoom no reservatório (3,40 a 6,15) e desce para a bomba (6,15 a 8,95)
kenburns(f"{SRC}/ferrugem.png", 2.75, f"{WD}/s2.mp4", 1.0, 1.25, 0.5, 0.45, 0.25, 0.40); segs.append((f"{WD}/s2.mp4", 2.75))
kenburns(f"{SRC}/ferrugem.png", 2.80, f"{WD}/s3.mp4", 1.30, 1.45, 0.75, 0.50, 0.90, 0.55); segs.append((f"{WD}/s3.mp4", 2.80))
# 3) aditivo (8,95 a 13,45)
kenburns(f"{SRC}/aditivo.png", 4.50, f"{WD}/s4.mp4", 1.0, 1.15, 0.5, 0.5, 0.5, 0.4); segs.append((f"{WD}/s4.mp4", 4.50))
# 4) café com leite real (reel do radiador, 5,70 a 6,95 s, área do vídeo y 250..1600) em câmera lenta + quadro final com zoom
crop = "crop=760:1350:160:250,scale=1080:1920:flags=lanczos"
run(["ffmpeg", "-v", "error", "-y", "-ss", "5.70", "-t", "1.05", "-i", RAD, "-vf",
     f"{crop},setpts=2.0*PTS,fps={FPS},{COR},format=yuv420p", *ENC, f"{WD}/s5a.mp4"])
run(["ffmpeg", "-v", "error", "-y", "-ss", "6.60", "-i", RAD, "-frames:v", "1", "-vf", crop, f"{WD}/cafe_last.png"])
kenburns(f"{WD}/cafe_last.png", 3.05, f"{WD}/s5b.mp4", 1.0, 1.15, 0.5, 0.6, 0.5, 0.7)
segs.append((f"{WD}/s5a.mp4", 2.10)); segs.append((f"{WD}/s5b.mp4", 3.05))
# 5) boneco, fechamento (3,65 s em diante do clipe HeyGen) a partir de 18,60
run(["ffmpeg", "-v", "error", "-y", "-ss", "3.65", "-i", BON, "-t", "2.95", "-vf",
     f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},{COR},"
     f"tpad=stop_mode=clone:stop_duration={FIM + 0.2},format=yuv420p", *ENC, f"{WD}/s6.mp4"])
segs.append((f"{WD}/s6.mp4", TOT - 18.60))
t = 0
for _, d in segs[:-1]: t += d
assert abs(t - 18.60) < 0.02, t

lst = f"{WD}/lista.txt"; open(lst, "w").write("".join(f"file '{p}'\nduration {d}\n" for p, d in segs))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-t", str(TOT), "-vf", f"fps={FPS},format=yuv420p", *ENC, f"{WD}/base.mp4"])

# ---------- camadas ----------
# topo fixo: degradê + selo DICA DA STAR
top = Image.new("RGBA", (W, H), (0, 0, 0, 0))
g = Image.new("L", (1, H), 0)
for y in range(H):
    a = 0
    if y < 520: a = int(200 * (1 - y / 520) ** 1.2)
    if y > H - 560: a = max(a, int(215 * min(1, (y - (H - 560)) / 400) ** 1.2))
    g.putpixel((0, y), a)
top.paste(Image.new("RGBA", (W, H), GRAF + (255,)), (0, 0), g.resize((W, H)))
d = ImageDraw.Draw(top)
f = bc(54); txt = "DICA DA STAR"; tw = d.textlength(txt, font=f); bw = tw + 110; x0 = (W - bw) / 2; y0 = 70
d.rounded_rectangle((x0, y0, x0 + bw, y0 + 84), radius=14, fill=GOLD)
estrela(d, x0 + 40, y0 + 42, 22, GRAF)
d.text((x0 + 72, y0 + 42), txt, font=f, fill=GRAF, anchor="lm")
top.save(f"{WD}/topo.png")

# capa/título da abertura (0 a 3,4 s): texto grande amarelo/vermelho estilo "capa"
cap = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dc = ImageDraw.Draw(cap)
def stroke_text(dd, xy, t, font, fill, sw=10):
    dd.text(xy, t, font=font, fill=fill, anchor="mm", stroke_width=sw, stroke_fill=(10, 10, 10))
stroke_text(dc, (W / 2, 250), "RADIADOR SÓ", bc(150), WHITE)
stroke_text(dc, (W / 2, 400), "COM ÁGUA?", bc(170), GOLD)
# faixa vermelha "PARA TUDO!"
band = Image.new("RGBA", (620, 110), (229, 57, 53, 255)); db = ImageDraw.Draw(band)
db.text((310, 55), "PARA TUDO!", font=bc(84), fill=WHITE, anchor="mm")
band = band.rotate(-4, expand=True, resample=Image.BICUBIC)
cap.alpha_composite(band, (int((W - band.width) / 2), 1480))
cap.save(f"{WD}/capa.png")

# fechamento
fim = Image.new("RGBA", (W, H), (0, 0, 0, 0)); df = ImageDraw.Draw(fim)
fim.paste(Image.new("RGBA", (W, 640), (8, 8, 9, 232)), (0, H - 640))
stroke_text(df, (W / 2, H - 560), "AQUI NA STAR", bc(110), WHITE, 0)
stroke_text(df, (W / 2, H - 450), "A GENTE RESOLVE.", bc(110), GOLD, 0)
pill(df, W / 2, H - 350, f"CHAME NO WHATSAPP  {WA}", bc(62), GRAF, GOLD, padx=34, pady=16, center=True)
logo(fim, 300, (W - 300) / 2, H - 200)
fim.save(f"{WD}/fim.png")

# marca d'água @staroleo_rj (flutua devagar)
wm = Image.new("RGBA", (420, 70), (0, 0, 0, 0)); dw = ImageDraw.Draw(wm)
dw.text((210, 35), "@staroleo_rj", font=mr(44), fill=(255, 255, 255, 120), anchor="mm")
wm.save(f"{WD}/wm.png")

# textos animados (palavras-chave) sincronizados com a narração
POP = "\\fscx70\\fscy70\\t(0,170,\\fscx106\\fscy106)\\t(170,260,\\fscx100\\fscy100)"
STY = HDR.replace("[Events]", "Style: Card,Barlow Condensed ExtraBold,104,&H00FFFFFF,&H00FFFFFF,&H00141211,&H00000000,0,0,0,0,100,100,1,0,1,7,0,5,0,0,0,1\n"
                  "Style: Alerta,Barlow Condensed ExtraBold,120,&H00FFFFFF,&H00FFFFFF,&H003539E5,&H003539E5,0,0,0,0,100,100,2,0,3,24,0,5,0,0,0,1\n\n[Events]")
YC = 1560; ev = []
def card(a, b, txt, st="Card", y=YC):
    ev.append(f"Dialogue: 2,{ts(a)},{ts(b)},{st},,0,0,0,,{{\\pos(540,{y})\\fad(50,100){POP}}}{txt}")
card(3.50, 6.15, f"ENFERRUJA{G}\\NPOR DENTRO")
card(6.20, 7.35, f"FERVE MAIS{G}\\NRÁPIDO")
card(7.40, 8.95, f"ESTRAGA A{G}\\NBOMBA D'ÁGUA")
card(9.05, 11.70, f"O CERTO:{G}\\NÁGUA + ADITIVO")
card(11.75, 13.40, f"NA MEDIDA DO{G}\\NFABRICANTE")
card(13.60, 16.00, f"CAFÉ COM LEITE{G}\\NNO RESERVATÓRIO?")
card(16.00, 17.60, f"É ÓLEO{G}\\NMISTURADO COM ÁGUA")
card(17.62, 18.58, "AÍ NÃO ESPERA!", "Alerta")
ass = f"{WD}/textos.ass"; open(ass, "w").write(STY + "\n".join(ev) + "\n")

fc = (f"[0:v]format=rgba[b];[b][1:v]overlay=0:0[v1];"
      f"[2:v]format=rgba[cp];[v1][cp]overlay=0:0:enable='lt(t,3.40)'[v2];"
      f"[v2]ass={ass}[v3];"
      f"[3:v]format=rgba,fade=t=in:st=18.55:d=0.3:alpha=1[fm];[v3][fm]overlay=0:0:enable='gte(t,18.55)'[v4];"
      f"[v4][4:v]overlay=x='330+260*sin(t/3.1)':y='860+520*sin(t/4.3+1)':enable='lt(t,18.55)',format=yuv420p,"
      f"setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[v];"
      f"[5:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{TOT}[voz];"
      f"[6:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{TOT},volume=0.13,afade=t=in:d=0.3,afade=t=out:st={TOT-0.9}:d=0.9[mus];"
      f"[voz][mus]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
run(["ffmpeg", "-v", "error", "-y", "-i", f"{WD}/base.mp4",
     "-loop", "1", "-framerate", str(FPS), "-i", f"{WD}/topo.png",
     "-loop", "1", "-framerate", str(FPS), "-i", f"{WD}/capa.png",
     "-loop", "1", "-framerate", str(FPS), "-i", f"{WD}/fim.png",
     "-loop", "1", "-framerate", str(FPS), "-i", f"{WD}/wm.png",
     "-i", NARR, "-stream_loop", "-1", "-i", MUSIC,
     "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(TOT),
     "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
     "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT])
print(OUT, TOT)
