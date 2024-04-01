import numpy as np


def virtual_depth_reduce(x, depth=12):
    return ((x * (2 ** (depth - 1))) // 1) / (2 ** (depth - 1))


def cutout_pollute(x, sr, cutout_length_in_sec=10):
    # Determine a position in the audio file to be cut out. Make sure, that the
    # cut out does not happen at the start or at the end of the file as this would
    # create an extrapolation not interpolation task.
    startpos = np.random.randint(
        cutout_length_in_sec * sr, len(x) - cutout_length_in_sec * 2 * sr
    )
    endpos = startpos + cutout_length_in_sec * sr
    x[startpos:endpos] = np.zeros(cutout_length_in_sec * sr)
    return x, sr, startpos, endpos, cutout_length_in_sec


if __name__ == "__main__":
    import argparse
    import os
    import pathlib

    import soundfile as sf
    import yaml

    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", type=str)
    parser.add_argument("-s", "--src", type=str)
    parser.add_argument("-o", "--out", type=str, default="")
    parser.add_argument("--depth", type=int, default=12)

    args = parser.parse_args()

    src = pathlib.Path(args.src)
    out = pathlib.Path(args.out)

    # Check if src is valid
    if not src.exists or not src.is_dir:
        raise Exception()
    # Create out folder, if it does not exist
    os.makedirs(out, exist_ok=True)

    for f in src.glob("*.wav"):
        # Read audio file
        x, sr = sf.read(f)

        if args.cmd == "depthreduce":
            x_res = virtual_depth_reduce(x, args.depth)
        elif args.cmd == "cutout":
            pass
        else:
            raise Exception("No valid command")

        sf.write(out / f.name, x_res, samplerate=sr)

    # Write setup yaml
    config_content = {
        "depthreduce": {"type": "virtual bit reduction", "depth": args.depth},
        "cutout": {"type": "cutout"},
    }

    with open(out / "_pollution_setup.yaml", "w") as sf:
        sf.write(yaml.dump({"pollution": config_content[args.cmd]}, Dumper=yaml.Dumper))
