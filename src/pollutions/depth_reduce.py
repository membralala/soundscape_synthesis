import soundfile as sf


def pollute(f_path, out_path, cargs):
    (depth,) = cargs
    # Assuming that x is symmetric audio signal between [-1, 1]
    x, sr = sf.read(f_path)
    y = ((x * (2 ** (depth - 1))) // 1) / (2 ** (depth - 1))
    sf.write(out_path / f_path.name, data=y, samplerate=sr)
