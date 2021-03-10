import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

"""
These functions execute useful tasks for the pre- and post-processing.
"""


def to_graph(num_nodes, edges):
    """
    Generate a graph using networkx library
    :param num_nodes: int number of nodes
    :param edges: list of edges, where each edge is a tuple (node1, node2, weight)

    :returns Graph and list of nodes
    :rtype networx.Graph, numpy.NDarray
    """
    nodes = np.arange(0, num_nodes, 1)
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_weighted_edges_from(edges)
    return graph, nodes


def plot_graph(graph):
    """
    Generate a plot of the graph
    :param graph: a networkx graph
    """
    colors = ['r' for node in graph.nodes()]
    default_axes = plt.axes(frameon=True)
    pos = nx.spring_layout(graph)

    nx.draw_networkx(graph, node_color=colors, node_size=600, alpha=1, ax=default_axes, pos=pos)


def plot_graph_two_partitions(graph, bitstring):
    """
    Plot the Graph and its two sub-graphs by mapping 0's and 1's in red, blue color nodes
    :param graph: a networkx graph
    :param bitstring: string of 0's and 1's
    """
    colors = []
    for bit in bitstring:
        if bit == '1':
            colors.append('b')
        else:
            colors.append('r')

    default_axes = plt.axes(frameon=True)
    pos = nx.spring_layout(graph)

    nx.draw_networkx(graph, node_color=colors, node_size=600, alpha=1, ax=default_axes, pos=pos)


def cost_function(graph, x):
    """
    Cost function to optimization problem (MAXCUT)
    :param graph: a networkx graph
    :param x: list of int 0's and 1's

    :returns cost function evaluation
    :rtype float
    """

    if (len(x) != len(graph.nodes())):
        return np.nan

    cost: float = 0
    for k, l in graph.edges:
        w = graph[k][l]['weight']
        cost = cost + w * x[k] * (1 - x[l]) + w * x[l] * (1 - x[k])

    return cost


def pre_processing(n):
    """
    Starting parameters in terms of the graph
    :param n: number of nodes
    :return:
        graph
        nodes
    :rtype
        networkx.Graph
        numpy.NDarray
    """
    if (n == 5):
        edges = [(0, 1, 1.0), (0, 2, 1.0), (1, 2, 1.0), (3, 2, 1.0), (3, 4, 1.0), (4, 2, 1.0)]

    if (n == 10):
        edges = [(0, 1, 1.0), (0, 2, 1.0), (1, 2, 1.0), (3, 2, 1.0), (3, 4, 1.0),
                 (4, 2, 1.0), (3, 0, 1.0), (5, 2, 1.0), (6, 5, 1.0), (7, 5, 1.0),
                 (5, 8, 1.0), (6, 8, 1.0), (9, 5, 1.0), (9, 7, 1.0), (9, 8, 1.0)]

    graph, nodes = to_graph(n, edges)
    return graph, nodes


def post_processing(graph, counts, shots):
    """
    Obtaining the bit string optimized and its cost function sampled mean value
    :param graph: a networkx graph
    :param counts: a list of int values representing wave-function amplitudes
    :param shots: a int representing the quantum circuit execution sampling
    :return: m1_sampled: averaged value of cost function
            max_C two element sequence: first, the best bit string; second, its cost function value
    :rtype float

    """
    avr_C = 0
    max_C = [0, 0]
    hist = {}

    for k in range(len(graph.edges()) + 1):
        hist[str(k)] = hist.get(str(k), 0)

    for sample in list(counts.keys()):

        # use sampled bit string x to compute the cost function
        x = [int(num) for num in list(sample)]
        tmp_eng = cost_function(graph, x)

        # compute the cost function expectation value
        avr_C = avr_C + counts[sample] * tmp_eng
        # const function distribution
        hist[str(round(tmp_eng))] = hist.get(str(round(tmp_eng)), 0) + counts[sample]

        # save best bit string
        if (max_C[1] < tmp_eng):
            max_C[0] = sample
            max_C[1] = tmp_eng

    m1_sampled = avr_C / shots

    print('\n --- SIMULATION RESULTS ---\n')
    print('The sampled mean value is M1_sampled = %.02f. \n' % (
        m1_sampled))
    print('The approximate solution is x* = %s with C(x*) = %d \n' % (max_C[0], max_C[1]))
    print('The cost function is distributed as it shown in the histogram.')
    plot_histogram(hist, figsize=(8, 6), bar_labels=False)

    return m1_sampled, max_C


def post_processing_opt(graph, counts, shots):
    """Obtaining the bit string optimized and its cost function sampled mean value
    :param graph: a networkx graph
    :param counts: a list of int values representing wave-function amplitudes
    :param shots: a int representing the quantum circuit execution sampling

    :returns
        max_C: [0] is the best bit string, and [1] it is its cost function value
    :rtype
        list
    """
    max_C = [0, 0]

    for sample in list(counts.keys()):

        # use sampled bit string x to compute the cost function
        x = [int(num) for num in list(sample)]
        tmp_eng = cost_function(graph, x)

        # save best bit string
        if (max_C[1] < tmp_eng):
            max_C[0] = sample
            max_C[1] = tmp_eng

    return max_C

