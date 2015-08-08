class Module(object):
    def __init__(self, playback, module_info):
        self.module_info = module_info
        self.playback = playback

    def start(self):
        return False

    def is_responsibly(self, words):
        for word in self.module_info.words:
            if word in words:
                return True
        return False

    def handle(self, text):
        return False

    def shutdown(self):
        return False


class ModuleInfo(object):
    def __init__(self, raw_module_info):
        self.__dict__ = raw_module_info
        self.instance = None

    def create(self, playback):
        return self.cls(playback, self)

    def set_instance(self, instance):
        self.instance = instance

    def get_instance(self):
        return self.instance

    def is_responsibly(self, words):
        return self.instance.is_responsibly(words)
