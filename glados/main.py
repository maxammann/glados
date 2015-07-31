import pkgutil
import threading
import time
import signal
import logging

import pyaudio

from glados.audio.playback import Playback
from glados.audio.recognizer import Recognizer
from glados.audio.suppress_alsa import noalsaerr
from glados.audio.julius import Julius
from glados.modules import Modules
from glados.passive import start_passive_recognizing, start_listening
from glados import passive


def run():
    this_dir, this_filename = pkgutil.os.path.split(__file__)
    locations = [pkgutil.os.path.join(this_dir, "../modules")]
    modules = Modules(logging.getLogger(), locations)

    modules.get_modules()[3].MODULE["class"](Playback(pyaudio.PyAudio())).handle()

    # Playback(pyaudio.PyAudio()).play_tts("Hello World")
    # Playback(pyaudio.PyAudio()).play_high_beep()

    julius = Julius()

    print("Waiting for julius module server...")

    connected = False
    while not connected:
        try:
            connected = julius.connect_module()
            time.sleep(0.5)
        except KeyboardInterrupt:
            return

    print("Waiting for julius adin server...")
    connected = False
    while not connected:
        try:
            connected = julius.connect_adin()
            time.sleep(0.5)
        except KeyboardInterrupt:
            return

    print("Initialising audio...")
    with noalsaerr():
        audio = pyaudio.PyAudio()
    recognizer = Recognizer(audio)
    playback = Playback(audio)

    recognizer.open()

    recognizer.sample_threshold()

    print "Threshhold " + str(recognizer.threshold)

    def shutdown(signal, frame):
        passive.stop(recognizer)

    signal.signal(signal.SIGINT, shutdown)

    print("Starting listening thread")
    t = threading.Thread(target=start_listening, args=[recognizer])
    t.start()

    start_passive_recognizing(playback, recognizer, julius)

    print('Exiting...')
    julius.disconnect()

    t.join()
    recognizer.close()
    audio.terminate()
