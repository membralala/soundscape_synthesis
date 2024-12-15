""" Handle soundscape data from the SALVE project. This module provides functionalities
for soundscape data management. For that it assumes a certain file naming convention, that 
was used in the SALVE project. That is, a filename - also called Recodring_ID - is 
structured as '<Device_ID>_<datetime>.wav' where datetime is formatted as '%Y%m%d_%H%M%S'.
"""

import datetime
import os
import pathlib
import re

import pandas as pd

"""Initial meta data scheme with headers for all relevant information, that can be 
extracted from file path and filename without opening the file descriptor."""
INIT_SCHEME = ["Record_ID", "Device_ID", "Datetime", "Path"]

"""The datetime format convention used for the naming of the SALVE soundscapes"""
SALVE_DATETIME_FORMAT = "%Y%m%d_%H%M%S"


class InvalidRecordIdException(Exception):
    """Exception for filenames that do not follow the SALVE file naming convention."""

    pass


def is_valid_record_id(filename: str) -> bool:
    """Validate, if given string follows the SALVE naming convention.

    Parameters
    ----------
    filename : str
        The filename string to validate

    Returns
    -------
    bool
        Whether the given filename string follows the convention
    """

    return (
        True
        if re.match(r"[a-zA-Z0-9]+_[0-9]{8}_[0-9]{6}.[(wav)(WAV)]", filename)
        else False
    )


def read_metadata_from_filename(
    filename: str | pathlib.Path, relpath: str | pathlib.Path = None
) -> pd.Series:
    """Extract metadata from soundscape filename, that follows the SALVE naming convention.

    Parameters
    ----------
    filename : str | pathlib.Path
        The given filename

    relpath : str | pathlib.Path, optional
        A reference path to safe the current filename path as relative path

    Returns
    -------
    pd.Series
        The extracted metadata

    Raises
    ------
    TypeError
        If filename argument is not a str or a pathlib.Path
    InvalidRecordIdException
        If filename does not follow the SALVE naming convention
    """

    if isinstance(filename, str):
        srcpath = pathlib.Path().resolve() / filename
    elif isinstance(filename, pathlib.Path):
        srcpath = filename
    else:
        raise TypeError("filename has to be either a string or a pathlib.Path.")
    if not is_valid_record_id(srcpath.name):
        raise InvalidRecordIdException(f"'{srcpath.name}' is not a valid Record_ID.")

    record_id = srcpath.name
    device_id, raw_date, raw_time = srcpath.stem.split("_")
    datetime_str = "_".join([raw_date, raw_time])
    path = os.path.relpath(srcpath, pathlib.Path(relpath))

    return pd.Series(
        data=dict(
            Record_ID=record_id,
            Device_ID=device_id,
            Datetime=datetime_str,
            Path=path,
        )
    )


def read_metadata_from_directory(
    dirname: str | pathlib.Path, recursive: bool = False
) -> pd.DataFrame:
    """Extract metadata from all soundscape filenames in a given directory, that follow
    the SALVE naming convention.

    Parameters
    ----------
    dirname : str | pathlib.Path
        The given directory name
    recursive : bool, optional
        Whether the resulting dataframe should also list files from all subfolders

    Returns
    -------
    pd.DataFrame
        The extracted metadata

    Raises
    ______
    AttributeError
        If directory not exists
    """
    dir = pathlib.Path(dirname)
    if not dir.exists():
        raise AttributeError(f"Directory '{dirname}' does not exist.")

    df = pd.DataFrame(columns=INIT_SCHEME)
    if recursive:
        glob_iterator = dir.rglob
    else:
        glob_iterator = dir.glob

    for i, filename in enumerate(glob_iterator("*.wav")):
        df.loc[i] = read_metadata_from_filename(filename, relpath=dir)

    return df


def read_datetime(date_string: str) -> datetime.datetime:
    """Convert datetime string to datetime.datetime object.

    Parameters
    ----------
    date_string : str
        The given datetime string

    Returns
    -------
    datetime.datetime
        The datetime object
    """
    return datetime.datetime.strptime(date_string, SALVE_DATETIME_FORMAT)


def write_datetime(date_time: datetime.datetime) -> str:
    """Convert datetime.datetime object to datetime string.

    Parameters
    ----------
    date_time : datetime.datetime
        The datetime object

    Returns
    -------
    str
        The datetime string
    """
    return datetime.datetime.strftime(date_time, SALVE_DATETIME_FORMAT)


if __name__ == "__main__":
    # Test validation
    valid_record_ids = [
        "S4A09106_20190507_074400.wav",  # valid format .wav
        "S4A09106_20190507_074400.WAV",  # also valid format .WAV
    ]

    for valid_record_id in valid_record_ids:
        assert is_valid_record_id(valid_record_id) == True

    invalid_record_ids = [
        "",  # empty string
        "S4A09106_20190507_074400",  # no file ending
        "S4A09106_190507_074400.wav"  # bad date format
        "S4A09106_20190507_0744001.wav",  # bad time format
    ]

    for invalid_record_id in invalid_record_ids:
        assert is_valid_record_id(invalid_record_id) == False

    # Test datetime string formatting
    date_string = "20190507_074400"
    assert date_string == write_datetime(read_datetime(date_string))
