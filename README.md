# whisper Benchmark

Thank you for helping us to evaluate the performance of Whisper on different hardware platforms!

## How to run the benchmark

```bash
# clone the repository
git clone https://github.com/MayNiklas/whisper_bench.git

# change into the directory
cd whisper_bench

# create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install the benchmark into the virtual environment
pip install -e .

# run the benchmark
whisper_bench
```

### Audio files being used

To compare the performance for different lengths of audio files, we run the benchmark with one short and one long audio file.
In theory, the setup time should stay arround the same for both files, while the processing time should linearly increase with the length of the audio file.

* https://en.wikipedia.org/wiki/File:En-Open_Source_Software_CD-article.ogg (public domain license)
* https://commons.wikimedia.org/wiki/File:A_Time_for_Choosing.ogg (public domain license)
