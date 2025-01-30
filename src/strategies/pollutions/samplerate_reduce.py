import ffmpeg
import soundfile as sf

from .. import strategy


class VirtualSamplerateReduceStrategy(strategy.Strategy):
    def __init__(self, samplerate):
        self.samplerate = samplerate

    def __call__(self, wavfile, outfile):
        # Capture the original samplerate
        _, sr = sf.read(wavfile)
        # Perform the actual samplerate reduction and save the output
        stream = ffmpeg.output(
            ffmpeg.input(filename=wavfile), filename=outfile, ar=self.samplerate
        )
        ffmpeg.run(stream, capture_stderr=True)
        # Perform a second samplerate transformation recovering the original samplerate
        # and override the file, that was generated in the previous step
        stream = ffmpeg.output(ffmpeg.input(filename=outfile), filename=outfile, ar=sr)
