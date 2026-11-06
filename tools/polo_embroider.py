import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
LOGO='/Users/ronniefoster/motg-website/assets/logo-m.png'
def embroider(img, cx, cy, w, light=(-1,-1), rot=0):
    S=3  # supersample
    lg=Image.open(LOGO).convert('RGBA'); lg=lg.crop(lg.getbbox())
    W=w*S; H=int(lg.height*W/lg.width); lg=lg.resize((W,H),Image.LANCZOS)
    a=np.asarray(lg).astype(float); rgb=a[...,:3]; al=a[...,3]/255
    # thread colors: snap every pixel to a small set of solid thread fills
    PAL=np.array([(36,20,58),(58,31,102),(104,66,160),(201,162,75),(238,236,230)],float)
    d2=((rgb[...,None,:]-PAL[None,None])**2).sum(-1)
    rgb=PAL[d2.argmin(-1)]
    # matte: knock down gloss and specular highlights
    lum=rgb.mean(2,keepdims=True)
    rgb=np.where(lum>200, 200+(rgb-200)*0.45, rgb)
    rgb=rgb*0.93
    # flatten the glossy ball into white thread
    sat=rgb.max(2)-rgb.min(2); ball=(rgb.mean(2)>150)&(sat<40)
    bm=ndimage.gaussian_filter(ball.astype(float),1.0)[...,None]
    rgb=rgb*(1-bm)+(np.array([228,226,222])*(0.92+0.08*rgb.mean(2,keepdims=True)/255))*bm
    # satin stitch texture: fine diagonal threads (~1.6px period at final size)
    yy,xx=np.mgrid[0:H,0:W]
    period=2.0*S
    tex=0.5+0.5*np.sin((xx+yy)*0.7071*2*np.pi/period)
    tex=ndimage.gaussian_filter(tex,0.6)
    rgb=rgb*(0.84+0.30*tex[...,None])
    # raised edge: highlight on light-facing edge, shade on the other
    am=ndimage.gaussian_filter(al,1.8*S)
    gy,gx=np.gradient(am)
    lx,ly=light; n=np.hypot(lx,ly); lx,ly=lx/n,ly/n
    face=-(gx*lx+gy*ly)  # positive where edge faces the light
    face=face/ (np.abs(face).max()+1e-6)
    rgb=rgb*(1+0.10*face[...,None])
    rgb=np.clip(rgb,0,255)
    out=Image.fromarray(np.dstack([rgb,al*255]).astype('uint8'),'RGBA')
    if rot: out=out.rotate(rot,Image.BICUBIC,expand=True)
    out=out.resize((out.width//S,out.height//S),Image.LANCZOS)
    out=out.filter(ImageFilter.GaussianBlur(0.45))
    arr=np.asarray(out).astype(float); al=arr[...,3:]/255
    x,y=cx-out.width//2, cy-out.height//2
    base=np.asarray(img.convert('RGB')).astype(float)
    reg=base[y:y+out.height,x:x+out.width]
    # take on the fabric's local light (folds and falloff)
    l=reg.mean(2); blur=ndimage.gaussian_filter(l,18)+1
    shade=np.clip(l/blur,0.85,1.12)[...,None]
    big=ndimage.gaussian_filter(base.mean(2),60)
    ref=np.median(big[max(0,y-200):y+out.height+200, max(0,x-200):x+out.width+200])
    tone=np.clip(big[y:y+out.height,x:x+out.width]/ref,0.85,1.1)[...,None]
    # soft contact shadow, offset away from light
    sh=ndimage.shift(arr[...,3],( -ly*1, -lx*1 )); sh=ndimage.gaussian_filter(sh,0.8)/255
    reg=reg*(1-0.25*sh[...,None])
    col=arr[...,:3]*shade*tone
    col=col+np.random.default_rng(1).normal(0,3.5,col.shape)
    reg=reg*(1-al)+col*al
    base[y:y+out.height,x:x+out.width]=reg
    return Image.fromarray(np.clip(base,0,255).astype('uint8'))
