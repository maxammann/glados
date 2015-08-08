import time
from glados.module import Module


class TimeModule(Module):

    def handle(self, words):
        self.playback.play_tts("It is " + time.strftime('%H %M'), lang="en")
        pass

MODULE = {
    'name': "time",
    'description': "Tells the time",
    'version': "0.1",
    'words': ["time", "clock"],
    'priority': 0,
    'cls': TimeModule
}
