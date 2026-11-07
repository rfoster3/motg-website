import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='fonts/'
def font(n,s,w=None):
    f=ImageFont.truetype(F+n,s)
    if w: f.set_variation_by_axes([w])
    return f
PURPLE=(75,42,127); GOLD=(201,162,75); INK=(46,30,72); MUTED=(110,96,128)
W,H=2160,2700
def bg():
    yy,xx=np.mgrid[0:H,0:W]
    r=np.hypot((xx-W/2)/W,(yy-H*0.55)/H)
    top=np.array([247,243,235]); edge=np.array([229,221,206])
    t=np.clip(r/0.75,0,1)[...,None]**1.6
    return Image.fromarray((top*(1-t)+edge*t).astype('uint8')).convert('RGBA')
def shirt(c,v,h):
    im=Image.open(f'cut/{c}-{v}.png'); w=round(im.width*h/im.height)
    return im.resize((w,h),Image.LANCZOS)
def put(base,im,cx,top):
    x=int(cx-im.width/2); y=int(top)
    a=im.split()[3]
    # soft ground shadow + contact shadow
    sh=Image.new('RGBA',base.size,(0,0,0,0))
    s1=Image.new('RGBA',im.size,(40,25,60,0)); s1.putalpha(a.point(lambda p:p*0.22))
    sh.alpha_composite(s1,(x+14,y+34)); sh=sh.filter(ImageFilter.GaussianBlur(34))
    base.alpha_composite(sh)
    base.alpha_composite(im,(x,y))
def ctext(d,t,f,y,fill,cx=W/2,sp=0):
    w=sum(d.textlength(ch,font=f)+sp for ch in t)-sp; x=cx-w/2
    for ch in t: d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+sp
def footer(d):
    ctext(d,'MAGICIANS ON THE GREEN',font('Cinzel%5Bwght%5D.ttf',34,700),2590,MUTED,sp=7)

# ---- A: all four colors, 2x2 ----
base=bg(); d=ImageDraw.Draw(base)
ctext(d,'THE M GOLF POLO',font('Cinzel%5Bwght%5D.ttf',96,700),120,INK,sp=4)
ctext(d,'Four colors. One M.',font('Allura-Regular.ttf',120),236,PURPLE)
h=960; cols=[W*0.27,W*0.73]; rows=[420,1440]
lab=font('Figtree%5Bwght%5D.ttf',40,600)
for i,(c,name) in enumerate([('purple','Purple'),('black','Black'),('white','White'),('lightgray','Light Gray')]):
    im=shirt(c,'front',h); cx=cols[i%2]; top=rows[i//2]
    put(base,im,cx,top); ctext(d,name.upper(),lab,top+h+14,MUTED,cx=cx,sp=5)
footer(d)
base.convert('RGB').save('out/motg-polo-all-colors.jpg',quality=93)

# ---- B: purple front and back ----
base=bg(); d=ImageDraw.Draw(base)
ctext(d,'THE M GOLF POLO',font('Cinzel%5Bwght%5D.ttf',96,700),120,INK,sp=4)
ctext(d,'Front and back',font('Allura-Regular.ttf',120),236,PURPLE)
hb=1700; back=shirt('purple','back',hb); front=shirt('purple','front',hb)
put(base,back,W*0.33,560)
put(base,front,W*0.67,640)
# wizard close-up inset from the back shirt
src=Image.open('cut/purple-back.png'); s=hb/src.height
# locate wizard: find non-purple pixels in top-center region of the back cutout
a=np.asarray(src.convert('RGB')).astype(int); al=np.asarray(src.split()[3])
X0,Y0,X1,Y1=650,120,1050,520
reg=a[Y0:Y1,X0:X1]; ok=al[Y0:Y1,X0:X1]>250
med=np.median(reg[ok].reshape(-1,3),0)
dd=((reg[...,1]>reg[...,2]-5)|(reg.min(2)>200))&ok
dd=ndimage.binary_opening(dd,iterations=2)
ys,xs=np.where(dd)
wx=X0+(xs.min()+xs.max())/2; wy=Y0+(ys.min()+ys.max())/2
print('wizard',xs.min()+X0,xs.max()+X0,ys.min()+Y0,ys.max()+Y0)
R=170
zoom=src.crop((int(wx-R),int(wy-R),int(wx+R),int(wy+R))).convert('RGB').resize((520,520),Image.LANCZOS)
m=Image.new('L',(520,520),0); ImageDraw.Draw(m).ellipse((0,0,519,519),fill=255)
ix,iy=150,1790
sh=Image.new('RGBA',(600,600),(0,0,0,0)); ImageDraw.Draw(sh).ellipse((40,52,560,572),fill=(40,25,60,90)); sh=sh.filter(ImageFilter.GaussianBlur(18))
base.alpha_composite(sh,(ix-40,iy-40))
ring=Image.new('RGBA',(540,540),(0,0,0,0)); ImageDraw.Draw(ring).ellipse((0,0,539,539),fill=GOLD+(255,))
base.alpha_composite(ring,(ix-10,iy-10)); base.paste(zoom,(ix,iy),m)
# leader line from inset to the wizard on the back shirt
bx=W*0.33-back.width/2+wx*s; by=560+wy*s
wh=(ys.max()-ys.min())*s/2; ex,ey=bx,by+wh+26
d.line((ix+260+190,iy+70,ex,ey),fill=GOLD,width=5)
d.ellipse((ex-9,ey-9,ex+9,ey+9),fill=GOLD)
ctext(d,'The Magician rides on the back.',font('Figtree%5Bwght%5D.ttf',40,600),iy+540,INK,cx=ix+260)
footer(d)
base.convert('RGB').save('out/motg-polo-front-back.jpg',quality=93)
for n in ['all-colors','front-back']:
    Image.open(f'out/motg-polo-{n}.jpg').resize((540,675),Image.LANCZOS).save(f'out/{n}-small.png')
