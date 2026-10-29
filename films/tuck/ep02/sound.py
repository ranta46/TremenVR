import numpy as np, wave
from scipy.signal import butter, lfilter
SR=44100; TOTAL=76.0; N=int(TOTAL*SR); t=np.arange(N)/SR
rng=np.random.default_rng(11); L=np.zeros(N); Rr=np.zeros(N)
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

# ambience: wind + water far below
wind=bp(rng.normal(size=N),150,900); wmod=0.6+0.4*np.sin(2*np.pi*t/8.0)+0.2*np.sin(2*np.pi*t/3.1)
L+=wind*wmod*0.05; Rr+=np.roll(wind,3000)*wmod*0.05
wat=bp(rng.normal(size=N),60,300)*(0.5+0.5*np.sin(2*np.pi*t/5.5))*0.04; L+=wat; Rr+=np.roll(wat,7000)
# last lamp flicker far away
for a,b in ((40,46),(52,60)): d=(b-a)/24; add(bp(noise(d),90,400)*env(int(d*SR),0.005,0.02),f2s(a),0.12,0.4)
# letter rustle
add(bp(noise(0.5),1500,6000)*env(int(0.5*SR),0.02,0.2),f2s(98),0.18)
def steps(f0,f1,every=8,g=0.2,pan=0.0):
    for f in range(f0,f1,every): add(bp(noise(0.08),300,2500)*np.exp(-np.arange(int(0.08*SR))/SR*60),f2s(f),g*rng.uniform(0.8,1.1),pan)
steps(217,600); steps(871,1080)
def wf(y): return int(217+(y+2)/16*383) if y<=14 else int(871+(y-14)/10.4*209)
for y in (2,6.5,11,15.5,20):
    f=wf(y-1.0); add(bp(noise(0.25),90,500)*env(int(0.25*SR),0.005,0.1),f2s(f),0.15); add(tone(220,0.6,'sin',4,140),f2s(f+3),0.05)
# the Tall One rises from the abyss
g0,g1=f2s(605),f2s(845); dur=g1-g0
rum=lp(rng.normal(size=int(dur*SR)),70)*8*env(int(dur*SR),2.5,2.5); add(rum,g0,0.55,-0.5)
pour=bp(rng.normal(size=int(4*SR)),200,1800)*env(int(4*SR),0.8,2.5); add(pour,f2s(612),0.18,-0.6)
add(pour[::-1].copy(),f2s(780),0.14,-0.6)
add(tone(1400,0.3,'sin',4,850),f2s(662),0.1)
# letter into slot + clunk
add(bp(noise(0.5),1200,5000)*env(int(0.5*SR),0.03,0.15),f2s(1150),0.22,0.2)
add(tone(140,0.25,'sin',12,90)+bp(noise(0.25),400,2000)*np.exp(-np.arange(int(0.25*SR))/SR*20)*0.5,f2s(1168),0.4,0.2)
# last lamp ignites, chain of lamps
add(bp(noise(1.2),200,3000)*env(int(1.2*SR),0.05,0.8),f2s(1226),0.25,0.2); add(bp(noise(4),110,130)*env(int(4*SR),0.1,2),f2s(1230),0.08,0.2)
SCL=[523,587,659,784,880,1047]
for k in range(5):
    f=1254+k*22; add(bp(noise(0.05),2000,7000)*np.exp(-np.arange(int(0.05*SR))/SR*80),f2s(f),0.2,-0.2*k)
    a=tone(SCL[k],2.2,'tri',1.8); add(a,f2s(f),0.12)
add(tone(1046,3,'tri',1),f2s(1364),0.12); add(tone(1318,3,'tri',1),f2s(1368),0.08)
# happy triple beep, bow
for i,fq in enumerate((1318,1568,2093)): add(tone(fq,0.1,'sq',8),f2s(1442)+i*0.11,0.13)
# reply letter slides out, lands, surprised beeps
add(bp(noise(0.7),1100,5000)*env(int(0.7*SR),0.05,0.2),f2s(1528),0.22,0.2)
add(bp(noise(0.3),800,3000)*np.exp(-np.arange(int(0.3*SR))/SR*15),f2s(1560),0.2)
add(tone(990,0.2,'sq',6,1320),f2s(1600),0.13); add(tone(1320,0.25,'sq',6,880),f2s(1612),0.1)
# music box: lonely minor walk, major when lamps light
mb=[(2,659),(3,587),(4.5,523),(10,440),(11,523),(12,587),(14,523),(18,440),(19,415),(20,440),(36,494),(37,523),(38,587),(44,523)]
for ts,fq in mb:
    a=tone(fq,2.0,'tri',2.2) if False else tone(fq,2.0,'tri',2.2); b=tone(fq*2,1.2,'sin',4); a[:len(b)]+=0.3*b; add(a,ts,0.07)
def pad(fs,t0,d,g):
    n=int(d*SR); tt=np.arange(n)/SR; s=sum(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*f*2.01*tt) for f in fs); add(s*env(n,1.5,2.0),t0,g)
pad((110,164.8,220),0,24,0.011); pad((87.3,130.8,174.6),25,11,0.012); pad((98,146.8,196),36,15,0.011); pad((130.8,196,261.6,329.6),51,19,0.016)
for i,fq in enumerate((523,659,784,1046)): add(tone(fq,3.5,'tri',0.8),70.2+i*0.15,0.07)
mix=np.stack([L,Rr],1); mix=np.tanh(mix*1.4)*0.9
fade=np.clip((TOTAL-t)/1.5,0,1)[:,None]*np.minimum(1,t/0.5)[:,None]; mix*=fade
with wave.open('sound.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok',TOTAL)
