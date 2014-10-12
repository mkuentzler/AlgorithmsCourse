import collections
import sys
import resource

# For large graphs, we may need many recursions. This command
# increases Python's recursion limit. It might need to be supplemented by a
# manually increased call stack size. On Linux/Mac OS X, use 'ulimit -a' to
# read all sizes, and 'ulimit -s SIZE' to set the call stack size to SIZE.
sys.setrecursionlimit(2**20)
resource.setrlimit(resource.RLIMIT_STACK, (2**25, 2**25))


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
            if edge in rev_graph:
                rev_graph[edge].append(node)
            else:
                rev_graph[edge] = [node]
    return rev_graph


def find_scc(graph, r):
    """
    Finds the strongly connected components of a graph. The input graph should
    be formatted as a dictionary representing its adjacency list, with nodes
    being the dictionary keys and edge lists being the dictionary values.
    
    find_scc will then output the sizes of the r largest SCCs.
    """

    # Create a new graph with reversed edges.
    rev_graph = reverse_graph(graph)
    print 'Reversing complete.'
    
    # Initialize a list to keep track of the order in which the nodes finish
    # in the first dfs pass, and a dictionary to keep track of the leaders in
    # the second dfs pass. A leader is a root node of the dfs subroutine in the
    # second pass.
    finishers = []
    leaderlist = {}

    # First depth-first search pass subroutine.
    def dfs1(graph, node, explored, finishers):
        """
        Subroutine of find_scc for the first deph-first search pass.
        """
        explored[node] = True
        for edge in graph[node]:
            if not explored[edge]:
                dfs1(graph, edge, explored, finishers)
        finishers.append(node)

    # Initialize a dictionary to keep track of whether a node has been explored
    # in the first dfs.
    explored_rev = {}
    for node in rev_graph:
        explored_rev[node] = False
    
    for node in rev_graph:
        if not explored_rev[node]:
            dfs1(rev_graph, node, explored_rev, finishers)

    print 'First dfs pass complete.'

    # Second depth-first search pass subroutine.
    def dfs2(graph, node, explored, leadingnode, leaderlist):
        explored[node] = True
        leaderlist[node] = leadingnode
        # Since the graph is stored as an adjacency list, and some nodes may not
        # have outgoing edges, some nodes may not be in the graph list.
        if node in graph:
            for edge in graph[node]:
                if not explored[edge]:
                    dfs2(graph, edge, explored, leadingnode, leaderlist)

    # For the second dfs pass, pass through the nodes in order of reverse
    # finishing of the first pass.
    finishers.reverse()

    # Initialize a dictionary to keep track of whether a node has been explored
    # in the second dfs.
    explored = {node: False for node in finishers}

    for node in finishers:
        if not explored[node]:
            leadingnode = node
            dfs2(graph, node, explored, leadingnode, leaderlist)

    print 'Second dfs pass complete.'

    # Leaderlist contains the leading node for each node. The leading nodes also
    # denote the SCC equivalence classes. We can get the number of elements in
    # each equivalence class by counting the occurences of each leading node.
    # We return the number of elements in the top r SCCs.
    sccs = collections.Counter(leaderlist.values()).values()
    sccs.sort(reverse=True)
    
    # If there are less SCCs than r, pad them with zeroes.
    if len(sccs) < r:
        sccs += [0] * (r - len(sccs))
    
    return sccs[:r]


# Optimization scope: List of lists instead of dict. Using a hash table is
# probably not so important when the values are integers, unique, and
# well-distributed.

test_files = ['SCCtest1.txt', 'SCCtest2.txt', 'SCCtest3.txt', 'SCCtest4.txt']
hw_file = ['SCC_hw.txt']

for filename in test_files:
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        example_graph = {}
        for row in rows:
            row = row.strip('\r').strip(' ').split(' ')
            row = map(int, row)
            if row[0] in example_graph:
                example_graph[row[0]].extend(row[1:])
            else:
                example_graph[row[0]] = row[1:]
        print
        print 'Reading complete.'
        print find_scc(example_graph, 5)