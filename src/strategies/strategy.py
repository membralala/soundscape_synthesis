import soundfile as sf


class Strategy:
    @property
    def name(self):
        return type(self).__name__

    def to_dict(self):
        return dict(name=self.name, config=self.__dict__)

    def __call__(self, wavfile, outfile):
        raise NotImplementedError
