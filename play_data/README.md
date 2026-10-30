# Play data log (TremenVR)

Every work sends anonymous events to GoatCounter (site: thehush).
Path format: tremen/<work id>/<version>/<event>
- start-pc / start-phone / start-vr : opened and started
- step events (work-specific, numbered in play order)
- finish : reached the ending
- quit-at-... : closed the page before the ending (last state)

One file per day: YYYY-MM-DD.json = counts per path, copied from GoatCounter.
Never delete or overwrite old files. Before updating a work, read all files
for that work, find the step with the biggest drop, fix that first, bump the version.

## Since 2026-10-30: second counter we can read without a login
GoatCounter (thehush) login was lost, so trk() in w01-w05 ALSO sends every event to the public counter
abacus.jasoncameron.dev, namespace "tremenvr-play", key "<work>.v1.<event>" (non [A-Za-z0-9_.-] -> ".").
The cloud cannot reach it; tools/vr_collect.py runs inside Blender on the owner's PC (daily task
"VR プレイデータ収集（PC）"), writes C:\Users\81803\TremenFilm\vr_play\YYYY-MM-DD.json, which is copied
here as play_data/vr_YYYY-MM-DD.json. Values are cumulative totals since 2026-10-30.
New events in a new work: add them to the W table in tools/vr_collect.py, or they will not be read.
