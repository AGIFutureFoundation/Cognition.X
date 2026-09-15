#!/usr/bin/env python3
"""Offline narration for the film kit.

    echo "text" | python3 tts.py --out clip.wav [--engine kokoro|piper] [--voice af_heart] [--speed 1.0]

kokoro (default): kokoro-onnx with kokoro-v1.0.onnx + voices-v1.0.bin (CX_KOKORO_DIR);
piper: a piper .onnx voice (CX_PIPER_VOICE). Writes 16-bit PCM wav."""
import argparse, os, sys, subprocess
ap = argparse.ArgumentParser()
ap.add_argument('--out', required=True); ap.add_argument('--engine', default=os.environ.get('CX_TTS', 'kokoro'))
ap.add_argument('--voice', default=os.environ.get('CX_TTS_VOICE', 'af_heart')); ap.add_argument('--speed', type=float, default=float(os.environ.get('CX_TTS_SPEED', '1.0')))
a = ap.parse_args(); text = sys.stdin.read().strip()
if a.engine == 'kokoro':
    import numpy as np, soundfile as sf
    from kokoro_onnx import Kokoro
    d = os.environ.get('CX_KOKORO_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kokoro'))
    k = Kokoro(os.path.join(d, 'kokoro-v1.0.onnx'), os.path.join(d, 'voices-v1.0.bin'))
    samples, sr = k.create(text, voice=a.voice, speed=a.speed, lang='en-us')
    sf.write(a.out, (np.asarray(samples) * 32767).astype('int16'), sr, subtype='PCM_16')
else:
    voice = os.environ.get('CX_PIPER_VOICE', os.path.dirname(os.path.abspath(__file__)) + '/voices/en-us-ryan-high.onnx')
    subprocess.run(['python3', '-m', 'piper', '-m', voice, '--length-scale', str(1/a.speed), '--sentence-silence', '0.3', '-f', a.out], input=text.encode(), check=True)
