# TUCK film pipeline (one episode per day)
Read BIBLE.md first. Character and world must stay consistent.

## Where things are (user's Windows PC, Blender 5.2 via Blender MCP)
- Episode folders: C:\Users\81803\TremenFilm\epNN\  (tuck_epNN.blend, frames\, raw.mp4, render_status.json)
- Start a new episode by opening the previous episode's .blend and saving it as the new one. Reuse Tuck,
  the street, lamps, post office, door house, the Tall One. Delete the old animation, cameras and markers
  (Cam_* objects, timeline markers) and build new ones. New places can be added (keep the same style).
- Tuck's parts are children of the empty "Tuck". Animate the root (walk = tools in ep01: bob, ±3° roll,
  legs swing ±18° every 8 frames), Tuck_Eyelid location z (0.47 closed, 0.6 normal, 0.665 wide),
  material "Bulb" emission strength (0 off, 3 afraid, 25 normal, 45 happy) + light "BulbGlow".
- Cameras: one camera per shot, bound to timeline markers. 24 fps. Episode 60-90 s (1440-2160 frames).

## GPU safety (Intel UHD laptop) — never break these
- EEVEE only, 1280x720, 24 samples, use_raytracing False, NO world volume / volumetrics, NO heavy
  transparency. Fog = the "TuckFog" node group on every material (copy it to new materials).
- Previews: 40% size, 8 samples, sleep 0.5 s between frames.
- Final render: tools/blender_render_timer.py start(ep_dir,end). It rests between frames and stops itself
  if a frame comes out empty. Check render_status.json. Never run two heavy renders at once.

## Finish (cloud side)
1. In Blender: tools/blender_encode.py encode(ep_dir) -> raw.mp4. Stage it to the cloud.
2. Sound: copy tools/sound_ep01.py, change the cue times for the new episode (frame/24 = seconds),
   total = film length + 6 s end card.
3. tools/post.py raw.mp4 with EP, TITLE, HOOK, NEXT env -> tuck_epNN_16x9.mp4 and tuck_epNN_9x16.mp4.
4. Upload both to ranta-videos/tremenvr/tuck/ and post (see episodes.json for history).

## Stock system (so a day is never missed) — since 2026-10-29
- episodes.json "status": "rendering" (render started on the PC) -> "stock" (finished mp4s pushed to
  ranta-videos/tremenvr/tuck/, not posted yet) -> "posted".
- PC runs (10:47 and 15:47): first finish any done render into stock; then, if stock < 3 and no render is
  running, build the next episode and start its render.
- Cloud run (19:13, no PC needed): post the OLDEST "stock" episode to all networks, mark "posted".
  If there is no stock, post a 10-15 s teaser cut from the latest posted episode (never skip a day).
- Cloud runs (11:17, 16:17, 21:41): check that the PC tasks are not suspended (device_absent), re-enable
  them and alert the owner; 21:41 also fills any network that has no post today.
