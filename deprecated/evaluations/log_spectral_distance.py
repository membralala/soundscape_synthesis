import numpy as np

# import torch
from maad import features, sound


def log_spectral_distance(x1, x2, sr=44100, epsilon=1e-12):
    """
    Calculate the log spectral distance of two audio signals.
    It is assumed, that both signals use the same sample rate and that they have the
    same shape.

    Parameters
    ----------
    x1 : array_like
        First audio signal
    x2 : array_like
        Second audio signal
    sr : int, optional
        Samplerate in Hz; the defined rate has to match the samplerate of x1 and x2.
        By default 44100
    epsilon : float, optional
        Very small value to prevent a calulation of log(0). Ideally epsilon should
        match the average noise floor of the given signals. By default 1e-12

    Returns
    -------
    float
        The log spectral distance of x1 and x2
    """

    Sx1_power, _, _, _ = sound.spectrogram(x1, sr)
    Sx2_power, _, _, _ = sound.spectrogram(x2, sr)
    # Calculate lsd per bin
    lsd_bins = (
        np.sum(
            np.square(np.log(Sx1_power + epsilon) - np.log(Sx2_power + epsilon)), axis=0
        )
        / Sx1_power.shape[0]
    )
    # Return the mean lsd over all bins
    return np.mean(lsd_bins)


if __name__ == "__main__":
    import soundfile as sf

    x1, sr = sf.read("../data/soundscapes_multiloc/AAD4/S4A08697_20190506_094000.wav")

    print(log_spectral_distance(x1, x1))
