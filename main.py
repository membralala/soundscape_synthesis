"""DEPRECATED! This file is just kept as reference for code snippets.
DO NOT USE!"""

import os
import pathlib
import re

import yaml

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str)
    parser.add_argument("-s", "--src", type=str, required=True)
    parser.add_argument("--config", type=str, default="")
    args = parser.parse_args()

    src_path = pathlib.Path(args.src)

    if args.command == "pollute":
        # Create pollutions main directory if necessary
        out_path = pathlib.Path(args.src) / "pollutions"
        os.makedirs(out_path, exist_ok=True)
        # Create new pollutions directory
        dirs = sorted(
            [f.name for f in out_path.glob("*") if re.match(r"\d\d\d", f.name)]
        )
        if len(dirs) == 0:
            next_dir_name = "001"
        else:
            next_dir_name = f"{int(dirs[-1]) + 1:03d}"
        out_path = out_path / next_dir_name
        os.makedirs(out_path, exist_ok=False)

        # Choose pollution layer based on selected config
        if args.config == "copy":
            ll = layers.CopyLayer(out_path)
        else:
            raise Exception("pollution command requires valid --config option")

        # Export yaml config
        print(ll.get_config())
        with open(out_path / "_pollution_setup.yaml", "w") as f:
            f.write(yaml.dump(ll.get_config(), Dumper=yaml.Dumper))

        # Run the actual layer command on files in src directory
        if src_path.is_dir():
            ll(src_path.glob("*.wav"))
        else:
            ll(src_path)
