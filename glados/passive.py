import Queue
import sys

import pyjulius

from glados.matrix.matrix import discover_matrix


class Passive:
    STOP_TOKEN = object()

    def __init__(self, playback, recognizer, julius, modules):
        self.julius = julius
        self.modules = modules
        self.recognizer = recognizer
        self.playback = playback

        self.running = True
        self.segments = Queue.Queue()
        self.passive = True

    def recognize(self, data):

        print("Recognizing input...")

        try:
            text = str(self.recognizer.recognize(data, show_all=True))
            print("You said: " + text)
            # self.playback.play_tts(text)
        except LookupError as e:
            self.playback.play_low_beep()
            text = e.message

        try:
            self.modules.handle(text)
        except Exception as e:
            print("Unexpected error in module: " + e.message)

        discover_matrix().pause()  # todo test

        return True

    def stop(self):
        self.running = False
        self.segments.put(self.STOP_TOKEN)

    def listen(self):
        while self.running:
            try:
                data = self.recognizer.listen(min_duration=2)

                if data is None:
                    continue

                self.segments.put(data)
            except KeyboardInterrupt:
                break

    def get_segments(self):
        # todo retry if timeout
        data = self.segments.get(True, sys.maxint)

        if data is self.STOP_TOKEN:
            return self.STOP_TOKEN

        result = []

        while self.segments.qsize() > 0:
            get = self.segments.get(True, sys.maxint)
            if get is self.STOP_TOKEN:
                return self.STOP_TOKEN
            result.append(get)

        result.insert(0, data)

        return "".join(result)

    last_passive = None

    def recognize_string(self, data, text):
        try:
            lower = str(self.recognizer.recognize(data, show_all=True)).lower()

            if text in lower:
                return True
            else:
                return False
        except LookupError:
            return False

    def is_activated(self):
        result = self.julius.client.results.get()

        if isinstance(result, pyjulius.Sentence):
            words = [word.word.encode("UTF-8") for word in result.words]

            if "ALEXA" in words:
                if self.last_passive and self.recognize_string(self.last_passive, "alexa"):
                    return True
            print("Switching to passive...")
            self.passive = True

        return False

    def passive_recognize(self):

        while self.running:
            try:

                if self.passive:
                    print("Recording for julius")
                    data = self.get_segments()
                    if data is self.STOP_TOKEN:
                        break

                    self.last_passive = data
                    print("Sending audio to julius")
                    self.julius.send_audio(data)
                    print("Finished")
                    self.passive = False
                else:
                    if self.is_activated():
                        print("Activated")

                        self.playback.play_high_beep()
                        discover_matrix().unpause()  # todo test

                        print("Waiting for input...")

                        data = self.get_segments()
                        # todo only continue if there's enough data
                        if data is self.STOP_TOKEN:
                            break

                        self.recognize(data)

                        self.passive = True
                        print("Switching to passive...")

            except KeyboardInterrupt:
                break
