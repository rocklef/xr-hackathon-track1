"""Pack the slide-6 submission: SRMIST_Rocklef.zip with exactly
scene.blend, wrapper/eyes.py, renders/ (10 frames), metadata.json and README.md at the top level.

    python tools/make_zip.py
"""
import glob
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "bundle")
OUT = os.path.join(ROOT, "SRMIST_Rocklef.zip")      # team_name.zip (team name = CollegeName_TeamName)

files = ["scene.blend", "wrapper/eyes.py", "metadata.json", "README.md"]
files += sorted(os.path.relpath(p, B).replace(os.sep, "/") for p in glob.glob(os.path.join(B, "renders", "frame_*.png")))
assert len(files) == 14, files
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in files:
        z.write(os.path.join(B, f), f)
print(OUT, round(os.path.getsize(OUT) / 2**20, 1), "MB,", len(files), "files")
