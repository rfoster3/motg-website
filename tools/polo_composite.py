import sys
from PIL import Image, ImageFilter, ImageChops
import numpy as np
A='/Users/rfj/motg-website/assets/'
LOGO={'m':A+'logo-m.png','wiz':A+'wizard-mascot.png'}
def place(img,kind,cx,cy,w,rot=0):
    lg=Image.open(LOGO[kind]).convert('RGBA'); lg=lg.crop(lg.getbbox())
    h=int(lg.height*w/lg.width); lg=lg.resize((w,h),Image.LANCZOS)
    if rot: lg=lg.rotate(rot,Image.BICUBIC,expand=True)
    x,y=cx-lg.width//2,cy-lg.height//2
    base=np.asarray(img.convert('RGB')).astype(float)
    region=base[y:y+lg.height,x:x+lg.width]
    lum=region.mean(axis=2)
    blur=np.asarray(Image.fromarray(lum.astype('uint8')).filter(ImageFilter.GaussianBlur(25))).astype(float)+1
    shade=np.clip(lum/blur,0.86,1.12)[...,None]
    arr=np.asarray(lg).astype(float); a=arr[...,3:]/255
    # soft thread shadow under the patch
    sh=Image.fromarray(arr[...,3].astype('uint8')).filter(ImageFilter.GaussianBlur(2))
    sa=(np.asarray(sh).astype(float)/255)[...,None]*0.22
    out=region*(1-sa); out=out*(1-a)+arr[...,:3]*shade*a
    base[y:y+lg.height,x:x+lg.width]=out
    return Image.fromarray(np.clip(base,0,255).astype('uint8'))
JOBS=[l.split() for l in open(sys.argv[1]) if l.strip()]
for f,kind,cx,cy,w,rot in JOBS:
    im=place(Image.open(f'gen/{f}.png'),kind,int(cx),int(cy),int(w),float(rot))
    im.save(f'final/{f}.png'); 
