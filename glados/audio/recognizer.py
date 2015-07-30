import time
import wave
import audioop
import json
import pyaudio
from urllib2 import URLError, Request, urlopen

SPEECH_URL = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang=%s&key=%s"

THRESHOLD_MULTIPLIER = 3

CHANNELS = 1
RATE = 16000
CHUNK = 1024

DELAY_MULTIPLIER = 0.6


def get_score(data):
    rms = audioop.rms(data, 2)
    score = rms / 3
    return score


def sample_threshold(stream, time=2):
    # stores the audio data
    frames = []

    # stores the lastN score values
    last_n = [i for i in range(20)]

    average = 0

    # calculate the long run average, and thereby the proper threshold
    for i in range(0, RATE / CHUNK * time):
        data = stream.read(CHUNK)
        frames.append(data)

        # save this data point as a score
        last_n.pop(0)
        last_n.append(get_score(data))
        average = sum(last_n) / len(last_n)

    # this will be the benchmark to cause a disturbance over!
    threshold = average * THRESHOLD_MULTIPLIER

    return threshold


def save_speech(audio, data):
    filename = 'output_' + str(int(time.time()))
    # writes data to WAV file
    data = ''.join(data)
    wf = wave.open(filename + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)  # TODO make this value a function parameter?
    wf.writeframes(data)
    wf.close()
    return filename + '.wav'


class Recognizer:
    def __init__(self, audio):
        self.audio = audio
        self.stream = None
        self.threshold = 50

    def open(self):
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()

    def sample_threshold(self, duration=1):
        self.threshold = sample_threshold(self.stream, duration)

    def listen(self):
        # save some memory for sound data
        frames = []

        # flag raised when sound disturbance detected
        listening = False

        while True:
            data = self.stream.read(CHUNK)
            frames.append(data)
            score = get_score(data)

            if score > self.threshold:
                listening = True
            elif listening:
                break

        # cutoff any recording before this disturbance was detected
        frames = frames[-20:]

        # let's keep recording for few seconds and save the file
        for i in range(0, int(round(RATE / CHUNK * DELAY_MULTIPLIER))):
            data = self.stream.read(CHUNK)
            frames.append(data)

        return ''.join(frames)

    def recognize(self, audio_data, show_all=False):
        url = SPEECH_URL % ("en_US", "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw")
        request = Request(url, data=audio_data, headers={"Content-Type": "audio/l16; rate=16000"})

        # check for invalid key response from the server
        try:
            response = urlopen(request)
        except URLError:
            raise IndexError("No internet connection available to transfer audio data")
        except:
            raise KeyError("Server wouldn't respond (invalid key or quota has been maxed out)")
        response_text = response.read().decode("utf-8")

        # print response_text

        # ignore any blank blocks
        actual_result = []
        for line in response_text.split("\n"):
            if not line:
                continue
            result = json.loads(line)["result"]
            if len(result) != 0:
                actual_result = result[0]
                break

        # make sure we have a list of transcriptions
        if "alternative" not in actual_result:
            raise LookupError("Speech is unintelligible")

        # return the best guess unless told to do otherwise
        if not show_all:
            for prediction in actual_result["alternative"]:
                if "transcript" in prediction:
                    return prediction["transcript"]
            raise LookupError("Speech is unintelligible")

        # return all the possibilities
        spoken_text = []
        for i, prediction in enumerate(actual_result["alternative"]):
            if "transcript" in prediction:
                spoken_text.append({"text": prediction["transcript"], "confidence": 1 if i == 0 else 0})
        return spoken_text
