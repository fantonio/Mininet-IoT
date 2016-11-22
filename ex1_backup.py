from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.cli import CLI
from functools import partial
import os



class SDNProjectTopo(Topo):
    def build(self):
#        Topo.__init__(self)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

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


def monitorTest():
	topo = SDNProjectTopo()
	net = Mininet(topo=topo,link=TCLink, controller=partial(RemoteController, ip='127.0.0.1', port=6633))
	hosts=net.hosts
	net.start()
	net.staticArp()


	dumpNodeConnections(net.hosts)
	net.pingAll()

	
#	for h in hosts:
#		print h.cmd('cat ./con_python/output_txt/output_link_length.txt')
#		print h.cmd('pwd')
#		print h.cmd('iperf -s &')

	CLI( net )
	net.stop()


if __name__=='__main__':
	setLogLevel('info')

# python controller & server & client
	os.system("sudo /home/byounguklee/mininet/con_python/run.sh")

	monitorTest()



#topos = {'mytopo':(lambda:SDNProjectTopo())}
