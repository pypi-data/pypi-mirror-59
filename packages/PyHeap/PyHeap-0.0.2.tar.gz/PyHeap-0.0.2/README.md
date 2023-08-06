# PyHeap

- Simple implementation of a heap that takes an arbitrary key for sorting.
- By default, the heaps are minHeaps. (can be changed by setting `isMin=False`) in constructor

## Example Usage:

```python
from PyHeap import Heap

# instantiate an empty heap as follows
# insert elements using the insert method
heap = Heap()
for i in range(5):
    heap.insert(i)
print(heap.heap) # [0. 0, 1, 2, 3, 4]

# instantiate a heap with a predefined array or set
a = [i for i in range(5)]
heap = Heap(a)
print(heap.heap) # [0. 0, 1, 2, 3, 4]
```

You can perform common heap operations such as `insert`, `getMin/deleteMin`:

```python
minVal = heap.getMin() # value is still present in the heap
minVal = heap.deleteMin() # value no longer present
```

You can also delete an arbitrary value if present in the heap:

```python
val = heap.deleteVal(3)
```

The heap can also be iterated over:

- The iteration order goes from smallest to largest if minHeap or largest to smallest if maxHeap

```python
for val in heap:
    print(val)
```

The heap can also be indexed:

- In this case, `heap[0]` returns the smallest number and `heap[k]` returns the kth smallest

Finally, the heap supports adding any kind of type, as long as you provide a `key` that provides a method of ordering values.

- NOTE: by default, the key is an indentity function
- If the key fails on an item, it will raise a `ValueError`

```python
test = [((3, 4), 2.8284271247461903), ((8, 9), 9.899494936611665), ((10, 2), 9.0), ((0.1, 2), 0.9), ((10, 5), 9.486832980505138)]
heap = Heap(test, key=lambda x:x[1]) # this will order by the second value

# you can change the heaps key as follows (this will change the heap)
heap.reconstructHeap(lambda x: 1/(x + 1))

# outside of the heap, you can get access to the heap's key as folows:
heap.applyKey(3)
```
