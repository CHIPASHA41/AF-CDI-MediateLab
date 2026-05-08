#!/usr/bin/env python3

import argparse
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel


class CDITopo(Topo):
    def build(self, enterprise=10, ot=5):
        s1 = self.addSwitch("s1", protocols="OpenFlow13")

        for i in range(1, enterprise + 1):
            h = self.addHost(f"e{i}", ip=f"10.0.0.{i}/24")
            self.addLink(h, s1)

        for j in range(1, ot + 1):
            ip_last = enterprise + j
            h = self.addHost(f"o{j}", ip=f"10.0.0.{ip_last}/24")
            self.addLink(h, s1)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--enterprise", type=int, default=10)
    parser.add_argument("--ot", type=int, default=5)
    parser.add_argument("--controller-ip", default="127.0.0.1")
    parser.add_argument("--controller-port", type=int, default=6633)
    args = parser.parse_args()

    topo = CDITopo(enterprise=args.enterprise, ot=args.ot)

    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(
            name,
            ip=args.controller_ip,
            port=args.controller_port
        ),
        link=TCLink,
        autoSetMacs=True
    )

    net.start()
    print(f"*** CDI topology started: enterprise={args.enterprise}, ot={args.ot}")
    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run()
