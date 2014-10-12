import heaps

print type((1, 2, 3))
print - (1, 2, 3)[0]
heap = heaps.Maxheap([5])

heap.push((1, 2))
heap.push((2, 'a'))
heap.push((1.5, 'b'))
print str(heap)
print heap.pushpop((1, 1))
print heap.heapreplace((34, 'a')), heap.largest()
print str(heap)
print

minheap = heaps.Minheap([1, 2, 3])
minheap.push('ca')
for i in minheap:
    print i

lst = [(1, 2, 3), (3, 1, 2), (2, 3, 1)]
lst.sort()
print
print str(lst)