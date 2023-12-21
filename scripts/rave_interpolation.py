from pathlib import Path

import numpy as np
import soundfile as sf
import torch

MODEL_PATH = Path("runs/rave_scapes_1_fe77618ebd/rave_scapes_1_fe77618ebd_streaming.ts")


torch.set_grad_enabled(False)

model = torch.jit.load(MODEL_PATH).eval()
model.double()

f1 = Path("Australia44100.wav")
f2 = Path("Jordan44100.wav")

x1, sr1 = sf.read(f1)
x2, sr2 = sf.read(f2)
# Make mono
x1 = x1.transpose()[0]
x2 = x2.transpose()[0]

# trim to shorter length
start = 5 * 60 * 44100
end = 6 * 60 * 44100
x1 = x1[start:end]
x2 = x2[start:end]
print("Trimmed audios")
x1 = torch.from_numpy(x1).reshape(1, 1, -1)
x1.double()
x2 = torch.from_numpy(x2).reshape(1, 1, -1)
x2.double()
y1 = model.encode(x1)
y2 = model.encode(x2)
print("Audios encoded. Start interpolation.")

# Make single transition
mix_curve = np.linspace(0, 1, 1292)
y = y1 * (1 - mix_curve) + y2 * mix_curve
z = model.decode(y).numpy().reshape(-1)
sf.write("rave_interpolation.wav", z, samplerate=44100)


# for i in range(10):
#     # Interpolate between two latent spaces
#     y = y1 * (10 - i) * 0.1 + y2 * i * 0.1
#     z = model.decode(y).numpy().reshape(-1)

#     sf.write(f"rave_interpolation_{i:02d}.wav", z, samplerate=44100)
