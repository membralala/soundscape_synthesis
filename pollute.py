import argparse
import importlib
import os
import pathlib

import soundfile as sf
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("src", type=str)
parser.add_argument("-o", "--out", type=str, required=True)
parser.add_argument("--config", default="simple")
parser.add_argument("--cargs", nargs="+")
args = parser.parse_args()

args = parser.parse_args()

# Get paths
src_path = pathlib.Path(args.src)
out_path = pathlib.Path(args.out)
os.makedirs(out_path, exist_ok=True)

# Get config module.
config = importlib.import_module(f"pollutions.{args.config}")

# Save setup_config
setup = {"config": args.config, "config_args": args.cargs}
with open(out_path / "_pollution_setup.yaml", "w") as f:
    f.write(yaml.dump(setup, Dumper=yaml.Dumper))

audio_out_path = out_path / "test_audio"
os.makedirs(audio_out_path, exist_ok=True)

# Perform selected pollution
for fname in src_path.glob("*.wav"):
    # Assuming samplerate = 44100 Hz and depth = 16 bit.
    # Assuming a method pollute(model, fname, out_path) -> None
    # in each config as interface.
    print(f"Processing {fname} ...")
    config.pollute(fname, audio_out_path, args.cargs)
