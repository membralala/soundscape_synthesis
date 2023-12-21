import argparse
import os
import pathlib
import sys

import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import yaml

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str, help="path to the wav file")
parser.add_argument("-o", "--out", type=str, default="", help="outpath")
parser.add_argument(
    "--config", type=str, default="./default.yaml", help="path to the config file"
)
args = parser.parse_args()

# Get config
config_path = pathlib.Path(args.config)
try:
    with open(config_path, "r") as f:
        config = yaml.load(f.read(), yaml.Loader)
except FileNotFoundError:
    print("Config File Not Found at {}".format(config_path))
    sys.exit()

# Get audio configs
sampling_rate = config["audio"].get("sampling_rate")
hop_length = config["audio"].get("hop_length")
bins_per_octave = config["audio"].get("bins_per_octave")
num_octaves = config["audio"].get("num_octaves")
n_bins = int(num_octaves * bins_per_octave)
n_iter = config["audio"].get("n_iter")
cqt_bit_depth = config["audio"].get("cqt_bit_depth")
if cqt_bit_depth not in ("float64", "float32"):
    raise TypeError(f"Datatype {cqt_bit_depth} for cqt bitdepth is unknown.")

# Get audiofile
audiofile_path = pathlib.Path(args.filename)
try:
    y, sr = sf.read(audiofile_path)
except sf.LibsndfileError:
    print(f"Audiofile file not found at {audiofile_path}.")
    sys.exit()

if sr != sampling_rate:
    print(f"Resampling audio: {sr} -> {sampling_rate}")
    y = librosa.resample(y, sr, sampling_rate)

# Calculate cqt
C_complex = librosa.cqt(
    y=y,
    sr=sampling_rate,
    hop_length=hop_length,
    bins_per_octave=bins_per_octave,
    n_bins=n_bins,
)
C = np.abs(C_complex)
if cqt_bit_depth == "float32":
    C = C.astype("float32")

# Make plot
fig, ax = plt.subplots()
img = librosa.display.specshow(
    librosa.amplitude_to_db(C, ref=np.max),
    sr=sampling_rate,
    x_axis="time",
    y_axis="cqt_note",
    ax=ax,
    hop_length=hop_length,
    bins_per_octave=bins_per_octave,
)
ax.set_title("Constant-Q power spectrum")
fig.colorbar(img, ax=ax, format="%+2.0f dB")

# Save plot and meta information
outpath = pathlib.Path(args.out) / audiofile_path.stem
try:
    os.makedirs(outpath)
except OSError:
    print(f"Path {outpath} already exists.")
    sys.exit()

audio_outpath = outpath / audiofile_path.name
yaml_outpath = audio_outpath.with_suffix(".yaml")
plot_outpath = audio_outpath.with_suffix(".png")

sf.write(file=audio_outpath, data=y, samplerate=sampling_rate)
plt.savefig(plot_outpath)

meta = config["audio"]
meta.pop("cqt_fmin")
meta.pop("n_iter")
with open(yaml_outpath, "w") as f:
    f.write(yaml.dump(meta, Dumper=yaml.Dumper))
