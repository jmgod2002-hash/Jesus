import sys, numpy as np, cv2, potrace
img = cv2.imread(sys.argv[1])[:, :, ::-1].astype(int)  # RGB
H, W = img.shape[:2]; print("size", W, H)
R,G,B = img[...,0],img[...,1],img[...,2]
orange = (R>200)&(G>60)&(G<150)&(B<110)
white = (R>220)&(G>220)&(B>220)
purple = (B>120)&(R<140)&(G<110)
yy,xx=np.mgrid[0:H,0:W]; inside=(xx-626.5)**2+(yy-623.5)**2 < 595**2
white&=inside
for n,m in [("orange",orange),("white",white),("purple",purple)]:
    c = img[m].mean(0) if m.any() else None
    print(n, m.sum(), np.round(c).astype(int), '#%02x%02x%02x'%tuple(np.round(c).astype(int)))
ys,xs=np.nonzero(purple|orange); print("disc bbox",xs.min(),xs.max(),ys.min(),ys.max())
def trace(mask, name):
    m = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    m = cv2.medianBlur(m*255, 9) > 127
    bm = potrace.Bitmap(m)
    plist = bm.trace(turdsize=400, alphamax=1.2, opticurve=True, opttolerance=0.4)
    d=[]
    for curve in plist:
        s=curve.start_point; d.append(f"M{s.x:.1f} {s.y:.1f}")
        for seg in curve.segments:
            if seg.is_corner: d.append(f"L{seg.c.x:.1f} {seg.c.y:.1f}L{seg.end_point.x:.1f} {seg.end_point.y:.1f}")
            else: d.append(f"C{seg.c1.x:.1f} {seg.c1.y:.1f} {seg.c2.x:.1f} {seg.c2.y:.1f} {seg.end_point.x:.1f} {seg.end_point.y:.1f}")
        d.append("Z")
    print(name, len(plist), "curves"); open(name+".d","w").write("".join(d))
trace(orange|white, "t_shape")   # silhouette du T (œil compris)
trace(white, "eye_white")
