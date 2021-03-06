### Distance vector routing
import random,sys,math
from optparse import OptionParser
from net_sim import *

# import p2_tests

class DVRouter(Router):
    INFINITY = 32

    def send_advertisement(self, time):
        adv = self.make_dv_advertisement()
        for link in self.links:
            p = self.network.make_packet(self.address, self.peer(link),
                                         'ADVERT', time,
                                         color='red', ad=adv)
            link.send(self, p)

    # Make a distance vector protocol advertisement, which will be sent
    # by the caller along all the links
    def make_dv_advertisement(self):
        # Just send out my current cost table
        distance_vector=[]
        for dst, cost in self.spcost.items():
            distance_vector.append((dst,cost))
        return distance_vector

    def link_failed(self, link):
        # If a link is broken, remove it from my routing/cost table
        self.clear_routes(self)


    def process_advertisement(self, p, link, time):
        self.integrate(link, p.properties['ad'])

    # Integrate new routing advertisement to update routing
    # table and costs
    def integrate(self,link,adv):
        # Loop over all (dst, dst_cost) pairs from the adv
        for dst, dst_cost in adv:
            # If I don't know dst yet, or the cost to dst thru link is smaller
            if ((not dst in self.spcost) or (link.cost + dst_cost < self.spcost[dst])):
                # Update the new cost to my cost table
                self.spcost[dst]=link.cost + dst_cost
                # Update the new neighbour link to my routing table
                self.routes[dst]=link

            # Handle the cases when cost changes
            if (self.routes[dst] == link and self.spcost[dst] != link.cost + dst_cost):
                self.spcost[dst]=link.cost + dst_cost
                self.routes[dst]=link



# A network with nodes of type DVRouter.
class DVRouterNetwork(RouterNetwork):
    # nodes should be an instance of DVNode (defined above)
    def make_node(self,loc,address=None):
        return DVRouter(loc,address=address)

########################################################################

if __name__ == '__main__':
    NODES = (('C', 0, 1), ('A', 1, 0), ('B', 2, 1))
    # format: (link start, link end)
    LINKS = (('C', 'A'), ('A', 'B'), ('C', 'B'))

    net = DVRouterNetwork(4000, NODES, LINKS, 0)
    # parser = OptionParser()
    # parser.add_option("-g", "--gui", action="store_true", dest="gui",
    #                   default=False, help="show GUI")
    # parser.add_option("-n", "--numnodes", type="int", dest="numnodes",
    #                   default=12, help="number of nodes")
    # parser.add_option("-t", "--simtime", type="int", dest="simtime",
    #                   default=2000, help="simulation time")
    # parser.add_option("-r", "--rand", action="store_true", dest="rand",
    #                   default=False, help="use randomly generated topology")
    #
    # (opt, args) = parser.parse_args()
    #
    # if opt.rand == True:
    #     rg = RandomGraph(opt.numnodes)
    #     (NODES, LINKS) = rg.genGraph()
    # else:
    #     # build the deterministic test network
    #     #   A---B   C---D
    #     #   |   | / | / |
    #     #   E   F---G---H
    #     # format: (name of node, x coord, y coord)
    #
    #     NODES =(('A',0,0), ('B',1,0), ('C',2,0), ('D',3,0),
    #             ('E',0,1), ('F',1,1), ('G',2,1), ('H',3,1))
    #
    #     # format: (link start, link end)
    #     LINKS = (('A','B'),('A','E'),('B','F'),('E','F'),
    #              ('C','D'),('C','F'),('C','G'),
    #              ('D','G'),('D','H'),('F','G'),('G','H'))
    #
    # # setup graphical simulation interface
    # if opt.gui == True:
    #     net = DVRouterNetwork(opt.simtime, NODES, LINKS, 0)
    #     sim = NetSim()
    #     sim.SetNetwork(net)
    #     sim.MainLoop()
    # else:
    #     p2_tests.verify_routes(DVRouterNetwork)

