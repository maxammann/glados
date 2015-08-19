import Queue
from pyjulius.models import Sentence

from glados.byte_buffer_queue import ByteBufferQueue
from glados.matrix.matrix import discover_matrix


class Passive:
    def __init__(self, playback, recognizer, julius, modules):
        self.julius = julius
        self.modules = modules
        self.recognizer = recognizer
        self.playback = playback

        self.running = True
        self.segments = ByteBufferQueue()
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
        self.segments.destroy()

    def listen(self):
        while self.running:
            try:
                data = self.recognizer.listen(min_duration=2)

                if data is None:
                    continue

                self.segments.append(data)
            except KeyboardInterrupt:
                break

    def get_segments(self):
        return self.segments.pop()

    active = False

    def recognize_string(self, data, text):
        try:
            lower = str(self.recognizer.recognize(data, show_all=True)).lower()

            if text in lower:
                return True
            else:
                return False
        except LookupError:
            return False

    def is_activated(self, data):
        ret = False
        print("Testing activated")
        while self.running:
            print("Getting result")
            try:
                result = self.julius.client.results.get(timeout=3)
            except Queue.Empty:
                break
            print("Finished Getting result")
            if result.tag == 'RECOGOUT':
                sentence = Sentence.from_shypo(result.find('SHYPO'))
                words = [word.word.encode("UTF-8") for word in sentence.words]

                if "ALEXA" in words:
                    print("Start google recognize ")
                    if self.recognize_string(data, "alexa"):
                        ret = True
                        break
                print("Switching to passive...")
                break
            elif result.tag == 'INPUT' and result.attrib['STATUS'] == 'LISTEN':
                break

        print("Clearing")
        self.julius.client.results.queue.clear()
        print("Clearing finished")
        print("Finished activated " + str(ret))

        return ret

    def passive_recognize(self):

        while self.running:
            try:
                if self.active:
                    print("Activated")

                    self.playback.play_high_beep()
                    discover_matrix().unpause()  # todo test

                    print("Waiting for input...")

                    data = self.get_segments()
                    # todo only continue if there's enough data
                    if data is None:
                        break

                    self.recognize(data)

                    self.passive = True
                    self.active = False
                    print("Switching to passive...")
                elif self.passive:
                    print("Recording for julius")
                    data = self.get_segments()
                    if data is None:
                        break

                    print("Sending audio to julius")
                    # todo stuck in here
                    self.julius.send_audio(data)
                    print("Finished")

                    self.active = self.is_activated(data)
                    if self.active:
                        self.passive = False
                else:
                    print "Hmm"
                    print "Passive " + str(self.passive)
                    print "Active " + str(self.active)

            except KeyboardInterrupt:
                break
