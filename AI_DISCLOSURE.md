# AI disclosure

Team Rocklef (Sree Rohith Balaji, Thackshanaramana), Samsung PRISM Hackathon 2026, XR Perception Group, 3D Assets Track.

## AI tools we used

| Tool | What it was used for |
|---|---|
| **Claude** (Anthropic), through Claude Code | Coding assistant. It wrote and debugged the Python scripts (Blender `bpy` scene, rig and render scripts, procedural texture generation, the motion model, the control wrappers, the checker), ran the renders, and drafted the README and documentation. The team set the goals and design, reviewed the results, and judged every render. |
| **Microsoft Edge neural text-to-speech** (`edge-tts`, voice `en-US-AndrewNeural`) | The voiceover of the demo video (`demo/narration.py`). The script was written by the team with Claude's help. |

## What is not AI-generated

- **No generative image or video models were used.** Every skin, eye, hair and brow texture is computed by our own
  Python code (`gnm_rig/textures.py`, `gnm_rig/iris_hq.py`, `gnm_rig/eye_tiles.py`) and baked through GNM's UV
  layout. No textures were downloaded, scanned or produced by text-to-image tools.
- **Every image and video in this repository was rendered by Blender's Cycles path tracer** from the 3D scene,
  including the rubric videos, the texture renders, the Timeline `.blend` and the demo footage.
- **Eye motion** comes from our scripted motion model (`gnm_rig/motion.py`: saccades, fixations, blinks), not from a
  learned or generated animation.

## Third-party models and assets

- **GNM v3 head model** (Google, Apache-2.0): a parametric head model learned from 3D scans. We use its mesh, UV
  layout, rig, identity and expression spaces. It is a statistical shape model, not a generative AI tool.
- **Studio HDRI** `interior.exr`: bundled with Blender (CC0).
- `legacy/` (our earlier exploration) uses MakeHuman/MPFB assets (CC0).
