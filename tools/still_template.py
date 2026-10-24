import sys, json, base64
from playwright.sync_api import sync_playwright
opts=json.loads(sys.argv[1]); out=sys.argv[2]; w,h=(540,960) if opts.get("v",1) else (960,540)
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    pg=b.new_page(viewport={"width":w,"height":h},device_scale_factor=2)
    pg.route("**/three.min.js", lambda r: r.fulfill(path="/home/claude/promo/three_src/build/three.min.js", content_type="application/javascript"))
    pg.route("**/gc.zgo.at/**", lambda r: r.abort())
    pg.on("console", lambda m: print("console:",m.text) if m.type=="error" else None)
    pg.on("pageerror", lambda e: print("pageerror:",e))
    pg.goto("file:///home/claude/tremen/w01/index.html")
    pg.wait_for_timeout(1500)
    pg.evaluate("document.getElementById('intro').hidden=true")
    pg.evaluate(f"window.__still({json.dumps(opts)})")
    pg.wait_for_timeout(1500)
    cdp=pg.context.new_cdp_session(pg)
    r=cdp.send("Page.captureScreenshot",{"format":"png"})
    open(out,"wb").write(base64.b64decode(r["data"]))
    b.close()
