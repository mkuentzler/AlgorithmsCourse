test_files = ['2sum_test.txt']
hw_file = ['2sum.txt']

for filename in hw_file:
    numbers = {}
    count = 0
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        example_graph = {}
        for row in rows:
            row = row.strip('\r').strip(' ')
            row = int(row)
            numbers[row] = None
        for t in xrange(-10000, 10001):
            if not t % 100:
                print t
            for num in numbers:
                if t-num in numbers and num != t-num:
                    count += 1
                    break
        print count