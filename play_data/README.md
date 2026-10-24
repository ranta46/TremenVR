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
