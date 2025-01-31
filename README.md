# soundscape_synthesis
### Analyse the reconstruction capabilities of generative models in the audio domain in the context of soundscape ecology.

This repository provides an infrastructure to analyse generative models in the context of soundscape ecoliogy. It does so by providing a set of _pollution strategies_, that can be applied to audio signals in order to 'damage' the signals in different ways, and a set of _reconstruction strategies_, that can be applied to audio singals in order to 'repair' the singals in different ways. 
It then provides an easy interface to calculate a suite of common bioacoustic indices on whole datasets to make comparison and evaluation easy.

This repository is the reworked code base of my bachelor thesis _Einsatz generativer Architekturen zur Synthese von Soundscapes_ at TU Dormund..

## Requirements & Ressources
### RAVE
Within the scope of my thesis the [RAVE](https://arxiv.org/abs/2111.05011) Variational Auto Encoder was used as state-of-the-art audio generative model and therefore the implemented reconstruction strategies rely quite heavyly on RAVEs architecture. RAVE's official pytorch implementation can be found [here](https://github.com/acids-ircam/RAVE/tree/master).

### scikit-maad
For calculations of bioacoustic indices the python package [scikit-maad](https://scikit-maad.github.io/) was used extensively.


