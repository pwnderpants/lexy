# Vosk transcription engine wrapper

import json
import vosk
from typing import Optional, Tuple
from ..audio.utils import suppress_alsa_messages, restore_stderr


class TranscriptionEngine:
    # Manages Vosk speech recognition engine
    
    def __init__(self, model_path: str = "vosk-model-small-en-us-0.15", debug: bool = False):
        self.model_path = model_path
        self.debug = debug
        self.vosk_model = None
        self.vosk_rec = None
        self._initialize_vosk()
    
    def _initialize_vosk(self) -> None:
        # Initialize Vosk model and recognizer
        # Suppress ALSA messages if not in debug mode
        old_stderr = None
        if not self.debug:
            old_stderr = suppress_alsa_messages()
        
        try:
            # Initialize Vosk model
            if self.debug:
                print(f"Loading Vosk model from: {self.model_path}")
            self.vosk_model = vosk.Model(self.model_path)
            self.vosk_rec = vosk.KaldiRecognizer(self.vosk_model, 16000)
        finally:
            # Restore stderr
            if not self.debug and old_stderr is not None:
                restore_stderr(old_stderr)
    
    def transcribe_audio(self, raw_data: bytes) -> Tuple[Optional[str], Optional[str]]:
        # Transcribe raw audio data using Vosk
        # Returns: (final_text, partial_text)
        try:
            # Process audio with Vosk
            if self.vosk_rec.AcceptWaveform(raw_data):
                result = json.loads(self.vosk_rec.Result())
                final_text = result.get('text', '').lower().strip()
                
                # Check for partial results
                partial_result = json.loads(self.vosk_rec.PartialResult())
                partial_text = partial_result.get('partial', '').lower().strip()
                
                return final_text if final_text else None, partial_text if partial_text else None
            
            # Only partial results available
            partial_result = json.loads(self.vosk_rec.PartialResult())
            partial_text = partial_result.get('partial', '').lower().strip()
            
            return None, partial_text if partial_text else None
            
        except Exception as e:
            if self.debug:
                print(f"Speech recognition error: {e}")
            return None, None