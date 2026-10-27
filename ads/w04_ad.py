# Ad for w04 The Moss Giants. Copied from tools/ad_template.py / ad_template_16x9.py and edited.
# ORIENT=9x16 or 16x9  FRAMES=... OUTDIR=... AD_MP4=...
import glob, os, subprocess, numpy as np, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.signal import butter,lfilter
ORIENT=os.environ.get("ORIENT","9x16"); P=ORIENT=="9x16"
FR=os.environ.get("FRAMES","frames"); OUT=os.environ.get("OUTDIR","ad_out"); os.makedirs(OUT,exist_ok=True)
W,H=(1080,1920) if P else (1920,1080); FPS=30
SER="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
def F(p,s): return ImageFont.truetype(p,s)
files=sorted(glob.glob(FR+"/f*.jpg")); idx={int(os.path.basename(f)[1:6]):f for f in files}
OFF=float(os.environ.get("TOFF","0"))
def rng(a,b): return [idx[i] for i in range(int((a+OFF)*30),int((b+OFF)*30)) if i in idx]
SEG=[(rng(44,48),"Something huge is behind you."),
     (rng(5,12),"Turn around... slowly."),
     (rng(80,90),"They only move when you don't look."),
     (rng(90,99),"Hold her gaze until the sun comes up.")]
# hook first: 44 s is the giant's face right in front of you
for fs,t in SEG: assert len(fs)>60, (t,len(fs))
URL="ranta46.github.io/TremenVR/moss-giants"
gold=(255,201,74); paper=(255,246,230); dark=(10,10,30)
def st(d,xy,txt,font,fill,anchor="mm",sw=7): d.text(xy,txt,font=font,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill=dark)
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
for si,(fs,txt) in enumerate(SEG):
    for k,f in enumerate(fs):
        im=Image.open(f).convert("RGB").resize((W,H)); d=ImageDraw.Draw(im)
        if P: st(d,(W//2,300),"PLAY FREE · NO APP",F(MONO,40),gold,"mm",5)
        else: st(d,(60,60),"PLAY FREE · NO APP · LINK BELOW",F(MONO,36),gold,"lm",5)
        if k>=4:
            fnt=F(SER,84 if P else 80); lines=wrap(txt,fnt,960 if P else 1600,d)
            y=(1420 if P else 930)-len(lines)*50
            for L in lines: st(d,(W//2,y),L,fnt,paper,"mm",8); y+=100
        put(im)
base=Image.open(SEG[-1][0][-1]).convert("RGB").resize((W,H)).filter(ImageFilter.GaussianBlur(14))
base=Image.blend(base,Image.new("RGB",(W,H),dark),0.5)
for k in range(int(4.5*FPS)):
    im=base.copy(); d=ImageDraw.Draw(im)
    if P:
        st(d,(W//2,520),"TREMENVR · WORK 04",F(MONO,40),gold)
        st(d,(W//2,700),"The Moss",F(SER,120),paper); st(d,(W//2,840),"Giants",F(SER,130),gold)
        st(d,(W//2,1060),"Play it now. Free.",F(SER,72),paper)
        st(d,(W//2,1160),"Phone · PC · VR headset",F(SER,48),(200,198,235))
        d.rounded_rectangle((50,1330,1030,1470),radius=28,fill=gold)
        d.text((W//2,1400),URL,font=F(MONO,38),fill=(42,26,0),anchor="mm")
        st(d,(W//2,1570),"Link in profile",F(SER,56),paper)
    else:
        st(d,(W//2,180),"TREMENVR · WORK 04",F(MONO,40),gold)
        st(d,(W//2+10,330),"The Moss",F(SER,120),paper,"rm"); st(d,(W//2+50,330),"Giants",F(SER,120),gold,"lm")
        st(d,(W//2,500),"Play it now. Free.",F(SER,70),paper)
        st(d,(W//2,590),"Phone · PC · VR headset",F(SER,48),(200,198,235))
        d.rounded_rectangle((360,690,1560,830),radius=28,fill=gold)
        d.text((W//2,760),URL,font=F(MONO,44),fill=(42,26,0),anchor="mm")
        st(d,(W//2,920),"Link in the description",F(SER,52),paper)
    put(im)
total=n/FPS; print("frames",n,"sec",round(total,1))
# ---- soundtrack (original, synthesized) ----
SR=44100; N=int(total*SR); t=np.arange(N)/SR; mix=np.zeros(N); R=np.random.default_rng(5)
def add(sig,t0,g=1.0):
    i=int(t0*SR)
    if i>=N: return
    sig=sig[:N-i]; mix[i:i+len(sig)]+=sig*g
def tone(f,dur,dec=3.0,typ="tri",f1=None):
    tt=np.arange(int(dur*SR))/SR; fr=f if f1 is None else f*(f1/f)**(tt/dur); ph=2*np.pi*np.cumsum(fr)/SR
    s=(2/np.pi)*np.arcsin(np.sin(ph)) if typ=="tri" else (np.sign(np.sin(ph))*0.5 if typ=="sq" else np.sin(ph))
    return s*np.exp(-tt*dec)*np.minimum(1,tt/0.01)
def noise(dur,lo,hi): x=R.normal(size=int(dur*SR)); return lfilter(*butter(2,[lo/(SR/2),hi/(SR/2)],"band"),x)
ss=[];acc=0
for fs,_ in SEG: ss.append(acc/FPS); acc+=len(fs)
endt=ss[-1]+len(SEG[-1][0])/FPS
# moonlit forest pad + stone grinding + sunrise chimes (original, synthesized)
pad=sum(np.sin(2*np.pi*f*t+0.3*np.sin(t*0.3+f)) for f in (49,73.4,98,146.8))*0.05
mix+=pad+noise(total,300,1200)*0.04
def grind(t0,dur,g):
    nn=int(dur*SR); env=np.sin(np.pi*np.linspace(0,1,nn))**0.8*(0.6+0.4*np.sin(np.linspace(0,dur*23,nn)))
    add(noise(dur,60,420)*env*1.4+tone(48,dur,0.3,"sin",40)*0.5,t0,g)
def thud(t0,g): add(tone(70,0.9,6,"sin",38),t0,g)
thud(0.05,1.0); grind(0.3,1.6,0.8); thud(2.2,0.8)
for k in range(3): add(tone((392,466,523)[k],1.4,2.0,"tri"),3.5+k*1.6,0.10)
for k in range(2): thud(ss[1]+0.5+k*0.7,0.6)
grind(ss[1]+3.0,2.2,0.9); thud(ss[1]+5.4,1.0)
grind(ss[2]+0.2,0.8,0.8); thud(ss[2]+1.1,0.7); grind(ss[2]+2.0,0.8,0.8); thud(ss[2]+2.9,0.7)
grind(ss[3]+0.3,2.0,0.6)
for i,f in enumerate((392,494,587,784,988,1175)): add(tone(f,2.6,1.0),ss[3]+2.5+i*0.8,0.12)
for i,f in enumerate((392,494,587,784)): add(tone(f,4,0.7),endt+0.1+i*0.08,0.12)
fade=np.minimum(1,t/0.2)*np.clip((total-t)/1.0,0,1); mix=np.tanh(mix*1.5)*0.85*fade
sdat=np.stack([mix,mix],1)
with wave.open(OUT+"/sound.wav","wb") as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((sdat*32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",OUT+"/o%05d.jpg","-i",OUT+"/sound.wav","-c:v","libx264","-preset","medium","-crf","22","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",os.environ.get("AD_MP4","ad.mp4")],check=True)
print("done")
