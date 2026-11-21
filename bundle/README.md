# Team Rocklef: Track 1 gaze rig (GNM head)

Samsung XR Hackathon 2026, Track 1: synthetic eye movement and virtual camera rendering in Blender.
SRM Institute of Science and Technology.

```
scene.blend          textured GNM head, left/right eye bones, materials, fixed lights, locked camera (textures packed)
wrapper/eyes.py      eyes.move(h, v) / eyes.reset() / eyes.render()
renders/             frame_00.png ... frame_09.png, the ten clockwise renders (1024 x 1024 PNG)
metadata.json        one record per render: inputs, eye rotations, 2D pupil centres, camera matrix
README.md            this file
```

## Requirements

Blender only: 5.2 LTS (tested on Windows 11 with an NVIDIA RTX 4060 Laptop GPU). No add-ons and no Python packages.
`scene.blend` packs its textures, so nothing else has to be downloaded. A GPU is optional: the wrapper uses
OptiX/CUDA/HIP/oneAPI/Metal if present, otherwise the CPU (same image, slower).

## Run

From this folder:

```
blender -b scene.blend -P wrapper/eyes.py -- --sequence       # renders/frame_00..09.png + metadata.json
blender -b scene.blend -P wrapper/eyes.py -- --directions     # checks/center, left, right, up, down, reset
blender -b scene.blend -P wrapper/eyes.py -- --move 1 0 --out right.png
```

Options: `--samples N` (default 128, as saved), `--no-eyes` (skip the eye close-up renders),
`--root DIR` (output folder). If OptiX fails on an older NVIDIA driver, set `XR_CYCLES_DEVICE=CUDA`.

Inside Blender with `scene.blend` open (Scripting tab):

```python
import sys; sys.path.append(r"<this folder>/wrapper")
import eyes
eyes.move(0.5, -1.0)          # h, v in [-1, +1]
rec = eyes.render("test.png")  # writes the PNG and returns its metadata record
eyes.reset()
```

## Conventions

| Item | Value |
|---|---|
| `h`, `v` | normalised to [-1, +1]; values outside are clamped. `+h` = towards the **image right** (the subject's left), `+v` = up |
| Fixation target | `M + 0.35 m forward + h * 0.05 m right + v * 0.05 m up`, where `M` is the midpoint of the two eyeball centres |
| Eyes | true 3D rotation of each eye bone about its eyeball centre (Damped Track to the target), so the eyes converge |
| Camera | `CAM_Gaze`, locked 0.40 m forward of `M`, looking straight at the face; 70 mm lens on a 36 mm sensor, 1024 x 1024 |
| Lighting | one fixed studio rig (key, fill, rim, catchlight, studio HDRI); identical for every render |
| Sequence | `theta_k = 2*pi*k/10`, `h = sin(theta_k)`, `v = cos(theta_k)`, `k = 0..9`, starting at the top and going clockwise |

## metadata.json

One record per frame. Required fields:

| Field | Meaning |
|---|---|
| `frame`, `theta`, `input {h, v}` | frame index, angle in radians, normalised inputs |
| `eye_rotation_L`, `eye_rotation_R` | degrees, XYZ Euler, world frame: the rotation from straight ahead (-Y) to that eye's line of sight |
| `pupil_center_2D_L`, `pupil_center_2D_R` | pixels in the 1024 x 1024 render, origin top-left, x right, y down |
| `camera_matrix` | intrinsics K (OpenCV) |

Extra fields: `camera_extrinsics_RT` (world to camera) and `camera_projection_P = K[R|t]`, eye yaw/pitch, gaze
vectors, eyeball and pupil centres in 3D, the fixation target, its forward distance, the camera distance and the
vergence angle. `L` is the subject's left eye, which appears on the image right.

The 2D pupil centres are the projection of each eye's pupil point (the centre of the iris texture on the eyeball,
calibrated once when the scene was built and carried rigidly with the eye). They are checked against the pupils
detected in the rendered images by `tools/check_bundle.py` in the project repository.

## Assets and licences

GNM head model (Google, Apache-2.0). Skin, eye and hair textures, brows, lashes and hair were generated
procedurally by this project's scripts. The studio HDRI is Blender's bundled `interior.exr` (CC0).
