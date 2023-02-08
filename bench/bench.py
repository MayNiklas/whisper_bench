import json
import os
import time
from typing import Optional

import torch
import whisper


def get_system_info() -> list:
    """
    Get the system info of the current machine
    """

    # initialize device info dict
    device_info = []

    # get cpu info
    cpu = {
        "type": "cpu",
        "architecture": os.uname().machine,
        # TODO: get the cpu name and manufacturer
        "cores": os.cpu_count(),
    }
    device_info.append(cpu)

    # get gpu info if being used
    if torch.cuda.is_available():
        gpu = {
            "type": "gpu",
            "cuda version": torch.version.cuda,
            "name": torch.cuda.get_device_name(0),
            "memory": torch.cuda.get_device_properties(0).total_memory,
        }
        device_info.append(gpu)

    return device_info


def ensure_model_is_present_and_usable(model_name="medium") -> bool:
    """
    Download the models from the internet if not present in cache.
    Also ensures the model fits into the GPU

    By just importing the model, it will be downloaded automatically if needed.
    We want to download the models before the benchmark starts.
    Otherwise, the benchmark would be unfair, since it would be influenced by the download time.

    The models are downloaded to the following path:
    ~/.cache/whisper/

    Returns:
        True: model is present and fits into GPU, False: model doesn't fit or something (like the download) goes wrong
    """

    # not all models are available for all devices!
    # especially the large model is not available for smaller gpu's

    print(
        f"Trying to load '{model_name}' model (might be downloaded if not in cache)..."
    )
    try:
        whisper.load_model(model_name)
        print(f"'{model_name}' model loaded...")
        return True
    except Exception:
        print(f"'{model_name}' doesn't work for this device.")
        return False


def benchmark_model(model_name="medium") -> Optional[tuple[float, float, float]]:
    """
    Benchmark the loading time and transcribing time of the model

    Args:
        model_name (str, optional): The model to benchmark. Defaults to "medium".
    Returns:
        (model loading time, short transcription time, long transcription time) if model could be loaded, else None
    """

    print(f"Benchmarking loading time for '{model_name}' model...")
    start_load_time = time.time()
    try:
        model = whisper.load_model(model_name, in_memory=True)
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
    model.transcribe("test_files/En-Open_Source_Software_CD-article.ogg", language="EN")
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
    model.transcribe("test_files/A_Time_for_Choosing.ogg", language="EN")
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

    # models that load successfully on the current device
    available_models = []

    # load the models
    for model_name in model_names:
        # when the model won't load on the current device, stop loading
        # size is only increasing
        if not ensure_model_is_present_and_usable(model_name):
            break
        else:
            available_models.append(model_name)
    else:
        print("All models are loaded successfully!")

    print("Available models on this hardware: ", available_models)

    # set that hold all models that weren't able to load or failed for other reasons
    not_available_or_failed_set = set(model_names).difference(set(available_models))

    results: list[dict] = []  # list with model timings that worked
    failed_models: list[str] = []  # list with model_names that failed to load
    for model in available_models:
        print("==================================")

        model_times = benchmark_model(model)
        # only add models to result that actually worked
        # keep track over which models failed
        print(model_times)
        if model_times is None:
            not_available_or_failed_set.add(model)
            continue

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
        "results": results,
        "failed_models": list(not_available_or_failed_set),
    }

    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    cli()
