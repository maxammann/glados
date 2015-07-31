import io
import os
import wave
import time

from glados.audio.mp3_decoder import mp3_decode
from glados.audio.ivona import Ivona

CHUNK = 1024
this_dir, this_filename = os.path.split(__file__)
high_beep = os.path.join(this_dir, "../../audio", "beep_hi.wav")
low_beep = os.path.join(this_dir, "../../audio", "beep_lo.wav")


def open_microphone(audio, channels, rate, sample_size):
    width = audio.get_format_from_width(sample_size)
    return audio.open(format=width,
                      channels=channels,
                      rate=rate,
                      output=True)


class Playback:
    def __init__(self, audio):
        self.audio = audio

    def play_wav(self, path):
        wf = wave.open(path, 'rb')

        stream = open_microphone(self.audio, wf.getnchannels(), wf.getframerate(), wf.getsampwidth())

        data = wf.readframes(CHUNK)

        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()

    def play_high_beep(self):
        self.play_wav(high_beep)

    def play_low_beep(self,):
        self.play_wav(low_beep)

    def play_raw(self, audio_data, channels, rate, sample_size):
        stream = open_microphone(self.audio, channels, rate, sample_size)
        stream.write(audio_data)
        time.sleep(len(audio_data) / float(sample_size * channels * rate))
        stream.stop_stream()
        stream.close()

    def play_tts(self, text):
        v = Ivona("GDNAI3522R3EVOJTXNZQ", "iqQ0grzlzTTNOP+Ab6hQm+eMZ1jPa+x802mbfbNu")
        v.codec = "mp3"
        v.region = 'us-east'
        v.voice_name = "Salli"

        tts_audio = io.BytesIO()
        v.fetch_voice_fp(text, tts_audio)
        v.fetch_voice(text, "test")
        raw_audio = mp3_decode(tts_audio.getvalue())

        self.play_raw(raw_audio, 1, 22050, 2)

    # def play_tts(self, text, language="en"):
    #     tts = gTTS(text=text, lang=language)
    #     tts_audio = io.BytesIO()
    #     tts.write_to_fp(tts_audio)
    #     print tts_audio.getvalue()
    #     raw_audio = mp3_decode(tts_audio.getvalue())
    #
    #     self.play_raw(raw_audio, 1, 16000, 2)
