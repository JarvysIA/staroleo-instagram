#!/usr/bin/env python3
"""Lote 2026-11-27 (produção da execução de 27/11): stories de 04/12 e 05/12 (dezembro, sem Black).
04/12 (sexta, dia PAR do teste: story 11h50 e 19h00)
  11h50 "Já passou aqui · Chevrolet Spin" (Tudo até Outubro 26/IMG_4256.HEIC, Spin amarela, capa de placa da Star).
  19h00 oferta pneus Crystone a partir de R$ 199,90 no pix, montagem grátis (Pneus Crystone/IMG_0286.HEIC,
        215/65R16 com etiqueta "pneu remold": não escrever "novo"; sem 10x na mesma peça).
05/12 (sábado, dia ÍMPAR: story 11h50 e 17h00)
  11h50 "Já passou aqui · Nissan Kicks" (Tudo até Outubro 26/IMG_4237.HEIC, Kicks prata 1ª geração).
  17h00 bastidor "Filtro velho x filtro novo" (Tudo até Outubro 26/IMG_1839.HEIC, filtro sujo x novo WEGA nas mãos).
"""
import sys, os
sys.path.insert(0, "/home/claude/staroleo-instagram/_codigo")
from star_lib import *
from star_lib import SW, SH

T = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/Tudo até Outubro 26/"
P = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/Pneus Crystone/"
O = "/home/claude/staroleo-instagram/2026-11/lote-2026-11-27/"
os.makedirs(O, exist_ok=True)
o = lambda n: O + n

def topo(src, dst, dy=0):
    """Foto 3:4 na largura do story, colada no alto (dy px), com o fundo de baixo desfocado: o assunto fica acima dos textos."""
    im = abrir(src).resize((SW, round(abrir(src).height * SW / abrir(src).width)), Image.LANCZOS)
    c = Image.new("RGB", (SW, SH), GRAF)
    fundo = im.crop((0, im.height - 300, SW, im.height)).resize((SW, SH)).filter(ImageFilter.GaussianBlur(40))
    c.paste(fundo, (0, 0)); c.paste(im, (0, dy))
    m = Image.new("L", (SW, 160), 0)
    for y in range(160): m.paste(int(255 * y / 159), (0, y, SW, y + 1))
    c.paste(fundo.crop((0, dy + im.height - 160, SW, dy + im.height)), (0, dy + im.height - 160), m)
    c.save(dst, quality=95); return dst

def recorte(src, dst, y1=0.80):
    im = abrir(src); w, h = im.size
    im.crop((0, 0, w, int(h * y1))).save(dst, quality=95)

# 04/12 11h50 Spin
recorte(T + "IMG_4256.HEIC", o("_sp.jpg"))
story_carro(o("_sp.jpg"), "CHEVROLET SPIN", o("story_0412_1150_spin.jpg"), fy=0.15)

# 04/12 19h00 pneus Crystone
topo(P + "IMG_0286.HEIC", o("_pn.jpg"), dy=-40)
story_oferta(o("_pn.jpg"), "PNEUS CRYSTONE", "R$ 199,90", "no pix",
             "Montagem grátis · chama no WhatsApp", o("story_0412_1900_pneus.jpg"), fy=0.25)

# 05/12 11h50 Kicks
recorte(T + "IMG_4237.HEIC", o("_ki.jpg"))
story_carro(o("_ki.jpg"), "NISSAN KICKS", o("story_0512_1150_kicks.jpg"), fy=0.15)

# 05/12 17h00 bastidor filtro velho x novo
def story_bastidor(foto, out):
    c = grad(cover(carregar(foto), SW, SH), top=420, top_a=200, bot=760, bot_a=245)
    d = ImageDraw.Draw(c)
    pill(d, SW / 2, 270, "BASTIDOR DA STAR", bc(44), GRAF, GOLD, padx=30, pady=14, center=True)
    # etiquetas sobre cada filtro (velho à esquerda, novo à direita)
    pill(d, 300, 470, "VELHO", bc(54), WHITE, (229, 57, 53), padx=30, pady=12, center=True)
    pill(d, 790, 470, "NOVO", bc(54), GRAF, GOLD, padx=30, pady=12, center=True)
    y = 1220
    ctext(d, SW, y, "ISSO SAI DO SEU CÂMBIO.", bc(96), WHITE); y += 108
    ctext(d, SW, y, "NA STAR, O FILTRO É TROCADO.", bc(68), GOLD); y += 96
    ctext(d, SW, y, "Troca completa do óleo do câmbio automático", mr(36), WHITE)
    c.save(out, quality=93); return out

topo(T + "IMG_1839.HEIC", o("_bf.jpg"), dy=40)
story_bastidor(o("_bf.jpg"), o("story_0512_1700_bastidor_filtro.jpg"))

for n in ["_sp.jpg", "_ki.jpg", "_pn.jpg", "_bf.jpg"]: os.remove(o(n))
folha_previa([o("story_0412_1150_spin.jpg"), o("story_0412_1900_pneus.jpg"),
              o("story_0512_1150_kicks.jpg"), o("story_0512_1700_bastidor_filtro.jpg")],
             sys.argv[1] if len(sys.argv) > 1 else "/tmp/previa.jpg", larg=420)
print("ok")
