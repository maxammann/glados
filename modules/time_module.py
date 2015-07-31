import time
from glados.module import Module


class TimeModule(Module):

    def handle(self):
        self.playback.play_tts(time.strftime('%l:%M%p %Z on %b %d, %Y'))
        pass

MODULE = {
    'name': "time",
    'description': "Tells the time",
    'version': "0.1",
    'words': ["time", "clock"],
    'class': TimeModule
}
