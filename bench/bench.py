import json
import os
import time

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


def download_model(model_name="medium"):
    """
    Download the models from the internet.

    By just importing the model, it will be downloaded automatically.
    We want to download the models before the benchmark starts.

    The models are downloaded to the following path:
    ~/.cache/whisper/
    """

    # not all models are available for all devices!
    # especially the large model is not available for smaller gpu's

    print("Trying to download and load " + model_name + " model...")
    try:
        model = whisper.load_model(model_name)
        print(model_name + " model loaded...")
        return True
    except:
        print(model_name + " model not available for this device.")
        return False


def benchmark_model_load(model_name="medium"):
    """
    Benchmark the model loading time
    """

    print("Benchmarking model load time for " + model_name + " model...")

    start_time = time.time()
    model = whisper.load_model(model_name)
    end_time = time.time()

    print("Model load time for " + model_name + " model: ", end_time - start_time)

    return end_time - start_time


def benchmark_transcription(model_name="medium"):
    """
    Benchmark the transcription time
    """

    model = whisper.load_model(model_name, in_memory=True)

    print("Benchmarking transcription time for " + model_name + " model...")

    start_time = time.time()
    result = model.transcribe("benchmark_file.ogg", language="DE")
    end_time = time.time()

    print("Transcription time for " + model_name + " model: ", end_time - start_time)

    return end_time - start_time


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

    # download the models
    for model_name in model_names:
        # when the model won't load on the current device, stop downloading
        if not download_model(model_name):
            break
        else:
            available_models.append(model_name)
    print("All models downloaded successfully!")
    print("Available models on this hardware: ", available_models)

    results = []

    for model in available_models:
        print("Benchmarking " + model + " model...")

        model_results = {
            "model": model,
            "model_load_time": benchmark_model_load(model),
            "transcription_time": benchmark_transcription(model),
        }

        results.append(model_results)

    print("Benchmark finished!")
    print("Please send the following results:")

    output = {
        "system_info": system_info,
        "results": results,
    }

    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    cli()
