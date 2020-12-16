"""Quicksort not in place."""
from typing import List, Tuple


def quicksort_notinplace(A: List[float]) -> List[float]:
    """Sort array using quicksort (not in place)."""
    if len(A) > 1:
        left, right, pivot = partition_nip(A)
        left = quicksort_notinplace(left)
        right = quicksort_notinplace(right)
        del A[:]
        A[:] = [*left, pivot, *right]
    return A


def partition_nip(A: List[float]) -> Tuple[List[float], List[float], float]:
    """Partition array using last element as pivot (not in place)."""
    x = A[-1]
    left = []
    right = []
    for j in range(0, len(A)-1):
        if A[j] <= x:
            left.append(A[j])
        else:
            right.append(A[j])
    return left, right, x

if __name__ == "__main__":
    import random, time
    n = 1000000
    arr = [random.randint(0, n*10) for x in range(n)]
    t1 = time.monotonic_ns()
    arr = quicksort_notinplace(arr)
    t2 = time.monotonic_ns()
    print(arr)
    print((t2-t1)/10**9)