import os
import signal
from typing import Callable


def do_after_sigint(callback: Callable[[], None]):
    def signal_handler(sig, frame):
        callback()
        os.kill(os.getpid(), signal.SIGKILL)

    signal.signal(signal.SIGINT, signal_handler)
