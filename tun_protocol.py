#!/usr/bin/env python

from zope.interface import implementer

from twisted.internet import reactor, protocol, interfaces
from twisted.pair.tuntap import TuntapPort
from twisted.pair.ip import IPProtocol


@implementer(interfaces.IPushProducer, interfaces.IConsumer)
class TunProducerConsumer(IPProtocol):

    def __init_(self):
        print "__init__"
        # IConsumer
        self.producer = None

    def setConsumer(self, consumer):
        # IPushProducer
        consumer.registerProducer(self, streaming=True)
        self.consumer = consumer

    # XXX correct?
    def logPrefix(self):
        return 'TunProducerConsumer'

    # IPProtocol
    def datagramReceived(self, datagram, partial=None):
        print "datagramReceived"
        # XXX should we keep this assertion?
        # TuntapPort expects our function signature to contain a partial= argument but sets it's value to zero.
        # https://twistedmatrix.com/trac/browser/tags/releases/twisted-15.4.0/twisted/pair/tuntap.py#L338
        assert partial == 0
        self.consumer.write(datagram)

    # IPushProducer

    def pauseProducing(self):
        print "pauseProducing"

    def resumeProducing(self):
        print "resumeProducing"

    def stopProducing(self):
        print "stopProducing"

   # IConsumer

    def write(self, packet):
        print "write"
        self.transport.write(packet)

    def registerProducer(self, producer, streaming):
        print "registerProducer"
        assert streaming is True

        self.producer = producer
        self.producer.resumeProducing()

    def unregisterProducer(self):
        print "unregisterProducer"
        self.producer.stopProducing()
