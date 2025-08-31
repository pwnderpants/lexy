# Main entry point for Lexy speech transcription application

from .cli import ArgumentParser, list_microphones
from .transcription import SpeechTranscriber


def main() -> None:
    # Main application entry point
    # Parse command line arguments
    parser = ArgumentParser()
    config = parser.parse_args()
    
    # Handle special commands
    if config.show_help:
        parser.show_help()
        return
    
    if config.list_mics:
        list_microphones()
        return
    
    # Start main application
    print(f"Starting Lexy Speech-to-Text Transcriber", flush=True)
    
    transcriber = SpeechTranscriber(
        debug=config.debug,
        device_index=config.device_index,
        model_path=config.model_path
    )
    transcriber.start_listening()


if __name__ == "__main__":
    main()