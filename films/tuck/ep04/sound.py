import numpy as np, wave
from scipy.signal import butter, lfilter
SR=44100; TOTAL=76.0; N=int(TOTAL*SR); t=np.arange(N)/SR
rng=np.random.default_rng(14); L=np.zeros(N); Rr=np.zeros(N)
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

# ep04 "The Window That Never Sleeps": cue times from the cut list (frame/24 = s). Film 1680 f = 70 s + 6 s end card.
# ambience: city wind high up + far hum; gets colder when the window goes dark (1140)
wind=bp(rng.normal(size=N),150,900); wmod=0.6+0.4*np.sin(2*np.pi*t/8.0)+0.2*np.sin(2*np.pi*t/3.1)
up=np.clip((t-f2s(289))/20,0,1)*0.5+0.5   # wind grows as Tuck climbs
L+=wind*wmod*0.04*up; Rr+=np.roll(wind,2500)*wmod*0.04*up
hum=lp(rng.normal(size=N),70)*4; L+=hum*0.02; Rr+=hum*0.02
# steps: sidewalk, iron stairs (ringing), balcony
def steps(f0,f1,every=8,g=0.2,pan=0.0,lo=300,ring=False):
    for f in range(f0,f1,every):
        n=int(0.08*SR); s=bp(noise(0.08),lo,2500)*np.exp(-np.arange(n)/SR*60)
        add(s,f2s(f),g*rng.uniform(0.8,1.1),pan)
        if ring: add(tone(rng.uniform(380,460),0.35,'sin',9),f2s(f),g*0.25,pan)
steps(276,338,8,0.15,0.3); steps(338,528,8,0.17,0.2,250,True); steps(529,545,8,0.12,0,250,True)
steps(673,790,8,0.17,0.1,250,True); steps(790,840,8,0.13,0,250,True); steps(1000,1012,6,0.1)
# C1 lit window: soft warm tone. C2 letter: paper rustle
add(tone(523,4,'sin',0.5)+0.4*tone(784,4,'sin',0.6),0.3,0.04)
add(bp(noise(0.5),1500,6000)*env(int(0.5*SR),0.02,0.2),f2s(100),0.15)
# C3 afraid of the height: falling beep 214; lamp flickers on 245-252 (buzz clicks); brave beep 264
add(tone(1100,0.25,'sq',6,700),f2s(214),0.12)
for f in (245,249,252):
    add(bp(noise(0.05),2000,7000)*np.exp(-np.arange(int(0.05*SR))/SR*80),f2s(f),0.2,0.4)
hz=np.sin(2*np.pi*100*np.arange(int(3*SR))/SR)*env(int(3*SR),0.01,1.5); add(hz,f2s(252),0.02,0.4)
add(tone(800,0.12,'sq',8,950),f2s(264),0.09)
# C5/C6 the Tall One: two deep footsteps, then passing eyes swell; Tuck freezes (beep 590)
for f in (572,604,636,668):
    add(lp(rng.normal(size=int(1.2*SR)),70)*12*np.exp(-np.arange(int(1.2*SR))/SR*3),f2s(f),0.35,-0.2)
add(tone(1000,0.3,'sq',6,600),f2s(590),0.10)
add(lp(rng.normal(size=int(4*SR)),110)*8*env(int(4*SR),1.5,1.5),f2s(600),0.3)
add(tone(196,4,'sin',0.5,185)+0.5*tone(294,4,'sin',0.5,277),f2s(610),0.07)
add(tone(700,0.15,'sq',8,900),f2s(684),0.08)
# C8 window: curious rising beeps, warm room hum (until 1140)
add(tone(880,0.15,'sq',7,1180),f2s(868),0.1); add(tone(1050,0.15,'sq',7,1400),f2s(876),0.08)
rm=np.sin(2*np.pi*60*t)*0.5+np.sin(2*np.pi*120*t)*0.3; gate=((t>f2s(841))&(t<f2s(1140))).astype(float); L+=rm*gate*0.006; Rr+=rm*gate*0.006
# C9 letter slides in + bow
add(bp(noise(0.6),1300,6000)*env(int(0.6*SR),0.02,0.25),f2s(1010),0.2)
add(bp(noise(0.25),800,3000)*np.exp(-np.arange(int(0.25*SR))/SR*15),f2s(1062),0.12)
# C10 the light goes out: click + flicker, dark drop; afraid beep then brave beep
for f in (1136,1140): add(bp(noise(0.04),1500,6000)*np.exp(-np.arange(int(0.04*SR))/SR*90),f2s(f),0.25)
add(tone(330,3,'sin',0.8,165),f2s(1141),0.09)
add(tone(1050,0.3,'sq',6,620),f2s(1147),0.11); add(tone(800,0.12,'sq',8,1000),f2s(1192),0.08)
# C11 quiet: small sigh beep
add(tone(700,0.4,'sq',5,520),f2s(1290),0.06)
# C12 reply slides out: paper, surprised rising beeps, happy triple
add(bp(noise(0.8),1100,5000)*env(int(0.8*SR),0.05,0.2),f2s(1372),0.2)
add(tone(990,0.2,'sq',6,1320),f2s(1380),0.12); add(tone(1320,0.25,'sq',6,1760),f2s(1392),0.1)
for i,fq in enumerate((1318,1568,2093)): add(tone(fq,0.1,'sq',8),f2s(1402)+i*0.11,0.13)
# C14 the far clock: one slow, distant bell (it does not tick)
for f in (1575,):
    b=tone(196,6,'sin',0.5)+0.5*tone(392.5,6,'sin',0.8)+0.3*tone(588,6,'sin',1.2); add(lp(b,1500),f2s(f),0.12,-0.5)
add(tone(900,0.15,'sq',7,1200),f2s(1606),0.08)
# music box: curious little tune, tense in the middle, warm at the end
mb=[(1.5,523),(2.5,659),(3.5,784),(6,698),(7,659),(9,587),(16,523),(17,587),(18,659),(26,494),(27,523),
    (34,587),(35,523),(36,494),(46,440),(47,494),(48,523),(58,659),(59,784),(64,880),(65,784),(66,659)]
for ts,fq in mb:
    a=tone(fq,2.0,'tri',2.2); b=tone(fq*2,1.2,'sin',4); a[:len(b)]+=0.3*b; add(a,ts,0.07)
def pad(fs,t0,d,g):
    n=int(d*SR); tt=np.arange(n)/SR; s=sum(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*f*2.01*tt) for f in fs); add(s*env(n,1.5,2.0),t0,g)
pad((130.8,196,261.6),0,24,0.011); pad((98,146.8,196),24,24,0.013); pad((110,164.8,220),47,10,0.011); pad((130.8,196,261.6,329.6),56,20,0.016)
for i,fq in enumerate((523,659,784,1046)): add(tone(fq,3.5,'tri',0.8),70.2+i*0.15,0.07)
mix=np.stack([L,Rr],1); mix=np.tanh(mix*1.4)*0.9
fade=np.clip((TOTAL-t)/1.5,0,1)[:,None]*np.minimum(1,t/0.5)[:,None]; mix*=fade
with wave.open('sound.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok',TOTAL)
