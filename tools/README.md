# Tools for the daily TremenVR run
- cap.py: headless capture with virtual time (Playwright + swiftshader).
  WORK_HTML=wNN/index.html python3 tools/cap.py probe probe_dir      -> logs captions/HUD/ENDING times
  WORK_HTML=wNN/index.html python3 tools/cap.py cap frames '[[a,b],...]' -> 1080x1920 frames f%05d.jpg (frame = t*30)
  Needs: the work supports #auto (autopilot, tracking off), has #cap caption, #hud, #ending elements.
  Slow: ~0.5 s per frame. Capture only the windows the ad needs.
- ad_template.py: copy and edit per work (SEG windows + overlay lines, title, end card).
  FRAMES=frames OUTDIR=ad_out AD_MP4=wNN_ad.mp4 python3 tools/ad_template.py
- three.r128.min.js: local copy so capture works without network.
