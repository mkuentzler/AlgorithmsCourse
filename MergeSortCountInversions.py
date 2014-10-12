import time


def merge_count(l, r):
    """
    Merges two lists assumed to be sorted, and counts the number of split
    inversions of those lists. Intended to be called as helper function in
    merge_sort_count.

    :param l: Sorted list
    :param r: Sorted list
    :returns: The list (@l + @r), sorted.
    :rtype: list
    """

    # In its merge step, MergeSort systematically pops off elements from the
    # left side of a list. Since Python lists are implemented as arrays, they
    # support this operation only in O(n) time. They do, however, support pops
    # from their right side in O(1) time. We therefore reverse the two lists
    # a and b and always check things on and pop things off their right side.

    l.reverse()
    r.reverse()

    merged = []
    inv_count = 0
    while l or r:
        if not l:
            r.reverse()  # Reverse back before extending the merged list
            merged.extend(r)
            r = []
        elif not r:
            l.reverse()  # Reverse back before extending the merged list
            merged.extend(l)
            l = []
        else:
            if l[-1] <= r[-1]:
                merged.append(l.pop())
            else:
                merged.append(r.pop())
                inv_count += len(l)
    return merged, inv_count


def merge_sort_count(lst):
    """
    Merge sorts a list and counts its inversions. Run-time for n-element list is
    n log(n).
    """
    if len(lst) in [0, 1]:
        return lst, 0
    else:
        center = len(lst)/2
        first_half = lst[:center]
        second_half = lst[center:]

        first_sorted, first_count = merge_sort_count(first_half)
        second_sorted, second_count = merge_sort_count(second_half)

        ordered, split_count = merge_count(first_sorted, second_sorted)
        return ordered, first_count + second_count + split_count


def count_inversions(a):
    """
    Counts the number of inversions in a list of length n in n log(n) run-time.
    """
    ordered, count = merge_sort_count(a)
    return count

# Some test cases
A = [1, 2, 4]  # 0
B = [3, 5, 6]  # 0
C = [37, 7, 2, 14, 35, 47, 10, 24, 44, 17, 34, 11, 16, 48, 1, 39, 6, 33, 43, 26,
     40, 4, 28, 5, 38, 41, 42, 12, 13, 21, 29, 18, 3, 19, 0, 32, 46, 27, 31, 25,
     15, 36, 20, 8, 9, 49, 22, 23, 30, 45]  # 590
D = [1, 6, 3, 2, 4, 5]  # 5
E = [9, 12, 3, 1, 6, 8, 2, 5, 14, 13, 11, 7, 10, 4, 0]  # 56

print count_inversions(C)
print count_inversions(D)
print count_inversions(E)

with open('IntegerArray.txt', 'r') as f:
    intArray = f.read().split('\r\n')
    intArray = map(int, intArray)

tic = time.clock()
print count_inversions(intArray)  # 2407905288
toc = time.clock()
print "Runtime:", toc - tic
# Measured runtime for intArray with naive .pop() from the left end
# in merge_count(): 2.44s
# Measured runtime after implementing the sublist reversal described above in
# merge_count(): 0.78s. That's a factor 3 improvement.