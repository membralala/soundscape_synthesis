import os
import pathlib

import pandas as pd
import yaml


def _apply_dataset_to_dataset_strategy(strategy, source_path, out_path, stype=""):
    """
    Apply a strategy, that expects audio files within the source_path and creates
    new audio files with the same name in the out_path directory.
    """
    source_path = pathlib.Path(source_path)
    # Prepare output directory (override if directory exists)
    out_path = pathlib.Path(out_path)
    os.makedirs(out_path, exist_ok=True)
    # Create the index file with configuration details
    index_data = dict(
        type=stype,
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


def _apply_dataset_to_dataframe_strategy(strategy, source_path, out_path, stype=""):
    """
    Apply a strategy, that expects audio files within the source_path and creates
    dicts that serve as dataframe rows. A dataframe will be created and saved in the
    out_path directory.
    """
    source_path = pathlib.Path(source_path)
    # Prepare output directory (override if directory exists)
    out_path = pathlib.Path(out_path)
    os.makedirs(out_path, exist_ok=True)
    # Create the index file with configuration details
    index_data = dict(
        type=stype,
        path=str(out_path),
        source_path=str(source_path),
        strategy=strategy.to_dict(),
    )
    with open(out_path / "_index.yaml", "w") as f:
        f.write(yaml.dump(index_data, sort_keys=False))
    # Create a dataframe based on strategy results
    df = pd.DataFrame([strategy(f) for f in source_path.glob("*.wav")])
    df.to_csv(out_path)


def pollute(strategy, source_path, out_path):
    _apply_dataset_to_dataset_strategy(
        strategy, source_path, out_path, stype="pollution"
    )


def reconstruct(strategy, source_path, out_path):
    _apply_dataset_to_dataset_strategy(
        strategy, source_path, out_path, stype="reconstruction"
    )


def evaluate(strategy, source_path, out_path):
    _apply_dataset_to_dataframe_strategy(
        strategy, source_path, out_path, stype="evaluation"
    )
