from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
net = Mininet()

#creating nodes in network
c0 = net.addController()
h0 = net.addHost('h0')
s0 = net.addSwitch('s0')
h1 = net.addHost('h1')
s1 = net.addSwitch('s2')
h2 = net.addHost('h2')
s2 = net.addSwitch('s2')
h3 = net.addHost('h3')
s3 = net.addSwitch('s3')

#adding links between nodes in network
net.addLink (h0,s0)
net.addLink (h1,s1)
net.addLink (h2,s2)
net.addLink (h3,s3)
net.addLink (s1,s0)
net.addLink (s2,s1)
net.addLink (s3,s2)
net.addLink (s3,s0)
net.addLink (s2,s0)
net.addLink (s3,s1)

#configuration of IP address in interfaces
ho.setIP ('192.168.1.0',24)
h1.setIP ('192.168.1.1',24)
h2.setIP ('192.168.1.2',24)
h3.setIP ('192.168.1.3',24)

net.start ()
net.pingAll()
net.stop()

topos = {'mesh' : MeshTopo}


















































9

