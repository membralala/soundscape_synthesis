## Preprocess audio to RAVE dataset

```
rave preprocess --input_path path/to/your/audio --output_path path/to/your/dataset 
```
Arguments:
- `--num_signal`: Number of audio samples to use during training, default: 131072
- `--sampling-rate`: Sampling rate to use during training, default: 44100
- `--max_db_size`: Maximum size (in GB) of the dataset, default: 100
- `--ext`: Extension to search for in the input directory, default: `['aif', 'aiff', 'wav', 'opus', 'mp3', 'aac', 'flac', 'ogg']`
- `--lazy`: Decode and resample audio samples, default: False
- `--dyndb`: Allow the database to grow dynamically, default: True