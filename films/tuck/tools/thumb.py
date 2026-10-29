# YouTube thumbnail (1280x720 jpg) from a frame of the finished 16x9 episode.
# usage: EP=2 HOOK="Who sleeps under the bridge?" T=37.5 python3 thumb.py tuck_ep02_16x9.mp4
# SHIFT = px the frame is moved right so the subject sits right of the text (default 380).
# T = second with a big clear Tuck face / eye or the scary moment (look at a contact sheet first).
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
SER="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
EP=int(os.environ.get("EP","1")); HOOK=os.environ.get("HOOK",""); T=os.environ.get("T","10")
src=sys.argv[1]; F=lambda p,s: ImageFont.truetype(p,s)
subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",T,"-i",src,"-frames:v","1","th_src.png"],check=True)
fr=Image.open("th_src.png").convert("RGB").resize((1280,720)); SH=int(os.environ.get("SHIFT","380"))
im=Image.new("RGB",(1280,720),(5,6,12)); im.paste(fr,(SH,0))
im=ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(1.25)).enhance(1.25)
# dark band on the left for text
band=Image.new("L",(1280,720),0); bd=ImageDraw.Draw(band)
for x in range(SH+260): bd.line([(x,0),(x,720)],fill=int(255*max(0,min(1,(SH+260-x)/260))))
im.paste(Image.new("RGB",(1280,720),(5,6,12)),(0,0),band)
d=ImageDraw.Draw(im)
def sh(xy,t,f,fill): d.text(xy,t,font=f,fill=fill,stroke_width=6,stroke_fill=(5,6,12))
words=HOOK.split(); lines=[""]
for w in words:
    if len(lines[-1])+len(w)+1>13 and lines[-1]: lines.append(w)
    else: lines[-1]=(lines[-1]+" "+w).strip()
sz=96 if len(lines)<=3 else 78
y=360-len(lines)*sz//2
for l in lines: sh((50,y),l,F(SER,sz),(243,234,216)); y+=sz+8
sh((52,40),"TUCK",F(SER,64),(224,167,62)); sh((52,620),"Letter %d"%EP,F(SANS,48),(243,234,216))
im.save("tuck_thumb_ep%02d.jpg"%EP,quality=92); print("done tuck_thumb_ep%02d.jpg"%EP)
