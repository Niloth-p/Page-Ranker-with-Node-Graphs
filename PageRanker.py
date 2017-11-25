"""
This program ranks all the 6012 web pages
in the dataset of hollins university,
according to the Page Algorithm
Then displays graphs of the nodes and their edges in these variations:
It takes approximately 105s for the program to page rank all the 6012 links in this corpus
"""

# pylint: disable=C0103

import time
from decimal import Decimal
import linecache
from collections import defaultdict, OrderedDict
from random import randint
import matplotlib.pyplot as plt
import networkx as nx

B = 0.85
file = "hollins.dat"
N = int(linecache.getline(file, 1).partition(' ')[0])


def converge(rnew, rold, loop):
    """
    Checks for converging of the rank vector values, every loop
    """
    sumofdiffs = 0
    sumtotal = 0
    if loop == 1:
        return True
    else:
        for i in range(0, N):
            sumofdiffs += abs(Decimal(rnew[i]) - Decimal(rold[i]))
            sumtotal += Decimal(rnew[i])
        print("sumofdiffs is " + str(sumofdiffs))
        print("sumtotal is " + str(sumtotal))
        if sumofdiffs > 0.5:
            return True
    return False


def initialize():
    """
    Initializes the rank vector to 1/N, before starting the page algo
    """
    rold = []
    rnew = []
    rnew2 = []
    for _ in range(0, N):
        rold.append(1/N)
        rnew.append(0)
        rnew2.append(0)
    print("Assigned rold")
    return rold, rnew, rnew2


def listofdegrees():
    """
    Returns a list of the degrees of all nodes
    """
    f = open(file, "r")
    degrees = []
    for _ in range(0, N):
        degrees.append(0)
    l = 0
    for line in f:
        l += 1
        if l > N+1:
            lister = line.split()
            degrees[int(lister[0])] += 1
    f.close()
    #print(degrees)
    print("Got degrees list")
    return degrees


def getinlinks(nodei):
    """
    Returns a list of inlinks to a specific node
    """
    f = open(file, "r")
    node = nodei + 1
    inlinks = []
    l = 0
    for line in f:
        l += 1
        if l > N+1:
            lister = line.split()
            if lister[1] == str(node):
                inlinks.append(int(lister[0]))
    f.close()
    print("cur : " + str(node))
    #print(inlinks)
    return inlinks


def draw_graph(edgelist, nodesizeratios, mapping):
    """
    Plots the graph given the nodes, edges, and sizes the nodes wrt to their importance i.e rank
    Plots only the nodes that have atleast 1 edge, to reduce the clutter.
    Default red node circles, and black edges
    If the webpageID is large, then only the number will be displayed, without its node circle
    to reduce overlap of space
    """
    G = nx.DiGraph()
    G.add_edges_from(edgelist)
    nodesizes = []
    for i in range(0, len(nodesizeratios)):
        nodesizes.append(nodesizeratios[i] * 1000 * 1000 * 3)
    pos = nx.random_layout(G)
    nx.draw_networkx(G, pos, arrows=True, with_labels=True, node_size=nodesizes)
    print(mapping)
    #nx.draw_networkx_labels(G, pos, mapping, font_size=16)
    G = nx.relabel_nodes(G, mapping)
    nx.draw_networkx(G, pos, arrows=True, with_labels=True, node_size=nodesizes)
    plt.show()


def getrandomnodes(n):
    """
    Return n random nodes, given n
    """
    if not n:
        n = 200
    nodelist = []
    nodelist = set(nodelist)
    while len(nodelist) < int(n):
        nodelist.add(randint(1, N))
        nodelist = set(nodelist)
    #print(nodelist)
    print("Got random nodes")
    return nodelist


def popularityclassification(rnew):
    """
    Returns the list of nodes ranked in the descending order of importance
    """
    dicty = defaultdict(list)
    for i in range(1, N+1):
        dicty[i] = rnew[i-1]
    rankednodes = OrderedDict(sorted(dicty.items(), key=lambda x: x[1], reverse=True))
    return rankednodes


def getpopularnodes(rankednodes, n):
    """
    Returns n popular nodes
    """
    nodelist = []
    nodesizeratios = []
    c = 0
    if not n:
        n = 30
    for key in rankednodes:
        if c < int(n):
            nodelist.append(int(key))
            nodesizeratios.append(float(rankednodes[key])/10)
            c += 1
        else:
            break
    print("Got popular nodes")
    #print(nodelist)
    return nodelist, nodesizeratios


def getmixedpopularnodes(rankednodes, n):
    """
    Returns n equally distributed nodes
    """
    nodelist = []
    nodesizeratios = []
    if not n:
        n = 500
    x = int(N / int(n))
    c = 1
    print("x : " + str(x) + "c : " + str(c))
    for key in rankednodes:
        if c % x == 0:
            nodelist.append(int(key))
            nodesizeratios.append(float(rankednodes[key]))
        c += 1
    print("Got equally distributed nodes")
    #print(nodelist)
    return nodelist, nodesizeratios


def writeToHumanReadableFile(filename, index):
    """
    Writes object to file in a readable form
    """
    with open(filename + 'readable.txt', 'w') as f:
        for k, v in index.items():
            f.write(str(k) + ' >>> ' + str(v) + '\n\n')
    f.close()
    print("Written to readable file " + filename + "readable.txt")


def getspecificnodes():
    """
    Returns 20 specific nodes
    """
    nodelist = [310, 510, 810, 1210, 9, 10, 61, 37, 38, 43, 23, 204, 1208]
    print("Got specific nodes")
    return nodelist


def getedges(nodelist):
    """
    Gets all edges between the given nodes, from the database
    """
    f = open(file, "r")
    edgelist = []
    l = 0
    for line in f:
        l += 1
        if l > N+1:
            lister = line.split()
            if (int(lister[0]) in nodelist) and (int(lister[1]) in nodelist):
                edgelist.append([lister[0], lister[1]])
    #print("edgelist : " + str(edgelist))
    f.close()
    print("Got edges")
    return edgelist


def getimportance(nodelist, file2):
    """
    Gets the node size ratios wrt each other, from the ranked list of nodes,
    and mutiplies them by a suitable scale for display
    """
    nodesizeratios = []
    for nodes in nodelist:
        nodesizeratios.append(float(linecache.getline(file2, nodes)) / N)
        #as is, if summing to 1. If summing to N, divide by N, before assigning
    #print("nodesizeratios : " + str(nodesizeratios))
    return nodesizeratios


def main():
    """
    main : runs the page rank algo,
    writes the ranked list,
    gets different nodelists, edgelists and nodesizeratios,
    and plots different graphs
    """
    start = time.time()
    rold, rnew, rnew2 = initialize()
    loop = 1
    degrees = listofdegrees()
    while converge(rnew, rold, loop):
        #Updating rold with rnew
        if loop != 1:
            for i in range(0, N):
                rold[i] = rnew[i]
                rnew2[i] = 0

        #Calculating rnew2
        for i in range(0, N):
            inlinks = getinlinks(i)

            for node in inlinks:
                rnew2[i] += rold[node]/degrees[node]
            rnew2[i] = B * rnew2[i]

        print("Calculated rnew2")

        #Accounting for spider traps and dead ends
        s = 0
        for j in range(0, N):
            s += rnew2[j]
        print("S = " + str(s))
        for j in range(0, N):
            rnew[j] = rnew2[j] + (1-s)/N
        print("Calculated rnew")

        #Writing the pagerank of each loop to a file
        f = open("PageRank" + str(loop) + ".txt", "w+")
        for i in range(0, N):
            f.write(str(N*rnew[i]) + "\n")
        f.close()
        print("Loop " + str(loop) + "is completed")
        loop += 1
        file2 = "PageRank" + str(loop - 1) + ".txt"
        #print("file2 : " + str(file2))

    end = time.time()
    print("running time : " + str(end - start))

    #Plotting 20 specific nodes with the numbers inside the circles
    #representing their scaled page rank scores
    nodelist = getspecificnodes()
    edgelist = getedges(nodelist)
    nodesizeratios = getimportance(nodelist, file2)
    #noderatios = ['%.2f' % (item * 1000 * 10 * 3) for item in nodesizeratios]
    noderatios = [int(item * 1000 * 10) for item in nodesizeratios]
    print("nodelist : " + str(nodelist))
    print("nodesizeratios : " + str(nodesizeratios))
    print("noderatios : " + str(noderatios))
    #noderatios = [float(item) for item in noderatios]
    noderatios = [str(item) for item in noderatios]
    mapping = dict(zip(nodelist, noderatios))
    draw_graph(edgelist, nodesizeratios, mapping)

    #Plotting all nodes
    nodelist = []
    for i in range(1, N+1):
        nodelist.append(i)
    print("Got all nodes")
    edgelist = getedges(nodelist)
    nodesizeratios = getimportance(nodelist, file2)
    draw_graph(edgelist, nodesizeratios, {})

    rankednodes = popularityclassification(rnew)
    writeToHumanReadableFile('rankednodes', rankednodes)
    #print("the top 10 ranked nodes")
    #for _, key in zip(range(0, 10), rankednodes):
    #    print(key)

    #Plotting top n popularnodes
    print("for n=10, 6 visible nodes in graph, n=20->11, n=30->14, n=50->31")
    n = input("Enter the number of popular nodes whose edges to display : ")
    nodelist, nodesizeratios = getpopularnodes(rankednodes, n)
    edgelist = getedges(nodelist)
    draw_graph(edgelist, nodesizeratios, {})

    # #Plotting 20 equivalently distributed nodes (as per their popularity)
    # n = input("Enter the number of equally distributed nodes (by popularity) : ")
    # nodelist = getmixedpopularnodes(rankednodes, n)
    # edgelist = getedges(nodelist)
    # print(edgelist)
    # #nodesizeratios = getimportance(nodelist, file2)
    # draw_graph(edgelist, nodesizeratios, {})

    #Plotting 20 specific nodes
    nodelist = getspecificnodes()
    edgelist = getedges(nodelist)
    nodesizeratios = getimportance(nodelist, file2)
    draw_graph(edgelist, nodesizeratios, {})

    #Plotting n random nodes
    print("On avg, for n=200 to 250, 30-40 nodes will be displayed")
    n = input("Enter the number of random nodes whose edges to display : ")
    nodelist = getrandomnodes(n)
    edgelist = getedges(nodelist)
    nodesizeratios = getimportance(nodelist, file2)
    draw_graph(edgelist, nodesizeratios, {})


if __name__ == '__main__':
    main()
