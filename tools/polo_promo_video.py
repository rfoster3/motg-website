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
B=[0,2.667,5.333,9.333,12.667,17.0]   # cuts on 90 bpm beats
N=int(B[-1]*FPS)
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def load(path):
    p=subprocess.run(['ffmpeg','-v','error','-i',path,'-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.uint8).reshape(-1,H,W,3)
A=load(V+'a2.mp4'); T=load(V+'t1.mp4')
FRONT=Image.open(V+'start_front.jpg').convert('RGB'); BACK=Image.open(V+'start_back.jpg').convert('RGB')
WX,WY=895,830
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
spaced(d,(64,1120),'WEAR THE',CIN(56,700),CREAM,6)
d.text((54,1146),'Magic',font=ALL(200),fill=GOLD)
L1b=layer(); d=ImageDraw.Draw(L1b)
d.text((68,1404),'The M Golf Polo',font=FIG(42,600),fill=CREAM)
d.text((68,1456),'10% of every purchase supports',font=FIG(37,600),fill=GOLD)
d.text((68,1500),'LeMoyne-Owen golf.',font=FIG(37,600),fill=GOLD)
WM=layer(); d=ImageDraw.Draw(WM)
spaced(d,(56,288),'MAGICIANS',CIN(30,700),CREAM,4); spaced(d,(56,326),'ON THE GREEN',CIN(30,700),CREAM,4)
L2=layer(); d=ImageDraw.Draw(L2)
spaced(d,(64,1300),'SMOOTH STRETCH',CIN(54,700),CREAM,5)
spaced(d,(64,1366),'PERFORMANCE KNIT',CIN(54,700),CREAM,5)
d.text((66,1446),'86% polyester  |  14% spandex',font=FIG(38,500),fill=GOLD)
L3=layer(); d=ImageDraw.Draw(L3)
f=CIN(46,700); tw=spaced_w(d,'AND ON THE BACK',f,6); spaced(d,((W-tw)/2,1250),'AND ON THE BACK',f,CREAM,6)
f2=ALL(150); tw=d.textlength('the Magician',font=f2); d.text(((W-tw)/2,1276),'the Magician',font=f2,fill=GOLD)
L4=layer(); d=ImageDraw.Draw(L4)
f=CIN(46,700); tw=spaced_w(d,'FOUR COLORS',f,6); spaced(d,((W-tw)/2,280),'FOUR COLORS',f,CREAM,6)
f2=ALL(130); tw=d.textlength('One M',font=f2); d.text(((W-tw)/2,316),'One M',font=f2,fill=GOLD)
COLS=[('purple','PURPLE'),('black','BLACK'),('white','WHITE'),('lightgray','LIGHT GRAY')]
cutimgs={}
for c,_ in COLS:
    im=Image.open(S+f'cut/{c}-front.png').convert('RGBA'); bb=im.getbbox(); im=im.crop(bb)
    r,g,b,al=im.split(); al=al.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1)); im=Image.merge('RGBA',(r,g,b,al))
    s=700/im.width; cutimgs[c]=im.resize((700,int(im.height*s)),Image.LANCZOS)
def shirt_frame(c,label,zoom):
    base=Image.fromarray(BG.astype(np.uint8)).convert('RGBA')
    im=cutimgs[c]; s=zoom; im2=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    x=(W-im2.width)//2; y=500+(1-s)*400
    a=im2.split()[3]
    sh=Image.new('RGBA',im2.size,(10,5,20,0)); sh.putalpha(a.point(lambda p:p*0.55))
    shl=layer(); shl.alpha_composite(sh,(x+10,int(y)+40)); shl=shl.filter(ImageFilter.GaussianBlur(30))
    base.alpha_composite(shl); base.alpha_composite(im2,(x,int(y)))
    dd=ImageDraw.Draw(base); f=CIN(44,700); tw=spaced_w(dd,label,f,8)
    spaced(dd,((W-tw)/2,1376),label,f,CREAM,8)
    sw={'purple':(101,55,157),'black':(27,27,28),'white':(236,238,244),'lightgray':(196,199,198)}
    cx0=W/2-1.5*84
    for j,(cc,_) in enumerate(COLS):
        x=cx0+j*84; y=1478
        if cc==c: dd.ellipse((x-31,y-31,x+31,y+31),outline=GOLD,width=4)
        dd.ellipse((x-22,y-22,x+22,y+22),fill=sw[cc],outline=(245,240,225),width=2)
    return base
# end card
def endcard():
    base=Image.fromarray(BG.astype(np.uint8)).convert('RGBA')
    im=cutimgs['purple']; im2=im.resize((430,int(im.height*430/im.width)),Image.LANCZOS)
    x=(W-im2.width)//2; y=385
    a=im2.split()[3]; sh=Image.new('RGBA',im2.size,(10,5,20,0)); sh.putalpha(a.point(lambda p:p*0.55))
    shl=layer(); shl.alpha_composite(sh,(x+8,y+30)); shl=shl.filter(ImageFilter.GaussianBlur(24))
    base.alpha_composite(shl); base.alpha_composite(im2,(x,y))
    return base
EC=endcard()
PRE=(MODE=='prelaunch'); oy=0 if PRE else -50
def ctr(d,y,tx,f,fill,sp=0):
    tw=spaced_w(d,tx,f,sp) if sp else d.textlength(tx,font=f)
    assert (W-tw)/2>=60, ('too wide',tx)
    if sp: spaced(d,((W-tw)/2,y),tx,f,fill,sp)
    else: d.text(((W-tw)/2,y),tx,font=f,fill=fill)
E1=layer(); d=ImageDraw.Draw(E1)
ctr(d,280,'MAGICIANS',CIN(34,700),CREAM,7); ctr(d,324,'ON THE GREEN',CIN(34,700),CREAM,7)
E2=layer(); d=ImageDraw.Draw(E2)
ctr(d,975,'WEAR THE',CIN(56,700),CREAM,7)
ctr(d,990,'Magic',ALL(190),GOLD)
E3=layer(); d=ImageDraw.Draw(E3)
ctr(d,1212,'THE M GOLF POLO',CIN(40,700),CREAM,4)
if PRE: ctr(d,1262,'COMING SOON',CIN(40,700),GOLD,6)
d.line(((W-120)/2,1330+oy,(W+120)/2,1330+oy),fill=GOLD,width=3)
for i,tx in enumerate(['10% of every purchase supports','LeMoyne-Owen golf.']): ctr(d,1352+oy+i*52,tx,FIG(40,500),CREAM)
E4=layer(); d=ImageDraw.Draw(E4)
for i,tx in enumerate(['Independent supporter brand.','Not an official LeMoyne-Owen College product.']): ctr(d,1470+oy+i*38,tx,FIG(29,500),CREAM+(200,))
SC_BOT=scrim(860,1480,amax=0.93); SC_TOP=scrim(0,470,top=True,amax=0.6)
# still close-up source
CL=Image.open(S+'gen/m1_logo.png').convert('RGB'); LX,LY=1281,1023
rng=np.random.default_rng(7)
def grade(img):
    a=np.asarray(img.convert('RGB')).astype(np.float32); r,g,b=a[...,0],a[...,1],a[...,2]
    m=(np.clip((b-g-25)/40,0,1)*np.clip((r-g)/30,0,1))[...,None]
    gd=a*1.36+np.array([10,18,8],np.float32)
    return Image.fromarray(np.clip(a*(1-m)+gd*m,0,255).astype(np.uint8)).convert('RGBA')
def push(img,cx,cy,cw):
    ch=cw*16/9; return img.resize((W,H),Image.LANCZOS,box=(cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2)).convert('RGBA')
def ease2(x): x=min(max(x,0),1); return x*x*(3-2*x)
def mix(a,b,k): return Image.blend(a,b,k)
def frame(i):
    t=i/FPS
    if t<B[1]:
        fr=grade(Image.fromarray(A[min(int(t*0.93*24),len(A)-1)]))
        fr.alpha_composite(SC_BOT); fr.alpha_composite(SC_TOP)
        fr.alpha_composite(L1); fr.alpha_composite(WM); fr=anim(fr,L1b,0.35,t)
    elif t<B[2]:
        u=(t-B[1])/(B[2]-B[1]); cw=980-380*ease(u*0.9); ch=cw*16/9
        cx=LX-cw*0.08; cy=LY+ch*0.24
        box=(cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2)
        fr=grade(CL.resize((W,H),Image.LANCZOS,box=box))
        fr.alpha_composite(SC_BOT); fr=anim(fr,L2,B[1]+0.2,t)
    elif t<B[3]:
        u=t-B[2]; FW=1792
        def front(u): return push(FRONT,FW/2,3186/2,FW*(1-0.06*ease2(u/1.0)))
        def turn(u):
            st=2.4+(u-1.0)*(0.35/0.5); return Image.fromarray(T[min(max(int(st*24),0),len(T)-1)]).convert('RGBA')
        def back(u):
            k=ease2((u-1.5)/2.0); cw=FW*(1-k)+600*k
            cx=FW/2*(1-k)+WX*k; cy=3186/2*(1-k)+(WY+170)*k
            return push(BACK,cx,cy,cw)
        if u<1.0: fr=front(u)
        elif u<1.5: fr=turn(u)
        else: fr=back(u)
        fr.alpha_composite(SC_BOT if u>1.9 else layer()); fr=anim(fr,L3,B[2]+2.2,t)
    elif t<B[4]:
        k=min(int((t-B[3])/((B[4]-B[3])/4)),3); tl=(t-B[3])-k*(B[4]-B[3])/4
        c,lab=COLS[k]; fr=shirt_frame(c,lab,0.97+0.03*ease(tl/0.7))
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
        '-i',V+'music1.mp3','-filter_complex','[1:a]atrim=0:17,afade=t=in:d=0.15,afade=t=out:st=16.3:d=0.7,loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.79:level=false[a]',
        '-map','0:v','-map','[a]','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-profile:v','high','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
        '-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-shortest',OUT],stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print('done',OUT)
