#!/usr/bin/env python3
"""VERSÃO TOKYO DRIFT (27/11): mesmos cortes do vídeo de referência, SEM música (o Fernando põe o áudio da trend no app do Instagram).
Reel 'cortes no ritmo' da troca de óleo do câmbio (pedido do Fernando em 27/11/2026, a partir de um vídeo de
referência de carro: abertura lenta com aproximação, cortes rápidos na batida, plano aberto, silêncio, batida
final com a marca). Material: VW de 05/11 (IMG_4841..4873, Downloads do notebook) + b-roll do Cronos (IMG_6155)
e cárter com borra (IMG_2548). Trilha paga trilha_r15mil (~158 bpm, batida 0,3805 s).
Uso: python3 reel_cortes_cambio_ritmo.py <pasta_fontes> <saida.mp4>"""
import subprocess, os, sys
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from reel_lib import cor_video

SRC, OUT = sys.argv[1], sys.argv[2]
W, H, FPS = 1080, 1920, 30
WD = "/home/claude/ed27/t2"; os.makedirs(WD, exist_ok=True)
MUS = "/home/claude/staroleo-instagram/_codigo/audio/trilha_r15mil.mp3"
LOGO = "/home/claude/staroleo-instagram/_codigo/logo.png"
B = 0.3805                       # batida da trilha
GRADE = "eq=saturation=1.28:contrast=1.07:brightness=0.01,unsharp=5:5:0.6"
TAG = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
def run(a): subprocess.run(a, check=True)
def enc(o): return ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "15", "-pix_fmt", "yuv420p", "-r", str(FPS), o]
def s(n): return os.path.join(SRC, n)

def clip(src, a, d, out, lento=1.0, z0=1.0, z1=1.0, cx=0.5, cy=0.5):
    """trecho de vídeo; lento=2 = câmera lenta (60 fps); z0->z1 = aproximação digital"""
    pre = f"setpts={lento}*PTS," if lento != 1 else ""
    n = int(round(d * FPS))
    zoom = ""
    if z0 != 1.0 or z1 != 1.0:
        zoom = (f",scale={W*2}:{H*2},zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw*{cx}-iw/zoom/2':"
                f"y='ih*{cy}-ih/zoom/2':d=1:s={W}x{H}:fps={FPS}")
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(d / lento + 0.2), "-i", src, "-vf",
         f"{pre}scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS}{zoom},"
         f"format=yuv420p,{cor_video(src)},{GRADE},{TAG}", "-frames:v", str(n)] + enc(out))

# tempos exatos dos cortes do vídeo de referência (detecção de cena): 4,00 4,43 4,90 5,40 5,87 6,17 6,50 6,83 7,30 7,80 8,73 9,73 11,67; batida forte em 12,0
CUTS = [0.0, 4.0, 4.43, 4.9, 5.4, 5.87, 6.17, 6.5, 6.83, 7.3, 7.8, 8.73, 9.73, 11.67]
INTRO = 4.0
SH = [("IMG_4849.MOV", 0.9, 2.0, 1.0, 1.25),                       # abertura (até o Fernando gravar a água pingando)
      ("IMG_4850.MOV", 20.9), ("IMG_4848.MOV", 1.0), ("IMG_4851.MOV", 57.0), ("IMG_4855.MOV", 6.0),
      ("IMG_6155.MOV", 1.0), ("IMG_4850.MOV", 27.0), ("IMG_4854.MOV", 9.6), ("IMG_6155.MOV", 5.6), ("IMG_4873.MP4", 3.2),
      ("IMG_4848.MOV", 25.6, 1.0, 1.0, 1.05),                       # 7,80: entra o grave -> técnico com a chave
      ("IMG_6155.MOV", 9.4, 1.0, 1.0, 1.05),                        # máquina Motul
      ("IMG_4841.MOV", 0.0, 1.0, 1.0, 1.0)]                         # plano aberto VW com a placa da Star
OPEN = os.environ.get("ABERTURA")                                   # vídeo da água pingando, se houver
SC = []
for i, sh in enumerate(SH):
    d = round(CUTS[i + 1] - CUTS[i], 3)
    n, a = sh[0], sh[1]; lento, z0, z1 = (sh[2:] + (1.0, 1.0, 1.0))[:3] if len(sh) > 2 else (1.0, 1.0, 1.0)
    if i == 0 and OPEN: SC.append((OPEN, float(os.environ.get("ABERTURA_INI", "0")), d, 1.0, 1.0, 1.25)); continue
    SC.append((s(n), a, d, lento, z0, z1))
GAP = 12.0 - 11.67                                                  # silêncio antes da batida
END = 15.7 - 12.0
parts, t = [], 0.0
for i, (src, a, d, lento, z0, z1) in enumerate(SC):
    p = f"{WD}/c{i:02d}.mp4"; clip(src, a, d, p, lento, z0, z1, cy=0.45 if i == 0 else 0.5); parts.append(p); t += d
V_CUT = t
# fundo do fim: último quadro do VW escurecido (silêncio + cartela)
run(["ffmpeg", "-v", "error", "-y", "-ss", "1.55", "-i", s("IMG_4841.MOV"), "-frames:v", "1", "-vf",
     f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{cor_video(s('IMG_4841.MOV'))},{GRADE}", f"{WD}/fim.png"])
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{WD}/fim.png", "-t", str(GAP + END), "-vf",
     f"boxblur=14:2,eq=brightness=-0.40:saturation=0.85,format=yuv420p,{TAG}"] + enc(f"{WD}/fim.mp4"))
parts.append(f"{WD}/fim.mp4")
open(f"{WD}/lista.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/lista.txt", "-c", "copy", f"{WD}/base.mp4"])
TOT = V_CUT + GAP + END
T_END = V_CUT + GAP                     # batida final

# textos (ASS): @ no canto (como a referência) e cartela final
def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); sec = x % 60
    return f"{h}:{m:02d}:{sec:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Arroba,Barlow Condensed ExtraBold,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,0,2,9,0,48,150,1
Style: Tit,Barlow Condensed ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Gold,Barlow Condensed ExtraBold,96,&H0021C3F0,&H0021C3F0,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Btn,Barlow Condensed ExtraBold,60,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,24,0,5,0,0,0,1
Style: Info,Manrope,40,&H00E6E6E6,&H00E6E6E6,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
POP = "\\fscx70\\fscy70\\t(0,180,\\fscx104\\fscy104)\\t(180,260,\\fscx100\\fscy100)"
ev = [f"Dialogue: 0,{ts(0.3)},{ts(V_CUT)},Arroba,,0,0,0,,@staroleo_rj"]
ev += [f"Dialogue: 0,{ts(T_END + 0.25)},{ts(TOT)},Tit,,0,0,0,,{{\\pos(540,1060){POP}\\fad(0,0)}}TROCA DE ÓLEO",
       f"Dialogue: 0,{ts(T_END + 0.40)},{ts(TOT)},Gold,,0,0,0,,{{\\pos(540,1160){POP}}}DO CÂMBIO AUTOMÁTICO",
       f"Dialogue: 0,{ts(T_END + 0.9)},{ts(TOT)},Info,,0,0,0,,{{\\pos(540,1290)\\fad(200,0)}}Aqui na Star a gente resolve.",
       f"Dialogue: 0,{ts(T_END + 1.2)},{ts(TOT)},Btn,,0,0,0,,{{\\pos(540,1460){POP}}}WHATSAPP (21) 97544-6417",
       f"Dialogue: 0,{ts(T_END + 1.4)},{ts(TOT)},Info,,0,0,0,,{{\\pos(540,1580)\\fad(200,0)}}Estr. dos Bandeirantes, 841"]
open(f"{WD}/txt.ass", "w").write(hdr + "\n".join(ev) + "\n")

# logo: entra na batida final com escala e brilho
LW = 620
vf = (f"[1:v]scale={LW}:-1:flags=lanczos,format=rgba[lg];"
      f"[lg]split[l1][l2];[l2]boxblur=18:2,colorchannelmixer=aa=0.9[gl];"
      f"[0:v][gl]overlay=x=(W-w)/2:y=640-h/2:enable='gte(t,{T_END})'[g1];"
      f"[g1][l1]overlay=x=(W-w)/2:y=640-h/2:enable='gte(t,{T_END})'[g2];"
      f"[g2]ass={WD}/txt.ass,"
      f"fade=t=in:st=0:d=0.25,fade=t=out:st={TOT-0.5}:d=0.5,{TAG}[v]")
run(["ffmpeg", "-v", "error", "-y", "-i", f"{WD}/base.mp4", "-loop", "1", "-i", LOGO,
     "-filter_complex", vf, "-map", "[v]", "-an", "-t", str(TOT),
     "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
     "-movflags", "+faststart", OUT])
print("ok", OUT, round(TOT, 2), "s; batida final em", round(T_END, 2))
