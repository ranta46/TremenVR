# Ad for w02 Pip's Star Jar. Copied from tools/ad_template.py / ad_template_16x9.py and edited.
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
T=eval(os.environ["TIMES"])  # dict of segment start times
SEG=[(rng(T["hook"],T["hook"]+4.0),"A sleepy comet is falling on you!"),
     (rng(T["intro"],T["intro"]+3.0),"Catch the falling wishes."),
     (rng(T["catch"],T["catch"]+4.5),"Tap a star to catch it."),
     (rng(T["red"],T["red"]+4.0),"Never tap the red ones!"),
     (rng(T["comet"],T["comet"]+4.0),"Then... something BIG comes."),
     (rng(T["wake"],T["wake"]+6.5),"Tap fast. Wake him up!"),
     (rng(T["fox"],T["fox"]+6.0),"Give the stars back to the sky.")]
for fs,t in SEG: assert len(fs)>60, (t,len(fs))
URL="ranta46.github.io/TremenVR/w02"
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
        st(d,(W//2,520),"TREMENVR · WORK 02",F(MONO,40),gold)
        st(d,(W//2,700),"Pip's Star",F(SER,120),paper); st(d,(W//2,840),"Jar",F(SER,130),gold)
        st(d,(W//2,1060),"Play it now. Free.",F(SER,72),paper)
        st(d,(W//2,1160),"Phone · PC · VR headset",F(SER,48),(200,198,235))
        d.rounded_rectangle((70,1330,1010,1470),radius=28,fill=gold)
        d.text((W//2,1400),URL,font=F(MONO,44),fill=(42,26,0),anchor="mm")
        st(d,(W//2,1570),"Link in profile",F(SER,56),paper)
    else:
        st(d,(W//2,180),"TREMENVR · WORK 02",F(MONO,40),gold)
        st(d,(W//2+10,330),"Pip's Star",F(SER,120),paper,"rm"); st(d,(W//2+50,330),"Jar",F(SER,120),gold,"lm")
        st(d,(W//2,500),"Play it now. Free.",F(SER,70),paper)
        st(d,(W//2,590),"Phone · PC · VR headset",F(SER,48),(200,198,235))
        d.rounded_rectangle((410,690,1510,830),radius=28,fill=gold)
        d.text((W//2,760),URL,font=F(MONO,50),fill=(42,26,0),anchor="mm")
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
# pad (A major) for the calm parts, rumble for the comet parts
pad=sum(np.sin(2*np.pi*f*t) for f in (220,277.2,329.6,440))*0.035
calm=np.zeros(N); 
def env(a,b,v,arr):
    i,j=int(a*SR),int(min(b,total)*SR); arr[i:j]=v
env(ss[1],ss[4],1,calm); env(ss[6],total,1,calm)
calm=lfilter([0.0005],[1,-0.9995],calm)
mix+=pad*calm
rum=np.zeros(N); env(0,ss[1],1,rum); env(ss[4],ss[6],1,rum); rum=lfilter([0.0005],[1,-0.9995],rum)
mix+=sum(np.sin(2*np.pi*f*t+np.sin(t*0.7)) for f in (46,49,69))*0.09*rum
mix+=lfilter(*butter(2,[150/(SR/2),600/(SR/2)],"band"),R.normal(size=N))*0.05
SC=[523,587,659,784,880,1047,1175,1319,1568,1760]
# hook: bonk taps then BOOM at the bounce (~2.5s in)
for k in range(4): add(tone(200+k*15,0.25,8,"tri",130+k*15),ss[0]+0.2+k*0.42,0.5)
boom=tone(80,1.5,2.5,"sin",30)+noise(1.5,200,800)*np.exp(-np.arange(int(1.5*SR))/SR*3)*0.6
add(boom,ss[0]+2.5,1.0)
for k in range(3): add(tone(SC[k],0.9,3),ss[1]+0.6+k*0.8,0.22)
for k in range(5): add(tone(SC[k+2],0.9,3),ss[2]+0.4+k*0.85,0.22); add(tone(SC[k+2]*2,0.4,6),ss[2]+0.4+k*0.85,0.05)
for k in range(2): add(noise(0.5,1500,4000)*np.exp(-np.arange(int(0.5*SR))/SR*6),ss[3]+1.2+k*1.5,0.35); add(tone(300,0.4,5,"sq",90),ss[3]+1.2+k*1.5,0.15)
add(tone(SC[6],0.9,3),ss[3]+0.5,0.2)
for k in range(3): add(tone(60,1.2,2,"sin",40),ss[4]+0.5+k*1.2,0.5)
for k in range(10): add(tone(200+k*14,0.22,9,"tri",130+k*14),ss[5]+0.2+k*0.38,0.45)
for i,f in enumerate((523,659,784,1047,1319)): add(tone(f,1.6,1.5),ss[5]+4.0+i*0.12,0.16)
for k in range(8): add(tone(SC[(k*2)%10],1.2,2),ss[6]+0.3+k*0.5,0.16)
for i,f in enumerate((440,554,659,880)): add(tone(f,4,0.7),endt+0.1+i*0.08,0.12)
fade=np.minimum(1,t/0.2)*np.clip((total-t)/1.0,0,1); mix=np.tanh(mix*1.5)*0.85*fade
sdat=np.stack([mix,mix],1)
with wave.open(OUT+"/sound.wav","wb") as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((sdat*32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",OUT+"/o%05d.jpg","-i",OUT+"/sound.wav","-c:v","libx264","-preset","medium","-crf","22","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",os.environ.get("AD_MP4","ad.mp4")],check=True)
print("done")
