from os.path import splitext

import requests

from glados.module import Module


def get(file, payload=None):
    return requests.get("http://192.168.0.97:28781/" + file, params=payload).json()


class MPRISModule(Module):
    def handle(self, words):
        if "play" in words or "they" in words:
            get("play")
        elif "pause" in words or "boss" in words:
            get("pause")
        elif "stop" in words:
            get("stop")
        elif "next" in words:
            get("next")
        elif "currently" in words or "what" in words:
            self.playback.play_tts("Currently playing " + splitext(get("title")['title'])[0], lang="en")
        elif "seek" in words:
            get("seek", payload={"offset": 85})


MODULE = {
    'name': "mpris",
    'description': "Controls an mpris server",
    'version': "0.1",
    'words': ["movie", "mpris"],
    'priority': 0,
    'cls': MPRISModule
}
