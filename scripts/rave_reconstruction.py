from pathlib import Path

import soundfile as sf
import torch

MODEL_PATH = Path("runs/rave_scapes_1_fe77618ebd/rave_scapes_1_fe77618ebd_streaming.ts")


torch.set_grad_enabled(False)

model = torch.jit.load(MODEL_PATH).eval()
model.double()

f1 = Path("data/soundscapes_sm_corr/test/S4A09106_20190706_110700.wav")

x1, sr = sf.read(f1)

x1 = torch.from_numpy(x1).reshape(1, 1, -1)
x1.double()
y1 = model.encode(x1)

z = model.decode(y1).numpy().reshape(-1)
sf.write(f"{f1.stem}_reconstruction{f1.suffix}", z, samplerate=sr)
