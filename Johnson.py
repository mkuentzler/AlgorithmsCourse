import heaps
import time


def reverse_graph(graph):
    """
    Returns a graph with edges reversed with respect to the input graph. Both
    graphs should be/are formatted as dictionaries implementing adjacency lists,
    with nodes being the dictionary keys and the corresponding edge lists being
    the dictionary values.
    """
    rev_graph = {}
    for node in graph:
        rev_graph[node] = []
    for node in graph:
        for edge in graph[node]:
            if edge[0] in rev_graph:
                rev_graph[edge[0]].append([node, edge[1]])
            else:
                rev_graph[edge[0]] = [[node, edge[1]]]
    return rev_graph


def dijkstra(graph, starting_node):
    """
    Finds the legnth of shortest paths through a graph.

    Inputs:
    - Dict containing weighted graph edge list. Each node is a dict key,
    with edge lists as values. Entries in the edge lists are lists containing
    the target node as first entry and the weight as second entry.
    - Starting node, from which path costs are calculated.

    Output: Dict containing shortest distances from starting node to each node.

    Utilizes a heap to keep track of edge costs for the algorithm.
    """
    cost = {starting_node: 0}
    unvisited = {node: None for node in graph}
    # The list of unvisited nodes is mainly used for lookups
    # and therefore stored as a dict.
    unvisited.pop(starting_node)
    current_node = starting_node
    cost_heap = heaps.Minheap()
    # While there are unvisited nodes...
    while unvisited:
        # ...push all outgoing edges of the current node to unvisited nodes
        #  with their cost onto the cost heap, ...
        for edge in graph[current_node]:
            if edge[0] in unvisited:
                target_node = edge[0]
                edge_cost = cost[current_node] + edge[1]
                cost_heap.push((edge_cost, target_node))
        # ...then extract the minimum element of the cost heap that corresponds
        # to an unvisited node.
        while True:
            try:
                new_node = cost_heap.pop()
            except IndexError:
                # If the heap runs empty, all unvisited nodes are unreachable
                # from the starting node. We set their shortest path length
                # to positive infinity.
                for node in unvisited:
                    cost[node] = float('inf')
                return cost
            if new_node[1] in unvisited:
                break
        # This node is removed from the unvisited nodes list,
        # and together with its cost appended to the cost dict.
        unvisited.pop(new_node[1])
        cost[new_node[1]] = new_node[0]
        current_node = new_node[1]
    return cost


def bellman_ford(graph, starting_node):
    """
    An implementation of the Bellman-Ford algorithm to determine shortest paths
    of a @graph from a given @starting_node.

    Returns a dictionary containing all graph nodes and associated shortest
    path costs.
    """

    # Reverse input graph
    rev_graph = reverse_graph(graph)

    # Initialize Bellman-Ford table
    bf_table = {(-1, node): float('inf') for node in graph}
    bf_table[(-1, starting_node)] = 0

    # Run the dynamic programming algorithm
    for i in xrange(len(graph)):
        for node in graph:
            min_list = [bf_table[(i-1, node)]]
            for edge in rev_graph[node]:
                min_list.append(bf_table[(i-1, edge[0])] + edge[1])
            bf_table[(i, node)] = min(min_list)

    # Construct the output graph from the final entries of the table. If the
    # last and next-to-last entries differ for some node, the graph contains
    # negative cost cycles.
    out_graph = {}
    for node in graph:
        if bf_table[(len(graph) - 2, node)] != bf_table[(len(graph) - 1, node)]:
            print 'Graph contains negative cost cycle.'
            break
        out_graph[node] = bf_table[(len(graph) - 1, node)]
    return out_graph


def johnson(graph):
    """
    An implementation of Johnson's algorithm, which returns the shortest
    distance between each pair of nodes of the input @graph as values in a dict,
    with the node pairs being the keys.
    """

    # Step 1: Construct the augmented graph. Use first value less or equal to
    # zero that does not appear in the original graph as extra node name.
    extra_node = 0
    while True:
        if extra_node not in graph:
            break
        extra_node -= 1
    augmented_graph = graph.copy()
    augmented_graph[extra_node] = [[node, 0] for node in graph]
    #TODO: Change above line as to include nodes which have no outgoing edges.

    # Step 2: Run the Bellman-Ford algorithm on the augmented graph to determine
    # the vertex weights
    print 'Starting Bellman-Ford.'
    v_weights = bellman_ford(augmented_graph, extra_node)

    # Step 3: Perform the edge reweighting
    reweighted_graph = {}
    for node in graph:
        try:
            reweighted_graph[node] = [[edge[0], edge[1]
                                       + v_weights[node] - v_weights[edge[0]]]
                                      for edge in graph[node]]
        # If a KeyError is flagged, Bellman-Ford did not return a proper graph.
        # This happens iff the graph contains negative-cost cycles.
        except KeyError:
            return None

    shortest_paths = {}
    total_nodes = len(reweighted_graph)
    print 'Starting Dijkstra.'
    for node in reweighted_graph:
        print 'Approximate progress:', round(100 * float(node) /
                                             float(total_nodes), 2), "% \r",
    # Step 4: Run Dijkstra's algorithm on the reweighted graph to determine
    # shortest paths
        shortest_paths[node] = dijkstra(reweighted_graph, node)

    # Step 5: Undo the reweighting.
        for target_node in shortest_paths[node]:
            shortest_paths[node][target_node] += \
                v_weights[target_node] - v_weights[node]

    return shortest_paths


test_files = ['johnson_test1.txt', 'johnson_test2.txt', 'johnson_test3.txt']
hw_files = ['johnson_hw1.txt', 'johnson_hw2.txt', 'johnson_hw3.txt']

for fileindex, filename in enumerate(hw_files):
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        example_graph = {}
        # Omit first row, which contains info about graph
        for row in rows[1:]:
            row = row.strip(' \r').strip(' ').strip('\t').split(' ')
            row = map(int, row)
            if row[0] in example_graph:
                example_graph[row[0]].append([row[1], row[2]])
            else:
                example_graph[row[0]] = [[row[1], row[2]]]
            # Make sure nodes with only incoming edges are in the adjacency list
            if row[1] not in example_graph:
                example_graph[row[1]] = []
        print
        print 'Reading complete.'

        tic = time.clock()
        j_paths = johnson(example_graph)
        toc = time.clock()

        if j_paths:
            minlist = []
            for source_node in j_paths:
                minlist.append(min(j_paths[source_node].itervalues()))
            print 'Shortest shortest path:', min(minlist)
        print "Time elapsed:", round(toc - tic, 2)
