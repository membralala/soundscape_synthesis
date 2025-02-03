import pathlib

import soundfile as sf


class Strategy:
    excludes = []

    def to_dict(self):
        config = dict()
        for key, value in self.__dict__.items():
            if key in type(self).excludes:
                continue
            if isinstance(value, pathlib.Path):
                config[key] = str(value)
            else:
                config[key] = value
        return dict(name=type(self).__name__, config=config)

    def __call__(self, wavfile, outfile):
        raise NotImplementedError
