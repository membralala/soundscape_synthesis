"""
This module provides methods to analyse audio files in the context of soundscape ecology.
It also provides functionalities to extract some more generous informations, that require
a reading of the given files or at least of their meta data. 
"""

import pathlib

import numpy as np
import soundfile as sf
from maad import features, sound


def get_file_info(filename: str | pathlib.Path) -> dict:
    """Read meta data information from an audio file header.

    Parameters
    ----------
    filename : str | pathlib.Path
        The name of the file

    Returns
    -------
    dict
        Meta information as a dict containing following meta information:
        - filename as "Record_ID"
        - number of channels as "Channels"
        - samplerate as "Samplerate"
        - length of the file in seconds as "Length_sec"
    """
    path = pathlib.Path(filename)
    info = dict(Recording_ID=path.name)
    with sf.SoundFile(path) as soundfile:
        info["Channels"] = soundfile.channels
        info["Samplerate"] = soundfile.samplerate
        info["Length_sec"] = soundfile.frames / soundfile.samplerate
    return info


def get_bioindex_suite(filename: str | pathlib.Path) -> dict:
    """Calculate all bioindices that were compared in the thesis.

    Parameters
    ----------
    filename : str | pathlib.Path
        _description_

    Returns
    -------
    dict
        _description_
    """
    path = pathlib.Path(filename)
    indices = dict(Recording_ID=path.name)
    # Load file data and calculate power spectrogram as well as amplitude spectrogram as
    # inputs for bioacoustic indices.
    x, sr = sf.read(path)
    Sxx_power, tn, fn, extend = sound.spectrogram(
        x, sr, mode="psd"
    )  # Power spectrogram
    Sxx = np.sqrt(Sxx_power)  # Amplitude spectrogram
    # Calculate a suite of bioacoustic indices.
    indices["NP"] = features.number_of_peaks(Sxx, fn)
    indices["Bio"] = features.bioacoustics_index(Sxx, fn)
    indices["NDSI"] = features.soundscape_index(Sxx_power, fn)[0]
    indices["ACI"] = features.acoustic_complexity_index(Sxx)[2]
    indices["ADI"] = features.acoustic_diversity_index(Sxx, fn)
    indices["AEI"] = features.acoustic_eveness_index(Sxx, fn)
    indices["Ht"] = features.temporal_entropy(x)
    indices["Hf"] = features.spectral_entropy(Sxx, fn)[0]
    indices["H"] = indices["Ht"] * indices["Hf"]
    return indices


if __name__ == "__main__":
    with sf.SoundFile("../data/SALVE001/S4A08684_20190507_182200.wav") as s:
        print(s.channels)
        print(s.frames)
        print(s.samplerate)
        print(s.frames / s.samplerate)
