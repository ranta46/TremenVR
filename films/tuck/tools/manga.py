# One manga page (black/white, screentone) per episode, from frames of the finished 16x9 video.
# usage: python3 manga.py spec.json tuck_epNN_16x9.mp4
# spec.json = {"ep":2,"title":"The Last Lamp","panels":[8 items]}  each panel:
#   {"t":12.5, "crop":[x0,y0,x1,y1] (optional, in 1280x720), "gamma":0.6 (lower = brighter),
#    "caption":"text" (optional, box top-left), "sfx":"BOOM" (optional), "bubble":"beep..." (optional)}
# Layout (8 panels): wide | half half | wide-left narrow-right | wide | half half(tall).
# Never use t between 1.0 and 4.5 s (title overlay) or after the film ends (end card).
# Pick panels that tell the episode in order; last panel = a quiet question, not the final answer.
# Output: tuck_manga_epNN.png (1600x2400, 2:3 for Pinterest/Threads/Bluesky/Facebook)
#         tuck_manga_epNN_ig.jpg (1920x2400, 4:5 for Instagram)
import json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
spec=json.load(open(sys.argv[1])); src=sys.argv[2]; EP=int(spec["ep"])
W,H=1600,2400; M=40; G=22
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; SER="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F=lambda p,s: ImageFont.truetype(p,s)
def grab(t,i):
    p="mg_%d.png"%i; subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(t),"-i",src,"-frames:v","1","-vf","scale=1280:720",p],check=True); return p
def manga(img,size,crop=None,gamma=1.0):
    im=Image.open(img).convert("RGB")
    if crop: im=im.crop(tuple(crop))
    im=ImageOps.fit(im,size,Image.LANCZOS)
    g=np.asarray(im.convert("L"),dtype=np.float32)/255.0
    g=np.clip((g-g.min())/(max(1e-3,np.percentile(g,99.5)-g.min())),0,1)**gamma
    e=np.asarray(Image.fromarray((g*255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES),dtype=np.float32)/255.0
    h,w=g.shape; yy,xx=np.mgrid[0:h,0:w]
    p=6; cx=(xx%p)-p/2+0.5; cy=(yy%p)-p/2+0.5; d=np.sqrt(cx*cx+cy*cy)/(p*0.7)
    tone=(d>(1-g)*0.95).astype(np.float32)
    out=np.where(g<0.07,0.0,np.where(g>0.62,1.0,tone)); out=np.where(e>0.22,0.0,out)
    return Image.fromarray((out*255).astype(np.uint8)).convert("RGB")
page=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(page)
def caption(xy,txt,size=34):
    f=F(SER,size); b=d.multiline_textbbox(xy,txt,font=f); pad=14
    d.rectangle((b[0]-pad,b[1]-pad,b[2]+pad,b[3]+pad),fill="white",outline="black",width=4); d.multiline_text(xy,txt,font=f,fill="black")
def sfx(xy,txt,size=84,rot=6):
    f=F(BOLD,size); tmp=Image.new("RGBA",(1000,300),(0,0,0,0)); td=ImageDraw.Draw(tmp)
    td.text((20,20),txt,font=f,fill="black",stroke_width=8,stroke_fill="white"); tmp=tmp.rotate(rot,expand=True); page.paste(tmp,xy,tmp)
def bubble(xy,txt,tail,size=36):
    f=F(BOLD,size); b=d.multiline_textbbox(xy,txt,font=f,align="center"); pad=26
    e=(b[0]-pad-10,b[1]-pad,b[2]+pad+10,b[3]+pad); cx,cy=(e[0]+e[2])//2,e[3]-8
    d.polygon([(cx-22,cy),(cx+22,cy),tail],fill="white",outline="black"); d.line([(cx-22,cy),tail,(cx+22,cy)],fill="black",width=5)
    d.ellipse(e,fill="white",outline="black",width=5); d.multiline_text(xy,txt,font=f,fill="black",align="center")
hs=[400,400,400,440,520]; r=[M]
for h in hs: r.append(r[-1]+h+G)
mid=W//2
boxes=[(M,r[0],W-M,r[0]+hs[0]),(M,r[1],mid-G//2,r[1]+hs[1]),(mid+G//2,r[1],W-M,r[1]+hs[1]),
       (M,r[2],mid+180,r[2]+hs[2]),(mid+180+G,r[2],W-M,r[2]+hs[2]),(M,r[3],W-M,r[3]+hs[3]),
       (M,r[4],mid-G//2,r[4]+hs[4]),(mid+G//2,r[4],W-M,r[4]+hs[4])]
P=spec["panels"]; assert len(P)==8, "need 8 panels"
for i,(pn,box) in enumerate(zip(P,boxes)):
    x0,y0,x1,y1=box; page.paste(manga(grab(pn["t"],i),(x1-x0,y1-y0),pn.get("crop"),pn.get("gamma",0.6)),(x0,y0)); d.rectangle(box,outline="black",width=7)
for i,(pn,box) in enumerate(zip(P,boxes)):
    x0,y0,x1,y1=box
    if pn.get("sfx"): sfx((x0+30,y0+20),pn["sfx"],96 if x1-x0>1000 else 72,6 if i%2 else -5)
    if pn.get("bubble"): bubble((x0+(x1-x0)//2-120,y0+50),pn["bubble"],(x0+(x1-x0)//2,y0+230))
    if pn.get("caption"): caption((x0+28,y1-40-38*(pn["caption"].count("\n")+1)),pn["caption"],34)
d.text((W//2,r[5]+30),"TUCK  -  Letter %d: %s"%(EP,spec["title"]),font=F(SER,34),fill="black",anchor="mm")
page.save("tuck_manga_ep%02d.png"%EP)
ig=Image.new("RGB",(1920,2400),"white"); ig.paste(page,(160,0)); ig.save("tuck_manga_ep%02d_ig.jpg"%EP,quality=92)
print("done tuck_manga_ep%02d.png"%EP)
