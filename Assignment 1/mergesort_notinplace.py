"""Mergesort not in place."""
import math
from typing import List


def merge(A: List[float], p: int, q: int, r: int) -> None:
    """Split A at q and merge together in order."""
    n_1 = q-p+1
    n_2 = r-q
    L = []
    R = []
    for i in range(n_1):
        L.append(A[p+i])
    for j in range(n_2):
        R.append(A[q+j+1])
    L.append(math.inf)
    R.append(math.inf)
    i = 0
    j = 0
    for k in range(p, r+1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1


def mergesort_notinplace(A: List[float]) -> List[float]:
    """Sort array elements in A between p and r using mergesort."""
    if len(A) > 1:
        p = 0
        r = len(A)-1
        q = (p+r)//2
        left = mergesort_notinplace(A[p:q+1])
        right = mergesort_notinplace(A[q+1:r+1])
        A = left + right
        merge(A, p, q, r)
    return A


if __name__ == "__main__":
    import random
    n = 100
    arr = [random.randint(0, n*10) for x in range(n)]
    arr = mergesort_notinplace(arr)
    print(arr)
