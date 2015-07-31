from glados.module import Module


class MPRISModule(Module):

    def start(self):
        pass

    def handle(self):
        pass

    def shutdown(self):
        pass

MODULE = {
    'name': "mpris",
    'description': "Controls an mpris server",
    'version': "0.1",
    'words': ["movie", "mpris"],
    'class': MPRISModule
}



