import numpy as np, wave
from scipy.signal import butter, lfilter
SR=44100; TOTAL=79.0; N=int(TOTAL*SR); t=np.arange(N)/SR
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
# ambience: wind + far city hum
wind=bp(rng.normal(size=N),150,900); wmod=0.6+0.4*np.sin(2*np.pi*t/9.0)+0.2*np.sin(2*np.pi*t/3.3)
L+=wind*wmod*0.05; Rr+=np.roll(wind,3000)*wmod*0.05
hum=(np.sin(2*np.pi*55*t)+0.5*np.sin(2*np.pi*110*t))*0.012; L+=hum; Rr+=hum
# lamp flicker buzz
for a,b in ((30,33),(36,42),(45,52)):
    d=(b-a)/24; z=bp(noise(d),90,400)*env(int(d*SR),0.005,0.02); add(z,f2s(a),0.25,0.3)
add(bp(noise(4),110,130)*env(int(4*SR),0.05,1.5),f2s(52),0.08,0.3)
# letter slide + drop
add(bp(noise(0.85),1200,5000)*env(int(0.85*SR),0.05,0.2),f2s(150),0.25,-0.4)
add(bp(noise(0.5),800,4000)*np.exp(-np.arange(int(0.5*SR))/SR*12),f2s(184),0.4,-0.4)
# wake: servo + beeps
add(tone(300,0.9,'sin',1.5,f1=520)*0.5+bp(noise(0.9),600,1600)*0.1,f2s(296),0.35)
for i,(fq,d) in enumerate(((880,0.09),(1175,0.12),(1568,0.16))): add(tone(fq,d,'sq',8),f2s(303)+i*0.12,0.18)
# footsteps
def steps(f0,f1,every=8,g=0.22,pan=0.0):
    for f in range(f0,f1,every): add(bp(noise(0.08),300,2500)*np.exp(-np.arange(int(0.08*SR))/SR*60),f2s(f),g*rng.uniform(0.8,1.1),pan)
steps(420,446,10,0.16); steps(725,1075,8,0.2); steps(1275,1375,8,0.2,0.2); steps(1625,1650,8,0.15,0.3)
# pickup rustle
add(bp(noise(0.4),1500,6000)*env(int(0.4*SR),0.02,0.2),f2s(472),0.2)
# questioning beeps while looking around
add(tone(990,0.18,'sq',6,f1=1320),f2s(590),0.12,-0.3); add(tone(1175,0.18,'sq',6,f1=880),f2s(650),0.12,0.3)
# lamps clicking on
def fy(y): return int(725+(y+0.72)/(9.5+0.72)*350)
for y in (4.5-1.2,8.5-1.2):
    add(bp(noise(0.05),2000,7000)*np.exp(-np.arange(int(0.05*SR))/SR*80),f2s(fy(y)),0.25); add(bp(noise(2.0),100,140)*env(int(2*SR),0.02,1.5),f2s(fy(y)),0.06)
add(bp(noise(0.05),2000,7000)*np.exp(-np.arange(int(0.05*SR))/SR*80),f2s(1290),0.2)
# giant: rumble + distant footfalls
g0,g1=f2s(1050),f2s(1320); dur=g1-g0
rum=lp(rng.normal(size=int(dur*SR)),70)*8*env(int(dur*SR),2.0,2.5); add(rum,g0,0.5)
for k in range(9):
    ts=g0+0.8+k*1.25; thud=tone(48,1.2,'sin',3,f1=32)+lp(noise(1.2),200)*0.6*np.exp(-np.arange(int(1.2*SR))/SR*4)
    add(thud,ts,0.55,-0.6+k*0.15)
# tiny scared beep
add(tone(1400,0.25,'sin',4,f1=900),f2s(1102),0.1)
# letter under door
add(bp(noise(0.45),1200,5000)*env(int(0.45*SR),0.03,0.15),f2s(1428),0.22,0.3)
# window light off click, then return letter slide, surprised beeps
add(bp(noise(0.04),1500,6000)*np.exp(-np.arange(int(0.04*SR))/SR*90),f2s(1556),0.3,0.4)
add(bp(noise(1.2),1000,4500)*env(int(1.2*SR),0.1,0.3),f2s(1620),0.22,0.3)
for i,fq in enumerate((1046,1318,1568,2093)): add(tone(fq,0.14,'sq',7),f2s(1660)+i*0.1,0.14)
# music box melody (sparse), A minor -> ends on C major
mb=[(2.5,659),(3.4,587),(4.3,523),(5.6,494),(14.5,523),(15.4,587),(16.3,659),(17.6,587),(24,440),(25,523),(26,494),(31,523),(32,587),(33,659),(34.5,784),(36,659),(38,587),(40,523),
    (56,440),(57,415),(58,440),(66,0),(70,523),(70.6,659),(71.2,784),(72.0,1046)]
for ts,fq in mb:
    if fq:
        a=tone(fq,2.0,'tri',2.2); b=tone(fq*2,1.2,'sin',4); a[:len(b)]+=0.3*b; add(a,ts,0.08)
# pads
def pad(fs,t0,d,g):
    n=int(d*SR); tt=np.arange(n)/SR; s=sum(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*f*2.01*tt) for f in fs)
    add(s*env(n,1.5,2.0),t0,g)
pad((110,164.8,220),0,14,0.012); pad((98,146.8,196),30,15,0.012); pad((87.3,130.8,174.6),56,9,0.01); pad((130.8,196,261.6),69,10,0.016)
# end card sting
for i,fq in enumerate((523,659,784,1046)): add(tone(fq,3.5,'tri',0.8),73.2+i*0.15,0.07)
mix=np.stack([L,Rr],1); mix=np.tanh(mix*1.4)*0.9
fade=np.clip((TOTAL-t)/1.5,0,1)[:,None]*np.minimum(1,t/0.5)[:,None]; mix*=fade
with wave.open('sound.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok',TOTAL)
