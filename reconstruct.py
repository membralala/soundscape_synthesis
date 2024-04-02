import argparse
import importlib
import os
import pathlib

import torch
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("src", type=str)
parser.add_argument("-o", "--out", type=str, required=True)
parser.add_argument("--config", default="simple")
parser.add_argument("--model", required=True)
args = parser.parse_args()

# Get paths
src_path = pathlib.Path(args.src)
out_path = pathlib.Path(args.out)
os.makedirs(out_path, exist_ok=True)
# Get config module.

config = importlib.import_module(f"configs.{args.config}")

# Load model
torch.set_grad_enabled(False)
model = torch.jit.load(args.model).eval().double()

# Save setup_config
setup = {"model": args.model, "config": args.config}
with open(out_path / "_reconstruction_setup.yaml", "w") as f:
    f.write(yaml.dump(setup, Dumper=yaml.Dumper))

# Perform selected reconstruction
for fname in src_path.glob("*.wav"):
    # Assuming samplerate = 44100 Hz and depth = 16 bit.
    # Assuming a method reconstruct(model, fname, out_path) -> None
    # in each config as interface.
    print(f"Processing {fname} ...")
    config.reconstruct(model, fname, out_path)
