from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

class CDITopo(Topo):
    def build(self):

        # Switch (Mediation Layer)
        s1 = self.addSwitch('s1')

        # Enterprise Hosts (10)
        enterprise_hosts = []
        for i in range(1, 11):
            h = self.addHost(f'e{i}', ip=f'10.0.0.{i}/24')
            enterprise_hosts.append(h)
            self.addLink(h, s1)

        # OT Hosts (5)
        for i in range(11, 16):
            h = self.addHost(f'o{i-10}', ip=f'10.0.0.{i}/24')
            self.addLink(h, s1)

def run():
    topo = CDITopo()

    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633),
        link=TCLink
    )

    net.start()
    print("*** Network started")

    CLI(net)

    net.stop()

if __name__ == '__main__':
    run()
