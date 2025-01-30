import pathlib

import pandas as pd
import yaml


def list_datasets(source_path):
    source_path = pathlib.Path(source_path)

    rows = []
    for index_file in source_path.rglob("*/_index.yaml"):
        with open(index_file, "r") as f:
            index_file_data = yaml.load(f.read(), Loader=yaml.Loader)
        rows.append(
            dict(
                type=index_file_data["type"],
                strategy=index_file_data["strategy"]["name"],
                dataset_path=index_file_data["path"],
                index_file_path=str(index_file),
            )
        )

    return pd.DataFrame(rows)
