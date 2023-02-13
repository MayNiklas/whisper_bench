# whisper Benchmark

Thank you for helping us to evaluate the performance of Whisper on different hardware platforms!

## How to run the benchmark

### NixOS

```bash
# nix run the benchmark
nix run 'github:mayniklas/whisper_bench'#whisper_bench_withCUDA
```

### Linux

Pre-requisites:

1. install [NVIDIA CUDA](https://developer.nvidia.com/cuda-downloads?target_os=Linux)
2. install ffmpeg (e.g. `sudo apt install ffmpeg`)

```bash
# clone the repository
git clone https://github.com/MayNiklas/whisper_bench.git

# change into the directory
cd whisper_bench

# create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install dependencies into the virtual environment
.venv/bin/pip3 install -r requirements.txt

# run the benchmark from within the virtual environment
.venv/bin/python3 bench/bench.py
```

### Windows

Pre-requisites:

1. install [NVIDIA CUDA](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64)
2. install the command-line tool ffmpeg (e.g. `choco install ffmpeg`)

```powershell
# clone the repository
git clone 'https://github.com/MayNiklas/whisper_bench.git'

# create a virtual environment
python3 -m venv .venv
.venv\Scripts\activate

# change into the directory
cd whisper_bench

# install PyTorch - see https://pytorch.org/get-started/locally/
# to get the correct command for your system
# e.g.
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117

# install dependencies into the virtual environment
.venv\Scripts\pip3 install -r requirements.txt

# run the benchmark from within the virtual environment
.venv\Scripts\python3 bench\bench.py
```

## Projects being used

* [OpenAI Whisper](https://github.com/openai/whisper)
* [PyTorch](https://pytorch.org/)

## Audio files being used

To compare the performance for different lengths of audio files, we run the benchmark with one short and one long audio file.
In theory, the setup time should stay arround the same for both files, while the processing time should linearly increase with the length of the audio file.

* <https://en.wikipedia.org/wiki/File:En-Open_Source_Software_CD-article.ogg> (public domain license)
* <https://commons.wikimedia.org/wiki/File:A_Time_for_Choosing.ogg> (public domain license)
