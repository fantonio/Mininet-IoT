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

        h1 = self.addHost('h1',ip='10.0.0.1/32',mac='82:ff:9c:90:7d:a1')
        h2 = self.addHost('h2',ip='10.0.0.2/32',mac='82:ff:9c:90:7d:a2')
        h3 = self.addHost('h3',ip='10.0.0.3/32',mac='82:ff:9c:90:7d:a3')
        h4 = self.addHost('h4',ip='10.0.0.4/32',mac='82:ff:9c:90:7d:a4')

#        h1.setIP('10.0.0.1')
#        h2.setIP('10.0.0.2')
#        h3.setIP('10.0.0.3')
#        h4.setIP('10.0.0.4')

        

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        self.addLink(s1,h1)
        self.addLink(s4,h4)
        self.addLink(s3,h3)
        self.addLink(s2,h2)


# bandwidth link constraint need arguments '--link=tc' in mn command
        self.addLink(s1,s2,bw=500)
        self.addLink(s1,s3,bw=500)
        self.addLink(s2,s4,bw=500)
        self.addLink(s3,s4,bw=500)
        self.addLink(s2,s3,bw=500)

# making connection between my computer and virutal network
def connectToRootNS( network, switch, ip, routes):
	root = Node('root', inNamespace=False)
	intf = network.addLink(root,switch).intf1
	root.setIP(ip, intf=intf)
	root.setMAC('0a:b2:ee:19:37:16',intf=intf)
	root.cmd('echo hook')
	root.setARP('10.0.0.1/32','82:ff:9c:90:7d:a1')
	root.setARP('10.0.0.2/32','82:ff:9c:90:7d:a2')
	root.setARP('10.0.0.3/32','82:ff:9c:90:7d:a3')
	root.setARP('10.0.0.4/32','82:ff:9c:90:7d:a4')




	net.staticArp()
	network.start()

	for route in routes:
		root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )



# making network 'net'
def monitorTest():
	topo = SDNProjectTopo()
#	topo = TreeTopo(depth=1, fanout=4)
	return Mininet(topo=topo,link=TCLink, controller=partial(RemoteController, ip='127.0.0.1', port=6633), cleanup=True, autoStaticArp=True)



def sshd( network, cmd='/usr/sbin/sshd', opts='-D -p 22'):
	for host in network.hosts:
		host.cmd( cmd + ' ' + opts + '&' )
		host.cmd('arp -s 10.123.123.1 0a:b2:ee:19:37:16')



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


	dumpNodeConnections(net.hosts)
	net.pingAll()

	for host in net.hosts:
		host.cmd('arp -s 10.123.123.1 0a:b2:ee:19:37:16')

	os.system('arp -i root-eth0 -s 10.0.0.1/32 82:ff:9c:90:7d:a1')

	CLI( net )
	net.stop()




#topos = {'mytopo':(lambda:SDNProjectTopo())}
