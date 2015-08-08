import sys
from glados.module import Module


class UnintelligibleModule(Module):

    def handle(self, words):
        self.playback.play_tts("Couldn't understand", lang="en")

MODULE = {
    'name': "unintelligible",
    'description': "Answers if we failed to understand the voice",
    'version': "0.1",
    'words': [],
    'priority': -sys.maxint - 1,
    'cls': UnintelligibleModule
}
