"""Heapsort algorithms."""


def parent(i):
    """Get the index of the parent node."""
    return i // 2


def left(i):
    """Get the index of the left child node."""
    return 2*i


def right(i):
    """Get the index of the right child node."""
    return 2*i + 1


def max_heapify(A, i):
    """Maintain the max-heap property."""
    l = left(i)
    r = right(i)
    if l <= A[0] and A[l] > A[i]:
        largest = l
    else:
        largest = i
    if r <= A[0] and A[r] > A[largest]:
        largest = r
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        max_heapify(A, largest)


def build_max_heap(A):
    """Create a max-heap from an unsorted array."""
    A.insert(0, len(A))
    for i in range(len(A)//2, 0, -1):
        max_heapify(A, i)


def heapsort_inplace(A):
    """Sort an array A using heapsort."""
    build_max_heap(A)
    for i in range(len(A) - 1, 1, -1):
        A[1], A[i] = A[i], A[1]
        A[0] -= 1
        max_heapify(A, 1)
    del A[0]
    return A
