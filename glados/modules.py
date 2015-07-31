import pkgutil


class Modules(object):
    def __init__(self, logger, locations):
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
                    modules.append(module)

        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0, reverse=True)
        return modules

        # def query(self, texts):
        #     for module in self.modules:
        #         for text in texts:
        #
        #             if module.isValid(text):
        #                 self.logger.debug("'%s' is a valid phrase for module " +
        #                                   "'%s'", text, module.__name__)
        #                 try:
        #                     module.handle(text, self.mic, self.profile)
        #                 except:
        #                     self.logger.error('Failed to execute module',
        #                                       exc_info=True)
        #                     self.mic.say("I'm sorry. I had some trouble with " +
        #                                  "that operation. Please try again later.")
        #                 else:
        #                     self.logger.debug("Handling of phrase '%s' by " +
        #                                       "module '%s' completed", text,
        #                                       module.__name__)
        #                 finally:
        #                     return
        #     self.logger.debug("No module was able to handle any of these " +
        #                       "phrases: %r", texts)
