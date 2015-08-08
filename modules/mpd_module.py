import sched
import mpd
import time
from glados.module import Module


class MPDModule(Module):
    def __init__(self, playback, module_info):
        Module.__init__(self, playback, module_info)

        self.client = mpd.MPDClient()
        self.client.idletimeout = None

    def start(self):
        self.client.connect("192.168.0.97", 6600)

    def get_client(self):
        try:
            self.client.ping()
        except mpd.ConnectionError:
            self.start()

        return self.client

    def handle(self, words):
        if "play" in words or "they" in words:
            self.get_client().play()
        elif "pause" in words or "boss" in words:
            self.get_client().pause()
        elif "stop" in words:
            self.get_client().pause()
        elif "next" in words:
            self.get_client().next()
        elif "currently" in words or "what" in words:
            currentsong = self.get_client().currentsong()
            self.playback.play_tts("Currently playing " + currentsong['title'] + " by " + currentsong['artist'], lang="en")
        # print self.client.playlistid(self.client.status()['nextsongid'])

    def shutdown(self):
        self.client.close()
        self.client.disconnect()


MODULE = {
    'name': "mpd",
    'description': "Controls an mpd server",
    'version': "0.1",
    'words': ["music", "mpd", "song"],
    'cls': MPDModule
}
