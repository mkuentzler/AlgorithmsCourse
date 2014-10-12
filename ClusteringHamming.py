import unionfind


def close_nodes(input_node):
    """
    Returns a list with all nodes of Hamming distance at most 2 from the input
    node.
    """
    nodes = [input_node]
    for idx, val in enumerate(input_node):
        nodes.append(input_node[:idx] + str(int(val) ^ 1) + input_node[idx+1:])
        for idx2 in range(idx+1, len(input_node)):
            val2 = input_node[idx2]
            nodes.append(input_node[:idx] + str(int(val) ^ 1)
                         + input_node[idx+1:idx2] + str(int(val2) ^ 1)
                         + input_node[idx2+1:])
    return nodes


test_clustering_hamming = ['clustering_hamming_test1.txt',
                           'clustering_hamming_test2.txt',
                           'clustering_hamming_test3.txt']
hw_big = ['clustering_hw_big.txt']

for filename in hw_big:
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        nodes = {}
        # Omit first row, contains number of nodes
        for row in rows[1:]:
            # Add a node to the list of nodes
            row = row.replace(' ', '')
            nodes[row] = None
        print 'Reading complete.'
        node_num = float(len(nodes))

    # Initialize union find data structure to keep track of clusters
    cluster = unionfind.UnionFind()

    # For each node, unite all close nodes into a single cluster
    for idx, node in enumerate(nodes):
        # Progress indicator
        if idx % 1000 == 0:
            print str(round(float(idx)/node_num * 100, 1)) + '%'

        for close_node in close_nodes(node):
            if close_node in nodes:
                cluster.union(node, close_node)

    # Count the number of clusters
    cluster_list = {}
    for node in nodes:
        cluster_list[cluster[node]] = None

    print 'Number of clusters:', len(cluster_list)
    print