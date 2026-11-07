import numpy as np
from PIL import Image
from scipy import ndimage
A='perf/'
for c in ['purple','black','white','lightgray']:
  for v in ['front','back']:
    im=Image.open(f'{A}m-golf-polo-{c}-ghost-{v}.jpg').convert('RGB'); a=np.asarray(im).astype(int)
    near=(a.min(2)>=247)&((a.max(2)-a.min(2))<8)
    lab,n=ndimage.label(near)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bg=np.isin(lab,list(border))
    # background trapped under the hem (between front and back hem curves)
    Hh=a.shape[0]
    for i,sl in enumerate(ndimage.find_objects(lab),1):
        if sl is not None and sl[0].start>Hh*0.82 and (lab[sl]==i).sum()>200: bg|=lab==i
    if c in ('purple','black'):
        # the photo's soft hem shadow: bright, colorless pixels belong to the background
        shadow=(a.min(2)>=200)&((a.max(2)-a.min(2))<14)
        bg|=shadow
    fg=~bg
    fg=ndimage.binary_fill_holes(fg)
    fg=ndimage.binary_opening(fg,iterations=2)
    alpha=ndimage.gaussian_filter(ndimage.binary_erosion(fg,iterations=1).astype(float),1.0)
    out=np.dstack([a,(alpha*255)]).astype('uint8')
    o=Image.fromarray(out,'RGBA'); o=o.crop(o.getbbox()); o.save(f'cut/{c}-{v}.png')
    print(c,v,o.size)
