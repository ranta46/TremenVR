# VR design rules (read before every new work)

The owner's verdict on w02 "Pip's Star Jar": "just a bad game". It was a flat tap-to-catch game
that would be the same on a 2D screen. Never make that again. Every work must be an
experience that is better *because you are inside it*.

## The test (do this before writing code)
Write the concept in 5 lines. Then answer honestly:
1. Would this be just as fun as a flat phone game? -> If yes, REJECT and think again.
2. What is the ONE body action that makes it work? (look around, look behind you, hold still,
   look up, lean in, follow with your eyes, reach/point, turn to face, slow your breath...)
3. What is the "whoa" moment in the first 15 seconds? (scale, something huge, something close,
   something behind you, a character looking right at you)
4. How does the character react to *you* (your gaze, your stillness, where you look)?
5. What does the player remember tomorrow?
Write the answers into works.json as "vr_hook". If any answer is weak, change the concept.

## What makes it VR (use at least 3)
- Presence and scale: giant things, deep drops, high places, tiny you, huge sky.
- 360 degrees: important things happen to the side and BEHIND the player. Sound tells them to turn.
- Gaze as a verb: looking lights, reveals, calms, scares, or attracts things. Not looking matters too.
- Stillness / body control: "don't move", "hold your gaze", "look away now".
- A character that faces you, comes close, whispers, follows your eyes, remembers what you did.
- Spatial sound (THREE.PositionalAudio or panner): voices and dangers have a direction.
- One clear goal, one rising tension, one climax, one quiet ending. 2-3 minutes.
- Fear, wonder, or warmth. Pick one emotion and push it.

## Never
- Tapping falling objects, score counters as the main fun, menus, timers as the only tension.
- Things only in front of the camera. Flat UI games with a 3D background.
- More than 2 lines of instructions. If it needs a tutorial, the idea is wrong.

## Input on every device (same experience)
- VR headset: head look + controller "select" (or gaze dwell).
- Phone: tilt-to-look with the gyroscope (DeviceOrientation; on iPhone ask permission on the
  first tap) + drag to look as fallback. Tap = select. Tell the player "Turn your phone to look around."
- PC: drag/mouse to look, click = select.

## Quality check before publishing
- Render 4 stills (start, whoa moment, climax, ending) and look at them. Is the character
  clearly visible and readable? Is the space impressive? Is the climax readable without text?
- Play #auto to the end. Fix anything dull for more than 10 seconds.
- Read the play data of past works (play_data/): where people quit. Do not repeat that pattern.

## Good examples
- w01 The Signal Tower: high tower in the night, look at lamps to light them, a giant
  light-eater rises behind the town, it stares at you and you must not move. (gaze + stillness + scale)

## How to make every new work (owner's rule since 2026-10-31; model = w06 "TUCK: Night Delivery")
1. Start from games or films that are already loved worldwide. Pick 2-3 and name them in works.json
   "references" (w06: Moss = guide a tiny hero; Five Nights at Freddy's / Alan Wake = light vs things in the dark;
   Squid Game "red light, green light" = don't move while watched). Take their core fun, not their look or names.
2. ONE verb the body does, explained in one line on the start card ("He only walks where you look").
   The player must understand what to do within 5 seconds of starting.
3. A real game loop: goal (deliver 3 / reach X), pressure (things coming at you), a twist stage (new rule
   at the climax), and a result screen (time, score, rank S-C, saved best) so people want to play again.
4. 360 degrees: the route or the threats go all the way around the player; the "whoa" (something huge,
   something close) is staged so the game makes the player look at it (freeze + "LOOK UP").
5. Characters show who they are through what they do in the game (Tuck: afraid of the dark -> only walks
   in your light; hides in his box when hit; bows after a delivery). Keep the series bible rules.
6. Before publishing: auto-play to the end (#auto), take stills of start / whoa / climax / ending and look
   at them, 2-3 minutes for a human. Every step of the loop sends a trk() event (abacus, version tag).

## Must be fun for people who do NOT know the IP (owner's rule since 2026-10-31)
- Never require knowing the character, the films or the lore. The first 10 seconds work with zero context:
  a clear goal, a clear threat, a clear action. Story lines are short and optional flavour.
- Introduce the character by action, not by name or backstory ("A tiny robot needs your light" works for
  everyone; "Letter 3 from the series" works for nobody new).
- Never reference earlier episodes/works as something the player should know. Callbacks are bonus only.
- Test question before publishing: "Would a stranger from a TikTok ad enjoy this with no explanation?"
  If not, change it.
