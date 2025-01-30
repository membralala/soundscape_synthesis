import soundfile as sf

from .. import strategy


class VirtualDepthReduceStrategy(strategy.Strategy):
    def __init__(self, depth):
        self.depth = depth

    def reduce_depth(self, x, sr):
        return ((x * (2 ** (self.depth - 1))) // 1) / (2 ** (self.depth - 1))

    def __call__(self, wavfile, outfile):
        x, sr = sf.read(wavfile)
        sf.write(file=outfile, data=self.reduce_depth(x, sr), samplerate=sr)
