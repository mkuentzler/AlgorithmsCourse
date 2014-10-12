import numpy
import itertools
import time


def tsp(graph):
    """
    Solves the Travelling Salesman Problem for the input @graph, assumed to be
    complete. Uses the dynamic programming algorithm.
    """
    dp_table = {(node, 0): float('inf')
                for node in itertools.combinations(graph, 1)}
    dp_table[(0,), 0] = 0
    dp_table = {(nodes, nodes[1]): graph[nodes[0]][nodes[1]]
                for nodes in itertools.combinations(graph, 2)
                if 0 in nodes}

    for size in xrange(3, len(graph)+1):
        print 'Current problem size:', size, '/', len(graph), "\r",
        for subset in itertools.combinations(graph, size):
            if 0 in subset:
                for end_node in subset:
                    if end_node != 0:
                        new_subset = tuple(
                            [node for node in subset if node != end_node])
                        path_list = [dp_table[(new_subset, middle_node)]
                                     + graph[middle_node][end_node]
                                     for middle_node in subset
                                     if (middle_node != end_node
                                         and middle_node != 0)]
                        dp_table[(subset, end_node)] = min(path_list)

        # forget about stuff no longer needed
        for subset in itertools.combinations(graph, size - 1):
            if 0 in subset:
                for end_node in subset:
                    if end_node != 0:
                        del dp_table[(subset, end_node)]

    final_list = [dp_table[tuple(range(0, len(graph))), node] + graph[node][0]
                  for node in graph if node != 0]
    return min(final_list)


# Solutions: 10.4721, 6.26967, 16898.1, 26714.9
test_files = ['tsp_test1.txt', 'tsp_test2.txt',
              'tsp_test3.txt', 'tsp_test4.txt']
# Solution, rounded down: 26442. Best running time: 21131s.
hw_file = ['tsp_hw.txt']

for filename in test_files:
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        node_list = []
        # Omit first row, contains number of nodes
        for idx, row in enumerate(rows[1:]):
            row = row.split(' ')
            row = map(float, row)
            node_list.append([idx, row[0], row[1]])
        example_graph = {node[0]: {} for node in node_list}
        for node_x, node_y in itertools.combinations(node_list, 2):
            if node_x[0] != node_y[0]:
                diff = [node_y[1] - node_x[1], node_y[2] - node_x[2]]
                dist = numpy.linalg.norm(diff)
                example_graph[node_x[0]][node_y[0]] = dist
                example_graph[node_y[0]][node_x[0]] = dist
        print
        print 'Reading complete.'
        tic = time.clock()
        ans = tsp(example_graph)
        toc = time.clock()
        print 'Shortest tsp path:', ans
        print 'Running time:', round(toc - tic, 2)