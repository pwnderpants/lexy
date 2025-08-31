# CLI command implementations for Lexy

import speech_recognition as sr


def list_microphones() -> None:
    # List all available microphone devices
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  {index}: {name}")