import json
import os

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


def download_model():
    """
    Download the models from the internet.

    By just importing the model, it will be downloaded automatically.
    We want to download the models before the benchmark starts.

    The models are downloaded to the following path:
    ~/.cache/whisper/
    """

    # TODO: try / catch for each model
    # not all models are available for all devices!
    # especially the large model is not available for smaller gpu's

    model = whisper.load_model("tiny")
    print("tiny model loaded...")
    model = whisper.load_model("base")
    print("base model loaded...")
    model = whisper.load_model("small")
    print("small model loaded...")
    model = whisper.load_model("medium")
    print("medium model loaded...")
    model = whisper.load_model("large")
    print("large model loaded...")

    print("All models downloaded successfully!")

    return


def cli():
    """
    Entry point for the console script
    """

    print("Welcome to the Whisper benchmark script!")

    # get system info
    system_info = get_system_info()
    print(json.dumps(system_info, indent=4))

    # download the models
    download_model()


if __name__ == "__main__":
    cli()
