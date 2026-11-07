import numpy as np
from PIL import Image, ImageFilter
def place_w(img,cx,cy,w):
    lg=Image.open('/Users/ronniefoster/motg-website/assets/wizard-mascot.png').convert('RGBA'); lg=lg.crop(lg.getbbox())
    h=int(lg.height*w/lg.width); lg=lg.resize((w,h),Image.LANCZOS)
    x,y=cx-lg.width//2,cy-lg.height//2
    base=np.asarray(img.convert('RGB')).astype(float)
    region=base[y:y+lg.height,x:x+lg.width]; lum=region.mean(axis=2)
    blur=np.asarray(Image.fromarray(lum.astype('uint8')).filter(ImageFilter.GaussianBlur(25))).astype(float)+1
    shade=np.clip(lum/blur,0.86,1.12)[...,None]
    arr=np.asarray(lg).astype(float); a=arr[...,3:]/255
    sh=Image.fromarray(arr[...,3].astype('uint8')).filter(ImageFilter.GaussianBlur(2))
    sa=(np.asarray(sh).astype(float)/255)[...,None]*0.22
    out=region*(1-sa); out=out*(1-a)+arr[...,:3]*shade*a
    base[y:y+lg.height,x:x+lg.width]=out
    return Image.fromarray(np.clip(base,0,255).astype('uint8'))
