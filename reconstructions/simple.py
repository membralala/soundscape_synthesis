"""
Task: Reconstruct input by simple forward pass through the model.
"""

import soundfile as sf
import torch


def reconstruct(model, f_path, out_path, cargs):
    x, sr = sf.read(f_path)
    length = len(x)
    x = torch.from_numpy(x).reshape(1, 1, -1).double()
    y_hat = model(x)
    y_hat = y_hat[0, 0].numpy()
    y_hat = y_hat[:length]
    sf.write(file=out_path / f_path.name, data=y_hat, samplerate=sr)
