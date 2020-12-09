"""Quicksort inplace."""
from typing import List


def quicksort_inplace(A: List[float]) -> List[float]:
    """Sort array elements in A between p and r using quicksort."""
    if A:
        A = _quicksort_internal(A, 0, len(A)-1)
    return A


def _quicksort_internal(A, p, r):
    """Sort array elements in A between p and r using quicksort."""
    if p < r:
        q = partition(A, p, r)
        _quicksort_internal(A, p, q-1)
        _quicksort_internal(A, q + 1, r)
    return A


def partition(A: List[float], p: int, r: int) -> int:
    """Partition array using last element as pivot."""
    x = A[r]
    i = p
    for j in range(p, r):
        if A[j] <= x:
            A[i], A[j] = A[j], A[i]
            i += 1
    A[i], A[r] = A[r], A[i]
    return i


if __name__ == "__main__":
    import random
    n = 11
    arr = [random.randint(0, n*10) for x in range(n)]
    arr = quicksort_inplace(arr)
    print(arr)
