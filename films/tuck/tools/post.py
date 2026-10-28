import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SER="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
EP=os.environ.get("EP","1"); TITLE=os.environ.get("TITLE","Whoever Is Still Here"); HOOK=os.environ.get("HOOK","Who writes the letters?")
NEXT=os.environ.get("NEXT","Letter 2 tomorrow.")
raw=sys.argv[1]; W,H=1280,720
F=lambda p,s: ImageFont.truetype(p,s)
def sh(d,xy,txt,font,fill,anchor="mm"): d.text(xy,txt,font=font,fill=fill,anchor=anchor,stroke_width=3,stroke_fill=(5,6,12))
# opening overlay (transparent png) shown 1.0-4.5s
ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
sh(d,(60,H-110),"TUCK",F(SER,64),(243,234,216),"ls"); sh(d,(62,H-62),f"Letter {EP}: {TITLE}",F(SANS,30),(224,167,62),"ls")
ov.save("ov_open.png")
# end card 6s
ec=Image.new("RGB",(W,H),(8,10,18)); d=ImageDraw.Draw(ec)
d.text((W//2,250),"TUCK",font=F(SER,120),fill=(243,234,216),anchor="mm")
d.text((W//2,345),f"Letter {EP}: {TITLE}",font=F(SANS,34),fill=(224,167,62),anchor="mm")
d.text((W//2,460),HOOK,font=F(SER,46),fill=(243,234,216),anchor="mm")
d.text((W//2,560),NEXT,font=F(SANS,30),fill=(170,175,200),anchor="mm")
d.text((W//2,660),"TremenVR",font=F(MONO,24),fill=(120,125,150),anchor="mm")
ec.save("endcard.png")
def run(a): subprocess.run(a,check=True)
run(["ffmpeg","-y","-loglevel","error","-loop","1","-t","6","-i","endcard.png","-f","lavfi","-t","6","-i","anullsrc=r=44100:cl=stereo",
     "-vf","fps=24,format=yuv420p,fade=t=in:st=0:d=0.8","-c:v","libx264","-crf","18","-c:a","aac","-shortest","end.mp4"])
run(["ffmpeg","-y","-loglevel","error","-i",raw,"-i","ov_open.png",
     "-filter_complex","[0:v]fps=24,scale=1280:720,fade=t=in:st=0:d=1.0[b];[b][1:v]overlay=0:0:enable='between(t,1,4.5)',format=yuv420p[v]",
     "-map","[v]","-c:v","libx264","-crf","18","-preset","slow","body.mp4"])
run(["ffmpeg","-y","-loglevel","error","-i","body.mp4","-i","end.mp4","-filter_complex","[0:v][1:v]concat=n=2:v=1:a=0[v]","-map","[v]","-c:v","libx264","-crf","18","-preset","slow","video.mp4"])
run(["ffmpeg","-y","-loglevel","error","-i","video.mp4","-i","sound.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",f"tuck_ep{int(EP):02d}_16x9.mp4"])
# vertical: blurred bg + film centred + texts
top=Image.new("RGBA",(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(top)
sh(d,(540,330),"TUCK",F(SER,110),(243,234,216)); sh(d,(540,430),f"Letter {EP}",F(SANS,46),(224,167,62))
sh(d,(540,1500),HOOK,F(SER,58),(243,234,216)); sh(d,(540,1590),"Watch every letter. Follow.",F(SANS,38),(190,195,215))
top.save("ov_vert.png")
run(["ffmpeg","-y","-loglevel","error","-i",f"tuck_ep{int(EP):02d}_16x9.mp4","-i","ov_vert.png","-filter_complex",
     "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.15[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2[m];[m][1:v]overlay=0:0,format=yuv420p[v]",
     "-map","[v]","-map","0:a","-c:v","libx264","-crf","20","-preset","slow","-c:a","copy","-movflags","+faststart",f"tuck_ep{int(EP):02d}_9x16.mp4"])
print("done")
