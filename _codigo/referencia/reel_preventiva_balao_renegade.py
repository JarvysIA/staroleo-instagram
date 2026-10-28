#!/usr/bin/env python3
"""Reel Star: Jeep Renegade, troca PREVENTIVA do trocador de calor por radiador de óleo + troca do óleo do câmbio (27/10/2026).
Gancho com a voz real do Fernando (IMG_4781, gravado com microfone) + b-roll com locução (John Edgard) +
balão "café com leite" mostrando o RISCO (imagem do reservatório do reel do radiador, outro carro) + fechamento."""
import subprocess, os
os.chdir("/home/claude/renegade"); os.makedirs("t", exist_ok=True)
W, H, FPS = 1080, 1920, 30
LOGO = "/home/claude/staroleo-instagram/_codigo/logo.png"
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_corporativa_m1.mp3"
GOLD = "&H0021C3F0&"; WHITE = "&H00FFFFFF&"
# cor do iPhone (regra de 26/10): etiqueta bt709 + contraste forte + saturação 1,45
GRADE = "curves=preset=strong_contrast,eq=saturation=1.45"
HOOK_A, HOOK_B = 1.15, 7.85          # trecho da fala do gancho no IMG_4781
HOOK = HOOK_B - HOOK_A
VO_OFF = HOOK

BROLL = [("6277", 1.0, 2.8), ("6280", 0.3, 2.5),            # A: para-choque saindo, frente aberta
         ("6283", 0.2, 3.2), ("6280", 3.0, 3.1),            # B: trocador velho na mão / alma (balão do risco por cima)
         ("2648", 0.8, 2.5),                                # C: a Renegade (veio antes do problema)
         ("6277", 14.0, 2.0), ("6283", 4.5, 2.2), ("6282", 4.5, 2.0),   # D: tira, radiador de óleo no lugar, alma volta
         ("6289", 0.5, 2.9),                                # E: frente com o radiador de óleo
         ("6285", 21.0, 2.2), ("6286", 3.0, 2.1),           # F: óleo velho saindo / Mobil ATF na máquina
         ("6288", 5.0, 2.3),                                # G: visor, velho sai e novo entra
         ("2649", 5.8, 1.5),                                # H: nível conferido
         ("2650", 19.4, 2.7)]                               # I: Renegade pronta
END = 3.4

def seg(src, a, d, out):
    if os.environ.get("REUSE") and os.path.exists(out): return
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", src, "-t", str(d), "-an",
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv,{GRADE}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "14", out], check=True)

parts = ["t/hook.mp4"]; seg("src/4781.mov", HOOK_A, HOOK, "t/hook.mp4")
t = HOOK; starts = []
for i, (n, a, d) in enumerate(BROLL):
    p = f"t/b{i}.mp4"; seg(f"src/{n}.mov", a, d, p); parts.append(p); starts.append(t); t += d
B_END = t
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x111214:s={W}x{H}:r={FPS}:d={END}",
                "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "t/end.mp4"], check=True)
parts.append("t/end.mp4"); TOT = B_END + END
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "14",
                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "t/joined.mp4"], check=True)

# ---------- áudio ----------
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(HOOK_A), "-to", str(HOOK_B), "-i", "src/4781.mov", "-vn",
                "-af", f"highpass=f=80,loudnorm=I=-16:TP=-2,afade=t=in:d=0.05,afade=t=out:st={HOOK-0.12}:d=0.12,aresample=48000", "-ac", "2", "t/hook.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "el/narr_106.wav", "-af", "loudnorm=I=-16:TP=-2,aresample=48000", "-ac", "2", "t/narr.wav"], check=True)
vol = f"volume='if(lt(t,{HOOK}),0.12,if(lt(t,{B_END}),0.24,0.45))':eval=frame"
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
Style: TagR,Barlow Condensed ExtraBold,46,&H00FFFFFF,&H00FFFFFF,&H003539E5,&H003539E5,0,0,0,0,100,100,3,0,3,14,0,5,0,0,0,1
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

# gancho (tempos da fala no IMG_4781, já descontado o início do corte)
HW = [("Se",1.30,1.42),("você",1.42,1.68),("tem",1.68,1.98),("Jeep",1.98,2.26),("Compass,",2.26,2.74),("Jeep",3.04,3.32),
      ("Renegade",3.32,3.92),("ou",3.92,4.42),("Fiat",4.42,4.62),("Toro",4.62,4.94),("na",4.94,5.1),("sua",5.1,5.28),
      ("garagem,",5.28,6.04),("assiste",6.16,6.66),("esse",6.66,6.78),("vídeo",6.78,7.0),("até",7.0,7.24),("o",7.24,7.32),("final.",7.32,7.56)]
caption(HW, -HOOK_A)

NARR = [("Nesses",0.00,0.30),("modelos,",0.30,0.96),("o",1.14,1.28),("óleo",1.28,1.44),("do",1.44,1.62),("câmbio",1.62,1.94),("passa",1.94,2.24),
        ("por",2.24,2.44),("um",2.44,2.56),("trocador",2.56,3.02),("de",3.02,3.20),("calor",3.20,3.52),("junto",3.52,3.90),("com",3.90,4.18),
        ("a",4.18,4.30),("água",4.30,4.52),("do",4.52,4.64),("radiador.",4.64,5.12),
        ("Se",5.50,5.66),("ele",5.66,5.76),("fura,",5.76,6.26),("a",6.52,6.60),("água",6.60,6.80),("mistura",6.80,7.26),("com",7.26,7.46),("o",7.46,7.60),("óleo,",7.60,7.94),
        ("vira",8.08,8.32),("café",8.32,8.66),("com",8.66,8.90),("leite,",8.90,9.24),("e",9.24,9.62),("o",9.62,9.72),("conserto",9.72,10.12),("do",10.12,10.30),
        ("câmbio",10.30,10.66),("sai",10.66,10.90),("caro.",10.90,11.50),
        ("Essa",11.82,12.12),("Renegade",12.12,12.60),("veio",12.60,12.84),("antes",12.84,13.26),("do",13.26,13.44),("problema:",13.44,13.82),
        ("a",14.20,14.30),("gente",14.30,14.48),("tirou",14.48,14.86),("o",14.86,14.96),("para-choque",14.96,15.54),("e",15.54,15.76),("a",15.76,15.88),("alma,",15.88,16.22),
        ("retirou",16.46,16.86),("o",16.86,16.96),("trocador",16.96,17.28),("de",17.28,17.46),("calor",17.46,17.80),("e",17.80,18.12),("instalou",18.12,18.58),
        ("um",18.58,18.70),("radiador",18.70,19.16),("de",19.16,19.36),("óleo",19.36,19.66),("no",19.66,19.78),("lugar.",19.78,20.10),
        ("Água",20.54,20.90),("e",20.90,21.04),("óleo",21.04,21.26),("do",21.26,21.40),("câmbio",21.40,21.74),("não",21.74,22.06),("se",22.06,22.26),
        ("encontram",22.26,22.64),("mais.",22.64,22.96),
        ("Depois,",23.36,23.74),("troca",24.10,24.34),("completa",24.34,24.86),("do",24.86,25.16),("óleo",25.16,25.38),("do",25.38,25.50),("câmbio",25.50,25.86),
        ("com",25.86,26.02),("máquina",26.02,26.38),("especializada:",26.38,27.28),
        ("o",27.66,27.74),("óleo",27.74,27.90),("velho",27.90,28.16),("sai",28.16,28.48),("e",28.48,28.84),("o",28.84,28.92),("novo",28.92,29.14),("entra.",29.14,29.52),
        ("Nível",29.94,30.20),("conferido.",30.20,30.94),("Prevenir",31.28,31.64),("sai",31.64,31.98),("muito",31.98,32.42),("mais",32.42,32.64),("barato.",32.64,33.12)]
caption(NARR, VO_OFF)

# topo: modelo e etapas
add(HOOK, B_END, "Sub", 540, 330, "JEEP RENEGADE  •  MANUTENÇÃO PREVENTIVA", extra=FD)
V = VO_OFF
STEPS = [(V + 0.0, V + 5.3, "TROCA PREVENTIVA"), (V + 14.1, V + 18.1, "TROCADOR DE CALOR SAI"),
         (V + 18.1, V + 23.2, "RADIADOR DE ÓLEO ENTRA"), (V + 23.2, V + 29.8, "TROCA COMPLETA NA MÁQUINA"),
         (V + 29.8, V + 31.2, "NÍVEL CONFERIDO")]
for st, en, txt in STEPS:
    add(st, en, "TagG", 540, 420, txt, extra=FD)

# balão do risco (café com leite)
BAL_A, BAL_B = V + 6.4, V + 11.6
CX, CY = 540, 900
add(BAL_A, BAL_B, "TagR", CX, CY + 300, "SEM PREVENTIVA:", extra="\\fad(200,200)")
add(BAL_A + 0.1, BAL_B, "TagG", CX, CY + 372, "ÁGUA MISTURADA COM ÓLEO", extra="\\fad(200,200)")

# fechamento
D = "\\fad(300,0)"
add(B_END + 0.35, TOT, "Big", 540, 935, "MANUTENÇÃO PREVENTIVA", extra=D)
add(B_END + 0.5, TOT, "Big", 540, 1050, g("É COM A STAR."), extra=D)
add(B_END + 0.8, TOT, "Btn", 540, 1225, "WHATSAPP  (21) 97544-6417", extra=D + POP)
add(B_END + 1.0, TOT, "Info", 540, 1350, "Estr. dos Bandeirantes, 841 · Taquara", extra=D)
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

from PIL import Image
gimg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = gimg.load()
for y in range(H):
    a = 0
    if y < 620: a = int(170 * (1 - y / 620) ** 1.3)
    if y > 1150: a = max(a, int(190 * min(1, (y - 1150) / 600) ** 1.2))
    for x in range(W): px[x, y] = (17, 18, 20, a)
gimg.save("t/grad.png")

# balão: vídeo do reservatório em círculo com aro dourado, entra com zoom
S = 520; R = S + 28
bal = (f"[3:v]format=yuva420p,setpts=PTS-STARTPTS+{BAL_A}/TB[bv];[4:v]format=gray,setpts=PTS-STARTPTS+{BAL_A}/TB[bm];"
       f"[bv][bm]alphamerge[bc];[5:v]format=rgba,setpts=PTS-STARTPTS+{BAL_A}/TB[ring];"
       f"[bc]pad={R}:{R}:14:14:color=black@0[bp];[bp][ring]overlay=0:0:shortest=0:eof_action=pass[bal];"
       f"[bal]fade=t=in:st={BAL_A}:d=0.25:alpha=1,fade=t=out:st={BAL_B-0.25}:d=0.25:alpha=1[balf];")
fc = ("[1:v]format=rgba,scale=210:-1:flags=lanczos,split=2[ls][lb0];[lb0]scale=560:-1:flags=lanczos[lb];"
      f"[lb]fade=t=in:st={B_END+0.05}:d=0.45:alpha=1[lbf];" + bal +
      f"movie=t/grad.png[gr];[0:v][gr]overlay=0:0:enable='lt(t,{B_END})'[v0];"
      f"[v0][ls]overlay=x=(W-w)/2:y=150:enable='lt(t,{B_END})'[v1];"
      f"[v1][balf]overlay=x={CX}-{R}/2:y={CY}-{R}/2-40:enable='between(t,{BAL_A},{BAL_B})':eof_action=pass[v1b];"
      f"[v1b][lbf]overlay=x=(W-w)/2:y=480:enable='gte(t,{B_END})'[v2];[v2]ass=t/subs.ass,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mp4", "-loop", "1", "-framerate", str(FPS), "-i", LOGO, "-i", "t/mix.wav",
                "-i", "t/balao_raw.mp4", "-loop", "1", "-framerate", str(FPS), "-t", "6", "-i", "t/mask.png",
                "-loop", "1", "-framerate", str(FPS), "-t", "6", "-i", "t/ring.png",
                "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                "-profile:v", "high", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "reel_renegade_preventiva.mp4"], check=True)
print("ok", round(HOOK, 2), round(B_END, 2), round(TOT, 2))
