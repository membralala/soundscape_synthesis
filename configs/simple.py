"""
Task: Reconstruct input by simple forward pass through the model.
"""

import soundfile as sf
import torch


def reconstruct(model, f_path, out_path):
    x, sr = sf.read(f_path)
    x = torch.from_numpy(x).reshape(1, 1, -1).double()
    y_hat = model(x)
    y_hat = y_hat[0, 0].numpy()
    sf.write(file=out_path / f_path.name, data=y_hat, samplerate=sr)
