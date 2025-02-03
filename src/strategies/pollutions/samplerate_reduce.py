import os
import shutil

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
        try:
            ffmpeg.run(
                stream, overwrite_output=True, capture_stdout=True, capture_stderr=True
            )
        except ffmpeg.Error as e:
            print("stdout:", e.stdout.decode("utf-8"))
            print("stderr:", e.stderr.decode("utf-8"))

        # Perform a second samplerate transformation recovering the original samplerate
        # and override the file, that was generated in the previous step.
        # As ffmpeg can't edit in-place, create a tmp file and rename it afterwards to
        # overwrite the previous.
        tmpfile = outfile.with_stem("tmp")
        stream = ffmpeg.output(ffmpeg.input(filename=outfile), filename=tmpfile, ar=sr)
        try:
            ffmpeg.run(
                stream, overwrite_output=True, capture_stdout=True, capture_stderr=True
            )
        except ffmpeg.Error as e:
            print("stdout:", e.stdout.decode("utf-8"))
            print("stderr:", e.stderr.decode("utf-8"))
        # Overwrite samplerate reduced file with virtual samplerate reduced tmp file
        shutil.move(tmpfile, outfile)
        # Delete tmp file
        os.remove(tmpfile)
