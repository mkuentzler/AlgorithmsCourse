import random
import copy


def contract_edge(graph, node1, node2):
    """
    Contracts the edge between node1 and node2 of a graph. All modifications are
    done in-place, i.e., the input graph is mutated to the output graph. Thus,
    there is no explicit output value returned.
    """
    # Add the edges of the second note to the edges of the first node
    graph[node1].extend(graph.pop(node2))
    # Relabel all edges pointing to the second node to edges pointing
    # to the first node
    for node in graph:
        for idx, edge in enumerate(graph[node]):
            if edge == node2:
                graph[node][idx] = node1
    # Remove self-pointing edges. Note: list() function invoked as to not mutate
    # the iterand.
    [graph[node1].remove(edge) for edge in list(graph[node1]) if edge == node1]


def min_cuts(graph):
    """
    An implementation of the randomized contraction algorithm
    for the min cut problem.
    """
    # If the graph consists of only two nodes, we are return the
    # number of edges connecting the two nodes.
    if len(graph) == 2:
        return len(graph[graph.keys()[0]])
    # Otherwise, we contract one of the edges at random, and return the
    # min cuts of the contracted graph.
    else:
        node1 = random.choice(graph.keys())
        node2 = random.choice(graph[node1])
        contract_edge(graph, node1, node2)
        return min_cuts(graph)


def many_min_cuts(graph):
    """
    Runs the min cut algorithm for a graph many times,
    in order to get a good result.
    """
    min_cut_guesses = []
    for i in xrange(2 * len(graph)):
        if not i % 20 and i > 0:
            # Print a progress indicator.
            print str(float(i) / (2 * len(graph)) * 100) + '%'
        graph_copy = copy.deepcopy(graph)
        min_cut_guesses.append(min_cuts(graph_copy))
    return min(min_cut_guesses)


test_files = ['MinCutTest1.txt', 'MinCutTest2.txt']
hw_file = ['kargerMinCut.txt']

for filename in test_files + hw_file:
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        example_graph = {}
        for row in rows:
            row = row.strip('\r').split(' ')
            row = map(int, row)
            example_graph[row[0]] = row[1:]
    print many_min_cuts(example_graph)