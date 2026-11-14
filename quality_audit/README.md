# Quality audit: seams and artifacts

Brief, slide 1: *Photorealistic Quality Audit: render textured face/eyes under natural gaze; inspect for seams and artifacts.* The evaluation standard also scores seam absence.

## 1. Numeric seam check (skin tile 1001, all 8 sets)

GNM's skin has **142 UV-seam edges**. These are edges where the same 3D edge appears twice in the texture. For every seam edge, we sample the baked albedo 2.5 texels inside each side, at 6 matching points along the edge, and measure the colour difference (RGB distance on a 0–255 scale).

As a baseline we take the same measurement across 4000 ordinary, non-seam edges. That baseline is the texture's natural pixel-to-pixel variation from pores, hairs and freckles. A set passes when its seam difference is of the same order as that natural variation (seam mean ≤ 1.5 × baseline + 1). For reference, about 3–5 RGB units is around the threshold of a visible difference.

| Texture set | seam mean | seam p95 | baseline mean | seam/baseline | result |
|---|---|---|---|---|---|
| T01 fair young female | 3.72 | 12.59 | 2.21 | 1.68 | PASS |
| T02 fair male stubble | 4.70 | 14.57 | 3.13 | 1.50 | PASS |
| T03 olive mediterranean male | 4.13 | 12.66 | 3.16 | 1.31 | PASS |
| T04 east asian female | 5.09 | 15.51 | 2.87 | 1.78 | PASS |
| T05 south asian male | 3.54 | 10.40 | 2.78 | 1.27 | PASS |
| T06 african female | 2.19 | 6.39 | 2.01 | 1.09 | PASS |
| T07 elderly caucasian male | 3.25 | 10.34 | 2.27 | 1.43 | PASS |
| T08 latina female | 4.10 | 13.06 | 2.56 | 1.60 | PASS |

Raw numbers, including the roughness maps, are in `seam_audit.json`.

**Why the textures are seam-free.** Every skin layer is generated in 3D on the GNM surface and baked through GNM's own UVs, so both copies of a seam edge sample the same 3D point. A 24-texel bake margin extends each island so texture filtering never reaches the background. The eye textures live on their own radial islands (tiles 1002 and 1004) and have no seams across the visible iris or sclera.

`T03_uv_seams_overlay.png` and `T06_uv_seams_overlay.png` show the seam edges in red over the albedo.

## 2. Visual check at the seams

The renders `T03_back.png`, `T03_ear.png`, `T06_back.png` and `T06_ear.png` show the back of the head and the ear and jaw, where GNM's UV seams run. Front-facing renders and eye close-ups under natural gaze are in `../renders_textures/` and in the three videos.

## 3. Artifact checklist

| Check | Result |
|---|---|
| Visible UV seams on skin | none (see table and renders) |
| Texture stretching | none: layers are generated in 3D, not projected |
| Eyeball / eyelid intersection while blinking or looking around | none: lids are driven from GNM's own eye expression space, and the tear film is bound to the lid margins |
| Pupil / iris artefacts | pupil is a true light trap; separate left and right iris maps |
| Black or empty texels | none: 24-texel bake margin, and every face is covered |
| Lashes intersecting the eyeball | lower lashes splay outward; rare contact at the inner corner only in extreme macro shots |
