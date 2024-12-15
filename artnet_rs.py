"""(Very) Simple Implementation of Artnet.

Python Version: 3.6
Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf

NOTES
- Based off StupidArtnet by cpvalent
- For simplicity: NET and SUBNET not used by default but optional

"""
import socket
import errno

class ArtnetServer():
    """(Very) simple implementation of an Artnet Server."""
    UDP_PORT = 6454
    ARTDMX_HEADER = b'Art-Net\x00\x00P\x00\x0e'
    
    def __init__(self, ip_addr:str, timeout_ms: int):
        """Initializes Art-Net server."""
        # server active flag
        self.listen = True
        # Initialise socket - Bind to UDP on the correct PORT
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk_addr = socket.getaddrinfo(ip_addr, 6454)[0][-1]
        self.socket_server.bind(sk_addr)
        timeout = timeout_ms/1000  
        self.socket_server.settimeout(timeout)
        print("socket_server:  ", self.socket_server)

    def recv_data(self):
        """ Receive data with timeout"""
        try:
            data, unused_addr = self.socket_server.recvfrom(1024)
        except OSError as e:
            if e.errno == errno.ETIMEDOUT:
                return None 
        return data

    def close(self):
        print("Closing socket")
        self.socket_server.close()
