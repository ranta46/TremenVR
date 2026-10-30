# VR play data reader. Run INSIDE Blender on the owner's PC (execute_blender_code), because the cloud
# cannot reach the counter service. Reads public counters (abacus.jasoncameron.dev, namespace
# tremenvr-play, key = <work>.<ver>.<event>) for every possible event of w01-w05 and writes
# C:\Users\81803\TremenFilm\vr_play\YYYY-MM-DD.json  (only keys with a value > 0).
# The works send events with trk() -> both GoatCounter (thehush) and this counter (since 2026-10-30).
# Counts are cumulative totals since 2026-10-30 (diff two days for daily numbers).
import urllib.request, json, os, time, datetime
NS="tremenvr-play"; OUT=r"C:\Users\81803\TremenFilm\vr_play"
SRC=["direct","profile","yt","youtube","tt","tiktok","ig","instagram","fb","facebook","th","threads",
     "bs","bluesky","pin","pinterest","all","hub","x","twitter","li","link","bio","ad","ads"]
R=lambda a,b: [str(i) for i in range(a,b+1)]
COMMON=["finish"]+["start-"+d for d in ("pc","phone","vr")]+["open-"+s for s in SRC]+["from-"+s for s in SRC]
W={
 "w01": ["all-lit","stare","stare-passed"]+["lamp-"+i for i in R(0,20)]
        +["quit-at-lamps-"+i+x for i in R(0,20) for x in ("","-stare")],
 "w02": ["catch-1","catch-6","catch-12","catch-20","catch-26","comet","comet-hit","comet-woken","ember-hit","embers-start"]
        +["quit-at-"+p+"-"+i for p in ("intro","stars","red","comet","sky") for i in R(0,40)],
 "w03": ["dark","eye","eye-held","rise","whoa"]+["found-"+i for i in R(0,12)]
        +["quit-at-"+p for p in ("menu","","dark","eye","lights","rise","sink","surface")]+["quit-at-find-"+i for i in R(0,12)],
 "w04": ["game","gran","half","held","quake","whoa"]+["tag-"+i for i in R(0,5)]
        +["quit-at-"+p for p in ("menu","","dawn","gran","quake","wake")]+["quit-at-game-"+i for i in R(0,20)],
 "w05": ["echo","face","follow","look-down","rise","storm","touch","whoa"]+["bell-"+i for i in R(0,12)]
        +["quit-at-"+p for p in ("menu","","edge","face","glow","rise","spiral","storm")]+["quit-at-echo-"+i for i in R(0,12)],
}
def key(w,ev,ver="v1"):
    import re
    return re.sub(r"[^A-Za-z0-9_.-]",".",f"{w}.{ver}.{ev}")[:64]
def get(k):
    try:
        r=urllib.request.urlopen(urllib.request.Request(f"https://abacus.jasoncameron.dev/get/{NS}/{k}",headers={"User-Agent":"tremenvr"}),timeout=10)
        return json.loads(r.read()).get("value",0)
    except Exception:
        return 0   # 404 = never happened
def collect():
    os.makedirs(OUT,exist_ok=True); res={}
    for w,evs in W.items():
        for ev in COMMON+evs:
            v=get(key(w,ev))
            if v: res.setdefault(w,{})[ev]=v
            time.sleep(0.05)
    d=datetime.date.today().isoformat()
    data={"date":d,"source":f"abacus {NS} (cumulative since 2026-10-30)","works":res}
    json.dump(data,open(os.path.join(OUT,d+".json"),"w"),indent=1)
    return data
# usage in Blender: exec(open(path).read()); print(json.dumps(collect()))
def collect_bg():
    # runs in a background thread so Blender (and a running render) is not blocked; result file appears in OUT
    import threading; t=threading.Thread(target=collect,daemon=True); t.start(); return "started"
