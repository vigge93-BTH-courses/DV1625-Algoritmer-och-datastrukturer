"""Mergesort in place."""
from typing import List


def merge_in_place(A: List[float], p: int, q: int, r: int) -> None:
    """Split A at q and merge together in order."""
    n_1 = q - p + 1
    n_2 = r - q
    L = 0
    R = 0
    for k in range(p, r+1):
        if A[p] <= A[q + 1]:
            A.append(A[p])
            del A[p]
            L += 1
            q -= 1
        else:
            A.append(A[q+1])
            del A[q+1]
            R += 1

        if L == n_1:
            break

        if R == n_2:
            break
    end = len(A) - L - R
    A[p:p] = A[end:]
    del A[end + R + L:]


def mergesort_inplace(A: List[float]) -> List[float]:
    """Sort array elements in A using mergesort inplace."""
    if len(A) > 1:
        p = 0
        r = len(A)-1
        A = _mergesort_internal(A, p, r)
    return A


def _mergesort_internal(A: List[float], p: int, r: int) -> List[float]:
    if p < r:
        q = (p+r)//2
        _mergesort_internal(A, p, q)
        _mergesort_internal(A, q+1, r)
        merge_in_place(A, p, q, r)
    return A
