#!/usr/bin/env python3
"""Versão 2 do reel Kicks: identidade do site (grafite + dourado, Barlow Condensed), logo oficial, áudio corrigido.
Reaproveita tmp/base.mp4 (fotos com movimento) e tmp/mix.wav (locução + música)."""
import json, subprocess, os
os.chdir("/home/claude/kicks")

W, H = 1080, 1920
VO_OFF = 0.4
END = 23.6
E0 = 18.0                     # início do fechamento
GOLD = "&H0021C3F0&"          # #F0C321 (dourado do site)
GRAF = "&H00141211&"          # #111214 (grafite do site)
WHITE = "&H00FFFFFF&"
MUTED = "&H00ABA8A6&"         # #A6A8AB

def ts(t):
    t = max(t, 0); return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"

hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Barlow Condensed ExtraBold,108,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,7,3,5,40,40,0,1
Style: Title,Barlow Condensed ExtraBold,98,&H00FFFFFF,&H00FFFFFF,&H00141211,&H96000000,0,0,0,0,100,100,1,0,1,5,3,5,40,40,0,1
Style: Sub,Barlow Condensed,54,&H0021C3F0,&H0021C3F0,&H00141211,&H96000000,0,0,0,0,100,100,4,0,1,4,2,5,40,40,0,1
Style: TagG,Barlow Condensed ExtraBold,62,&H00141211,&H00141211,&H0021C3F0,&H0021C3F0,0,0,0,0,100,100,3,0,3,16,0,5,0,0,0,1
Style: TagD,Barlow Condensed ExtraBold,62,&H00FFFFFF,&H00FFFFFF,&H00141211,&H00141211,0,0,0,0,100,100,3,0,3,16,0,5,0,0,0,1
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

POP = "\\fscx70\\fscy70\\t(0,140,\\fscx104\\fscy104)\\t(140,220,\\fscx100\\fscy100)"
FADE = "\\fad(180,150)"
g = lambda t: "{\\c" + GOLD + "}" + t + "{\\c" + WHITE + "}"

# ---- títulos (abaixo do logo do topo) ----
TY = 395
add(0.15, 7.95, "Title", 540, TY, "TROCA COMPLETA DO " + g("CÂMBIO"), extra=FADE + POP)
add(0.45, 7.95, "Sub", 540, TY + 82, "NISSAN KICKS  •  CVT", extra=FADE)
add(8.2, 11.75, "Title", 540, TY, g("2 FILTROS") + " NOVOS", extra=FADE + POP)
add(8.4, 11.75, "Sub", 540, TY + 82, "SUBSTITUÍDOS NA TROCA", extra=FADE)
add(11.9, 15.25, "Title", 540, TY, "LIMPEZA DO " + g("CÁRTER"), extra=FADE + POP)
add(12.1, 15.25, "Sub", 540, TY + 82, "E DOS SOLENOIDES", extra=FADE)
add(15.4, 17.95, "Title", 540, TY, "PROCEDIMENTO " + g("COMPLETO"), extra=FADE + POP)
add(15.6, 17.95, "Sub", 540, TY + 82, "DO INÍCIO AO FIM", extra=FADE)

# ---- etiquetas (dourado = novo/depois, grafite = velho/antes) ----
add(8.5, 10.1, "TagG", 265, 640, "NOVO", extra=FADE + POP)
add(8.8, 10.1, "TagD", 820, 560, "VELHO", extra=FADE + POP)
add(10.25, 11.9, "TagG", 790, 520, "NOVO", extra=FADE + POP)
add(10.55, 11.9, "TagD", 300, 1010, "VELHO", extra=FADE + POP)
add(11.95, 13.6, "TagD", 210, 520, "ANTES", extra=FADE + POP)
add(13.7, 15.4, "TagG", 220, 520, "DEPOIS", extra=FADE + POP)

# ---- legenda palavra a palavra ----
words = json.load(open("words.json"))
groups, cur = [], []
for w in words:
    cur.append(w)
    if w[0][-1] in ".,!?" or len(cur) == 3 or len(" ".join(x[0] for x in cur)) > 16:
        groups.append(cur); cur = []
if cur: groups.append(cur)
for gi, grp in enumerate(groups):
    gs, ge = grp[0][1] + VO_OFF, grp[-1][2] + VO_OFF
    nxt = groups[gi + 1][0][1] + VO_OFF if gi + 1 < len(groups) else 99
    cy = 1640 if gs >= E0 - 0.1 else 1400      # no fechamento, legenda mais baixa
    for k, w in enumerate(grp):
        st = w[1] + VO_OFF if k else gs
        en = (grp[k + 1][1] + VO_OFF) if k + 1 < len(grp) else min(ge + 0.12, nxt - 0.01)
        parts = [(g(x[0].upper().rstrip(".,")) if j == k else x[0].upper().rstrip(".,")) for j, x in enumerate(grp)]
        add(st, en, "Cap", 540, cy, " ".join(parts), layer=2, extra=POP if k == 0 else "")

# ---- fechamento no estilo do site ----
D = "\\fad(300,0)"
add(E0 + 0.35, END, "Brow", 540, 760, "———  ESPECIALISTA EM CÂMBIO AUTOMÁTICO  ———", extra=D)
add(E0 + 0.55, END, "Big", 540, 880, "SEU CARRO BEM CUIDADO.", extra=D + "\\fscx88\\fscy88\\t(0,300,\\fscx100\\fscy100)")
add(E0 + 0.75, END, "Big", 540, 1005, g("SEU CÂMBIO EM BOAS MÃOS."), extra=D + "\\fscx88\\fscy88\\t(0,300,\\fscx100\\fscy100)")
add(E0 + 1.0, END, "Info", 540, 1135, "Estr. dos Bandeirantes, 841 · Taquara – RJ", extra=D)
add(E0 + 1.3, END, "Btn", 540, 1265, "AGENDE PELO WHATSAPP  (21) 97544-6417", extra=D + POP)
add(E0 + 1.6, END, "Info", 540, 1395, g("★★★★★") + "{\\c" + MUTED + "}  4,9 no Google · Delivery Car leva e traz", extra=D)

open("tmp/subs2.ass", "w").write(hdr + "\n".join(ev) + "\n")

# ---- logo: pequeno no topo durante as cenas, grande no fechamento ----
fc = (
    "[1:v]format=rgba,scale=230:-1:flags=lanczos,split=2[ls][lb0];"
    "[lb0]scale=600:-1:flags=lanczos[lb];"
    "[ls]fade=t=out:st=17.7:d=0.3:alpha=1[lsf];"
    f"[lb]fade=t=in:st={E0+0.05}:d=0.45:alpha=1[lbf];"
    "movie=tmp/grad.png[gr];"
    "[0:v][gr]overlay=0:0[v0];"
    "[v0][lsf]overlay=x=(W-w)/2:y=135:enable='lt(t,18.05)'[v1];"
    f"[v1][lbf]overlay=x=(W-w)/2:y=330:enable='gte(t,{E0})'[v2];"
    "[v2]ass=tmp/subs2.ass[v]"
)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "tmp/base.mp4", "-loop", "1", "-framerate", "30", "-i", "logo.png",
                "-i", "tmp/mix.wav", "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", str(END),
                "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "reel_kicks_cambio_v2.mp4"], check=True)
print("ok")
