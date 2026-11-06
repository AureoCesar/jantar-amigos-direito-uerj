from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

src=Path('/home/aureo/jantar-amigos-direito-uerj/assets/mapa-mesas-pareo.jpg')
out=Path('/home/aureo/jantar-amigos-direito-uerj/assets/mapa-mesas-pareo-colorido.jpg')
base=Image.open(src).convert('RGBA')

# Mesas de 8 lugares: 14 e 15 redesenhadas 10% menores; 16 e 17 incluídas embaixo.
import math
bd=ImageDraw.Draw(base,'RGBA')
tnum=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',19)
def table8(cx,cy,label,clear=True):
    if clear: bd.ellipse((cx-60,cy-60,cx+60,cy+60),fill='#fbfbfb')
    else: bd.ellipse((cx-56,cy-56,cx+56,cy+56),fill='#f7f7f7')
    r=29; cr=42; s=7.2
    for k in range(8):
        a=math.radians(k*45+22.5); x=cx+cr*math.cos(a); y=cy+cr*math.sin(a)
        pts=[(x+s*math.cos(a+math.radians(t))*1.41,y+s*math.sin(a+math.radians(t))*1.41) for t in (45,135,225,315)]
        bd.polygon(pts,fill='#ffffff',outline='#555555')
    bd.ellipse((cx-r,cy-r,cx+r,cy+r),fill='#ffffff',outline='#333333',width=2)
    b=bd.textbbox((0,0),label,font=tnum); bd.text((cx-(b[2]-b[0])/2,cy-(b[3]-b[1])/2-3),label,font=tnum,fill='#111111')
table8(876,556,'14'); table8(992,516,'15')
table8(595,560,'16',clear=False); table8(1165,560,'17',clear=False)
canvas=Image.new('RGBA',(1280,1165),'#f4f5f0')
canvas.alpha_composite(base,(0,0))
d=ImageDraw.Draw(canvas,'RGBA')
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
num=ImageFont.truetype(bold,26)
title=ImageFont.truetype(bold,22)
text=ImageFont.truetype(font,16)
small=ImageFont.truetype(font,14)

# Table center coordinates. Selected tables receive a translucent fill, preserving plan geometry.
centers={1:(585,171),2:(865,150),3:(1016,150),5:(785,267),6:(943,267),8:(493,398),9:(587,302),10:(786,399),11:(943,400)}
colors={1:'#f0bf19',5:'#f0bf19',6:'#f0bf19',10:'#f0bf19',8:'#16a7dd',9:'#ee3b17',11:'#ee8a1d'}
for table,color in colors.items():
    x,y=centers[table]; d.ellipse((x-42,y-42,x+42,y+42),fill=color+'B3',outline=color+'FF',width=5)
    label=str(table); box=d.textbbox((0,0),label,font=num); d.text((x-(box[2]-box[0])/2,y-(box[3]-box[1])/2-2),label,font=num,fill='#172029')
# Split marking for tables 2 and 3: shared allocation between internal board and special guests.
for table in (2,3):
    x,y=centers[table]
    d.pieslice((x-42,y-42,x+42,y+42),90,270,fill='#118a20B3',outline='#118a20FF',width=4)
    d.pieslice((x-42,y-42,x+42,y+42),270,90,fill='#c48ad3B3',outline='#c48ad3FF',width=4)
    label=str(table); box=d.textbbox((0,0),label,font=num); d.text((x-(box[2]-box[0])/2,y-(box[3]-box[1])/2-2),label,font=num,fill='#172029')

# Legend below the plan.
y0=872
d.rounded_rectangle((28,y0,1252,1140),radius=14,fill='#fffefa',outline='#dce2de',width=2)
d.text((52,y0+22),'Mesas já destinadas',font=title,fill='#172029')
d.text((52,y0+52),'Cores indicam grupos com mesa definida. Mesas sem cor ainda não têm escolha registrada.',font=small,fill='#6e7880')
entries=[
 ('#118a20','Diretoria / Comitês','mesas 2 e 3 · alocação compartilhada'),
 ('#c48ad3','Convidados especiais','mesas 2 e 3 · alocação compartilhada'),
 ('#f0bf19','Bermudes · mesa 1 | Binenbojm · mesa 5','Galdino · mesa 6 | Tepedino · mesa 10'),
 ('#ee3b17','BMA','mesa 9'),
 ('#ee8a1d','Turma 1991.2','mesa 11'),
 ('#16a7dd','Leonardo Espíndola','mesa 8'),
]
for i,(color,name,detail) in enumerate(entries):
    col=i%2; row=i//2; x=55+col*590; y=y0+88+row*55
    d.rounded_rectangle((x,y,x+24,y+24),radius=5,fill=color,outline='#ffffff',width=1)
    d.text((x+35,y-2),name,font=text,fill='#172029')
    d.text((x+35,y+19),detail,font=small,fill='#6e7880')
canvas.convert('RGB').save(out,quality=94)
print(out)
