import heaps

test_files = ['Median_test.txt', 'Median_test2.txt']
hw_file = ['Median.txt']

for filename in hw_file:
    with open(filename, 'r') as f:
        rows = f.read().strip(' ').split('\n')
        rows = map(int, rows)
        median_list = []
        left_heap = heaps.Maxheap([])
        right_heap = heaps.Minheap([])
        current_median = None
        for num in rows:
            if not current_median:
                current_median = num
            else:
                if len(right_heap) == len(left_heap):
                    if num >= current_median:
                        right_heap.push(num)
                    else:
                        right_heap.push(current_median)
                        if len(left_heap) > 0:
                            left_max = left_heap.pop()
                            current_median = max(left_max, num)
                            left_heap.push(min(left_max, num))
                        else:
                            current_median = num
                else:
                    if num <= current_median:
                        left_heap.push(num)
                    else:
                        left_heap.push(current_median)
                        if len(right_heap) > 0:
                            right_min = right_heap.pop()
                            current_median = min(right_min, num)
                            right_heap.push(max(right_min, num))
                        else:
                            current_median = num
            median_list.append(current_median)
        print sum(median_list) % 10000