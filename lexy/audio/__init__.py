# Audio handling modules for Lexy

from .utils import suppress_alsa_messages, restore_stderr
from .microphone import MicrophoneManager
from .processing import AudioProcessor

__all__ = ['suppress_alsa_messages', 'restore_stderr', 'MicrophoneManager', 'AudioProcessor']