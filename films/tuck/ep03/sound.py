import numpy as np, wave
from scipy.signal import butter, lfilter
SR=44100; TOTAL=76.0; N=int(TOTAL*SR); t=np.arange(N)/SR
rng=np.random.default_rng(13); L=np.zeros(N); Rr=np.zeros(N)
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

# ep03 "Under the Bridge": cue times from the cut list (frame/24 = s). Film 1680 f = 70 s + 6 s end card.
# ambience: low wind under the bridge + dripping water
wind=bp(rng.normal(size=N),120,700); wmod=0.6+0.4*np.sin(2*np.pi*t/9.0)+0.2*np.sin(2*np.pi*t/3.7)
L+=wind*wmod*0.045; Rr+=np.roll(wind,3000)*wmod*0.045
for ts in np.arange(1.3,70,2.7)+rng.uniform(-0.6,0.6,len(np.arange(1.3,70,2.7))):
    add(tone(rng.uniform(1500,2300),0.12,'sin',30,rng.uniform(900,1200)),ts,0.05,rng.uniform(-0.7,0.7))
# the sleeper's breathing (in/out every 2 s, frames 1-1344), big exhale at 590
def breath(t0,g,d=1.8):
    n=int(d*SR); s=lp(rng.normal(size=n),260)*6*env(n,0.7,0.9); add(s,t0,g,-0.4)
    add(lp(rng.normal(size=n),60)*10*env(n,0.6,0.9),t0,g*0.6,-0.4)
for f in range(1,1344,48):
    if 560<=f<=620: continue
    breath(f2s(f),0.10 if f<600 else 0.13)
breath(f2s(586),0.38,2.6)
# footsteps: stairs (stone, a bit hollow) and ledge
def steps(f0,f1,every=8,g=0.2,pan=0.0,lo=300):
    for f in range(f0,f1,every): add(bp(noise(0.08),lo,2500)*np.exp(-np.arange(int(0.08*SR))/SR*60),f2s(f),g*rng.uniform(0.8,1.1),pan)
steps(297,480,8,0.2,0.2,200); steps(481,589,8,0.2,0.1,200); steps(649,760,8,0.16); steps(845,880,8,0.12)
steps(1280,1372,8,0.15); steps(1407,1464,8,0.15)
# beeps: afraid falling at 232, small brave beep 280
add(tone(1100,0.25,'sq',6,700),f2s(232),0.12); add(tone(800,0.12,'sq',8,950),f2s(282),0.08)
add(tone(1000,0.3,'sq',6,600),f2s(594),0.10)
# letter rustle (hand -> ground) and bow
add(bp(noise(0.6),1500,6000)*env(int(0.6*SR),0.02,0.25),f2s(800),0.2)
add(bp(noise(0.25),800,3000)*np.exp(-np.arange(int(0.25*SR))/SR*15),f2s(812),0.15)
# the eye opens: deep swell + glassy tone
add(lp(rng.normal(size=int(3*SR)),90)*10*env(int(3*SR),1.2,1.2),f2s(930),0.4,-0.3)
add(tone(220,3.5,'sin',0.6,330)+0.5*tone(331,3.5,'sin',0.6,495),f2s(935),0.08,-0.3)
add(tone(1400,0.3,'sin',4,850),f2s(950),0.1)
add(tone(165,3,'sin',0.7,247),f2s(1070),0.06,-0.3)
# brave beep + polite bow
for i,fq in enumerate((880,1046)): add(tone(fq,0.12,'sq',8),f2s(1150)+i*0.13,0.1)
# eyes close: soft falling tone, the sleeper settles
add(tone(330,3,'sin',0.8,220),f2s(1210),0.08,-0.3); breath(f2s(1250),0.2,2.4)
# paper rustle behind Tuck, surprised rising beeps
add(bp(noise(0.7),1100,5000)*env(int(0.7*SR),0.05,0.2),f2s(1368),0.2,-0.3)
add(tone(990,0.2,'sq',6,1320),f2s(1378),0.12); add(tone(1320,0.25,'sq',6,1760),f2s(1392),0.1)
# reply close-up, happy triple beep
for i,fq in enumerate((1318,1568,2093)): add(tone(fq,0.1,'sq',8),f2s(1518)+i*0.11,0.13)
for i,fq in enumerate((1318,1568,2093)): add(tone(fq,0.1,'sq',8),f2s(1612)+i*0.11,0.11)
# music box: slow lullaby (the sleeper), tense at the eye, warm at the end
mb=[(1.5,659),(2.5,587),(3.5,523),(6,494),(7,523),(9,440),(16,523),(17,494),(18,440),(26,415),(27,440),
    (34,523),(35,494),(36,440),(46,494),(47,523),(48,587),(54,523),(64,659),(65,784),(66,880)]
for ts,fq in mb:
    a=tone(fq,2.0,'tri',2.2); b=tone(fq*2,1.2,'sin',4); a[:len(b)]+=0.3*b; add(a,ts,0.07)
def pad(fs,t0,d,g):
    n=int(d*SR); tt=np.arange(n)/SR; s=sum(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*f*2.01*tt) for f in fs); add(s*env(n,1.5,2.0),t0,g)
pad((110,164.8,220),0,24,0.011); pad((82.4,123.5,164.8),24,14,0.013); pad((98,146.8,196),38,18,0.011); pad((130.8,196,261.6,329.6),56,20,0.016)
for i,fq in enumerate((523,659,784,1046)): add(tone(fq,3.5,'tri',0.8),70.2+i*0.15,0.07)
mix=np.stack([L,Rr],1); mix=np.tanh(mix*1.4)*0.9
fade=np.clip((TOTAL-t)/1.5,0,1)[:,None]*np.minimum(1,t/0.5)[:,None]; mix*=fade
with wave.open('sound.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok',TOTAL)
