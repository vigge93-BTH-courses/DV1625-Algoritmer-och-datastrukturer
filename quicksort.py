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


def quicksort_nip(A):
    """Sort array elements in A between p and r using quicksort (not in place)."""
    if len(A) > 1:
        left, right, pivot = partition_nip(A)
        left = quicksort_nip(left)
        right = quicksort_nip(right)
        del A[:]
        A[:] = [*left, pivot, *right]
    return A


def partition(A, p, r):
    """Partition array using last element as pivot."""
    x = A[r]
    i = p
    for j in range(p, r):
        if A[j] <= x:
            A[i], A[j] = A[j], A[i]
            i += 1
    A[i], A[r] = A[r], A[i]
    return i


def partition_nip(A):
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
    quicksort_nip(arr)
    t2 = time.monotonic_ns()
    print(arr)
    print((t2-t1)/10**9)
