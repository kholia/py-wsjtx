import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pywsjtx.extra.simple_server

#IP_ADDRESS = '224.1.1.1'
#PORT = 5007

IP_ADDRESS = '127.0.0.1'
PORT = 2237

s = pywsjtx.extra.simple_server.SimpleServer(IP_ADDRESS, PORT, timeout=2.0)

while True:

    (pkt, addr_port) = s.rx_packet()
    if (pkt != None):
        print(pkt)
        the_packet = pywsjtx.WSJTXPacketClassFactory.from_udp_packet(addr_port, pkt)
        if type(the_packet) == pywsjtx.StatusPacket:
            pass
        print(the_packet)


