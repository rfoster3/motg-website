import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
A='/Users/ronniefoster/motg-website/assets/'
def place(img,cx,cy,w):
    lg=Image.open(A+'logo-m.png').convert('RGBA'); lg=lg.crop(lg.getbbox())
    h=int(lg.height*w/lg.width); lg=lg.resize((w,h),Image.LANCZOS)
    x,y=cx-lg.width//2,cy-lg.height//2
    base=np.asarray(img.convert('RGB')).astype(float)
    region=base[y:y+lg.height,x:x+lg.width]
    lum=region.mean(axis=2)
    blur=np.asarray(Image.fromarray(lum.astype('uint8')).filter(ImageFilter.GaussianBlur(25))).astype(float)+1
    shade=np.clip(lum/blur,0.86,1.12)[...,None]
    arr=np.asarray(lg).astype(float); a=arr[...,3:]/255
    sh=Image.fromarray(arr[...,3].astype('uint8')).filter(ImageFilter.GaussianBlur(2))
    sa=(np.asarray(sh).astype(float)/255)[...,None]*0.22
    out=region*(1-sa); out=out*(1-a)+arr[...,:3]*shade*a
    base[y:y+lg.height,x:x+lg.width]=out
    return Image.fromarray(np.clip(base,0,255).astype('uint8'))
def erase(im, box=(985,535,1245,745), dy=190):
    a=np.asarray(im.convert('RGB')).astype(float)
    x0,y0,x1,y1=box; r=a[y0:y1,x0:x1]
    med=np.median(r.reshape(-1,3),axis=0)
    m=np.zeros(a.shape[:2],bool); m[y0:y1,x0:x1]=np.abs(r-med).sum(2)>110
    m=ndimage.binary_opening(m,iterations=1)
    m=ndimage.binary_dilation(m,iterations=14)
    feather=ndimage.gaussian_filter(m.astype(float),5)[...,None]
    src=np.roll(a,-dy,axis=0)
    def lowpass(img,mask,sig=28):
        w=(~mask).astype(float)
        num=np.stack([ndimage.gaussian_filter(img[...,k]*w,sig) for k in range(3)],-1)
        return num/(ndimage.gaussian_filter(w,sig)[...,None]+1e-6)
    srcmask=np.roll(m,-dy,axis=0)&False
    hp=src-lowpass(src,srcmask)
    fill=lowpass(a,m)+hp
    out=a*(1-feather)+fill*feather
    return Image.fromarray(np.clip(out,0,255).astype('uint8'))
for c in ['purple','black','white','lightgray']:
    p=A+f'polo/m-golf-polo-{c}-ghost-front.jpg'; dy=300 if c=='purple' else 190
    im=Image.open(p); clean=erase(im,dy=dy)
    clean.save(f'out/{c}-clean.png')
    new=place(clean,1114,623,124)
    new.save(f'out/m-golf-polo-{c}-ghost-front.jpg',quality=93)
    new.crop((850,350,1400,900)).save(f'out/{c}-crop.png')
    clean.crop((850,350,1400,900)).save(f'out/{c}-cleancrop.png')
print('done')
