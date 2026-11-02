from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage as ni
TARGET=214.
def torso(a,box): x0,y0,x1,y1=box; return np.median(a[y0:y1,x0:x1].mean(axis=2))
for f,seed in [('lightgray_ghost_front',(896,1200)),('lightgray_ghost_back',(896,1200)),('lightgray_model_front',(760,1100)),('lightgray_model_back',(900,1100))]:
    im=Image.open(f'gen/{f}.png').convert('RGB'); a=np.asarray(im).astype(float)
    s=a.max(axis=2)-a.min(axis=2); l=a.mean(axis=2)
    m=(s<26)&(l>95)
    if 'ghost' in f: m&=(l<250)
    lab,_=ni.label(ni.binary_closing(m,iterations=3)); seedv=lab[seed[1],seed[0]]; print(f,'seed',seedv,'torso',round(float(l[seed[1]-60:seed[1]+60,seed[0]-60:seed[0]+60].mean())))
    mask=lab==seedv; mask=ni.binary_fill_holes(mask)
    k=TARGET/np.median(l[mask])
    al=np.asarray(Image.fromarray((mask*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.5))).astype(float)[...,None]/255
    o=a*(1-al)+np.clip(a*k,0,255)*al
    Image.fromarray(o.astype('uint8')).save(f'gen/{f}.png'); print(' k',round(k,3),'mask%',round(mask.mean()*100,1))
