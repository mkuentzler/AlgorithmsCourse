import numpy


def pick_pivot_idx(a):
    """
    Chooses a pivot index for the Quick Sort algorithm. Here, choose the median
    of the first, last and middle element.
    """
    mid = (len(a) - 1) / 2
    median = numpy.median([a[0], a[mid], a[-1]])
    if a[0] == median:
        return 0
    elif a[-1] == median:
        return -1
    else:
        return mid


def quick_sort_compare(a):
    """
    Sorts a list with the Quick Sort algorithm. Also outputs the number of
    comparisons made during the algorithm.
    """
    # Base case
    if len(a) in [0, 1]:
        compare_out = 0
    # Main recursion here
    else:
        # Pick a pivot, and swap it into first position
        pivot_idx = pick_pivot_idx(a)
        pivot = a[pivot_idx]
        a[0], a[pivot_idx] = a[pivot_idx], a[0]
        # From the second position onwards, look at all elements
        i = 1
        for idx in range(1, len(a)):
            # and swap in-place if they are less than the pivot. This partitions
            # the list.
            if a[idx] < pivot:
                a[i], a[idx] = a[idx], a[i]
                i += 1
        # Now, swap the pivot in between the two partitions
        a[0], a[i-1] = a[i-1], a[0]
        # Recursion on the partitions
        left_comps = 0
        right_comps = 0
        if i > 1:
            a[:i-1], left_comps = quick_sort_compare(a[:i-1])
        if i < len(a):
            a[i:], right_comps = quick_sort_compare(a[i:])
        # Count up comparisons
        compare_out = len(a) - 1 + left_comps + right_comps
    return a, compare_out

#file_names = ['10.txt', '100.txt', '1000.txt']
file_names = ['QuickSort.txt']

for filename in file_names:
    with open(filename, 'r') as f:
        intArray = f.read().split('\r\n')
        intArray = map(int, intArray)

    print
    sorted_array = quick_sort_compare(intArray)
    print sorted_array[1]
    print 'Sorted:', all(sorted_array[0][i] <= sorted_array[0][i+1]
                         for i in range(len(sorted_array)-1))