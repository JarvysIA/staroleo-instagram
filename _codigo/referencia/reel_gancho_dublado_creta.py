#!/usr/bin/env python3
"""Reel Star: Hyundai Creta com vazamento na tampa frontal do câmbio automático (26/10/2026).
Gancho do Fernando (fala dublada com sincronia labial, voz Cirilo) + b-roll com locução (John Edgard) + fechamento."""
import subprocess, os
os.chdir("/home/claude/creta"); os.makedirs("t", exist_ok=True)
W, H, FPS = 1080, 1920, 30
LOGO = "/home/claude/staroleo-instagram/_codigo/logo.png"
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_corporativa_m1.mp3"
GOLD = "&H0021C3F0&"; WHITE = "&H00FFFFFF&"
HOOK = 4.15            # gancho dublado (fala termina em 3,92 s)
VO_OFF = HOOK          # locução começa logo depois do gancho

# b-roll (arquivo, início, duração), casado com os trechos da locução
BROLL = [("6224", 0.5, 2.4), ("6225", 0.5, 2.9),      # chegou com vazamento / câmbio aberto
         ("6227", 0.9, 2.0), ("6228", 6.2, 1.7),      # limpeza da tampa e do câmbio
         ("6232", 2.9, 3.3),                          # tampa voltando com junta e cola
         ("6233", 0.8, 1.6), ("6239", 2.3, 3.0),      # aperto / Havoline na máquina
         ("6241", 4.8, 2.55),                         # visor: novo entra, velho sai
         ("6242", 0.3, 1.4), ("6242", 17.6, 1.35),    # nível conferido / óleo vermelho novo
         ("6242", 10.0, 2.5)]                          # Creta pronto no elevador (capa de placa Star)
END = 3.4

# Cor (26/10, Fernando achou os vídeos "pálidos"): o iPhone grava em HDR (HLG). Só trocar a etiqueta para bt709
# deixa a imagem lavada. Tone mapping de verdade (zscale+tonemap) deixou o funil amarelo laranja (desvio de cor nos
# claros). O que ficou igual à foto do iPhone, com as cores certas: etiqueta bt709 + curva de contraste forte + saturação 1,45.
GRADE = "curves=preset=strong_contrast,eq=saturation=1.45"

def seg(src, a, d, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", src, "-t", str(d), "-an",
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv,{GRADE}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", out], check=True)

parts = ["t/hook.mp4"]
seg("el/gancho_dublado.mp4", 0, HOOK, "t/hook.mp4")
t = HOOK; starts = []
for i, (n, a, d) in enumerate(BROLL):
    p = f"t/b{i}.mp4"; seg(f"src/{n}.mov", a, d, p); parts.append(p); starts.append(t); t += d
B_END = t
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x111214:s={W}x{H}:r={FPS}:d={END}",
                "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "t/end.mp4"], check=True)
parts.append("t/end.mp4"); TOT = B_END + END
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "16",
                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "t/joined.mp4"], check=True)

# ---------- áudio ----------
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "el/gancho_dublado.mp4", "-vn", "-t", str(HOOK),
                "-af", f"loudnorm=I=-16:TP=-2,afade=t=out:st={HOOK-0.15}:d=0.15,aresample=48000", "-ac", "2", "t/hook.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "el/narracao.mp3", "-af", "loudnorm=I=-16:TP=-2,aresample=48000", "-ac", "2", "t/narr.wav"], check=True)
vol = f"volume='if(lt(t,{HOOK}),0.14,if(lt(t,{B_END}),0.26,0.45))':eval=frame"
fc = (f"[1:a]adelay={int(VO_OFF*1000)}|{int(VO_OFF*1000)}[n];"
      f"[2:a]atrim=0:{TOT},{vol},afade=t=in:d=0.3,afade=t=out:st={TOT-1.0}:d=1.0[m];"
      f"[0:a][n][m]amix=inputs=3:normalize=0:duration=longest,atrim=0:{TOT},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "t/hook.wav", "-i", "t/narr.wav", "-stream_loop", "-1", "-i", MUSIC,
                "-filter_complex", fc, "-map", "[a]", "-ar", "48000", "t/mix.wav"], check=True)

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
Style: Sub,Barlow Condensed,50,&H0021C3F0,&H0021C3F0,&H00141211,&H96000000,0,0,0,0,100,100,4,0,1,4,2,5,40,40,0,1
Style: TagG,Barlow Condensed ExtraBold,50,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,3,0,3,14,0,5,0,0,0,1
Style: Big,Barlow Condensed ExtraBold,112,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Info,Manrope ExtraLight SemiBold,42,&H00ABA8A6,&H00ABA8A6,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Btn,Barlow Condensed ExtraBold,62,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,24,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
def add(st, en, style, x, y, text, layer=1, extra=""):
    ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{{\\pos({x},{y}){extra}}}{text}")
POP = "\\fscx70\\fscy70\\t(0,140,\\fscx104\\fscy104)\\t(140,220,\\fscx100\\fscy100)"
FD = "\\fad(200,150)"
g = lambda s: "{\\c" + GOLD + "}" + s + "{\\c" + WHITE + "}"

def caption(words, off, cy=1400):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if w[0][-1] in ".,!?:" or len(cur) == 3 or len(" ".join(x[0] for x in cur)) > 16:
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    for gi, grp in enumerate(groups):
        gs, ge = grp[0][1] + off, grp[-1][2] + off
        nxt = groups[gi + 1][0][1] + off if gi + 1 < len(groups) else 999
        for k, w in enumerate(grp):
            st = w[1] + off if k else gs
            en = (grp[k + 1][1] + off) if k + 1 < len(grp) else min(ge + 0.15, nxt - 0.01)
            clean = lambda s: s.upper().rstrip(".,!?:")
            parts = [(g(clean(x[0])) if j == k else clean(x[0])) for j, x in enumerate(grp)]
            add(st, en, "Cap", 540, cy, " ".join(parts), layer=2, extra=POP if k == 0 else "")

# gancho (tempos da fala dublada)
HOOKW = [("Se",0,0.24),("você",0.24,0.48),("tem",0.48,0.74),("um",0.74,0.84),("Hyundai",0.84,1.14),("Creta",1.14,1.56),
         ("na",1.56,1.66),("sua",1.66,1.9),("garagem,",1.9,2.58),("esse",2.86,2.94),("vídeo",2.94,3.26),("é",3.26,3.38),("pra",3.38,3.54),("você!",3.54,3.92)]
caption(HOOKW, 0.0)

# locução (texto do roteiro, tempos da transcrição local)
NARR = [("Esse",0.00,0.22),("Hyundai",0.22,0.56),("Creta",0.56,1.06),("chegou",1.06,1.36),("com",1.36,1.58),("vazamento",1.58,2.06),
        ("de",2.06,2.34),("óleo",2.34,2.60),("no",2.60,2.74),("câmbio",2.74,3.04),("automático,",3.04,3.74),("pela",3.92,4.10),("tampa",4.10,4.48),("frontal.",4.48,4.92),
        ("A",5.50,5.52),("gente",5.52,5.72),("tirou",5.72,6.10),("a",6.10,6.20),("tampa",6.20,6.60),("e",6.60,6.70),("limpou",6.70,6.96),("tudo,",6.96,7.42),
        ("por",7.60,7.76),("dentro",7.76,8.08),("e",8.08,8.26),("por",8.26,8.44),("fora.",8.44,8.78),
        ("Junta",9.12,9.42),("nova",9.42,9.82),("e",9.82,10.04),("cola",10.04,10.26),("certa,",10.26,10.72),("pra",10.90,11.04),("não",11.04,11.28),("vazar",11.28,11.62),("mais.",11.62,11.96),
        ("Depois",12.46,12.68),("que",12.68,12.88),("a",12.88,12.96),("cola",12.96,13.10),("secou,",13.10,13.56),("troca",13.92,14.12),("completa",14.12,14.70),
        ("do",14.70,15.02),("óleo",15.02,15.30),("com",15.30,15.46),("máquina",15.46,15.82),("especializada:",15.82,16.74),
        ("o",17.10,17.22),("óleo",17.22,17.42),("novo",17.42,17.68),("entra",17.68,18.18),("enquanto",18.18,18.52),("o",18.52,18.74),("velho",18.74,18.92),("sai.",18.92,19.28),
        ("Nível",19.64,19.94),("conferido",19.94,20.56),("e",20.56,20.86),("câmbio",20.86,21.24),("protegido.",21.24,22.04),
        ("Mais",22.42,22.62),("um",22.62,22.84),("Creta",22.84,23.22),("pronto",23.22,23.62),("pra",23.62,23.92),("rodar.",23.92,24.32)]
caption(NARR, VO_OFF)

# topo: modelo e etapas
add(HOOK, B_END, "Sub", 540, 330, "HYUNDAI CRETA  •  CÂMBIO AUTOMÁTICO", extra=FD)
STEPS = [(HOOK + 0.0, HOOK + 5.3, "VAZAMENTO NA TAMPA FRONTAL"), (HOOK + 5.3, HOOK + 9.0, "LIMPEZA COMPLETA"),
         (HOOK + 9.0, HOOK + 13.9, "JUNTA NOVA E COLA"), (HOOK + 13.9, HOOK + 19.45, "TROCA COMPLETA NA MÁQUINA"),
         (HOOK + 19.45, HOOK + 22.2, "NÍVEL CONFERIDO")]
for st, en, txt in STEPS:
    add(st, en, "TagG", 540, 420, txt, extra=FD)

# fechamento
D = "\\fad(300,0)"
add(B_END + 0.35, TOT, "Big", 540, 935, "VAZANDO ÓLEO", extra=D)
add(B_END + 0.5, TOT, "Big", 540, 1050, g("NO CÂMBIO? CHAMA A STAR."), extra=D)
add(B_END + 0.8, TOT, "Btn", 540, 1225, "WHATSAPP  (21) 97544-6417", extra=D + POP)
add(B_END + 1.0, TOT, "Info", 540, 1350, "Estr. dos Bandeirantes, 841 · Taquara", extra=D)
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

# gradiente topo e base para leitura
from PIL import Image
gimg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = gimg.load()
for y in range(H):
    a = 0
    if y < 620: a = int(170 * (1 - y / 620) ** 1.3)
    if y > 1150: a = max(a, int(190 * min(1, (y - 1150) / 600) ** 1.2))
    for x in range(W): px[x, y] = (17, 18, 20, a)
gimg.save("t/grad.png")

fc = ("[1:v]format=rgba,scale=210:-1:flags=lanczos,split=2[ls][lb0];[lb0]scale=560:-1:flags=lanczos[lb];"
      f"[lb]fade=t=in:st={B_END+0.05}:d=0.45:alpha=1[lbf];"
      f"movie=t/grad.png[gr];[0:v][gr]overlay=0:0:enable='lt(t,{B_END})'[v0];"
      f"[v0][ls]overlay=x=(W-w)/2:y=150:enable='lt(t,{B_END})'[v1];"
      f"[v1][lbf]overlay=x=(W-w)/2:y=480:enable='gte(t,{B_END})'[v2];[v2]ass=t/subs.ass,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mp4", "-loop", "1", "-framerate", str(FPS), "-i", LOGO, "-i", "t/mix.wav",
                "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "reel_creta_tampa_frontal.mp4"], check=True)
print("ok", round(B_END, 2), round(TOT, 2))
