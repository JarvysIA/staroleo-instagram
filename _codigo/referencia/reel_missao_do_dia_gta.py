#!/usr/bin/env python3
"""Reel 'Missão do dia' (pegando o assunto do lançamento do GTA 6 em 19/11/2026, SEM logo, personagem, arte ou música do jogo).
Roteiro aprovado pelo Fernando em 17/11/2026 19h49. Material real da Star (do começo ao fim a mesma BMW X2 2021: óleo velho e sujo, troca na máquina; ajuste pedido pelo Fernando em 17/11 20h06).
HUD de 'missão' com visual próprio da Star (preto e dourado). Só texto + trilha + um 'plim' sintetizado no final."""
import subprocess, os, sys
W, H, FPS = 1080, 1920, 30
WD = "/home/claude/v1711"; os.makedirs(WD + "/t", exist_ok=True); os.chdir(WD)
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from black_lib import *
from reel_lib import cor_video
S = "/home/claude/v0711/src/"
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_r15mil.mp3"
OUT = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-17/reel_missao_do_dia_gta.mp4"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
TAG709 = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
def run(a): subprocess.run(a, check=True)
def enc(out): return ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p", out]

def broll(src, a, d, out):
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(d), "-i", src, "-vf",
         f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},format=yuv420p,{cor_video(src)}",
         "-t", str(d)] + enc(out))

# (fonte, início, duração, textos centrais)
SC = [
  (S + "b7221792-IMG_6499.mov", 8.0, 2.8, [("HOJE SAI", "w"), ("O GTA 6.", "g")]),
  (S + "IMG_6507.mov", 22.0, 2.6, [("ENQUANTO ISSO,", "w"), ("A MISSÃO DE HOJE:", "g")]),
  (S + "IMG_6507.mov", 10.5, 3.0, [("DIFICULDADE:", "w"), ("ÓLEO VELHO", "g"), ("E SUJO", "g")]),
  (S + "abedd302-IMG_6509.mov", 2.0, 2.6, [("TROCA COMPLETA", "w"), ("NA MÁQUINA", "g")]),
  (S + "abedd302-IMG_6509.mov", 8.4, 3.2, [("ÓLEO NOVO", "w"), ("ENTRANDO", "g")]),
  (S + "abedd302-IMG_6509.mov", 20.0, 2.4, [("MISSÃO", "g"), ("CUMPRIDA.", "w")]),
]
parts, starts, t = [], [], 0.0
for i, (src, a, d, txt) in enumerate(SC):
    p = f"t/s{i}.mp4"; broll(src, a, d, p); parts.append(p); starts.append(t); t += d
V_END = t; END = 3.6; TOT = V_END + END

# card final: "Aqui as estrelas são do Google: 4,9"
c = Image.new("RGB", (W, H), PRETO); logo(c, 230, (W - 230) // 2, 330); d = ImageDraw.Draw(c)
ctext(d, W, 640, "AQUI AS ESTRELAS", bc(112), WHITE); ctext(d, W, 760, "SÃO DO GOOGLE.", bc(112), GOLD)
num = "4,9"; fn = bc(250); tw = d.textlength(num, font=fn); x0 = (W - (tw + 230)) / 2
d.text((x0, 905), num, font=fn, fill=WHITE); estrela(d, x0 + tw + 125, 1050, 100, GOLD)
ctext(d, W, 1200, "mais de 160 avaliações", mr(40), MUTED)
pill(d, W / 2, 1320, f"WHATSAPP  {WA}", bc(60), GRAF, GOLD, padx=36, pady=20, center=True)
ctext(d, W, 1470, ENDERECO, mr(36), MUTED)
c.save("t/end.png")
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", "t/end.png", "-t", str(END), "-vf", f"fps={FPS},format=yuv420p,{TAG709}"] + enc("t/end.mp4"))
parts.append("t/end.mp4")
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "t/joined.mp4"])

# áudio: trilha + 'plim' próprio (3 notas sintetizadas) quando aparece MISSÃO CUMPRIDA
T_OK = starts[5] + 0.05
run(["ffmpeg", "-v", "error", "-y",
     "-i", MUSIC,
     "-f", "lavfi", "-i", "sine=f=1046.5:d=0.16", "-f", "lavfi", "-i", "sine=f=1318.5:d=0.16", "-f", "lavfi", "-i", "sine=f=1568:d=0.45",
     "-filter_complex",
     f"[0:a]atrim=0:{TOT},afade=t=in:d=0.2,afade=t=out:st={TOT-1.2}:d=1.2,volume=0.85[m];"
     f"[1:a]afade=t=out:st=0.08:d=0.08,volume=0.35,adelay={int(T_OK*1000)}|{int(T_OK*1000)}[a1];"
     f"[2:a]afade=t=out:st=0.08:d=0.08,volume=0.35,adelay={int((T_OK+0.14)*1000)}|{int((T_OK+0.14)*1000)}[a2];"
     f"[3:a]afade=t=out:st=0.15:d=0.3,volume=0.35,adelay={int((T_OK+0.28)*1000)}|{int((T_OK+0.28)*1000)}[a3];"
     f"[m][a1][a2][a3]amix=inputs=4:normalize=0,atrim=0:{TOT},loudnorm=I=-14:TP=-1.5:LRA=11[o]",
     "-map", "[o]", "-ar", "48000", "-ac", "2", "t/mix.wav"])

GA = "&H0021C3F0&"
def ts(x): x = max(x, 0); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: W,Barlow Condensed ExtraBold,128,&H00FFFFFF,&H00FFFFFF,&H00090808,&H96000000,0,0,0,0,100,100,1,0,1,8,5,5,0,0,0,1
Style: G,Barlow Condensed ExtraBold,128,{GA},{GA},&H00090808,&H96000000,0,0,0,0,100,100,1,0,1,8,5,5,0,0,0,1
Style: Big,Barlow Condensed ExtraBold,170,{GA},{GA},&H00090808,&H96000000,0,0,0,0,100,100,2,0,1,10,6,5,0,0,0,1
Style: HudT,Barlow Condensed ExtraBold,50,{GA},{GA},&H00090808,&H00090808,0,0,0,0,100,100,3,0,1,4,0,7,0,0,0,1
Style: HudS,Barlow Condensed ExtraBold,46,&H00FFFFFF,&H00FFFFFF,&H00090808,&H00090808,0,0,0,0,100,100,1,0,1,4,0,7,0,0,0,1
Style: Box,Arial,20,&H5A000000,&H5A000000,{GA},&H00000000,0,0,0,0,100,100,0,0,1,3,0,7,0,0,0,1
Style: Bar,Arial,20,{GA},{GA},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
POP = "\\fad(80,100)\\fscx60\\fscy60\\t(0,160,\\fscx106\\fscy106)\\t(160,240,\\fscx100\\fscy100)"
ev = []
for i, (src, a, d, txt) in enumerate(SC):
    st0 = starts[i]; en = starts[i] + d
    big = (i == 5)
    for j, (ln, col) in enumerate(txt):
        stj = st0 + 0.05 + j * 0.25
        y = (900 + j * 190) if big else (1300 + j * 140)
        sty = "Big" if big else ("G" if col == "g" else "W")
        if big and col == "w": sty = "Big"; ln = "{\\c&H00FFFFFF&}" + ln
        ev.append(f"Dialogue: 1,{ts(stj)},{ts(en - 0.03)},{sty},,0,0,0,,{{\\pos(540,{y}){POP}}}{ln}")

# HUD de missão (canto superior esquerdo), das cenas 2 a 5
hud_a, hud_b = starts[1], starts[5]
box = "m 0 0 l 600 0 600 150 0 150"
ev.append(f"Dialogue: 0,{ts(hud_a)},{ts(hud_b)},Box,,0,0,0,,{{\\pos(60,250)\\p1\\fad(200,150)}}{box}{{\\p0}}")
ev.append(f"Dialogue: 2,{ts(hud_a)},{ts(hud_b)},HudT,,0,0,0,,{{\\pos(84,266)\\fad(200,150)}}◆ MISSÃO DO DIA")
ev.append(f"Dialogue: 2,{ts(hud_a)},{ts(hud_b)},HudS,,0,0,0,,{{\\pos(84,330)\\fad(200,150)}}Troca do óleo do câmbio")
# HUD 'concluída' na cena final
ev.append(f"Dialogue: 0,{ts(hud_b)},{ts(V_END)},Box,,0,0,0,,{{\\pos(60,250)\\p1}}{box}{{\\p0}}")
ev.append(f"Dialogue: 2,{ts(hud_b)},{ts(V_END)},HudT,,0,0,0,,{{\\pos(84,266)}}✔ CONCLUÍDA")
ev.append(f"Dialogue: 2,{ts(hud_b)},{ts(V_END)},HudS,,0,0,0,,{{\\pos(84,330)}}Troca do óleo do câmbio")

# barra de progresso na cena 4 (óleo novo entrando): contorno + preenchimento que cresce
b0, bd = starts[4], SC[4][2]
bx, by, bw, bh = 140, 1610, 800, 44
ev.append(f"Dialogue: 0,{ts(b0)},{ts(b0+bd)},Box,,0,0,0,,{{\\pos({bx},{by})\\p1\\fad(120,100)}}m 0 0 l {bw} 0 {bw} {bh} 0 {bh}{{\\p0}}")
grow = int((bd - 0.5) * 1000)
ev.append(f"Dialogue: 1,{ts(b0)},{ts(b0+bd)},Bar,,0,0,0,,{{\\pos({bx+6},{by+6})\\p1\\clip({bx},{by},{bx+1},{by+bh})\\t(150,{grow},\\clip({bx},{by},{bx+bw},{by+bh}))}}m 0 0 l {bw-12} 0 {bw-12} {bh-12} 0 {bh-12}{{\\p0}}")
ev.append(f"Dialogue: 2,{ts(b0+bd-0.45)},{ts(b0+bd)},HudT,,0,0,0,,{{\\an9\\pos({bx+bw},{by-58})}}100%")
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mp4", "-i", "t/mix.wav", "-filter_complex",
     f"[0:v]drawbox=x=0:y=1150:w={W}:h=560:color=black@0.30:t=fill:enable='lt(t,{starts[5]})',ass=t/subs.ass,{TAG709}[v]",
     "-map", "[v]", "-map", "1:a", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
     "-profile:v", "high", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT])
print("ok", [round(s, 2) for s in starts], round(V_END, 2), round(TOT, 2))
