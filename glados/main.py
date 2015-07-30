import threading
import time
import pyaudio
import signal
from glados.audio.playback import Playback
from glados.audio.recognizer import Recognizer
from glados.audio.suppress_alsa import noalsaerr
from glados.julius import Julius
from glados.passive import start_passive_listening, start_passive_recognizing
from glados import passive


def shutdown(signal, frame):
    passive.running = False


def run():
    # Playback(pyaudio.PyAudio()).play_tts("Hello World")

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

    signal.signal(signal.SIGINT, shutdown)

    print("Starting listening thread")
    t = threading.Thread(target=start_passive_listening, args=[recognizer, julius])
    t.start()

    start_passive_recognizing(playback, recognizer, julius)

    print('Exiting...')

    shutdown(signal.SIGINT, 0)
    julius.disconnect()
    recognizer.close()
    audio.terminate()
