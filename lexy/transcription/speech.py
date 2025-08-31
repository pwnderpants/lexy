# Main speech transcription class combining audio and transcription components

import speech_recognition as sr
from typing import Optional
from ..audio import MicrophoneManager, AudioProcessor, suppress_alsa_messages, restore_stderr
from .engine import TranscriptionEngine


class SpeechTranscriber:
    # Main class for continuous speech transcription
    
    def __init__(self, timeout: int = 1, phrase_timeout: float = 0.3, 
                 device_index: Optional[int] = None, debug: bool = False, 
                 model_path: str = "vosk-model-small-en-us-0.15"):
        self.timeout = timeout
        self.phrase_timeout = phrase_timeout
        self.debug = debug
        self.is_listening = False
        
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.mic_manager = MicrophoneManager(device_index, debug)
        self.audio_processor = AudioProcessor(debug)
        self.transcription_engine = TranscriptionEngine(model_path, debug)
        
        # Configure recognizer settings
        self._configure_recognizer()
        
        # Test microphone and show configuration
        self.mic_manager.test_microphone()
        
        print("Continuous transcription mode" + (" (debug mode)" if self.debug else ""), flush=True)
    
    def _configure_recognizer(self) -> None:
        # Configure speech recognizer with optimal settings
        # Set microphone sensitivity - extremely sensitive settings
        self.recognizer.energy_threshold = 10   # Extremely low threshold
        self.recognizer.dynamic_energy_threshold = False  # Don't auto-adjust
        self.recognizer.pause_threshold = 0.5   # Shorter pause
        self.recognizer.non_speaking_duration = 0.3
        
        # Skip ambient noise adjustment - use our manual threshold
        if self.debug:
            print("Skipping ambient noise adjustment - using manual threshold")
            print("Using Vosk offline speech recognition")
            print(f"Energy threshold: {self.recognizer.energy_threshold}")
    
    def listen_for_speech(self) -> Optional[str]:
        # Listen for audio and return transcribed text if any
        # Suppress ALSA messages during audio capture if not in debug mode
        old_stderr = None
        if not self.debug:
            old_stderr = suppress_alsa_messages()
        
        try:
            with self.mic_manager.microphone as source:
                # Force capture audio data regardless of energy threshold
                # by using a very short phrase time limit and handling the timeout
                try:
                    # Use longer timeout to capture more speech
                    timeout_val = 0.5
                    phrase_limit = 2.0
                    audio = self.recognizer.listen(source, timeout=timeout_val, phrase_time_limit=phrase_limit)
                except sr.WaitTimeoutError:
                    # Even if timeout, try to get some ambient audio to show levels
                    audio = self.audio_processor.capture_ambient_audio(
                        source, source.CHUNK, source.SAMPLE_RATE
                    )
                    if audio is None:
                        if self.debug:
                            print("\\rAudio: [░░░░░░░░░░░░░░░░░░░░] 0.0 (0 bytes)", end="", flush=True)
                        return None
            
            # Calculate audio level for monitoring
            audio_level = self.audio_processor.get_audio_level(audio)
            
            if self.debug:
                # Show raw audio data info first
                raw_data = audio.get_raw_data()
                raw_bytes = len(raw_data) if raw_data else 0
                self.audio_processor.display_audio_level(audio_level, raw_bytes)
            
            # Only try speech recognition if we have any audio (very low threshold)
            if audio_level > 0.5:
                return self._process_audio_for_transcription(audio)
            else:
                return None
                
        except sr.WaitTimeoutError:
            # No audio detected within timeout
            if self.debug:
                print("\\rAudio: [░░░░░░░░░░░░░░░░░░░░] 0.0", end="", flush=True)
            return None
        except Exception as e:
            if self.debug:
                print(f"\\nMicrophone error: {e}")
            # Try to reinitialize microphone
            try:
                self.mic_manager._initialize_microphone()
                if self.debug:
                    print("Reinitialized microphone")
            except Exception:
                if self.debug:
                    print("Failed to reinitialize microphone")
            return None
        finally:
            # Restore stderr
            if not self.debug and old_stderr is not None:
                restore_stderr(old_stderr)
    
    def _process_audio_for_transcription(self, audio: sr.AudioData) -> Optional[str]:
        # Process audio data through the transcription engine
        raw_data = audio.get_raw_data()
        
        # Convert audio to 16kHz if needed (Vosk expects 16kHz)
        if audio.sample_rate != 16000:
            raw_data = self.audio_processor.resample_audio_for_vosk(
                raw_data, audio.sample_rate
            )
        
        # Get transcription results
        final_text, partial_text = self.transcription_engine.transcribe_audio(raw_data)
        
        if final_text:  # Got final result
            if self.debug:
                print(f" -> '{final_text}'")
            return final_text
        
        # Show partial results
        if partial_text:
            if self.debug:
                print(f" -> (partial) '{partial_text}'")
            # Don't return partial results as final, just for debugging
        elif self.debug:
            print(" -> (unclear)")
        
        return None
    
    def start_listening(self) -> None:
        # Start the main listening loop
        self.is_listening = True
        if self.debug:
            print("Press Ctrl+C to stop transcription (Debug mode - showing audio levels)")
        else:
            print("Press Ctrl+C to stop transcription")
        
        try:
            while self.is_listening:
                recognized_text = self.listen_for_speech()
                
                if recognized_text:
                    # Output all recognized text
                    if self.debug:
                        print()  # New line after audio bar
                    print(f"[TRANSCRIBED]: {recognized_text}")
                
        except KeyboardInterrupt:
            print("\\nStopping transcription...")
            self.is_listening = False