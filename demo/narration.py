"""Voiceover for the GNM demo video (edge-tts neural voice) + word timings for the subtitles.

    python demo/narration.py [--voice en-US-AndrewNeural]

Writes demo/build/voice/<scene>.mp3 and <scene>.json (word timings in seconds).
"""
import argparse
import asyncio
import json
import os

import edge_tts

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "demo", "build", "voice")

# Order follows the team's flow: plain problem (applications, then why it is hard) -> title -> literature -> gap -> solution -> architecture -> comparison
# -> novelty/applications -> future -> contact.
SCRIPT = {
    "open": "Watch someone's eyes, and you know what they're thinking about. Every glance, every blink, says "
            "something.",
    "apps": "That's why machines are learning to read our eyes. A headset sharpens only where you look. A car "
            "warns a driver whose eyes leave the road. People who can't speak type with their eyes. And a child's "
            "gaze can help doctors spot autism early.",
    "problem": "Every one of these systems has to learn from real faces, with eyes that move like real eyes. "
               "Filming people is slow, expensive and private. And most digital eyes look dead: glassy, staring "
               "and robotic.",
    "title": "This is Synthetic Eyes: eye movement and virtual camera rendering, built brick by brick by Team "
             "Rocklef from SRM Institute of Science and Technology.",
    "literature": "Researchers built 3D head models like FLAME and GNM, and eye tools like UnityEyes. But the head "
                  "models come without lifelike skin or eyes, and the eye tools only show the eye.",
    "solution": "So we built photoreal skin, living eyes and natural motion, all driven by one Python script.",
    "textures": "Every texture is painted straight onto the head's own UV map, so it wraps on with no "
                "seams. Eight faces, of different ages and backgrounds, with pores, freckles, wrinkles, and "
                "eyebrows drawn hair by hair.",
    "iris": "Each eye gets its own 4K iris, with fibres, crypts and a ring of colour, and a pupil that really "
            "traps the light.",
    "audit": "Then we check our own work: every UV seam on the head is measured against the skin's natural detail. "
             "All eight sets pass.",
    "motion": "Type Left, Right, or Generate Motion, and the script renders the frames and the video. The eyes "
              "jump at real human speeds, settle, drift, and blink: fast to close, slower to open. The head "
              "follows a little, and the eyelids follow the eyes.",
    "timeline": "The blend file plays a whole expression on Blender's timeline: surprise, a suspicious squint and "
                "an eye roll, with eyelids, pupils and brows moving together.",
    "identity": "Change the face with shape sliders, and the eyes stay perfectly in place.",
    "architecture": "Under the hood: the head model rebuilt in Python, expressions solved inside its own eye space, "
                    "textures baked through its UV map, and a control wrapper to look, open the eyelids and "
                    "blink.",
    "compare": "Compared with today's tools, ours gives a whole photoreal face, a separate iris for each eye, "
               "human motion over time, and eyelids that follow the gaze.",
    "novelty": "That opens the door to lifelike avatars, safer cars, better eye trackers, and medical research.",
    "future": "Next, we'll carry the textures over to FLAME, add infrared headset cameras, and run it all in real "
              "time.",
    "outro": "Thank you, from Team Rocklef.",
}


async def synth(key, text, voice, rate):
    com = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    words, audio = [], bytearray()
    async for ch in com.stream():
        if ch["type"] == "audio":
            audio.extend(ch["data"])
        elif ch["type"] == "WordBoundary":
            words.append({"w": ch["text"], "t0": ch["offset"] / 1e7, "t1": (ch["offset"] + ch["duration"]) / 1e7})
    with open(os.path.join(OUT, f"{key}.mp3"), "wb") as f:
        f.write(audio)
    with open(os.path.join(OUT, f"{key}.json"), "w") as f:
        json.dump({"text": text, "words": words}, f, indent=1)
    print(f"  {key:12s} {words[-1]['t1']:5.1f}s  {len(words)} words")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="en-US-AndrewNeural")
    ap.add_argument("--rate", default="+6%")
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    for k, t in SCRIPT.items():
        if a.only and k not in a.only.split(","):
            continue
        for attempt in range(5):
            try:
                await synth(k, t, a.voice, a.rate)
                break
            except edge_tts.exceptions.NoAudioReceived:
                print(f"  {k}: no audio, retry {attempt + 1}")
                await asyncio.sleep(2 + 2 * attempt)
        else:
            raise SystemExit(f"edge-tts failed for {k}")


if __name__ == "__main__":
    asyncio.run(main())
