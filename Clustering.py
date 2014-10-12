import unionfind


def max_spacing(input_graph, input_graph_nodes, target_cluster_num):
    """
    Returns the maximal spacing of a clustering of a graph into
    target_cluster_num clusters, using a variant of Kruskal's algorithm
    """
    # Pre-processing. Convert the graph into a form more suited to Kruskal's
    # algorithm: A list of edges represented as tuples, with edge weight as
    # first entry and endpoints as second and third entries,
    #  sorted by descending edge weight.
    graph = [(edge[1], node, edge[0])
             for node in input_graph for edge in input_graph[node]]
    graph.sort(reverse=True)
    cluster_num = input_graph_nodes
    # Use a Union Find data structure to keep track of the clusters.
    cluster = unionfind.UnionFind()
    # For all edges (in decreasing order of weight), merge clusters connected
    # by the edge,
    # until desired number of clusters is reached, then return minimum spacing.
    while True:
        edge = graph.pop()
        if cluster[edge[1]] != cluster[edge[2]]:
            if cluster_num != target_cluster_num:
                cluster.union(edge[1], edge[2])
                cluster_num -= 1
            else:
                return edge[0]


test_files = ['clustering_test1.txt', 'clustering_test2.txt']
hw_small = ['clustering_hw_small.txt']

for filename in hw_small:
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        example_graph = {}
        # Omit first row, contains number of nodes
        for row in rows[1:]:
            row = row.strip(' ').split(' ')
            row = map(int, row)
            if row[0] in example_graph:
                example_graph[row[0]].append([row[1], row[2]])
            else:
                example_graph[row[0]] = [[row[1], row[2]]]
            # Only need one direction per edge.
            #if row[1] in example_graph:
            #    example_graph[row[1]].append([row[0], row[2]])
            #else:
            #    example_graph[row[1]] = [[row[0], row[2]]]
        print
        print 'Reading complete.'
        print
        print max_spacing(example_graph, int(rows[0]), 4)