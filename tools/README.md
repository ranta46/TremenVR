# Tools for the daily TremenVR run
- cap.py: headless capture with virtual time (Playwright + swiftshader).
  WORK_HTML=wNN/index.html python3 tools/cap.py probe probe_dir      -> logs captions/HUD/ENDING times
  WORK_HTML=wNN/index.html python3 tools/cap.py cap frames '[[a,b],...]' -> 1080x1920 frames f%05d.jpg (frame = t*30)
  Needs: the work supports #auto (autopilot, tracking off), has #cap caption, #hud, #ending elements.
  Slow: ~0.5 s per frame. Capture only the windows the ad needs.
- ad_template.py: copy and edit per work (SEG windows + overlay lines, title, end card).
  FRAMES=frames OUTDIR=ad_out AD_MP4=wNN_ad.mp4 python3 tools/ad_template.py
- three.r128.min.js: local copy so capture works without network.
- Landscape (YouTube, normal video so description links are clickable):
  VW=960 VH=540 WORK_HTML=... python3 tools/cap.py cap frames16 '[...]'  -> 1920x1080 frames
  copy tools/ad_template_16x9.py and edit SEG / title / end card.
- One tap to play: index.html (the profile link) jumps straight to the newest work. Update LATEST in index.html
  (meta refresh, the script and the link) to the new wNN/ every day. all.html is the list of all works.
- Every work: tapping anywhere on the intro starts the game; links carry ?s=<source> (yt, ytshort, tt, ig, fb, th, bs, pin, x, li, profile)
  and the work sends open-<src> / from-<src> events. Ending card has "More free games" -> ../all.html.
