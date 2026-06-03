#!/usr/bin/env python3
import subprocess


class Engine:
    def __init__(self):
        self.gpu = self._probe()

    def _probe(self):
        try:
            r = subprocess.run(["ffmpeg", "-encoders"], capture_output=True, text=True, timeout=5)
            if "nvenc" in r.stdout:
                return "nv"
        except:
            pass
        return "cpu"

    def _hw(self):
        return ["-hwaccel", "cuda"] if self.gpu == "nv" else []

    def _vc(self):
        return {"nv": "h264_nvenc"}.get(self.gpu, "libx264")

    def _run(self, c):
        return subprocess.run(c, capture_output=True, timeout=300).returncode == 0

    def trim(self, s, d, t0, t1):
        return self._run(["ffmpeg", "-y"] + self._hw() + ["-i", s, "-ss", str(t0), "-to", str(t1), "-c:v", self._vc(), "-c:a", "copy", d])

    def resize(self, s, d, w, h):
        return self._run(["ffmpeg", "-y"] + self._hw() + ["-i", s, "-vf", f"scale={w}:{h}", "-c:v", self._vc(), "-c:a", "copy", d])

    def convert(self, s, d):
        return self._run(["ffmpeg", "-y"] + self._hw() + ["-i", s, "-c:v", self._vc(), "-c:a", "copy", d])
