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

## Daily ad short (cloud, 12:13 JST) — since 2026-10-30
- Target = the latest "posted" episode whose "promo_posted" is empty (if none, the latest posted episode
  again with different segments). Make a contact sheet (ffmpeg fps=1/4,tile) of its 16x9 video, pick 3-5
  segments (15-28 s total): Tuck eye close-up, the letter text, the big/scary moment, the emotional beat.
  Do NOT show the final reveal (reply letter). Then tools/promo.py (EP, HOOK, SEGS) -> tuck_promo_epNN.mp4.
- Check 3 frames of the result, push to ranta-videos/tremenvr/tuck/, post to TikTok, YouTube (short),
  Instagram (REEL). Text: hook + "Full story on the TremenVR YouTube channel." Record promo_segs,
  promo_video, promo_posted in episodes.json.

## YouTube thumbnail (every episode, in the 19:13 posting run) — since 2026-10-30
- Contact sheet -> pick T (big clear Tuck eye/face or the scary moment, not the final reveal).
  EP, HOOK, T (, SHIFT) python3 tools/thumb.py <16x9 mp4> -> tuck_thumb_epNN.jpg. Look at it: text must not
  cover Tuck's eye. Push to ranta-videos/tremenvr/tuck/ and pass its raw URL as "videoThumbnailUrl" ONLY on
  the YouTube 16:9 post (own createScheduledPost call). If Metricool rejects it (VIDEO_THUMBNAIL_NOT_APPLICABLE),
  post again without the thumbnail. Never skip the post because of the thumbnail.

## Manga page (daily, cloud 17:37) — since 2026-10-30
- Target = latest "posted" episode without "manga_posted". Contact sheet -> write spec.json (8 panels, see
  tools/manga.py header) that tells the episode in order, ending on a quiet question (not the final reveal).
  Text in simple English, short. python3 tools/manga.py spec.json <16x9 mp4> -> tuck_manga_epNN.png (2:3)
  and tuck_manga_epNN_ig.jpg (4:5). Look at the page. Save spec to films/tuck/epNN/manga_spec.json.
- Post: instagram (POST, image _ig.jpg, isAiGenerated true), threads, bluesky (<=300 chars), facebook (POST),
  pinterest (2:3 png, board "TremenVR Games", pinLink YouTube channel). Text: "TUCK - Letter N in one page."
  + hook + "Watch the film on the TremenVR YouTube channel."

## Weekly review (Sunday 20:47, cloud) — since 2026-11-01
- Metricool analytics for the last 7 days per network and per post type (film / ad short / manga).
  Write films/tuck/insights.md (newest first): what worked, what did not, and 1-3 concrete changes.
- Allowed automatic changes: promo segment rules and hooks in this README, and the times of the cloud
  posting tasks (ad short, film, manga) by up to +-3 h toward better hours. Never change the PC task,
  never stop a task, never skip a day. Report the changes to the owner in Japanese.

## Video storage safety
- ranta-videos is deleted and re-created by the owner on the 1st of each month. Before that reminder,
  the reminder run copies every "stock" episode's mp4s into TremenVR films/tuck/stock_backup/.
  The posting run: if a stock video URL is not 200, restore it from stock_backup/ to ranta-videos first.

## Game link in EVERY post (since 2026-10-30)
Every TUCK post (film, ad short, manga, teaser, re-posts) must include the free game link in its text /
description, with the network code so plays can be counted per network:
  "Play TUCK free (phone, PC or VR): https://ranta46.github.io/TremenVR/tuck/?s=<code>"
  codes: youtube=yt, tiktok=tt, instagram=ig, facebook=fb, threads=th, bluesky=bs, pinterest=pin, x=x, linkedin=li
Networks get separate createScheduledPost calls when their link code differs (one call per network is fine).
Pinterest pinLink = https://ranta46.github.io/TremenVR/tuck/?s=pin . Bluesky: keep the whole text <= 300 chars.
Play data of the game: TremenVR play_data/ (w06), collected daily on the PC.
