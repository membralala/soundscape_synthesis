"""
Task: Reconstruct input with support of a nonlinear MLP regressor based auto mapper. 
"""

import joblib
import soundfile as sf
import torch


def reconstruct(model, f_path, out_path, cargs):
    # Load mapper model
    (mapper_path,) = cargs
    mapper = joblib.load(mapper_path)
    # Load audio to model input tensor
    x, sr = sf.read(f_path)
    length = len(x)
    x = torch.from_numpy(x).reshape(1, 1, -1).double()
    # Encode audio to latent vectors
    z = model.encode(x)
    # Tensor to array
    z = z[0].t().numpy()
    # Mapping prediction
    z_hat = mapper.predict(z).transpose()
    # Convert array to latent space tensor
    z_hat = torch.from_numpy(z_hat).reshape(1, z_hat.shape[0], -1)
    # Decode and save audio
    y_hat = model.decode(z_hat)
    y_hat = y_hat[0, 0].numpy()
    y_hat = y_hat[:length]
    sf.write(file=out_path / f_path.name, data=y_hat, samplerate=sr)
