import gc
import json
import os
import platform
import sys
import time
from typing import Optional

import psutil
import torch
from faster_whisper import WhisperModel


if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    import os.path

    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import bench.utils as utils


def get_system_info() -> list:
    """
    Get the system info of the current machine
    """

    # initialize device info dict
    device_info = []

    os = {
        "type": "os",
        "system": platform.uname().system,
        "release": platform.uname().release,
        "version": platform.uname().version,
    }
    device_info.append(os)

    # get cpu info
    cpu = {
        "type": "cpu",
        "architecture": platform.uname().machine,
        "name": utils.get_cpu_name(),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
    }
    device_info.append(cpu)

    ram = {
        "type": "ram",
        "total": utils.get_size(psutil.virtual_memory().total),
    }
    device_info.append(ram)

    # get gpu info if being used
    if torch.cuda.is_available():
        gpu = {
            "type": "gpu",
            "cuda version": torch.version.cuda,
            "name": torch.cuda.get_device_name(0),
            "memory": utils.get_size(torch.cuda.get_device_properties(0).total_memory),
        }
        device_info.append(gpu)

    return device_info


def benchmark_model(model_name="medium") -> Optional[tuple[float, float, float]]:
    """
    Benchmark the loading time and transcribing time of the model

    Args:
        model_name (str, optional): The model to benchmark. Defaults to "medium".
    Returns:
        (model loading time, short transcription time, long transcription time) if model could be loaded, else None
    """

    gc.collect()
    torch.cuda.empty_cache()

    print(f"Benchmarking loading time for '{model_name}' model...")
    start_load_time = time.time()
    try:
        model = WhisperModel(model_name, device="cuda", compute_type="float16")
    except torch.cuda.OutOfMemoryError as e:
        print(f"Not enough memory - Can't load model '{model_name}'")
        return

    end_load_time = time.time()
    model_load_time = end_load_time - start_load_time
    print(f"Loading time for '{model_name}' model: {model_load_time}")

    # benchmark short audio file
    print(
        f"Benchmarking transcription time (short audio file) for '{model_name}' model..."
    )
    start_transcribe_time = time.time()
    segments, info = model.transcribe(
        os.path.dirname(os.path.abspath(__file__))
        + "/test_files/En-Open_Source_Software_CD-article.ogg"
    )
    segments = list(segments)
    end_transcribe_time = time.time()
    short_audio_file_transcription_time = end_transcribe_time - start_transcribe_time
    print(
        f"Transcription time (short audio file) for '{model_name}' model: {short_audio_file_transcription_time}"
    )

    # benchmark long audio file
    print(
        f"Benchmarking transcription time (long audio file) for '{model_name}' model..."
    )
    start_transcribe_time = time.time()
    
    segments, info = model.transcribe(
        os.path.dirname(os.path.abspath(__file__))
        + "/test_files/A_Time_for_Choosing.ogg"
    )
    segments = list(segments)

    end_transcribe_time = time.time()
    long_audio_file_transcription_time = end_transcribe_time - start_transcribe_time
    print(
        f"Transcription time (long audio file) for '{model_name}' model: {long_audio_file_transcription_time}"
    )

    return (
        model_load_time,
        short_audio_file_transcription_time,
        long_audio_file_transcription_time,
    )


def cli():
    """
    Entry point for the console script
    """

    print("Welcome to the Whisper benchmark script!")

    # get system info
    system_info = get_system_info()

    # models that we try to load
    model_names = ["tiny", "base", "small", "medium", "large"]

    results: list[dict] = []  # list with model timings that worked
    for model in model_names:
        print("==================================")

        model_times = benchmark_model(model)
        # only add models to result that actually worked
        # keep track over which models failed
        print(model_times)

        model_results = {
            "model": model,
            "model_load_time": model_times[0],
            "transcription_time_short": model_times[1],
            "transcription_time_long": model_times[2],
        }
        results.append(model_results)

    print("Benchmark finished!")
    print("Please send us the following results:")
    print("==================================")

    output = {
        "system_info": system_info,
        "results": results
    }

    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    cli()
