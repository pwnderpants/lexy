# Audio utility functions for suppressing system messages

import os
from typing import Optional


def suppress_alsa_messages() -> Optional[int]:
    # Suppress ALSA library error messages by redirecting stderr
    try:
        # Redirect stderr to devnull to suppress ALSA messages
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        os.dup2(devnull, 2)
        os.close(devnull)
        return old_stderr
    except OSError:
        return None


def restore_stderr(old_stderr: Optional[int]) -> None:
    # Restore stderr if it was previously saved
    if old_stderr is not None:
        try:
            os.dup2(old_stderr, 2)
            os.close(old_stderr)
        except OSError:
            pass