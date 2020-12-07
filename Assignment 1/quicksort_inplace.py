"""Quicksort inplace."""


def quicksort_inplace(A):
    """Sort array elements in A between p and r using quicksort."""
    if A:
        q = partition(A, 0, len(A)-1)
        left = quicksort_inplace(A[0:q])
        right = quicksort_inplace(A[q+1:len(A)])
        A = left + [A[q]] + right
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
