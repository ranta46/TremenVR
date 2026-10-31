import numpy as np, wave
from scipy.signal import butter, lfilter
SR=44100; TOTAL=76.0; N=int(TOTAL*SR); t=np.arange(N)/SR
rng=np.random.default_rng(15); L=np.zeros(N); Rr=np.zeros(N)
def f2s(f): return (f-1)/24.0
def add(sig,t0,g=1.0,pan=0.0):
    i=int(t0*SR); 
    if i>=N: return
    s=sig[:N-i]*g; L[i:i+len(s)]+=s*(1-max(0,pan)); Rr[i:i+len(s)]+=s*(1+min(0,pan))
def bp(x,lo,hi): b,a=butter(2,[lo/(SR/2),hi/(SR/2)],'band'); return lfilter(b,a,x)
def lp(x,hi): b,a=butter(2,hi/(SR/2),'low'); return lfilter(b,a,x)
def env(n,a=0.01,r=0.2):
    e=np.ones(n); na=int(a*SR); nr=int(r*SR)
    if na: e[:na]=np.linspace(0,1,na)
    if nr: e[-nr:]*=np.linspace(1,0,nr)
    return e
def tone(f,d,typ='sin',dec=3,f1=None):
    n=int(d*SR); tt=np.arange(n)/SR; fr=f if f1 is None else f*(f1/f)**(tt/d); ph=2*np.pi*np.cumsum(fr)/SR
    s=np.sin(ph) if typ=='sin' else ((2/np.pi)*np.arcsin(np.sin(ph)) if typ=='tri' else np.sign(np.sin(ph))*0.4)
    return s*np.exp(-tt*dec)*np.minimum(1,tt/0.005)
def noise(d): return rng.normal(size=int(d*SR))

# ep05 "The Clock That Stopped": cue times from the cut list (frame/24 = s). Film 1680 f = 70 s + 6 s end card.
# ambience: open square wind + far hum. Before 700 the clock is silent; after 700 it ticks every 24 frames.
wind=bp(rng.normal(size=N),120,800); wmod=0.6+0.4*np.sin(2*np.pi*t/9.0)+0.2*np.sin(2*np.pi*t/3.3)
L+=wind*wmod*0.035; Rr+=np.roll(wind,2600)*wmod*0.035
hum=lp(rng.normal(size=N),70)*4; L+=hum*0.02; Rr+=hum*0.02
def steps(f0,f1,every=8,g=0.2,pan=0.0,lo=300):
    for f in range(f0,f1,every):
        n=int(0.08*SR); s=bp(noise(0.08),lo,2500)*np.exp(-np.arange(n)/SR*60)
        add(s,f2s(f),g*rng.uniform(0.8,1.1),pan)
steps(4,90,8,0.13,0.2); steps(316,571,8,0.15,-0.1); steps(1600,1656,8,0.12,0.1)
# C1 huge silent clock: low cold tone
add(tone(147,5,'sin',0.4)+0.4*tone(220,5,'sin',0.6),0.2,0.05)
# C2 letter: paper rustle, curious rising beep
add(bp(noise(0.5),1500,6000)*env(int(0.5*SR),0.02,0.2),f2s(100),0.15)
add(tone(880,0.15,'sq',7,1180),f2s(130),0.09)
# C3 looks up: afraid falling beep, then brave beep
add(tone(1100,0.25,'sq',6,700),f2s(206),0.12); add(tone(800,0.12,'sq',8,950),f2s(292),0.09)
# C5 letter into the slot: paper slide + small metal flap
add(bp(noise(0.6),1300,6000)*env(int(0.6*SR),0.02,0.25),f2s(598),0.2)
add(bp(noise(0.05),2500,8000)*np.exp(-np.arange(int(0.05*SR))/SR*80),f2s(613),0.2)
add(tone(700,0.4,'sq',5,520),f2s(660),0.05)
# C6 silence ... CLUNK (700), the clock starts, BONG (720)
add(lp(rng.normal(size=int(1.0*SR)),180)*10*np.exp(-np.arange(int(1.0*SR))/SR*6),f2s(700),0.4)
add(tone(90,1.0,'sin',4),f2s(700),0.25)
for f in range(701,1680,24):
    add(bp(noise(0.03),1800,6000)*np.exp(-np.arange(int(0.03*SR))/SR*120),f2s(f),0.06 if f>760 else 0.12,-0.3)
for f in (720,):
    b=tone(130.8,8,'sin',0.35)+0.6*tone(261.6,8,'sin',0.6)+0.35*tone(392.5,8,'sin',0.9)+0.2*tone(523.5,8,'sin',1.4)
    add(lp(b,1800),f2s(f),0.22,-0.2)
# C7 Tuck startled: fast afraid beep
add(tone(1300,0.3,'sq',6,600),f2s(708),0.11)
# C7/C8 the Tall One turns to the sound: deep breath swell, two footsteps when it leaves
add(lp(rng.normal(size=int(5*SR)),110)*8*env(int(5*SR),1.5,2.0),f2s(800),0.3)
add(tone(196,5,'sin',0.4,185)+0.5*tone(277,5,'sin',0.4,262),f2s(840),0.07)
for f in (1000,1030,1060):
    add(lp(rng.normal(size=int(1.2*SR)),70)*12*np.exp(-np.arange(int(1.2*SR))/SR*3),f2s(f),0.32*(1-(f-1000)/120),0.3)
# C9 relief and bow
add(tone(700,0.3,'sq',6,520),f2s(1072),0.07)
add(bp(noise(0.25),800,3000)*np.exp(-np.arange(int(0.25*SR))/SR*15),f2s(1130),0.12)
# C10 reply slides out of the slot and falls: paper, surprised rising beeps
add(bp(noise(1.0),1100,5000)*env(int(1.0*SR),0.05,0.25),f2s(1228),0.2)
add(bp(noise(0.15),600,3000)*np.exp(-np.arange(int(0.15*SR))/SR*25),f2s(1280),0.12)
add(tone(990,0.2,'sq',6,1320),f2s(1290),0.12); add(tone(1320,0.25,'sq',6,1760),f2s(1302),0.1)
# C11 picks it up; C12 happy triple beep
add(bp(noise(0.4),1500,6000)*env(int(0.4*SR),0.02,0.2),f2s(1436),0.13)
for i,fq in enumerate((1318,1568,2093)): add(tone(fq,0.1,'sq',8),f2s(1476)+i*0.11,0.13)
# C13 one more soft bell far away
b=tone(196,6,'sin',0.5)+0.5*tone(392.5,6,'sin',0.8); add(lp(b,1500),f2s(1600),0.08,-0.4)
# music: quiet music box, stops during the silence before the clunk, warm at the end
mb=[(1.5,494),(2.5,587),(3.5,740),(6,659),(7,587),(9,523),(15,494),(16,523),(17,587),(24,440),(25,494),
    (33,523),(35,494),(47,440),(48,494),(49,523),(56,587),(57,659),(62,784),(63,659),(66,587),(67,494)]
for ts,fq in mb:
    a=tone(fq,2.0,'tri',2.2); b=tone(fq*2,1.2,'sin',4); a[:len(b)]+=0.3*b; add(a,ts,0.065)
def pad(fs,t0,d,g):
    n=int(d*SR); tt=np.arange(n)/SR; s=sum(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*f*2.01*tt) for f in fs); add(s*env(n,1.5,2.0),t0,g)
pad((123.5,185,246.9),0,26,0.011); pad((98,146.8,196),30,14,0.013); pad((110,164.8,220),44,8,0.011); pad((123.5,185,246.9,293.7),52,24,0.016)
for i,fq in enumerate((494,587,740,988)): add(tone(fq,3.5,'tri',0.8),70.2+i*0.15,0.07)
mix=np.stack([L,Rr],1); mix=np.tanh(mix*1.4)*0.9
fade=np.clip((TOTAL-t)/1.5,0,1)[:,None]*np.minimum(1,t/0.5)[:,None]; mix*=fade
with wave.open('sound.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok',TOTAL)
