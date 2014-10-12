import heaps
import random


def prim(graph):
    """
    Applies Prim's algorithm to find a minimum spanning tree, and returns the
    mst cost.
    """
    cost_heap = heaps.Minheap()
    mst_cost = 0
    unvisited = {node: None for node in graph}
    current_node = random.choice(graph.keys())
    unvisited.pop(current_node)
    while unvisited:
        for edge in graph[current_node]:
            target_node = edge[0]
            edge_cost = edge[1]
            cost_heap.push((edge_cost, target_node))
        while True:
            new_node = cost_heap.pop()
            if new_node[1] in unvisited:
                break
        mst_cost += new_node[0]
        current_node = new_node[1]
        unvisited.pop(current_node)
    return mst_cost


test_files = ['prim_test1.txt']
hw_file = ['prim_hw.txt']

for filename in hw_file:
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        example_graph = {}
        # Omit first row, contains number of nodes and edges
        for row in rows[1:]:
            row = row.split(' ')
            row = map(int, row)
            if row[0] in example_graph:
                example_graph[row[0]].append([row[1], row[2]])
            else:
                example_graph[row[0]] = [[row[1], row[2]]]
            if row[1] in example_graph:
                example_graph[row[1]].append([row[0], row[2]])
            else:
                example_graph[row[1]] = [[row[0], row[2]]]
        print
        print 'Reading complete.'
        print example_graph
        print
        print prim(example_graph)