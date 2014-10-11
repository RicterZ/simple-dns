from twisted.names import client, dns, server
from twisted.internet import reactor


def main():
    factory = server.DNSServerFactory(
        clients=[client.createResolver(servers=[('114.114.114.114', 53)], hosts='hosts')]
    )

    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(53, protocol)
    reactor.listenTCP(53, factory)

    reactor.run()


if __name__ == '__main__':
    raise SystemExit(main())