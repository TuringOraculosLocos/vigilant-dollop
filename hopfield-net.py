import matplotlib

matplotlib.use('TkAgg')



import pylab as PL

import networkx as NX

import random as RD



NumOfNodes = 10



def init():

    global step, network, positions, nextNetwork, listU



    step = 0



    network = NX.Graph()



    for x in range(0,NumOfNodes):

        for y in range(0,NumOfNodes):

            if RD.getrandbits(1) == 1:

                network.add_edge(x, y, weight = 1)

            else:

                network.add_edge(x, y, weight = -1)

    

    for i in network.nodes_iter():

        if RD.getrandbits(1) == 1:

            network.node[i]['state'] = 1

        else:

            network.node[i]['state'] = -1

    

    listU = [totalUtility()]

        

    positions = NX.circular_layout(network)



    nextNetwork = network.copy()



def draw():

    PL.subplot(1, 2, 1)

    PL.cla()

    states = [network.node[i]['state'] for i in network.nodes_iter()]

    weights = [network.edge[i][j]['weight'] for [i,j] in network.edges_iter()]

    NX.draw(network, with_labels = False, pos = positions,

            cmap = PL.cm.hsv, vmin = -1, vmax = 1,

            node_color = [colorNode(s) for s in states],

            edge_color = [colorEdge(w) for w in weights])

    PL.axis('image')

    PL.title('step = ' + str(step))



    PL.subplot(1, 2, 2)

    PL.cla()

    PL.plot(listU)

    PL.title('Total utility')



def step():

    global step, network, nextNetwork

    

    step += 1

    

    for i in range(0,NumOfNodes):

        u_i_neg = 0

        u_i_pos = 0

    

        s_i = -1       

        for j in range(0,NumOfNodes):

            if i != j:

                s_j = network.node[j]['state']

                w_ij = network.edge[i][j]['weight']

                u_i_neg += (w_ij * s_i * s_j)



        s_i = 1      

        for j in range(0,NumOfNodes):

            if i != j:

                s_j = network.node[j]['state']

                w_ij = network.edge[i][j]['weight']

                u_i_pos += (w_ij * s_i * s_j)           

        

        if u_i_neg > u_i_pos:

            nextNetwork.node[i]['state'] = -1

        elif u_i_pos > u_i_neg:

            nextNetwork.node[i]['state'] = 1

        else:

            nextNetwork.node[i]['state'] = network.node[i]['state']

        

    network, nextNetwork = nextNetwork, network

    listU.append(totalUtility())



def totalUtility():

    global network

    

    U = 0    

    for i in range(0,NumOfNodes):

        s_i = network.node[i]['state']

        

        for j in range(0,NumOfNodes):

            if i != j:

                s_j = network.node[j]['state']

                w_ij = network.edge[i][j]['weight']

                U += (w_ij * s_i * s_j)    

    return U



def colorNode(s):

    if s == -1:

        return 'blue'

    elif s == 1:

        return 'red'

    else:

        return 'black'

        

def colorEdge(w):

    if w < 0:

        return 'blue'

    elif w == 0:

        return 'white'

    elif w > 0:

        return 'red'

        

import pycxsimulator

pycxsimulator.GUI().start(func=[init,draw,step])

