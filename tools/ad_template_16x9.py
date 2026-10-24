import glob, os, sys, subprocess, numpy as np, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FR=os.environ.get("FRAMES","frames"); OUT=os.environ.get("OUTDIR","ad_out"); os.makedirs(OUT,exist_ok=True)
W,H=1920,1080; FPS=30
SER="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
def F(p,s): return ImageFont.truetype(p,s)
files=sorted(glob.glob(FR+"/f*.jpg")); idx={int(os.path.basename(f)[1:6]):f for f in files}
def rng(a,b): return [idx[i] for i in range(int(a*30),int(b*30)) if i in idx]
# segments: (frames, overlay text)
SEG=[(rng(69.8,74.6),"If it looks at you... don't move."),
     (rng(2.0,6.2),"Keep the lights on."),
     (rng(8,12),"Look at a lamp to light it."),
     (rng(14,20.5),"Something eats the light."),
     (rng(75,86),"Bring the last train home.")]
URL="ranta46.github.io/TremenVR"
def shadow_text(d,xy,txt,font,fill,anchor="mm",sw=6):
    d.text(xy,txt,font=font,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill=(8,6,12))
def wrap(txt,font,maxw,d):
    words=txt.split();lines=[];cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur);cur=w
    lines.append(cur);return lines
n=0
def put(im):
    global n; im.convert("RGB").save(f"{OUT}/o{n:05d}.jpg",quality=92); n+=1
gold=(224,167,62); paper=(243,234,216)
# hook badge on every footage frame
for si,(fs,txt) in enumerate(SEG):
    for k,f in enumerate(fs):
        im=Image.open(f).convert("RGB").resize((W,H)); d=ImageDraw.Draw(im)
        # top-left brand
        shadow_text(d,(60,60),"PLAY FREE · NO APP · LINK BELOW",F(MONO,34),gold,"lm",4)
        a=min(1,k/8)
        if a>0:
            fnt=F(SER,80); lines=wrap(txt,fnt,1600,d); y=900-len(lines)*45
            for L in lines: shadow_text(d,(W//2,y),L,fnt,paper); y+=92
        put(im)
# end card over blurred last frame
base=Image.open(SEG[-1][0][-1]).convert("RGB").resize((W,H)).filter(ImageFilter.GaussianBlur(14))
base=Image.blend(base,Image.new("RGB",(W,H),(10,8,16)),0.45)
for k in range(int(4.5*FPS)):
    im=base.copy(); d=ImageDraw.Draw(im)
    shadow_text(d,(W//2,190),"TREMENVR · WORK 01",F(MONO,40),gold)
    shadow_text(d,(W//2+170,330),"The Signal",F(SER,120),paper,"rm"); shadow_text(d,(W//2+200,330),"Tower",F(SER,120),gold,"lm")
    shadow_text(d,(W//2,500),"Play it now. Free.",F(SER,70),paper)
    shadow_text(d,(W//2,590),"Phone · PC · VR headset",F(SER,48),(190,180,205))
    d.rounded_rectangle((460,690,1460,830),radius=28,fill=gold)
    d.text((W//2,760),URL,font=F(MONO,52),fill=(27,18,6),anchor="mm")
    shadow_text(d,(W//2,920),"Link in the description",F(SER,50),paper)
    put(im)
total=n/FPS; print("frames",n,"sec",round(total,1))
# soundtrack
SR=44100; N=int(total*SR); t=np.arange(N)/SR; mix=np.zeros(N)
rngn=np.random.default_rng(3)
def add(sig,t0,g=1.0):
    i=int(t0*SR); sig=sig[:max(0,N-i)]; mix[i:i+len(sig)]+=sig*g
def tone(f,dur,dec=3.0,typ="tri"):
    tt=np.arange(int(dur*SR))/SR; ph=2*np.pi*f*tt
    s=(2/np.pi)*np.arcsin(np.sin(ph)) if typ=="tri" else np.sign(np.sin(ph))*0.5
    return s*np.exp(-tt*dec)*np.minimum(1,tt/0.01)
wind=rngn.normal(size=N); 
from scipy.signal import butter,lfilter
b,a=butter(2,[200/(SR/2),800/(SR/2)],"band"); mix+=lfilter(b,a,wind)*0.08
drone=sum(np.sin(2*np.pi*f*t) for f in (41,43.7,61.7))*0.06; mix+=drone
segstart=[];acc=0
for fs,_ in SEG: segstart.append(acc/FPS); acc+=len(fs)
BELL=[587,698,880,784,698,659,587,523]
for k in range(4): add(tone(BELL[k],1.8),segstart[2]+0.4+k*0.9,0.25)
for k in range(2): add(tone(BELL[k+4],1.8),segstart[1]+1.2+k*1.5,0.2)
hs=lfilter(*butter(2,[2500/(SR/2),9000/(SR/2)],"band"),rngn.normal(size=int(1.8*SR)))*np.sin(np.pi*np.linspace(0,1,int(1.8*SR)))**1.5
add(hs,segstart[3]+1.5,0.5); add(hs,segstart[3]+4.6,0.4)
th=np.sin(2*np.pi*(60-25*np.arange(int(0.7*SR))/SR)*np.arange(int(0.7*SR))/SR)*np.exp(-np.arange(int(0.7*SR))/SR*7)
add(th,segstart[0]+0.1,1.0); add(th,segstart[0]+1.6,0.7)
for f in (880,1108): add(tone(f,1.5,1.2,"sq"),segstart[4]+0.6,0.12)
for i,f in enumerate((587,740,880,1175)): add(tone(f,3.5,0.8),segstart[4]+5+i*0.12,0.12)
endt=len(files) and n/FPS-4.5
for f in (293,440,587): add(tone(f,4,0.6),endt+0.1,0.12)
fade=np.minimum(1,t/0.3)*np.clip((total-t)/1.0,0,1); mix=np.tanh(mix*1.6)*0.85*fade
st=np.stack([mix,mix],1)
with wave.open(OUT+"/sound.wav","wb") as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",OUT+"/o%05d.jpg","-i",OUT+"/sound.wav","-c:v","libx264","-preset","slow","-crf","22","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",os.environ.get("AD_MP4","ad_16x9.mp4")],check=True)
print("done")
