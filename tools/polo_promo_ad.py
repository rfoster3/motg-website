import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
F='fonts/'
def font(name,size,w=None):
    f=ImageFont.truetype(F+name,size)
    if w: f.set_variation_by_axes([w])
    return f
PURPLE=(75,42,127); GOLD=(214,178,96); CREAM=(245,240,225); DEEP=(36,18,64)
variant=sys.argv[1] if len(sys.argv)>1 else 'launch'
src=Image.open('gen/r1_logo.png').convert('RGB')   # 2160x2688
k=2160/896
x0,y0,w=int(80*k),0,int(700*k); h=int(w*1.25)
im=src.crop((x0,y0,x0+w,y0+h)).resize((1080,1350),Image.LANCZOS)
im.save(f'out/motg-polo-model-crop-clean.jpg',quality=94)
W,H=1080,1350
base=im.convert('RGBA')
# top-left scrim for wordmark legibility
g=np.zeros((H,W,4),np.uint8); g[...,:3]=DEEP
yy,xx=np.mgrid[0:H,0:W]
top=np.clip(1-np.hypot(xx/430,yy/300),0,1)**1.2*175
# bottom panel fade
bot=np.clip((yy-876)/230,0,1)**1.3*244
g[...,3]=np.maximum(top,bot).astype(np.uint8)
base=Image.alpha_composite(base,Image.fromarray(g,'RGBA'))
d=ImageDraw.Draw(base)
# wordmark top-left
mk=Image.open('/Users/ronniefoster/motg-website/assets/logo-m.png').convert('RGBA'); mk=mk.crop(mk.getbbox())
mk=mk.resize((58,int(mk.height*58/mk.width)),Image.LANCZOS)
fw=font('Cinzel%5Bwght%5D.ttf',28,700)
def spaced(xy,t,f,fill,sp=3):
    x,y=xy
    for ch in t: d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+sp
spaced((48,44),'MAGICIANS',fw,CREAM,3.4); spaced((48,78),'ON THE GREEN',fw,CREAM,3.4)
# bottom copy, left aligned
L=60
f1=font('Cinzel%5Bwght%5D.ttf',40,700); f2=font('Allura-Regular.ttf',128)
fS=font('Cinzel%5Bwght%5D.ttf',34,700); fB=font('Figtree%5Bwght%5D.ttf',34,500)
d.text((L+4,976),'WEAR THE',font=f1,fill=CREAM)
d.text((L,998),'Magic',font=f2,fill=GOLD)
sub='THE M GOLF POLO' if variant=='launch' else 'THE M GOLF POLO  |  COMING SOON'
d.text((L+4,1170),sub,font=fS,fill=CREAM)
d.text((L+4,1218),'10% of every purchase supports',font=fB,fill=CREAM)
d.text((L+4,1256),'LeMoyne-Owen golf.',font=fB,fill=CREAM)
# logo proof inset (close-up of the embroidered chest)
cx,cy,r=1281,1023,88
crop=src.crop((cx-r,cy-r,cx+r,cy+r)).resize((236,236),Image.LANCZOS)
m=Image.new('L',(236,236),0); ImageDraw.Draw(m).ellipse((0,0,235,235),fill=255)
ix,iy=790,1060
ring=Image.new('RGBA',(248,248),(0,0,0,0)); ImageDraw.Draw(ring).ellipse((0,0,247,247),fill=GOLD+(255,))
sh=Image.new('RGBA',(270,270),(0,0,0,0)); ImageDraw.Draw(sh).ellipse((11,15,259,263),fill=(0,0,0,120)); sh=sh.filter(ImageFilter.GaussianBlur(8))
base.alpha_composite(sh,(ix-17,iy-17))
base.alpha_composite(ring,(ix-6,iy-6))
base.paste(crop,(ix,iy),m)
fD=font('Figtree%5Bwght%5D.ttf',18,500)
lay=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(lay).text((L+4,1312),'Independent supporter brand. Not an official LeMoyne-Owen College product.',font=fD,fill=CREAM+(179,))
base=Image.alpha_composite(base,lay)
out=base.convert('RGB')
name='motg-polo-ad-4x5' + ('' if variant=='launch' else '-prelaunch')
out.save(f'out/{name}.jpg',quality=94)
out.resize((270,338),Image.LANCZOS).save(f'out/{name}-thumb.png')
