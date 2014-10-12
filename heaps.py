"""
heaps.py

Wrapper classes implementing the functions of the heapq module as methods of a
heap. Supports minimum heaps and maximum heaps. By Moritz Kuentzler.
"""
import heapq


class Minheap:
    """
    A wrapper class implementing the heapq functions as methods of a
    minimum heap.

    The Minheap class is initialized either with no arguments (yielding an empty
    heap) or with a list, which is then heapified.

    The Minheap class supports the following methods:
    .push(item) -- pushes item onto the heap
    .pop() -- pops the minimum element off the heap
    .smallest() -- returns the minimum element without removing it
    .pushpop(item) -- pushes item onto the heap, then returns minimum element
                      of the heap
    .heapreplace(item) -- returns minimum element of the heap (or returns
                          IndexError if heap is empty), then pushes item onto
                          the heap
    str(Minheap) -- prints the underlying list representation of the heap, with
                    its minimum element in the first place
    len(Minheap) -- prints the number of items stored in the heap

    For all those methods, item can be an integer, float, or tuple with first
    entry being an integer or float. If the latter, minimization will occur on
    the first entry of the tuple.

    The Minheap class supports iteration, which will consecutively pop and
    return the heap elements in increasing order, breaking ties arbitrarily.
    """
    def __init__(self, list_to_minheap=None):
        if list_to_minheap is None:
            self._heap = []
        else:
            self._heap = list_to_minheap
            heapq.heapify(self._heap)

    def __len__(self):
        return len(self._heap)

    def __str__(self):
        return str(self._heap)

    def push(self, item):
        heapq.heappush(self._heap, item)

    def pop(self):
        return heapq.heappop(self._heap)

    def pushpop(self, item):
        return heapq.heappushpop(self._heap, item)

    def heapreplace(self, item):
        return heapq.heapreplace(self._heap, item)

    def smallest(self):
        return self._heap[0]

    def __iter__(self):
        while self._heap:
            yield self.pop()


class Maxheap:
    """
    A wrapper class implementing the heapq functions as methods of a
    maximum heap.

    The Maxheap class is initialized either with no arguments (yielding an empty
    heap) or with a list, which is then heapified.

    The Minheap class supports the following methods:
    .push(item) -- pushes item onto the heap
    .pop() -- pops the maximum element off the heap
    .largest() -- returns the maximum element without removing it
    .pushpop(item) -- pushes item onto the heap, then returns maximum element
                      of the heap
    .heapreplace(item) -- returns maximum element of the heap (or returns
                          IndexError if heap is empty), then pushes item onto
                          the heap
    str(Maxheap) -- prints the underlying list representation of the heap, with
                    its maximum element in the first place
    len(Maxheap) -- prints the number of items stored in the heap

    For all those methods, item can be an integer, float, or tuple with first
    entry being an integer or float. If the latter, maximization will occur on
    the first entry of the tuple.

    The Minheap class supports iteration, which will consecutively pop and
    return the heap elements in decreasing order, breaking ties arbitrarily.
    """
    @staticmethod
    def __neg(item):
        # The Maxheap is implemented as a Minheap of the negative heap
        # elements.
        # Therefore, for any insertion or retrieval, one has to take the
        # negative (additive inverse) of the inserted/retrieved element.
        #  In order to not break support for tuples, tuples have to be treated
        #  differently from ints and floats wrt
        # taking the negative.
        # __neg takes the appropriate negative.
        if type(item) is int or type(item) is float:
            return - item
        elif type(item) is tuple:
            item = list(item)
            item[0] *= -1
            item = tuple(item)
            return item
        else:
            raise TypeError('Heap elements must be ints, floats, or tuples.')

    def __init__(self, list_to_maxheap=None):
        if list_to_maxheap is None:
            self._heap = []
        else:
            self._heap = map(self.__neg, list_to_maxheap)
            heapq.heapify(self._heap)

    def __len__(self):
        return len(self._heap)

    def __str__(self):
        return str(map(self.__neg, self._heap))

    def push(self, item):
        heapq.heappush(self._heap, self.__neg(item))

    def pop(self):
        return self.__neg(heapq.heappop(self._heap))

    def pushpop(self, item):
        return self.__neg(heapq.heappushpop(self._heap, self.__neg(item)))

    def heapreplace(self, item):
        return self.__neg(heapq.heapreplace(self._heap, self.__neg(item)))

    def largest(self):
        return self.__neg(self._heap[0])

    def __iter__(self):
        while self._heap:
            yield self.pop()