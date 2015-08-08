import socket
import struct
from glados.matrix import discovery
from glados.matrix.lm_pb2 import Request, SetScreen


def discover_matrix():
    return Matrix(discovery.discovery(), 6969)


class Matrix(object):

    def __init__(self,  host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.connect((host, port))

    def pause(self):
        request = Request()
        request.type = Request.PAUSE

        self.send(request)

    def set_screen(self, name):
        request = Request()
        request.type = Request.SETSCREEN
        set_screen = SetScreen()
        set_screen.name = name

        request.setscreen = set_screen

        self.send(request)

    def menu_previous(self):
        request = Request()
        request.type = Request.MENU_PREVIOUS
        self.send(request)

    def menu_next(self):
        request = Request()
        request.type = Request.MENU_NEXT
        self.send(request)

    def unpause(self):
        request = Request()
        request.type = Request.UNPAUSE

        self.send(request)

    def send(self, message):
        data = message.SerializeToString()

        self.socket.send(struct.pack(">I", len(data)))
        self.socket.send(data)
