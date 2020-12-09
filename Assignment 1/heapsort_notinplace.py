"""Heapsort not in place algorithm."""
from typing import List


def parent(i: int) -> int:
    """Get the index of the parent node."""
    return i // 2


def left(i: int) -> int:
    """Get the index of the left child node."""
    return 2*i


def right(i: int) -> int:
    """Get the index of the right child node."""
    return 2*i + 1


def max_heapify(A: List[float], i: int) -> None:
    """Maintain the max-heap property."""
    L = left(i)
    R = right(i)
    if L <= A[0] and A[L] > A[i]:
        largest = L
    else:
        largest = i
    if R <= A[0] and A[R] > A[largest]:
        largest = R
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        max_heapify(A, largest)


def build_max_heap(A: List[float]) -> None:
    """Create a max-heap from an unsorted array."""
    A.insert(0, len(A))  # Use first index to store heapsize
    for i in range(len(A)//2, 0, -1):
        max_heapify(A, i)


def heapsort_notinplace(A: List[float]) -> List[float]:
    """Sort an array A using heapsort (not in place)."""
    if not A:
        return A
    build_max_heap(A)
    res: List[float] = []
    for i in range(len(A) - 1, 1, -1):
        res.append(A[1])
        A[1], A[i] = A[i], A[1]
        A[0] -= 1
        max_heapify(A, 1)
    A[:] = [A[1]] + res[::-1]
    return A
