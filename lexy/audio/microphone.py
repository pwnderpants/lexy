# Microphone management and initialization

import speech_recognition as sr
from typing import Optional, Tuple
from .utils import suppress_alsa_messages, restore_stderr


class MicrophoneManager:
    # Manages microphone initialization and configuration
    
    def __init__(self, device_index: Optional[int] = None, debug: bool = False):
        self.device_index = device_index
        self.debug = debug
        self.microphone = None
        self._initialize_microphone()
    
    def _initialize_microphone(self) -> None:
        # Initialize the microphone with proper error handling
        # Suppress ALSA messages during microphone initialization if not in debug mode
        old_stderr = None
        if not self.debug:
            old_stderr = suppress_alsa_messages()
        
        try:
            # Use specific microphone device if provided, otherwise use default
            if self.device_index is not None:
                self.microphone = sr.Microphone(device_index=self.device_index)
                if self.debug:
                    mic_names = sr.Microphone.list_microphone_names()
                    if self.device_index < len(mic_names):
                        print(f"Using specified microphone: {mic_names[self.device_index]} (index {self.device_index})")
            else:
                # Try to find a working microphone automatically
                self.microphone, mic_name = self._find_working_microphone()
                print(f"Microphone: {mic_name}", flush=True)
        finally:
            # Restore stderr
            if not self.debug and old_stderr is not None:
                restore_stderr(old_stderr)
    
    def _find_working_microphone(self) -> Tuple[sr.Microphone, str]:
        # Find the first working microphone device
        # Use system default microphone - this is most reliable
        if self.debug:
            print("Using system default microphone (most reliable)")
        return sr.Microphone(), "System default microphone"
    
    def list_microphones(self) -> None:
        # List all available microphone devices
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  {index}: {name}")
    
    def test_microphone(self) -> None:
        # Test microphone access and show configuration
        # Suppress ALSA messages during microphone testing if not in debug mode
        old_stderr = None
        if not self.debug:
            old_stderr = suppress_alsa_messages()
        
        try:
            with self.microphone as source:
                if self.debug:
                    print(f"Microphone sample rate: {source.SAMPLE_RATE}")
                    print(f"Microphone chunk size: {source.CHUNK}")
                # Ensure sample rate matches Vosk model expectation
                if hasattr(source, 'SAMPLE_RATE') and source.SAMPLE_RATE != 16000:
                    if self.debug:
                        print(f"Note: Microphone rate {source.SAMPLE_RATE}Hz will be resampled to 16000Hz for Vosk")
        except OSError as e:
            if self.debug:
                print(f"Error accessing microphone: {e}")
                print("Available microphones:")
                self.list_microphones()
                # Try to use PulseAudio directly as fallback
                print("Attempting to use PulseAudio default source...")
            self.microphone = sr.Microphone()
            try:
                with self.microphone as source:
                    pass  # Just test access
                if self.debug:
                    print("Successfully switched to PulseAudio default")
            except Exception as fallback_e:
                if self.debug:
                    print(f"PulseAudio fallback also failed: {fallback_e}")
                raise
        finally:
            # Restore stderr
            if not self.debug and old_stderr is not None:
                restore_stderr(old_stderr)