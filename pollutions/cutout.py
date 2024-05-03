import random

import numpy as np
import soundfile as sf


def pollute(f_path, out_path, cargs):
    total_cutout_length = int(cargs[0])
    block_length = int(cargs[1])
    x, sr = sf.read(f_path)
    y, indices = cutout(x, total_cutout_length, block_length)
    sf.write(out_path / f_path.name, data=y, samplerate=sr)
    np.save(out_path / f"{f_path.stem}.npy", indices)


def cutout(x, total_cutout_length, block_length):
    # Assuming total_cutout_length and block_length as number of samples.
    # Assuming block_length is a true divisor of total_cutout_length
    assert total_cutout_length % block_length == 0

    n_blocks = total_cutout_length // block_length
    # Split not divisible rest
    if len(x) % n_blocks != 0:
        x_rest = x[-(len(x) % n_blocks) :]
        x = x[: -(len(x) % n_blocks)]
    x = x.reshape(n_blocks, -1)

    indices = np.zeros(n_blocks)
    for i in range(n_blocks):
        left_bound = block_length if i == 0 else 0
        right_bound = x.shape[1] - 2 * block_length
        idx = random.randrange(left_bound, right_bound)
        x[i, idx : idx + block_length] = 0
        indices[i] = idx

    x = x.reshape(-1)
    if len(x) % n_blocks != 0:
        x = np.concatenate((x, x_rest))
    return x, indices


if __name__ == "__main__":
    for i in range(100):
        x = np.ones(44100 * 10)
        y, _ = cutout_long(x, 44100, 441)
        assert (44100 * 10) - int(np.sum(y)) == 44100
    # for i in range(100):
    #     pollute(x, 44100, 4410)
    # for i in range(100):
    #     pollute(x, 44100, 2205)
