"""(Very) Simple Implementation of Artnet.

Python Version: 3.6
Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf

NOTES
- Based off StupidArtnet by cpvalent
- For simplicity: NET and SUBNET not used by default but optional

"""
import socket
import errno

ARTNET_POLL = b'Art-Net\x00\x00 \x00\x0e\x02\x00'
ARTDMX_HEADER = b'Art-Net\x00\x00P\x00\x0e'

class ArtnetServer():
    """(Very) simple implementation of an Artnet Server."""
    UDP_PORT = 6454
    
    def __init__(self, ip_addr:str, timeout_ms: int):
        """Initializes Art-Net server."""
        # server active flag
        self.listen = True
        # Initialise socket - Bind to UDP on the correct PORT
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk_addr = socket.getaddrinfo(ip_addr, 6454)[0][-1]
        self.socket_server.bind(sk_addr)
        #timeout = timeout_ms/1000
        #self.socket_server.settimeout(timeout)
        #self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("socket_server:  ", self.socket_server)

    def recv_data(self):
        """ Receive data with timeout"""
        try:
            bytestr, unused_addr = self.socket_server.recvfrom(1024)
        except OSError as e:
            if e.errno == errno.ETIMEDOUT:
                return None 
        #print(bytestr)
        if bytestr[:14] == ARTNET_POLL:
            #print("Artnet Poll")
            return None
        elif bytestr[:12] == ARTDMX_HEADER:
            data = list(bytestr)
            print("Sequence: ",data[12])
            #print("Physical input port: ",data[13])
            #print("15bit port address: ",data[14:16])
            #print("Array length: ",data[16:17])
            return data[18:42]
        else:
            print('ERROR!!!! - unknown packet type')

    def close(self):
        print("Closing socket")
        self.socket_server.close()
