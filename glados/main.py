import pkgutil
import threading
import time
import signal
import logging
import traceback
import subprocess
import sys

import pyaudio

from glados.audio.playback import Playback
from glados.audio.recognizer import Recognizer
from glados.audio.suppress_alsa import noalsaerr
from glados.audio.julius import Julius
from glados.modules import Modules
from glados.passive import Passive


def run():
    this_dir, this_filename = pkgutil.os.path.split(__file__)
    locations = [pkgutil.os.path.join(this_dir, "../modules")]

    # modules.get_modules()[3].MODULE["class"](Playback(pyaudio.PyAudio())).handle()

    # Playback(pyaudio.PyAudio()).play_tts("Hello World")
    # Playback(pyaudio.PyAudio()).play_high_beep()

    # modules = Modules(logging.getLogger(), locations, Playback(pyaudio.PyAudio()))
    #
    # print modules.query(["time"])

    julius_process = subprocess.Popen(("julius -C " + str(sys.argv[1]) + " -input adinnet -module -no_ccd").split(),
                             stdout=subprocess.PIPE)

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

    # recognizer.sample_threshold()
    recognizer.threshold = 90

    modules = Modules(logging.getLogger(), locations, playback)

    passive = Passive(playback, recognizer, julius, modules)

    print "Threshhold " + str(recognizer.threshold)

    def shutdown(signal, frame):
        recognizer.interrupt()
        passive.stop()

    signal.signal(signal.SIGINT, shutdown)

    print("Starting listening thread")
    t = threading.Thread(target=passive.listen)
    t.start()

    try:
        passive.passive_recognize()
    except Exception as e:
        traceback.print_exc(e)

    print('Exiting...')
    modules.stop_modules()

    julius.disconnect()

    t.join()
    recognizer.close()
    audio.terminate()
    julius_process.terminate()
