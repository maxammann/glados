from socket import *

PORT = 8888

DISCOVERY_REQUEST = 'DISCOVERY_REQUEST'
DISCOVERY_RESPONSE = "DISCOVERY_RESPONSE"


def discovery():
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    s.sendto(DISCOVERY_REQUEST, ('255.255.255.255', PORT))

    message = s.recvfrom(len(DISCOVERY_RESPONSE))
    if message[0] == DISCOVERY_RESPONSE:
        return message[1][0]
