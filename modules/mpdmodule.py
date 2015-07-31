import mpd
from glados.module import Module


class MPDModule(Module):
    def __init__(self, playback):
        Module.__init__(self, playback)

        self.client = mpd.MPDClient()

    def start(self):
        self.client.connect("localhost", 6600)

    def handle(self):
        print self.client.currentsong()
        print self.client.playlistid(self.client.status()['nextsongid'])
        pass

    def shutdown(self):
        self.client.close()
        self.client.disconnect()


MODULE = {
    'name': "mpd",
    'description': "Controls an mpd server",
    'version': "0.1",
    'words': ["music", "mpd"],
    'class': MPDModule
}
