from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

root = Path('/home/aureo/jantar-amigos-direito-uerj/assets')
src = root / 'mapa-mesas-pareo-v2.jpg'
out = root / 'mapa-mesas-pareo-colorido.jpg'
base = Image.open(src).convert('RGBA')
W, H = base.size

font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
num = ImageFont.truetype(bold, 24)
title = ImageFont.truetype(bold, 22)
text = ImageFont.truetype(font, 16)
small = ImageFont.truetype(font, 14)

# Table centers on the new plan (v2).
centers = {1: (624, 141), 2: (871, 73), 3: (992, 84), 4: (483, 155), 5: (791, 194),
           6: (935, 184), 7: (357, 285), 8: (487, 290), 9: (354, 162), 10: (782, 324),
           11: (916, 309), 12: (356, 420), 13: (756, 464), 14: (897, 437),
           15: (1012, 385), 16: (480, 408), 17: (348, 528), 18: (471, 525)}
TABLE_R = 33

# Tables 15 to 18: 8 chairs (two removed from each).
bd = ImageDraw.Draw(base, 'RGBA')
for t in (15, 16, 17, 18):
    cx, cy = centers[t]
    bd.ellipse((cx - 57, cy - 57, cx + 57, cy + 57), fill='#ffffff')
    for k in range(8):
        a = math.radians(k * 45)
        x, y = cx + 44 * math.cos(a), cy + 44 * math.sin(a)
        s = 9
        pts = [(x + s * 1.41 * math.cos(a + math.radians(d)), y + s * 1.41 * math.sin(a + math.radians(d)))
               for d in (45, 135, 225, 315)]
        bd.polygon(pts, fill='#ffffff', outline='#8a8a8a', width=2)
    bd.ellipse((cx - TABLE_R, cy - TABLE_R, cx + TABLE_R, cy + TABLE_R), fill='#ffffff', outline='#6a6a6a', width=2)

H2 = H + 300
canvas = Image.new('RGBA', (W, H2), '#f4f5f0')
canvas.alpha_composite(base, (0, 0))
d = ImageDraw.Draw(canvas, 'RGBA')

def label(t):
    x, y = centers[t]
    s = str(t); b = d.textbbox((0, 0), s, font=num)
    d.text((x - (b[2] - b[0]) / 2, y - (b[3] - b[1]) / 2 - 3), s, font=num, fill='#172029')

# Same allocation as the previous plan.
colors = {1: '#f0bf19', 5: '#f0bf19', 6: '#f0bf19', 10: '#f0bf19', 8: '#16a7dd', 9: '#ee3b17', 11: '#ee8a1d'}
r = TABLE_R + 2
for t, c in colors.items():
    x, y = centers[t]
    d.ellipse((x - r, y - r, x + r, y + r), fill=c + 'C0', outline=c + 'FF', width=4)
    label(t)
for t in (2, 3):
    x, y = centers[t]
    d.pieslice((x - r, y - r, x + r, y + r), 90, 270, fill='#118a20C0', outline='#118a20FF', width=3)
    d.pieslice((x - r, y - r, x + r, y + r), 270, 90, fill='#c48ad3C0', outline='#c48ad3FF', width=3)
    label(t)
for t in (15, 16, 17, 18):
    label(t)

y0 = H + 18
d.rounded_rectangle((28, y0, W - 28, H2 - 22), radius=14, fill='#fffefa', outline='#dce2de', width=2)
d.text((52, y0 + 20), 'Mesas já destinadas', font=title, fill='#172029')
d.text((52, y0 + 50), 'Mesas 1 a 14: 10 lugares · Mesas 15 a 18: 8 lugares. Mesas sem cor ainda não têm escolha registrada.', font=small, fill='#6e7880')
entries = [
    ('#118a20', 'Diretoria / Comitês', 'mesas 2 e 3 · alocação compartilhada'),
    ('#c48ad3', 'Convidados especiais', 'mesas 2 e 3 · alocação compartilhada'),
    ('#f0bf19', 'Bermudes · mesa 1 | Binenbojm · mesa 5', 'Galdino · mesa 6 | Tepedino · mesa 10'),
    ('#ee3b17', 'BMA', 'mesa 9'),
    ('#ee8a1d', 'Turma 1991.2', 'mesa 11'),
    ('#16a7dd', 'Leonardo Espíndola', 'mesa 8'),
]
for i, (c, name, detail) in enumerate(entries):
    col, row = i % 2, i // 2
    x, y = 55 + col * 590, y0 + 84 + row * 55
    d.rounded_rectangle((x, y, x + 24, y + 24), radius=5, fill=c, outline='#ffffff', width=1)
    d.text((x + 35, y - 2), name, font=text, fill='#172029')
    d.text((x + 35, y + 19), detail, font=small, fill='#6e7880')
canvas.convert('RGB').save(out, quality=94)
print(out, canvas.size)
