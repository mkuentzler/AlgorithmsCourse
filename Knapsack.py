import sys
import resource

# For very large knapsacks, we may need many recursions. The commands below
# increase Python's recursion limit. It might need to be supplemented by a
# manually increased function stack size. On Linux/Mac OS X, use 'ulimit -a' to
# read all sizes, and 'ulimit -s SIZE' to set the call stack size to SIZE.
sys.setrecursionlimit(2**20)
resource.setrlimit(resource.RLIMIT_STACK, (2**25, 2**25))


class Knapsack:
    """
    Runs the knapsack dynamic programming algorithm on a knapsack with @capacity
    and items stored in @item_list. Entries in item_list are lists, with item
    value as first entry and item weight as second entry.

    Initializing the Knapsack class performs and stores all relevant
    computations. The final result, that is the optimal knapsack value, can be
    read out using .optimal(). The composition of the optimal knapsack can be
    reconstructed using .reconstruct() (not implemented yet).
    """
    def __init__(self, capacity, item_list):
        self.num_items = len(item_list)
        self.capacity = capacity
        self.count = 0
        # Initialize knapsack table
        self._kp_table = {}
        for cap in range(capacity + 1):
            self._kp_table[(0, cap)] = 0
        # Compute optimal knapsack
        self.kp_compute(self.num_items-1, capacity)
        print "Improvement factor:", \
              round(float(self.num_items * self.capacity)
                    / float(len(self._kp_table)), 2)

    def kp_compute(self, item_num, cap):
        self.count += 1
        if self.count % 50000 == 0:
            print 'Rough progress:', round(
                float(item_num) / float(self.num_items) * 100, 1), "% \r",
        if (item_num-1, cap) not in self._kp_table:
            self.kp_compute(item_num-1, cap)
        value, weight = item_list[item_num]
        if weight > cap:
            self._kp_table[(item_num, cap)] = self._kp_table[(item_num-1, cap)]
        else:
            if (item_num-1, cap-weight) not in self._kp_table:
                self.kp_compute(item_num-1, cap-weight)
            self._kp_table[(item_num, cap)] = max(
                self._kp_table[(item_num-1, cap)],
                self._kp_table[(item_num-1, cap-weight)] + value)

    def optimal(self):
        return self._kp_table[(self.num_items-1, self.capacity)]

    def reconstruct(self):
        pass


test_files = ['knapsack_test1.txt', 'knapsack_test2.txt']
hw_file_sm = ['knapsack_hw_small.txt']
hw_file_big = ['knapsack_hw_big.txt']

for filename in hw_file_big:
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        # First row contains knapsack size and number of items
        capacity = int(rows[0].split(' ')[0])
        # Subsequent rows contain individual item values and weights
        item_list = []
        for row in rows[1:]:
            item = map(int, row.split(' '))
            item_list.append(item)
        print 'Reading complete.'
        kp = Knapsack(capacity, item_list)
        print "Optimal knapsack value:", kp.optimal()
        print