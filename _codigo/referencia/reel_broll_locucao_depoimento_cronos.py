#!/usr/bin/env python3
"""Reel Star: troca do óleo do câmbio do Fiat Cronos 1.3 CVT do Ramone (23/10/2026).
Gancho + b-roll com locução (John Edgard) + depoimento real do Ramone + chamada do Fernando + fechamento."""
import json, subprocess, os
os.chdir("/home/claude/cronos"); os.makedirs("t", exist_ok=True)
W, H, FPS = 1080, 1920, 30
LOGO = "/home/claude/staroleo-instagram/_codigo/logo.png"
MUSIC = "/home/claude/staroleo-instagram/_codigo/audio/trilha_corporativa_m1.mp3"
VO_OFF = 0.5
GOLD = "&H0021C3F0&"; WHITE = "&H00FFFFFF&"

# ---------- b-roll (arquivo, início, duração) ----------
BROLL = [("6160", 4.6, 2.3), ("6165", 0.2, 1.6),                     # gancho filtro / Cronos no elevador
         ("6156", 12.0, 1.0), ("6157", 14.3, 1.4),                    # máquina tira o óleo velho
         ("6158", 5.0, 1.6), ("6159", 6.5, 1.5), ("6160", 1.0, 1.0),  # cárter, borra, filtro
         ("6155", 0.3, 1.2), ("6164", 18.5, 2.0), ("6165", 4.5, 1.5), ("6167", 7.0, 1.4),  # óleo novo, visor
         ("6169", 0.8, 1.5), ("6166", 0.3, 1.3)]                      # nível, Ramone acompanhando
# ---------- falas reais (arquivo, início, fim, quem) ----------
TALK = [("4702", 10.45, 15.75, "R"), ("4702", 21.30, 22.50, "F"), ("4702", 24.88, 26.90, "R"),
        ("4702", 36.30, 38.40, "R"), ("4702", 40.05, 41.35, "FR"), ("4703", 1.00, 7.55, "F2")]
END = 2.8

def seg_video(n, a, d, out, keep_audio=False):
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", f"src/{n}.mov", "-t", str(d),
           "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},eq=contrast=1.05:saturation=1.08,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",
           "-c:v", "libx264", "-preset", "fast", "-crf", "17"]
    cmd += ["-an"] if not keep_audio else []
    subprocess.run(cmd + [out], check=True)

parts, t, cuts = [], 0.0, []
for i, (n, a, d) in enumerate(BROLL):
    p = f"t/b{i}.mp4"; seg_video(n, a, d, p); parts.append(p); t += d
B_END = t
talk_t = []
for i, (n, a, b, who) in enumerate(TALK):
    p = f"t/f{i}.mp4"; seg_video(n, a, b - a, p); parts.append(p)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", f"src/{n}.mov", "-vn",
                    "-af", f"highpass=f=90,afftdn=nf=-30,afade=t=in:d=0.04,afade=t=out:st={b-a-0.06:.2f}:d=0.06,aresample=48000",
                    "-ac", "2", f"t/f{i}.wav"], check=True)
    talk_t.append((t, n, a, b, who)); t += b - a
T_END = t
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x111214:s={W}x{H}:r={FPS}:d={END}",
                "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "t/end.mp4"], check=True)
parts.append("t/end.mp4"); TOT = T_END + END
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264",
                "-crf", "16", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "t/joined.mp4"], check=True)

# ---------- áudio ----------
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "narr.mp3", "-af", "loudnorm=I=-16:TP=-2,aresample=48000", "-ac", "2", "t/narr.wav"], check=True)
lst = "".join(f"file '{os.path.abspath(f't/f{i}.wav')}'\n" for i in range(len(TALK)))
open("t/talk.txt", "w").write(lst)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/talk.txt", "-af", "loudnorm=I=-16:TP=-2,aresample=48000", "t/talk.wav"], check=True)
vol = (f"volume='if(lt(t,{B_END}),0.28,if(lt(t,{T_END}),0.10,0.45))':eval=frame")
fc = (f"[0:a]adelay={int(VO_OFF*1000)}|{int(VO_OFF*1000)}[n];"
      f"[1:a]adelay={int(B_END*1000)}|{int(B_END*1000)}[s];"
      f"[2:a]atrim=0:{TOT},{vol},afade=t=in:d=0.3,afade=t=out:st={TOT-1.0}:d=1.0[m];"
      f"[n][s][m]amix=inputs=3:normalize=0:duration=longest,atrim=0:{TOT},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "t/narr.wav", "-i", "t/talk.wav", "-stream_loop", "-1", "-i", MUSIC, "-filter_complex", fc,
                "-map", "[a]", "-ar", "48000", "t/mix.wav"], check=True)

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
Style: Title,Barlow Condensed ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,6,3,5,40,40,0,1
Style: Sub,Barlow Condensed,52,&H0021C3F0,&H0021C3F0,&H00141211,&H96000000,0,0,0,0,100,100,4,0,1,4,2,5,40,40,0,1
Style: TagG,Barlow Condensed ExtraBold,50,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,3,0,3,14,0,5,0,0,0,1
Style: Big,Barlow Condensed ExtraBold,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Info,Manrope ExtraLight SemiBold,42,&H00ABA8A6,&H00ABA8A6,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Btn,Barlow Condensed ExtraBold,62,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,2,0,3,24,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
def add(st, en, style, x, y, text, layer=1, extra=""):
    ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{{\\pos({x},{y}){extra}}}{text}")
POP = "\\fscx70\\fscy70\\t(0,140,\\fscx104\\fscy104)\\t(140,220,\\fscx100\\fscy100)"
FADE = "\\fad(180,150)"
g = lambda s: "{\\c" + GOLD + "}" + s + "{\\c" + WHITE + "}"
TY = 395
add(0.1, 3.9, "Title", 540, TY, "OLHA O QUE SAIU DO\\N" + g("CÂMBIO DESSE CRONOS"), extra=FADE + POP)
add(3.9, B_END, "Sub", 540, TY - 20, "FIAT CRONOS 1.3  •  CVT", extra="\\fad(200,150)")
add(B_END, T_END - (TALK[-1][2] - TALK[-1][1]), "TagG", 540, TY - 20, "RAMONE, CLIENTE DA STAR", extra="\\fad(200,150)")
add(T_END - (TALK[-1][2] - TALK[-1][1]), T_END, "TagG", 540, TY - 20, "FERNANDO, DA STAR ÓLEO", extra="\\fad(200,150)")

def caption(words, off, cy=1400):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if w[0][-1] in ".,!?" or len(cur) == 3 or len(" ".join(x[0] for x in cur)) > 16:
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    for gi, grp in enumerate(groups):
        gs, ge = grp[0][1] + off, grp[-1][2] + off
        nxt = groups[gi + 1][0][1] + off if gi + 1 < len(groups) else 999
        for k, w in enumerate(grp):
            st = w[1] + off if k else gs
            en = (grp[k + 1][1] + off) if k + 1 < len(grp) else min(ge + 0.15, nxt - 0.01)
            clean = lambda s: s.upper().rstrip(".,!?").rstrip("-")
            parts = [(g(clean(x[0])) if j == k else clean(x[0])) for j, x in enumerate(grp)]
            add(st, en, "Cap", 540, cy, " ".join(parts), layer=2, extra=POP if k == 0 else "")

# locução (texto do roteiro, tempos da transcrição local)
NARR = [("Fiat",0.00,0.30),("Cronos",0.30,0.84),("1.3",0.84,1.6),("CVT",1.60,2.3),("aqui",2.32,2.54),("na",2.54,2.74),("Star.",2.74,3.08),
        ("A",3.52,3.7),("máquina",3.70,3.98),("tira",3.98,4.46),("o",4.46,4.6),("óleo",4.60,4.78),("velho",4.78,5.1),("do",5.10,5.28),("câmbio.",5.28,5.63),
        ("Depois,",6.00,6.3),("a",6.30,6.46),("gente",6.46,6.62),("baixa",6.62,7.08),("o",7.08,7.18),("cárter,",7.18,7.6),("limpa",7.78,8.1),("a",8.10,8.28),("borra",8.28,8.54),
        ("e",8.54,8.78),("troca",8.78,9.18),("o",9.18,9.32),("filtro.",9.32,9.61),
        ("Entra",10.00,10.28),("o",10.28,10.34),("Motul",10.34,10.66),("Multi",10.66,10.98),("CVTF,",10.98,11.96),("específico",11.96,12.94),("para",12.94,13.12),
        ("câmbio",13.12,13.44),("CVT,",13.44,14.02),("até",14.02,14.6),("o",14.60,14.78),("fluido",14.78,15.12),("sair",15.12,15.36),("limpo.",15.36,15.72),
        ("Nível",16.14,16.36),("conferido,",16.36,17.04),("câmbio",17.42,17.62),("pronto.",17.62,18.2)]
caption(NARR, VO_OFF)

# falas reais (palavras do Scribe)
SW = json.load(open("scribe_words.json"))["words"]
F2 = [("Você",1.1,1.34),("que",1.38,1.42),("tá",1.46,1.54),("na",1.58,1.66),("dúvida,",1.72,2.06),("tem",2.18,2.3),("50",2.46,2.7),("mil",2.72,2.8),
      ("quilômetros",2.84,3.18),("ou",3.22,3.28),("mais",3.36,3.56),("com",3.6,3.64),("seu",3.68,3.8),("câmbio",3.82,3.96),("automático,",3.98,4.52),
      ("entre",4.74,4.9),("em",4.96,4.96),("contato",4.98,5.32),("agora",5.36,5.56),("mesmo",5.64,6.0),("e",6.04,6.08),("agende",6.14,6.36),("a",6.38,6.4),
      ("troca",6.44,6.64),("de",6.68,6.7),("óleo",6.74,6.84),("do",6.86,6.92),("seu",6.96,7.06),("câmbio.",7.1,7.4)]
for (t0, n, a, b, who) in talk_t:
    src = SW if n == "4702" else [{"text": w, "start": s, "end": e} for w, s, e in F2]
    ws = [(w["text"].replace("Starol", "Star Óleo"), w["start"], w["end"]) for w in src if w.get("type", "word") == "word" and w["start"] >= a - 0.02 and w["end"] <= b + 0.05]
    caption(ws, t0 - a)

# fechamento
D = "\\fad(300,0)"
add(T_END + 0.35, TOT, "Big", 540, 935, "SEU CÂMBIO", extra=D)
add(T_END + 0.5, TOT, "Big", 540, 1055, g("EM BOAS MÃOS."), extra=D)
add(T_END + 0.8, TOT, "Btn", 540, 1225, "WHATSAPP  (21) 97544-6417", extra=D + POP)
add(T_END + 1.0, TOT, "Info", 540, 1350, "Estr. dos Bandeirantes, 841 · Taquara", extra=D)
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
      f"[lb]fade=t=in:st={T_END+0.05}:d=0.45:alpha=1[lbf];"
      "movie=t/grad.png[gr];[0:v][gr]overlay=0:0:enable='lt(t," + f"{T_END}" + ")'[v0];"
      f"[v0][ls]overlay=x=(W-w)/2:y=150:enable='lt(t,{T_END})'[v1];"
      f"[v1][lbf]overlay=x=(W-w)/2:y=520:enable='gte(t,{T_END})'[v2];[v2]ass=t/subs.ass,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mp4", "-loop", "1", "-framerate", str(FPS), "-i", LOGO, "-i", "t/mix.wav",
                "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "reel_cronos_ramone.mp4"], check=True)
print("ok", round(B_END, 2), round(T_END, 2), round(TOT, 2))
