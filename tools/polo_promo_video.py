import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S='/private/tmp/claude-501/-Users-ronniefoster/022544da-2e1b-4a69-b288-2227e95b178b/scratchpad/'
V=S+'vid/'; F=S+'fonts/'
MODE=sys.argv[1] if len(sys.argv)>1 else 'launch'   # launch | prelaunch
OUT=sys.argv[2] if len(sys.argv)>2 else V+f'motg-polo-promo-{MODE}.mp4'
W,H,FPS=1080,1920,30
GOLD=(214,178,96); CREAM=(245,240,225); DEEP=(36,18,64)
def font(n,s,w=None):
    f=ImageFont.truetype(F+n,s)
    if w:
        try: f.set_variation_by_axes([w])
        except Exception: pass
    return f
CIN=lambda s,w=600: font('Cinzel%5Bwght%5D.ttf',s,w)
FIG=lambda s,w=500: font('Figtree%5Bwght%5D.ttf',s,w)
ALL=lambda s: font('Allura-Regular.ttf',s)
B=[0,4.0,6.667,10.667,13.333,17.0]   # cuts on 90 bpm beats
N=int(B[-1]*FPS)
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def load(path):
    p=subprocess.run(['ffmpeg','-v','error','-i',path,'-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.uint8).reshape(-1,H,W,3)
A=load(V+'a1.mp4'); T=load(V+'t1.mp4')
# backdrop
yy,xx=np.mgrid[0:H,0:W]
d=np.sqrt(((xx-W/2)/W)**2+((yy-H*0.42)/H)**2)
t=np.clip(d/0.75,0,1)[...,None]
BG=(np.array([86,60,120.])*(1-t)+np.array([20,14,28.])*t)
def spaced(dr,xy,txt,f,fill,sp):
    x,y=xy
    for ch in txt: dr.text((x,y),ch,font=f,fill=fill); x+=dr.textlength(ch,font=f)+sp
def spaced_w(dr,txt,f,sp): return sum(dr.textlength(c,font=f)+sp for c in txt)-sp
def layer(): return Image.new('RGBA',(W,H),(0,0,0,0))
def put(base,lay,a,dy):
    if a<=0: return base
    l=lay
    if a<1:
        r,g,b,al=l.split(); al=al.point(lambda p:int(p*a)); l=Image.merge('RGBA',(r,g,b,al))
    base.alpha_composite(l,(0,int(round(dy))))
    return base
def anim(base,lay,t0,t,dur=0.45,rise=36):
    e=ease((t-t0)/dur); return put(base,lay,e,(1-e)*rise)
def scrim(y0,y1,top=False,amax=0.82):
    g=np.zeros((H,W,4),np.uint8); g[...,:3]=DEEP
    ys=np.arange(H); a=np.clip((ys-y0)/(y1-y0),0,1)
    if top: a=1-a
    g[...,3]=(255*amax*a**1.4)[:,None]
    return Image.fromarray(g,'RGBA')
# ---------- text layers ----------
L1=layer(); d=ImageDraw.Draw(L1)
spaced(d,(64,1236),'WEAR THE',CIN(56,700),CREAM,6)
d.text((54,1262),'Magic',font=ALL(210),fill=GOLD)
L1b=layer(); d=ImageDraw.Draw(L1b)
d.text((70,1530),'The M Golf Polo',font=FIG(40,600),fill=CREAM)
WM=layer(); d=ImageDraw.Draw(WM)
spaced(d,(56,170),'MAGICIANS',CIN(30,700),CREAM,4); spaced(d,(56,208),'ON THE GREEN',CIN(30,700),CREAM,4)
L2=layer(); d=ImageDraw.Draw(L2)
spaced(d,(64,1300),'SMOOTH STRETCH',CIN(54,700),CREAM,5)
spaced(d,(64,1366),'PERFORMANCE KNIT',CIN(54,700),CREAM,5)
d.text((66,1446),'86% polyester  |  14% spandex',font=FIG(38,500),fill=GOLD)
L3=layer(); d=ImageDraw.Draw(L3)
f=CIN(46,700); tw=spaced_w(d,'AND ON THE BACK',f,6); spaced(d,((W-tw)/2,150),'AND ON THE BACK',f,CREAM,6)
f2=ALL(150); tw=d.textlength('the Magician',font=f2); d.text(((W-tw)/2,176),'the Magician',font=f2,fill=GOLD)
L4=layer(); d=ImageDraw.Draw(L4)
f=CIN(46,700); tw=spaced_w(d,'FOUR COLORS',f,6); spaced(d,((W-tw)/2,150),'FOUR COLORS',f,CREAM,6)
f2=ALL(130); tw=d.textlength('One M',font=f2); d.text(((W-tw)/2,186),'One M',font=f2,fill=GOLD)
COLS=[('purple','PURPLE'),('black','BLACK'),('white','WHITE'),('lightgray','LIGHT GRAY')]
cutimgs={}
for c,_ in COLS:
    im=Image.open(S+f'cut/{c}-front.png').convert('RGBA'); bb=im.getbbox(); im=im.crop(bb)
    r,g,b,al=im.split(); al=al.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1)); im=Image.merge('RGBA',(r,g,b,al))
    s=780/im.width; cutimgs[c]=im.resize((780,int(im.height*s)),Image.LANCZOS)
def shirt_frame(c,label,zoom):
    base=Image.fromarray(BG.astype(np.uint8)).convert('RGBA')
    im=cutimgs[c]; s=zoom; im2=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    x=(W-im2.width)//2; y=430+(1-s)*400
    a=im2.split()[3]
    sh=Image.new('RGBA',im2.size,(10,5,20,0)); sh.putalpha(a.point(lambda p:p*0.55))
    shl=layer(); shl.alpha_composite(sh,(x+10,int(y)+40)); shl=shl.filter(ImageFilter.GaussianBlur(30))
    base.alpha_composite(shl); base.alpha_composite(im2,(x,int(y)))
    dd=ImageDraw.Draw(base); f=CIN(44,700); tw=spaced_w(dd,label,f,8)
    spaced(dd,((W-tw)/2,1440),label,f,CREAM,8)
    return base
# end card
def endcard():
    base=Image.fromarray(BG.astype(np.uint8)).convert('RGBA')
    im=cutimgs['purple']; im2=im.resize((560,int(im.height*560/im.width)),Image.LANCZOS)
    x=(W-im2.width)//2; y=290
    a=im2.split()[3]; sh=Image.new('RGBA',im2.size,(10,5,20,0)); sh.putalpha(a.point(lambda p:p*0.55))
    shl=layer(); shl.alpha_composite(sh,(x+8,y+30)); shl=shl.filter(ImageFilter.GaussianBlur(24))
    base.alpha_composite(shl); base.alpha_composite(im2,(x,y))
    return base
EC=endcard()
E1=layer(); d=ImageDraw.Draw(E1)
f=CIN(34,700)
for i,tx in enumerate(['MAGICIANS','ON THE GREEN']):
    tw=spaced_w(d,tx,f,7); spaced(d,((W-tw)/2,150+i*44),tx,f,CREAM,7)
E2=layer(); d=ImageDraw.Draw(E2)
f=CIN(60,700); tw=spaced_w(d,'WEAR THE',f,7); spaced(d,((W-tw)/2,980),'WEAR THE',f,CREAM,7)
f2=ALL(220); tw=d.textlength('Magic',font=f2); d.text(((W-tw)/2,1000),'Magic',font=f2,fill=GOLD)
E3=layer(); d=ImageDraw.Draw(E3)
sub='THE M GOLF POLO  |  COMING SOON' if MODE=='prelaunch' else 'THE M GOLF POLO'
f=CIN(40,700); tw=spaced_w(d,sub,f,4); spaced(d,((W-tw)/2,1268),sub,f,CREAM,4)
d.line(((W-120)/2,1338,(W+120)/2,1338),fill=GOLD,width=3)
f=FIG(42,500)
for i,tx in enumerate(['10% of every purchase supports','LeMoyne-Owen golf.']):
    tw=d.textlength(tx,font=f); d.text(((W-tw)/2,1366+i*54),tx,font=f,fill=CREAM)
E4=layer(); d=ImageDraw.Draw(E4)
f=FIG(26,500); tx='Independent supporter brand. Not an official LeMoyne-Owen College product.'
tw=d.textlength(tx,font=f); d.text(((W-tw)/2,1500),tx,font=f,fill=CREAM+(190,))
SC_BOT=scrim(1050,1700); SC_TOP=scrim(0,340,top=True,amax=0.55)
# still close-up source
CL=Image.open(S+'gen/m1_logo.png').convert('RGB'); LX,LY=1281,1023
rng=np.random.default_rng(7)
def frame(i):
    t=i/FPS
    if t<B[1]:
        fr=Image.fromarray(A[min(int(t*24),len(A)-1)]).convert('RGBA')
        fr.alpha_composite(SC_BOT); fr.alpha_composite(SC_TOP)
        fr=anim(fr,WM,0.15,t); fr=anim(fr,L1,0.2,t,0.55,44); fr=anim(fr,L1b,0.9,t)
    elif t<B[2]:
        u=(t-B[1])/(B[2]-B[1]); cw=980-380*ease(u*0.9); ch=cw*16/9
        cx=LX-cw*0.08; cy=LY+ch*0.24
        box=(cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2)
        fr=CL.resize((W,H),Image.LANCZOS,box=box).convert('RGBA')
        fr.alpha_composite(SC_BOT); fr=anim(fr,L2,B[1]+0.25,t)
    elif t<B[3]:
        st=0.55+(t-B[2])*(4.0/ (B[3]-B[2]))
        fr=Image.fromarray(T[min(int(st*24),len(T)-1)]).convert('RGBA')
        fr=anim(fr,L3,B[2]+2.2,t)
    elif t<B[4]:
        k=min(int((t-B[3])/((B[4]-B[3])/4)),3); tl=(t-B[3])-k*(B[4]-B[3])/4
        c,lab=COLS[k]; fr=shirt_frame(c,lab,0.97+0.03*ease(tl/0.6))
        fr.alpha_composite(L4)
    else:
        fr=EC.copy(); te=t-B[4]
        fr=anim(fr,E1,B[4]+0.1,t); fr=anim(fr,E2,B[4]+0.3,t,0.6,40); fr=anim(fr,E3,B[4]+0.9,t); fr=anim(fr,E4,B[4]+1.3,t)
    fr=np.asarray(fr.convert('RGB')).astype(np.float32)
    # quick 4-frame dip between segments for smoothness
    for b in B[1:-1]:
        dt=abs(t-b)
        if dt<2/FPS: fr*= (0.55+0.45*dt/(2/FPS))
    fr+=rng.normal(0,2.2,(H,W,1)).astype(np.float32)
    return np.clip(fr,0,255).astype(np.uint8)
if __name__=='__main__':
    if len(sys.argv)>3:
        for ts in sys.argv[3].split(','):
            Image.fromarray(frame(int(float(ts)*FPS))).save(V+f'chk_{MODE}_{ts}.jpg',quality=90)
        sys.exit()
    p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-i',V+'music1.mp3','-filter_complex','[1:a]atrim=0:17,afade=t=in:d=0.15,afade=t=out:st=16.3:d=0.7,loudnorm=I=-14:TP=-1.5:LRA=11[a]',
        '-map','0:v','-map','[a]','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-profile:v','high',
        '-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-shortest',OUT],stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print('done',OUT)
