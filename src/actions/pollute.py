import os
import pathlib

import yaml


def pollute(strategy, source_path, out_path):
    source_path = pathlib.Path(source_path)
    # Prepare output directory (override if directory exists)
    out_path = pathlib.Path(out_path)
    os.makedirs(out_path, exist_ok=True)
    # Create the index file with configuration details
    index_data = dict(
        type="pollution",
        path=str(out_path),
        source_path=str(source_path),
        strategy=strategy.to_dict(),
    )
    with open(out_path / "_index.yaml", "w") as f:
        f.write(yaml.dump(index_data, sort_keys=False))
    # Apply strategy to all wavfiles from source directory and save results
    # to out directory
    for wavfile in source_path.glob("*.wav"):
        outfile = out_path / wavfile.name
        strategy(wavfile, outfile)
