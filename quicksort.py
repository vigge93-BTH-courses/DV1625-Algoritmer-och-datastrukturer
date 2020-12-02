"""Quicksort algorithms."""
import random
import time


def quicksort(A, p, r):
    """Sort array elements in A between p and r using quicksort."""
    if p < r:
        q = partition(A, p, r)
        quicksort(A, p, q-1)
        quicksort(A, q + 1, r)


def quicksort_random(A, p, r):
    """Sort A's elements between p and r using random pivot quicksort."""
    if p < r:
        q = partition_random(A, p, r)
        quicksort_random(A, p, q-1)
        quicksort_random(A, q + 1, r)


def partition(A, p, r):
    """Partition array using last element as pivot."""
    x = A[r]
    i = p-1
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r], A[i+1]
    return i+1


def partition_random(A, p, r):
    """Partition array using random pivot."""
    n = random.randint(p, r)
    A[n], A[r] = A[r], A[n]
    x = A[r]
    i = p-1
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r], A[i+1]
    return i+1


if __name__ == "__main__":
    n = 10**6
    arr = [random.randint(0, n*10) for x in range(n)]
    t1 = time.monotonic_ns()
    quicksort(arr, 0, len(arr)-1)
    t2 = time.monotonic_ns()
    print((t2-t1)/10**9)
