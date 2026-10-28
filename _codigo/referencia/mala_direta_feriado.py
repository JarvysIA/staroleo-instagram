import sys; sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from star_lib import *
from PIL import Image, ImageDraw, ImageFilter
RED = (229, 57, 53)
W, H = 1080, 1350
foto = carregar("/home/claude/renegade/src/foto_renegade.jpg")
c = cover(foto, W, H, fy=0.55, zoom=1.0)
c = ImageEnhance.Brightness(c).enhance(0.55)
c = grad(c, top=700, top_a=245, bot=760, bot_a=255, full=0.7)
d = ImageDraw.Draw(c)

# faixa vermelha inclinada no topo
faixa = Image.new("RGBA", (W + 300, 118), RED + (255,))
fd = ImageDraw.Draw(faixa)
t = "FERIADÃO DE FINADOS  •  FERIADÃO DE FINADOS  •  FERIADÃO DE FINADOS"
fd.text((20, 14), t, font=bc(78), fill=WHITE)
faixa = faixa.rotate(-4, expand=True, resample=Image.BICUBIC)
c.paste(faixa, (-120, 40), faixa)
d = ImageDraw.Draw(c)

y = 215
ctext(d, W, y, "VAI PEGAR A ESTRADA?", bc(92), WHITE); y += 100
ctext(d, W, y, "PASSA NA STAR ANTES.", bc(92), GOLD); y += 128

# bloco 10x gigante
ctext(d, W, y, "TUDO EM", bc(84), WHITE); y += 92
f = bc(300); t = "10X"
tw = d.textlength(t, font=f); bx = (W - tw) / 2; top = f.getbbox(t)[1]
d.text((bx + 8, y - top + 8), t, font=f, fill=(0, 0, 0))
d.text((bx, y - top), t, font=f, fill=GOLD); y += f.getbbox(t)[3] - top + 18
ctext(d, W, y, "SEM JUROS", bc(118), WHITE); y += 126
ctext(d, W, y, "em todos os produtos e serviços", mr(40), WHITE); y += 74

# serviço destaque
y = pill(d, W / 2, y, "TROCA DE ÓLEO DO CÂMBIO AUTOMÁTICO", bc(54), GRAF, GOLD, padx=30, pady=14, center=True) + 10
ctext(d, W, y + 4, "completa, com máquina especializada", mrs(34), MUTED)

# selo cobrimos ofertas (estrela/círculo vermelho)
sel = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); sd = ImageDraw.Draw(sel)
import math
pts = []
for i in range(32):
    r = 148 if i % 2 == 0 else 128
    a = math.pi * 2 * i / 32
    pts.append((150 + r * math.cos(a), 150 + r * math.sin(a)))
sd.polygon(pts, fill=RED + (255,))
for txt, yy, s in [("COBRIMOS", 78, 62), ("OFERTAS", 140, 66)]:
    fo = bc(s); tw = sd.textlength(txt, font=fo); sd.text((150 - tw / 2, yy), txt, font=fo, fill=WHITE)
sel = sel.rotate(12, expand=False, resample=Image.BICUBIC)
c.paste(sel, (W - 300 - 12, 470), sel)
d = ImageDraw.Draw(c)

# rodapé: logo à esquerda, WhatsApp e endereço à direita
d.line((60, H - 205, W - 60, H - 205), fill=(60, 61, 64), width=2)
logo(c, 250, 50, H - 178)
fw = bc(58); tt = f"WHATSAPP  {WA}"; pw = d.textlength(tt, font=fw) + 56
pill(d, W - 50 - pw, H - 178, tt, fw, GRAF, GOLD, padx=28, pady=14)
fa = mrs(30); d.text((W - 50 - d.textlength(ENDERECO, font=fa), H - 80), ENDERECO, font=fa, fill=WHITE)
c.save("mala_direta_feriado.jpg", quality=94)
print("ok")
