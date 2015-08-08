import pkgutil

from glados.module import ModuleInfo


class Modules(object):
    def __init__(self, logger, locations, playback):
        self.playback = playback
        self.locations = locations
        self.logger = logger
        self.modules = self.get_modules()

    def get_modules(self):
        """
        Dynamically loads all the modules in the modules folder and sorts
        them by the PRIORITY key. If no PRIORITY is defined for a given
        module, a priority of 0 is assumed.
        """

        modules = []
        for finder, name, ispkg in pkgutil.walk_packages(self.locations):
            try:
                loader = finder.find_module(name)
                module = loader.load_module(name)
            except RuntimeError:
                self.logger.warning("Skipped module '%s' due to an error.", name, exc_info=True)
            else:
                if hasattr(module, 'MODULE'):
                    self.logger.debug("Found module: %s", module.MODULE)
                    info = ModuleInfo(module.MODULE)
                    instance = info.create(self.playback)
                    instance.start()
                    info.set_instance(instance)
                    modules.append(info)

        modules.sort(key=lambda info: info.priority if hasattr(info, 'priority') else 0, reverse=True)
        return modules

    def stop_modules(self):
        for info in self.modules:
            info.get_instance().shutdown()

    def handle_by_list(self, words):
        return self.query(words).handle(words)

    def handle(self, text):
        words = text.lower()
        return self.query_by_list(words).handle(words)

    def query(self, text):
        return self.query(text.lower())

    def query_by_list(self, words):
        if len(self.modules) == 0:
            return None

        for info in self.modules:
            if info.is_responsibly(words):
                return info.get_instance()

        return self.modules[-1].get_instance()
