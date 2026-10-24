import sys, os, json, base64, time
from playwright.sync_api import sync_playwright
INIT = """
(()=>{let vt=0;const q=[];let id=0;
performance.now=()=>vt; Date.now=()=>1.7e12+vt;
window.requestAnimationFrame=cb=>{q.push([++id,cb]);return id};
window.cancelAnimationFrame=i=>{const k=q.findIndex(x=>x[0]===i);if(k>=0)q.splice(k,1)};
window.__step=ms=>{vt+=ms;const c=q.splice(0);c.forEach(([i,cb])=>{try{cb(vt)}catch(e){console.log('ERR '+e)}})};
Math.random=(()=>{let s=7;return()=>{s=(s*16807)%2147483647;return s/2147483647}})();
})();
"""
mode=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else "frames"
windows=json.loads(sys.argv[3]) if len(sys.argv)>3 else []
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    pg=b.new_page(viewport={"width":540,"height":960},device_scale_factor=2)
    pg.add_init_script(INIT)
    pg.route("**/three.min.js", lambda r: r.fulfill(path=os.environ.get("THREE_JS",os.path.join(os.path.dirname(os.path.abspath(__file__)),"three.r128.min.js")), content_type="application/javascript"))
    pg.route("**/gc.zgo.at/**", lambda r: r.fulfill(body="window.goatcounter={count:function(o){console.log('GC '+o.path)}};",content_type="application/javascript"))
    pg.on("console", lambda m: print(m.text, flush=True) if ("ERR" in m.text or "GC" in m.text or m.type=="error") else None)
    pg.on("pageerror", lambda e: print("pageerror:",e, flush=True))
    pg.goto("file://"+os.path.abspath(os.environ["WORK_HTML"])+"#auto")
    os.makedirs(out,exist_ok=True); cdp=pg.context.new_cdp_session(pg)
    last=""; t0=time.time()
    for i in range(int(140*30)):
        pg.evaluate("__step(33.333)")
        t=i/30
        if mode=="probe" and i%15==0:
            c=pg.evaluate("document.getElementById('cap').style.opacity==='1'?document.getElementById('cap').textContent:''")
            if c and c!=last: print(f"{t:6.1f} CAP {c}",flush=True); last=c
            if i%300==0: print(f"{t:6.1f} hud", pg.evaluate("document.getElementById('hud').textContent"), flush=True)
            if i%600==0:
                r=cdp.send("Page.captureScreenshot",{"format":"jpeg","quality":70}); open(f"{out}/p{int(t):03d}.jpg","wb").write(base64.b64decode(r["data"]))
        if mode=="cap" and any(a<=t<b for a,b in windows):
            r=cdp.send("Page.captureScreenshot",{"format":"jpeg","quality":90}); open(f"{out}/f{i:05d}.jpg","wb").write(base64.b64decode(r["data"]))
        if pg.evaluate("!document.getElementById('ending').hidden"):
            print(f"{t:6.1f} ENDING", flush=True)
            if mode=="probe": break
            if not any(t<b for a,b in windows): break
    print("elapsed",round(time.time()-t0,1))
    b.close()
