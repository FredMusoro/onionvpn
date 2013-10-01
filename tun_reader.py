#!/usr/bin/env python

# External modules
from twisted.internet import main
from twisted.internet import reactor
import os

# Internal modules
from tunConfig import tunDevice


class tunReader(object):

    def __init__(self, tun, handlePacket):
        self.tun          = tun
        self.handlePacket = handlePacket
        reactor.addReader(self)

    def connectionLost(self, reason):
        # BUG: we should remove the tun device
        # unless someone is still using it...
        reactor.removeReader(self)

    def fileno(self):
        return self.tun.fileno()

    def doRead(self):
        packet = os.read(self.tun.fileno(), self.tun.mtu)
        self.handlePacket(packet)

    def logPrefix(self):
        return 'tunReader'

def main():

    def printPacketLen(p):
        print len(p)


    mytun = tunDevice(remote_ip = '10.1.1.1',
                    local_ip  = '10.1.1.2',
                    netmask   = '255.255.255.0',
                    mtu       = 1500)

    tunReader(mytun.tun, handlePacket=printPacketLen)

    reactor.run()

if __name__ == '__main__':
    main()