import sys
import resource
import time

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


def find_scc(graph):
    """
    Finds the strongly connected components of a graph. The input graph should
    be formatted as a dictionary representing its adjacency list, with nodes
    being the dictionary keys and edge lists being the dictionary values.

    find_scc outputs a dictionary with the classes -- i.e., leading nodes --
    for each node in the original graph.
    """

    # Create a new graph with reversed edges.
    rev_graph = reverse_graph(graph)

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

    return leaderlist


def two_sat(graph):
    """
    Computes the satisfiability of a 2SAT problem whose implication graph has
    been given as the input.
    """

    components = find_scc(graph)

    for node in graph:
        if components[node] == components[-node]:
            return False

    return True

test_files = ['2sat_test1.txt', '2sat_test2.txt']

hw_files = ['2sat1.txt', '2sat2.txt', '2sat3.txt',
            '2sat4.txt', '2sat5.txt', '2sat6.txt']


for filename in hw_files:
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        example_graph = {}
        # Construct the implication graph
        # Omit first row, contains number of constraints
        for row in rows[1:]:
            row = row.split(' ')
            row = map(int, row)
            if -row[0] in example_graph:
                example_graph[-row[0]].append(row[1])
            else:
                example_graph[-row[0]] = [row[1]]
            if -row[1] in example_graph:
                example_graph[-row[1]].append(row[0])
            else:
                example_graph[-row[1]] = [row[0]]
        print
        print 'Reading complete.'
        tic = time.clock()
        ans = two_sat(example_graph)
        toc = time.clock()
        print 'Satisfiable:', ans
        print 'Running time:', round(toc - tic, 2)