import soundfile as sf
import torch

from .. import strategy


class RaveSimpleReconstructStrategy(strategy.Strategy):
    excludes = ["model"]

    def __init__(self, model_path, model):
        self.model_path = model_path
        self.model = model

    def __call__(self, source_path, out_path):
        # Load source audio file
        y, sr = sf.read(source_path)
        # As y may be padded by the RAVE model, it is possible, that lengths between
        # y and y_hat will differ. Therefore keep track of the length of y and truncate
        # y_hat, if necessary.
        n_samples = len(y)
        # Convert to required input tensor
        y = torch.from_numpy(y).reshape(1, 1, -1).double()
        y_hat = self.model(y)
        # Convert result to numpy array
        y_hat = y_hat[0, 0].numpy()[:n_samples]
        sf.write(file=out_path, data=y_hat, samplerate=sr)
