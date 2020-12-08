"""Mergesort in place."""
import math
from typing import List


def merge_in_place(A: List[float], p: int, q: int, r: int) -> None:
    """Split A at q and merge together in order."""
    n_1 = q - p + 1
    n_2 = r - q
    L = 0
    R = 0
    for k in range(p, r+1):
        if A[p] <= A[q + 1]:
            A.insert(r+1, A[p])
            del A[p]
            L += 1
            q -= 1
        else:
            A.insert(r+1, A[q+1])
            del A[q+1]
            R += 1

        if L == n_1:
            A[r+1:r+1] = A[p:p+n_2-R]
            del A[p:p+n_2-R]
            break

        if R == n_2:
            A[r+1:r+1] = A[p:q+1]
            del A[p:q+1]
            break


def mergesort_inplace(A: List[float]) -> List[float]:
    """Sort array elements in A between p and r using mergesort."""
    if len(A) > 1:
        p = 0
        r = len(A)-1
        q = (p+r)//2
        left = mergesort_inplace(A[p:q+1])
        right = mergesort_inplace(A[q+1:r+1])
        A = left + right
        merge_in_place(A, p, q, r)
    return A
