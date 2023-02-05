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
