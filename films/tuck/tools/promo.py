# Ad short (9:16, 15-30 s) cut from a finished episode. Cloud only, no PC needed.
# usage: EP=1 HOOK="Who writes the letters?" SEGS="12-16,20-23,46-56,64-68" python3 promo.py tuck_ep01_16x9.mp4
# SEGS = seconds in the 16x9 final video (pick: a close-up of Tuck's eye, the letter text, the scary/big
# moment, the emotional end). Never show the very last reveal. Output: tuck_promo_epNN.mp4
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont
SER="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
EP=int(os.environ.get("EP","1")); HOOK=os.environ.get("HOOK","Who writes the letters?")
SEGS=[tuple(map(float,s.split("-"))) for s in os.environ["SEGS"].split(",")]
src=sys.argv[1]; F=lambda p,s: ImageFont.truetype(p,s)
def run(a): subprocess.run(a,check=True)
def sh(d,xy,t,f,fill): d.text(xy,t,font=f,fill=fill,anchor="mm",stroke_width=4,stroke_fill=(5,6,12))
def wrap(t,n=18):
    w=t.split(); L=[""]
    for x in w:
        if len(L[-1])+len(x)+1>n and L[-1]: L.append(x)
        else: L[-1]=(L[-1]+" "+x).strip()
    return L
top=Image.new("RGBA",(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(top)
for i,l in enumerate(wrap(HOOK)): sh(d,(540,300+i*95),l,F(SER,78),(243,234,216))
sh(d,(540,1520),"Full story on YouTube",F(SANS,52),(224,167,62)); sh(d,(540,1600),"TUCK  -  Letter %d"%EP,F(SANS,40),(200,205,220))
top.save("p_top.png")
end=Image.new("RGB",(1080,1920),(8,10,18)); d=ImageDraw.Draw(end)
d.text((540,760),"TUCK",font=F(SER,170),fill=(243,234,216),anchor="mm")
d.text((540,900),"Letter %d"%EP,font=F(SANS,56),fill=(224,167,62),anchor="mm")
for i,l in enumerate(wrap(HOOK)): d.text((540,1060+i*80),l,font=F(SER,64),fill=(243,234,216),anchor="mm")
d.text((540,1330),"Watch the full story on YouTube",font=F(SANS,44),fill=(190,195,215),anchor="mm")
d.text((540,1410),"@TremenVR",font=F(SANS,44),fill=(224,167,62),anchor="mm")
end.save("p_end.png")
parts=[]
for i,(a,b) in enumerate(SEGS):
    o="p_seg%d.mp4"%i; dur=b-a
    run(["ffmpeg","-y","-loglevel","error","-ss",str(a),"-t",str(dur),"-i",src,"-i","p_top.png","-filter_complex",
        "[0:v]fps=24,split[x][y];[x]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.2[bg];"
        "[y]scale=1440:-2,crop=1080:ih[fg];[bg][fg]overlay=0:(H-h)/2[m];[m][1:v]overlay=0:0,format=yuv420p,"
        "fade=t=in:st=0:d=0.15,fade=t=out:st=%f:d=0.15[v];[0:a]afade=t=in:st=0:d=0.1,afade=t=out:st=%f:d=0.15[au]"%(dur-0.15,dur-0.15),
        "-map","[v]","-map","[au]","-c:v","libx264","-crf","20","-preset","medium","-c:a","aac","-ar","44100","-ac","2",o])
    parts.append(o)
run(["ffmpeg","-y","-loglevel","error","-loop","1","-t","3","-i","p_end.png","-f","lavfi","-t","3","-i","anullsrc=r=44100:cl=stereo",
     "-vf","fps=24,format=yuv420p,fade=t=in:st=0:d=0.3","-c:v","libx264","-crf","20","-c:a","aac","-shortest","p_end.mp4"])
parts.append("p_end.mp4")
inp=[]; [inp.extend(["-i",p]) for p in parts]; n=len(parts)
run(["ffmpeg","-y","-loglevel","error",*inp,"-filter_complex","".join("[%d:v]setsar=1[v%d];"%(i,i) for i in range(n))+"".join("[v%d][%d:a]"%(i,i) for i in range(n))+"concat=n=%d:v=1:a=1[v][a]"%n,
     "-map","[v]","-map","[a]","-c:v","libx264","-crf","20","-preset","slow","-c:a","aac","-b:a","160k","-movflags","+faststart","tuck_promo_ep%02d.mp4"%EP])
print("done tuck_promo_ep%02d.mp4"%EP)
