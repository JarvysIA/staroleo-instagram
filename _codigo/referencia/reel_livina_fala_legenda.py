#!/usr/bin/env python3
"""Reel Star: Fernando e Rodrigão explicam a troca do filtro do câmbio do Nissan Livina (26/10/2026).
Vídeo bruto vertical (538E824A...MOV), 3 trechos da fala, legenda palavra por palavra (Scribe), gancho no topo,
trilha baixa por baixo da fala e fechamento grafite com o WhatsApp.
Uso: python3 reel_livina_fala_legenda.py <pasta de trabalho com src.mov e words.json> <saída.mp4>"""
import json, subprocess, os, sys
WD, OUT = sys.argv[1], os.path.abspath(sys.argv[2])
os.chdir(WD); os.makedirs("t", exist_ok=True)
W, H, FPS = 1080, 1920, 30
REPO = "/home/claude/staroleo-instagram/_codigo"
LOGO = f"{REPO}/logo.png"; MUSIC = f"{REPO}/audio/trilha_corporativa_m1.mp3"
GOLD = "&H0021C3F0&"; WHITE = "&H00FFFFFF&"
SEGS = [(2.50, 8.95), (32.80, 50.60), (50.80, 57.80)]   # trechos do vídeo original
END = 3.0

parts, t = [], 0.0
for i, (a, b) in enumerate(SEGS):
    p = f"t/v{i}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", "src.mov",
                    "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},eq=contrast=1.05:saturation=1.08,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",
                    "-af", f"highpass=f=90,afftdn=nf=-28,afade=t=in:d=0.04,afade=t=out:st={b-a-0.06:.2f}:d=0.06,aresample=48000",
                    "-ac", "2", "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-c:a", "pcm_s16le", p.replace(".mp4", ".mov")], check=True)
    parts.append(p.replace(".mp4", ".mov")); t += b - a
T_END = t
SEG_LAST = T_END - (SEGS[-1][1] - SEGS[-1][0])   # no último trecho a parede STAR ÓLEO aparece: sem logo por cima
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x111214:s={W}x{H}:r={FPS}:d={END}",
                "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo", "-t", str(END), "-c:v", "libx264", "-crf", "16",
                "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "t/end.mov"], check=True)
parts.append("t/end.mov"); TOT = T_END + END
open("t/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "t/list.txt", "-c:v", "libx264", "-crf", "16",
                "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "t/joined.mov"], check=True)

# ---------- áudio: fala + trilha baixa ----------
vol = f"volume='if(lt(t,{T_END}),0.07,0.40)':eval=frame"
fc = (f"[0:a]loudnorm=I=-16:TP=-2,aresample=48000[s];"
      f"[1:a]atrim=0:{TOT},{vol},afade=t=in:d=0.5,afade=t=out:st={TOT-1.0}:d=1.0[m];"
      f"[s][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:{TOT},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "t/joined.mov", "-stream_loop", "-1", "-i", MUSIC, "-filter_complex", fc,
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
Style: Cap,Barlow Condensed ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,7,3,5,40,40,0,1
Style: Title,Barlow Condensed ExtraBold,92,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,6,3,5,40,40,0,1
Style: TagG,Barlow Condensed ExtraBold,48,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,3,0,3,14,0,5,0,0,0,1
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
TY = 390
add(0.0, T_END, "Title", 540, TY, "TROCA DO FILTRO DO CÂMBIO\\N" + g("NISSAN LIVINA"), extra=FADE)
add(0.3, T_END, "TagG", 540, TY + 150, "DICA DO FERNANDO", extra="\\fad(200,150)")

def caption(words, cy=1420):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if w[0][-1] in ".,!?" or len(cur) == 3 or len(" ".join(x[0] for x in cur)) > 16:
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    for gi, grp in enumerate(groups):
        gs, ge = grp[0][1], grp[-1][2]
        nxt = groups[gi + 1][0][1] if gi + 1 < len(groups) else 999
        for k, w in enumerate(grp):
            st = w[1] if k else gs
            en = grp[k + 1][1] if k + 1 < len(grp) else min(ge + 0.25, nxt - 0.01)
            clean = lambda s: s.upper().rstrip(".,!?")
            txt = " ".join((g(clean(x[0])) if j == k else clean(x[0])) for j, x in enumerate(grp))
            add(st, en, "Cap", 540, cy, txt, layer=2, extra=POP if k == 0 else "")
caption(json.load(open("words.json")))

D = "\\fad(300,0)"
add(T_END + 0.35, TOT, "Big", 540, 935, "SEU CÂMBIO", extra=D)
add(T_END + 0.5, TOT, "Big", 540, 1055, g("EM BOAS MÃOS."), extra=D)
add(T_END + 0.8, TOT, "Btn", 540, 1225, "WHATSAPP  (21) 97544-6417", extra=D + POP)
add(T_END + 1.0, TOT, "Info", 540, 1350, "Estr. dos Bandeirantes, 841 · Taquara", extra=D)
open("t/subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

from PIL import Image
gimg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = gimg.load()
for y in range(H):
    a = 0
    if y < 700: a = int(190 * (1 - y / 700) ** 1.2)
    if y > 1200: a = max(a, int(170 * min(1, (y - 1200) / 600) ** 1.2))
    for x in range(W): px[x, y] = (17, 18, 20, a)
gimg.save("t/grad.png")

fc = ("[1:v]format=rgba,scale=200:-1:flags=lanczos,split=2[ls][lb0];[lb0]scale=560:-1:flags=lanczos[lb];"
      f"[lb]fade=t=in:st={T_END+0.05}:d=0.45:alpha=1[lbf];"
      f"movie=t/grad.png[gr];[0:v][gr]overlay=0:0:enable='lt(t,{T_END})'[v0];"
      f"[v0][ls]overlay=x=(W-w)/2:y=140:enable='lt(t,{SEG_LAST})'[v1];"
      f"[v1][lbf]overlay=x=(W-w)/2:y=520:enable='gte(t,{T_END})'[v2];[v2]ass=t/subs.ass,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "t/joined.mov", "-loop", "1", "-framerate", str(FPS), "-i", LOGO, "-i", "t/mix.wav",
                "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{TOT:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
print("ok", round(T_END, 2), round(TOT, 2))
