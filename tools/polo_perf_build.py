import sys; sys.argv=['x']; sys.path.insert(0,'.')
import numpy as np
from PIL import Image
from scipy import ndimage
exec(open('shrink.py').read().split('def erase')[0])      # place()
from embroider import embroider
from placew import place_w
P='/Users/ronniefoster/motg-website/assets/polo/'
def mask_of(a):
    near=(a.min(2)>=240)&((a.max(2)-a.min(2))<12)
    lab,n=ndimage.label(near)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bg=np.isin(lab,list(border))
    H=a.shape[0]
    for i,sl in enumerate(ndimage.find_objects(lab),1):
        if sl is not None and sl[0].start>H*0.8 and (lab[sl]==i).sum()>200: bg|=lab==i
    return ndimage.binary_opening(ndimage.binary_fill_holes(~bg),iterations=2)
def geom(m):
    ys,xs=np.where(m); top=ys.min()
    H=m.shape[0]; row=int(top+0.56*(ys.max()-top))
    r=np.where(m[row])[0]
    # torso only: longest run around center
    runs=np.split(r,np.where(np.diff(r)>1)[0]+1); run=max(runs,key=len)
    return top,(run[0]+run[-1])/2,run[-1]-run[0]
def ref_geom(path,logo_xy,logo_w):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int); m=mask_of(a)
    top,cx,tw=geom(m); return ((logo_xy[0]-cx)/tw,(logo_xy[1]-top)/tw,logo_w/tw)
# reference proportions from the current approved product images
RF=ref_geom(P+'m-golf-polo-purple-ghost-front.jpg',(1114,623),124)
RB=ref_geom(P+'m-golf-polo-purple-ghost-back.jpg',(895,362),180)
print('ref front',RF,'ref back',RB)
TARGET={'purple':(98,53,155),'black':(27,27,28),'white':(233,235,242),'lightgray':(221,223,222)}
GAM={'purple':1.0,'black':1.0,'white':0.55,'lightgray':0.7}
rng=np.random.default_rng(7)
for view,src,R in [('front','gen/fab1.png',RF),('back','gen/bk0.png',RB)]:
    im=Image.open(src).convert('RGB').resize((1792,2240),Image.LANCZOS)
    a=np.asarray(im).astype(float); m=mask_of(a.astype(int))
    alpha=ndimage.gaussian_filter(m.astype(float),1.0)[...,None]
    Y=a@[0.299,0.587,0.114]
    top,cx,tw=geom(m); print(view,'geom',top,cx,tw)
    ys,xs=np.where(m); chest=Y[int(top+0.35*(ys.max()-top)):int(top+0.6*(ys.max()-top)), int(cx-tw*0.3):int(cx+tw*0.3)]
    s=Y/np.median(chest)
    # take shading from the interior only, then extend it to the anti-aliased edge
    inner=ndimage.binary_erosion(m,iterations=4)
    idx=ndimage.distance_transform_edt(~inner,return_distances=False,return_indices=True)
    s=s[idx[0],idx[1]]
    LIM={'purple':(0.55,1.6),'black':(0.5,2.2),'white':(0.8,1.3),'lightgray':(0.75,1.35)}
    for c,t in TARGET.items():
        lo,hi=LIM[c]; sc=np.clip(s,lo,hi)
        t=np.array(t,float); light=t+(255-t)*0.45
        dark=t*np.clip(sc,0,1)[...,None]**GAM[c]
        up=np.clip((sc-1)/(hi-1),0,1)[...,None]
        col=np.where(sc[...,None]>1, t+(light-t)*up, dark)
        col=col+rng.normal(0,1.2,col.shape)          # faint knit grain
        out=a*(1-alpha)+np.clip(col,0,255)*alpha
        out=np.where(alpha>0.001,out,255.0)
        img=Image.fromarray(np.clip(out,0,255).astype('uint8'))
        lx=int(cx+R[0]*tw); ly=int(top+R[1]*tw); lw=int(R[2]*tw)
        if view=='front': img=embroider(img,lx,ly,lw,light=(-1,-1))
        else:
            img=place_w(img,lx,ly,lw)
        img.save(f'perf/m-golf-polo-{c}-ghost-{view}.jpg',quality=94)
