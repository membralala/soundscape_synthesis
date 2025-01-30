import numpy as np
import soundfile as sf


def pollute(f_path, out_path, cargs):
    total_cutout_length = int(cargs[0])
    block_length = int(cargs[1])
    x, sr = sf.read(f_path)
    y = cutout_short(x, total_cutout_length, block_length)
    sf.write(out_path / f_path.name, data=y, samplerate=sr)


def cutout_short(x, total_cutout_length, block_length):
    # Assuming total_cutout_length and block_length as number of samples.
    # Assuming block_length is a true divisor of total_cutout_length
    assert total_cutout_length % block_length == 0

    n_blocks = total_cutout_length // block_length
    x_rest = x[-(len(x) % block_length) :]
    x = x[: -(len(x) % block_length)]
    x = x.reshape(-1, block_length)
    idx = np.random.randint(0, len(x), n_blocks)
    x[idx] = 0
    x = x.reshape(-1)
    x = np.concatenate((x, x_rest))
    return x


if __name__ == "__main__":
    x = np.ones(205)
    print(cutout_short(x, 32, 2))
