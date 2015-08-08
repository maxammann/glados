from glados.matrix.matrix import discover_matrix
from glados.module import Module


class MatrixModule(Module):

    def handle(self, words):
        if "next" in words:
            discover_matrix().menu_next()  # todo test
        elif "previous" in words:
            discover_matrix().menu_previous()  # todo test

        # todo push activation


MODULE = {
    'name': "matrix",
    'description': "Controls an matrix alarm clock",
    'version': "0.1",
    'words': ["matrix"],
    'cls': MatrixModule
}
