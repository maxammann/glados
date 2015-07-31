import pyjulius
import socket
import struct

TERMINATOR = struct.pack("I", 0)


class Julius:

    def __init__(self, host="localhost", module_port=10500, adin_port=5530):
        self.host = host
        self.adin_port = adin_port

        # Initialize and try to connect
        self.client = pyjulius.Client(host, module_port)
        # Connect adin
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_module(self):
        try:
            self.client.connect()
        except pyjulius.ConnectionError:
            return False

        # Start listening to the server
        self.client.start()

        return True

    def connect_adin(self):
        try:
            self.s.connect((self.host, self.adin_port))
        except socket.error:
            return False

        return True

    def disconnect(self):
        self.client.stop()  # send the stop signal
        self.client.join()  # wait for the thread to die
        self.client.disconnect()  # disconnect from julius

        self.s.close()

    def send_audio(self, buffer):
        # https://github.com/Cinderella-Man/tofik/blob/master/adintool/adintool.c#L684
        # https://github.com/UFAL-DSG/openjulius/blob/master/libsent/src/net/rdwt.c#L100
        self.s.send(struct.pack("I", buffer.__len__()))
        self.s.send(buffer)
        # https://github.com/Cinderella-Man/tofik/blob/master/adintool/adintool.c#L728
        self.s.send(TERMINATOR)
