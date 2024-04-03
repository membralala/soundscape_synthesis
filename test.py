import numpy as np
import torch
from dtaidistance import dtw
from maad import features, sound


def prune_longest(x1, x2):
    if (x1_len := len(x1)) == (x2_len := len(x2)):
        return x1, x2
    print(f"Different lengths detected({x1_len}, {x2_len}). Pruning longer sample")
    min_len = min(x1_len, x2_len)
    return x1[:min_len], x2[:min_len]


def test_log_spectral_distance(x1, x2, sr=44100):
    # Not sure, if this is correct!
    Sx1_power, _, _, _ = sound.spectrogram(x1, sr)
    Sx2_power, _, _, _ = sound.spectrogram(x2, sr)
    return np.mean(
        np.sum(np.square(np.log(Sx1_power) - np.log(Sx2_power[:, :-1])), axis=0)
        / Sx1_power.shape[0]
    )


def test_dynamic_time_wrapping(x1, x2):
    # Limiting the window size, otherwise processing time explodes
    return dtw.distance_fast(x1, x2, window=1024, use_pruning=True)


def calculate_bioinices(x, sr=44100):
    # Calculate psd spectrogram
    Sxx_power, tn, fn, _ = sound.spectrogram(x, sr)
    # Calculate amplitude spectrogram. tn and fn are still the same as in psd spectrogram
    Sxx, _, _, ext = sound.spectrogram(x, sr, mode="amplitude")

    # Number of Peaks
    NP = features.number_of_peaks(Sxx_power, fn)
    # Bioacoustics Index
    Bio = features.bioacoustics_index(Sxx, fn)
    # NDSI
    NDSI = features.soundscape_index(Sxx_power, fn)[0]
    # Acoustic Complexity Index; only keep scalar
    ACI = features.acoustic_complexity_index(Sxx)[2]
    # Acoustic Diversity Index
    ADI = features.acoustic_diversity_index(Sxx, fn)
    # Acoustic Eveness Index
    AEI = features.acoustic_eveness_index(Sxx, fn)
    # Temporal Entropy
    Ht = features.temporal_entropy(x)
    # Spectral Entropy, only keep scalar
    Hf = features.frequency_entropy(Sxx_power)[0]
    # Calculate Acoustic Entropy Index as H = Ht * Hf
    H = Ht * Hf

    return {
        "NP": NP,
        "Bio": Bio,
        "NDSI": NDSI,
        "ACI": ACI,
        "ADI": ADI,
        "AEI": AEI,
        "Ht": Ht,
        "Hf": Hf,
        "H": H,
    }


def test_bioindex_distance(x1, x2):
    b1 = calculate_bioinices(x1)
    b2 = calculate_bioinices(x2)
    keys = b1.keys()
    abs_distances = np.abs(np.array(list(b1.values())) - np.array(list(b2.values())))
    return dict(zip(keys, abs_distances))


def test_latent_space_distance(x1, x2, model):
    wav_to_tensor = lambda x: torch.from_numpy(x).reshape(1, 1, -1).double()
    z1 = model.encode(wav_to_tensor(x1))[0].reshape(1, -1)
    z2 = model.encode(wav_to_tensor(x2))[0].reshape(1, -1)
    return torch.dist(z1, z2).numpy()[0]


if __name__ == "__main__":
    import argparse
    import os
    import pathlib
    import time

    import pandas as pd
    import soundfile as sf

    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    parser.add_argument("-gt", "--truth", type=str, required=True)
    parser.add_argument("--ld_model")
    args = parser.parse_args()

    src_path = pathlib.Path(args.src)
    ground_truth_path = pathlib.Path(args.truth)

    test_result_list = []
    try:
        fnames = list(src_path.glob("*.wav"))
        fnames.sort()
        for i, fname in enumerate(fnames):
            print(f"Processing {fname} ...")
            # Assuming that both files have the same name, samplerate and depth
            # Assuming samplerate = 44100 Hz, depth = 16 bit
            x1, sr = sf.read(fname)
            gt_fname = ground_truth_path / fname.name
            if os.path.samefile(fname.resolve(), gt_fname.resolve()):
                x2 = np.copy(x1)
            else:
                x2, _ = sf.read(gt_fname)

            s = time.time()
            x1, x2 = prune_longest(x1, x2)
            test_results = {"name": fname.name}
            test_results.update(test_bioindex_distance(x1, x2))
            test_results.update(
                {
                    "lsd": test_log_spectral_distance(x1, x2),
                    "dtw": test_dynamic_time_wrapping(x1, x2),
                }
            )
            test_result_list.append(test_results)
            print(test_results)
            print(f"Processed {i} / {len(fnames)}")
            print(f"time: {time.time() - s}")

        print("Saving results...")
        df = pd.DataFrame.from_dict(test_result_list)
        df.to_csv(src_path / "test_results.csv")
    except KeyboardInterrupt:
        print("Quitting due to forced exit.")
        while True:
            saving = input("Save results until this point? [y/n]")
            if saving == "y":
                df = pd.DataFrame.from_dict(test_result_list)
                df.to_csv(src_path / "test_results.csv")
            elif saving == "n":
                break
            else:
                print("No valid entry.")

        exit(-1)
