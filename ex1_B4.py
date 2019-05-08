from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections, waitListening
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.cli import CLI
from functools import partial
from mininet.node import Node
from mininet.topolib import TreeTopo

import os
import sys

class SDNProjectTopo(Topo):
    def build(self):
#        Topo.__init__(self)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        h9 = self.addHost('h9')
        h10 = self.addHost('h10')
        h11 = self.addHost('h11')
        h12 = self.addHost('h12')

#        h1.setIP('10.0.0.1')
#        h2.setIP('10.0.0.2')
#        h3.setIP('10.0.0.3')
#        h4.setIP('10.0.0.4')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')
        s9 = self.addSwitch('s9')
        s10 = self.addSwitch('s10')
        s11 = self.addSwitch('s11')
        s12 = self.addSwitch('s12')

        self.addLink(s1,h1)
        self.addLink(s2,h2)
        self.addLink(s3,h3)
        self.addLink(s4,h4)
        self.addLink(s5,h5)
        self.addLink(s6,h6)
        self.addLink(s7,h7)
        self.addLink(s8,h8)
        self.addLink(s9,h9)
        self.addLink(s10,h10)
        self.addLink(s11,h11)
        self.addLink(s12,h12)

# bandwidth link constraint need arguments '--link=tc' in mn command
        self.addLink(s1,s2,bw=500)
        self.addLink(s1,s3,bw=500)
        self.addLink(s2,s5,bw=500)
        self.addLink(s3,s4,bw=500)
        self.addLink(s3,s6,bw=500)
        self.addLink(s4,s5,bw=500)
        self.addLink(s4,s7,bw=500)
        self.addLink(s4,s8,bw=500)
        self.addLink(s5,s6,bw=500)
        self.addLink(s6,s7,bw=500)
        self.addLink(s6,s8,bw=500)
        self.addLink(s7,s8,bw=500)
        self.addLink(s7,s11,bw=500)
        self.addLink(s8,s10,bw=500)
        self.addLink(s9,s10,bw=500)
        self.addLink(s9,s11,bw=500)
        self.addLink(s10,s11,bw=500)
        self.addLink(s10,s12,bw=500)
        self.addLink(s11,s12,bw=500)

# making connection between my computer and virutal network
def connectToRootNS( network, switch, ip, routes):
	root = Node('root', inNamespace=False)
	intf = network.addLink(root,switch).intf1
	root.setIP(ip, intf=intf)
	network.start()

	for route in routes:
		root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )

# making network 'net'
def monitorTest():
	topo = SDNProjectTopo()
#	topo = TreeTopo(depth=1, fanout=4)
	return Mininet(topo=topo,link=TCLink, controller=partial(RemoteController, ip='127.0.0.1', port=6633))

def sshd( network, cmd='/usr/sbin/sshd', opts='-D -p 22'):
	for host in network.hosts:
		host.cmd( cmd + ' ' + opts + '&' )

#	for ihost in network.hosts:

if __name__=='__main__':
	setLogLevel('info')

	# python controller & server & client
	#os.system("sudo /home/byounguklee/mininet/con_python/run.sh")

	net=monitorTest()

	switch=net[ 's1' ]
	routes = [ '10.0.0.0/24' ]
 	connectToRootNS( net, switch, '10.123.123.1/24', routes)
	sshd(net)

	hosts=net.hosts
	net.staticArp()

	dumpNodeConnections(net.hosts)
	net.pingAll()

	CLI( net )
	net.stop()

#topos = {'mytopo':(lambda:SDNProjectTopo())}
