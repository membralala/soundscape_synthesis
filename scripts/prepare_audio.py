import os
import pathlib

import librosa
import numpy as np
import soundfile as sf

AUDIOPATH = "soundscapes"
OUTPATH = "soundscapes_corr"

SAMPLERATE = 44100

os.makedirs(OUTPATH, exist_ok=True)
audiopath = pathlib.Path(AUDIOPATH)
outpath = pathlib.Path(OUTPATH)


overall_max = 0  # Precalculated max: 0.14045432368947608
for fname in audiopath.glob(f"*.wav"):
    y, sr = sf.read(fname)
    # Resample if necessary
    if sr != SAMPLERATE:
        print(f"Resampling: {sr} -> {SAMPLERATE}")
        y = librosa.resample(y, orig_sr=sr, target_sr=SAMPLERATE)
    # Remove DC offset
    y -= np.mean(y)
    # Calculate the absolute max for normalization purposes
    overall_max = max(overall_max, np.max(np.abs(y)))
    # Write file to new path
    sf.write(outpath / fname.name, y, SAMPLERATE)


# Open overwrite all files to normalize based on the overall max
for fname in outpath.glob(f"*.wav"):
    y, _ = sf.read(fname)
    sf.write(fname, y / overall_max, SAMPLERATE)
