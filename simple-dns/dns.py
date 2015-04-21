import re
import sys
from twisted.names import client, dns, server, hosts as hosts_module, root, cache, resolve
from twisted.internet import reactor
from twisted.python.runtime import platform


def search_file_for_all(hosts_file, name):
    results = []
    try:
        lines = hosts_file.getContent().splitlines()
    except:
        return results

    name = name.lower()
    for line in lines:
        idx = line.find(b'#')
        if idx != -1:
            line = line[:idx]
        if not line:
            continue
        parts = line.split()
        for domain in [s.lower() for s in parts[1:]]:
            if (domain.startswith('/') and domain.endswith('/') and
                    re.search(domain.strip('/'), name.lower())) or name.lower() == domain.lower():
                results.append(hosts_module.nativeString(parts[0]))
    return results


class Resolver(hosts_module.Resolver):
    def _aRecords(self, name):
        return tuple([
            dns.RRHeader(name, dns.A, dns.IN, self.ttl, dns.Record_A(addr, self.ttl))
            for addr in search_file_for_all(hosts_module.FilePath(self.file), name)
            if hosts_module.isIPAddress(addr)
        ])


def create_resolver(servers=None, resolvconf=None, hosts=None):
    if platform.getType() == 'posix':
        if resolvconf is None:
            resolvconf = b'/etc/resolv.conf'
        if hosts is None:
            hosts = b'/etc/hosts'
        the_resolver = client.Resolver(resolvconf, servers)
        host_resolver = Resolver(hosts)
    else:
        if hosts is None:
            hosts = r'c:\windows\hosts'
        from twisted.internet import reactor
        bootstrap = client._ThreadedResolverImpl(reactor)
        host_resolver = Resolver(hosts)
        the_resolver = root.bootstrap(bootstrap, resolverFactory=client.Resolver)

    return resolve.ResolverChain([host_resolver, cache.CacheResolver(), the_resolver])


def main(port):
    factory = server.DNSServerFactory(
        clients=[create_resolver(servers=[('114.114.114.114', 53)], hosts='hosts')],
    )
    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(port, protocol)
    reactor.listenTCP(port, factory)
    reactor.run()


if __name__ == '__main__':
    if len(sys.argv) < 2 or not sys.argv[1].isdigest():
        port = 53
    else:
        port = int(sys.argv[1])
    raise SystemExit(main(port))
