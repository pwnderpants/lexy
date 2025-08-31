# Audio processing utilities for level calculation and monitoring

import numpy as np
import pyaudio
import speech_recognition as sr
from typing import Optional
from .utils import suppress_alsa_messages, restore_stderr


class AudioProcessor:
    # Handles audio processing and level monitoring
    
    def __init__(self, debug: bool = False):
        self.debug = debug
    
    def get_audio_level(self, audio_data: sr.AudioData) -> float:
        # Calculate RMS audio level from audio data
        try:
            # Convert audio data to numpy array
            audio_np = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
            # Calculate RMS (Root Mean Square) level
            rms = np.sqrt(np.mean(audio_np.astype(np.float32) ** 2))
            # Convert to dB-like scale (0-100)
            if rms > 0:
                level = min(100, max(0, 20 * np.log10(rms / 32768.0) + 100))
            else:
                level = 0
            return level
        except Exception:
            return 0
    
    def capture_ambient_audio(self, source: sr.Microphone, chunk: int, 
                             sample_rate: int) -> Optional[sr.AudioData]:
        # Capture a small chunk of ambient audio for level monitoring
        # Suppress ALSA messages if not in debug mode
        old_stderr = None
        if not self.debug:
            old_stderr = suppress_alsa_messages()
        
        try:
            # Get audio format from the source
            format_type = pyaudio.paInt16  # 16-bit audio
            channels = 1
            
            # Record a small chunk to show audio levels
            p = pyaudio.PyAudio()
            stream = p.open(format=format_type, channels=channels, rate=sample_rate, 
                          input=True, frames_per_buffer=chunk)
            
            try:
                raw_data = stream.read(chunk, exception_on_overflow=False)
                stream.stop_stream()
                stream.close()
                p.terminate()
                
                # Create a fake audio object for level calculation
                audio = sr.AudioData(raw_data, sample_rate, 2)  # 2 bytes per sample for int16
                return audio
            except Exception:
                if stream:
                    stream.stop_stream()
                    stream.close()
                if p:
                    p.terminate()
                return None
        finally:
            if not self.debug and old_stderr is not None:
                restore_stderr(old_stderr)
    
    def display_audio_level(self, audio_level: float, raw_bytes: int = 0) -> None:
        # Display audio level as a visual bar
        if self.debug:
            # Show audio level bar
            bar_length = 20
            filled_length = int(audio_level / 5)  # Scale 0-100 to 0-20
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            print(f"\\rAudio: [{bar}] {audio_level:.1f} ({raw_bytes} bytes)", end="", flush=True)
    
    def resample_audio_for_vosk(self, audio_data: bytes, original_rate: int, 
                               target_rate: int = 16000) -> bytes:
        # Resample audio data to target rate for Vosk processing
        if original_rate == target_rate:
            return audio_data
        
        # Resample audio data to target rate
        import audioop
        return audioop.ratecv(audio_data, 2, 1, original_rate, target_rate, None)[0]