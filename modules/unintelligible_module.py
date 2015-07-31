from glados.module import Module


class TimeModule(Module):

    def handle(self):
        self.playback.play_tts("Sorry, couldn't understand you!")
        pass

MODULE = {
    'name': "unintelligible",
    'description': "Answers if we failed to understand the voice",
    'version': "0.1",
    'words': [],
    'class': TimeModule
}
