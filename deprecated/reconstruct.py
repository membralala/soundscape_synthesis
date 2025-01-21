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
parser.add_argument("--repair", action="store_true")
parser.add_argument("--cargs", nargs="+")
args = parser.parse_args()

# Get paths
src_path = pathlib.Path(args.src)
out_path = pathlib.Path(args.out)
os.makedirs(out_path, exist_ok=True)

# Get config module.
config = importlib.import_module(f"reconstructions.{args.config}")

# Load model
torch.set_grad_enabled(False)
model = torch.jit.load(args.model).eval().double()

# Save setup_config
setup = {"model": args.model, "config": args.config, "config_args": args.cargs}
with open(out_path / "_reconstruction_setup.yaml", "w") as f:
    f.write(yaml.dump(setup, Dumper=yaml.Dumper))


# Collect files to reconstruct
src_files = set([elem.name for elem in src_path.glob("*.wav")])
error_log = out_path / "_errors.log"
# With --repair flag
if args.repair:
    # Check existing reconstruction files
    out_files = set([elem.name for elem in out_path.glob("*.wav")])

    # Check error log
    error_files = None
    if error_log.exists():
        with open(error_log, "r") as f:
            error_files = set(
                [pathlib.Path(elem).name for elem in f.readlines() if elem]
            )
            print(f"Found {len(error_files)} potentially damaged files:")
            for f_path in error_files:
                print(f_path)

    # Reconstruct only damaged and missing files
    if error_files:
        files = sorted((src_files - out_files) | error_files)
    else:
        files = sorted(src_files - out_files)
    print(
        f"Reconstucting {len(files)} files. \nSkipping {len(src_files) - len(files)} files."
    )
# Without repair flag
else:
    files = sorted(src_files)
    print(f"Reconstucting {len(files)} files. \n")

# Clear old error log
if error_log.exists():
    os.remove(error_log)

# Perform selected reconstruction
for i, fname in enumerate(files):
    f_path = src_path / fname
    # Assuming samplerate = 44100 Hz and depth = 16 bit.
    # Assuming a method reconstruct(model, fname, out_path) -> None
    # in each config as interface.
    print(f"Processing {f_path} ... ({i + 1}/{len(files)})")
    try:
        config.reconstruct(model, f_path, out_path, args.cargs)
    except Exception as e:
        with open(out_path / "_errors.log", "a") as f:
            f.write(str(f_path))
        print(e)
    except KeyboardInterrupt:
        with open(out_path / "_errors.log", "a") as f:
            f.write(str(f_path))
        exit()
