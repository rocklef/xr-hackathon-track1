# Headless Track 1 renderer: Blender 5.2 LTS on Linux, rendering the bundle with the wrapper (CPU by default).
#
#   docker build -t rocklef-gaze .
#   docker run --rm -v "$PWD/out:/out" rocklef-gaze                       # 10 clockwise frames + metadata.json
#   docker run --rm -v "$PWD/out:/out" rocklef-gaze --directions --no-eyes
#   docker run --rm --gpus all -e XR_CYCLES_DEVICE=CUDA -v "$PWD/out:/out" rocklef-gaze   # NVIDIA GPU
#
# Then check the output:  python tools/check_bundle.py out   (needs requirements.txt)
FROM ubuntu:24.04

ARG BLENDER_VERSION=5.2.4
ARG BLENDER_SERIES=5.2
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates wget xz-utils libxi6 libxxf86vm1 libxfixes3 libxrender1 libxkbcommon0 libsm6 libice6 \
        libgl1 libegl1 libglu1-mesa libx11-6 libxext6 libwayland-client0 libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*
RUN wget -q https://download.blender.org/release/Blender${BLENDER_SERIES}/blender-${BLENDER_VERSION}-linux-x64.tar.xz \
    && tar -xf blender-${BLENDER_VERSION}-linux-x64.tar.xz -C /opt \
    && rm blender-${BLENDER_VERSION}-linux-x64.tar.xz \
    && ln -s /opt/blender-${BLENDER_VERSION}-linux-x64/blender /usr/local/bin/blender

WORKDIR /app
COPY bundle/scene.blend bundle/README.md ./
COPY bundle/wrapper ./wrapper

ENTRYPOINT ["blender", "-b", "--factory-startup", "/app/scene.blend", "-P", "/app/wrapper/eyes.py", "--", "--root", "/out"]
CMD ["--sequence", "--no-eyes"]
