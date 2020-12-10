"""Mergesort not in place."""
import math
from typing import List, Dict
import multiprocessing as mp


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


def merge_interface(A_in):
    A = A_in[0] + A_in[1]
    merge(A, 0, len(A_in[0]) - 1, len(A) - 1)
    return A


def mergesort(A: List[float]) -> List[float]:
    """Sort array elements in A between p and r using mergesort."""
    if len(A) > 1:
        p = 0
        r = len(A)-1
        q = (p+r)//2
        left = mergesort(A[p:q+1])
        right = mergesort(A[q+1:r+1])
        A = left + right
        merge(A, p, q, r)
    return A


def mergesort_notinplace_mt(A: List[float]) -> List[float]:
    """Sort array elements in A between p and r using mergesort."""
    cores = mp.cpu_count()
    if len(A) >= cores:
        sub_size = len(A)//cores
        sub_lists = [A[i*sub_size:(i+1)*sub_size] for i in range(cores - 1)]
        sub_lists.append(A[(cores-1)*sub_size:])
        with mp.Pool(processes=cores) as pool:
            res = pool.map(mergesort, sub_lists)
            while len(res) > 1:
                extra = []
                if len(res) % 2 == 1:
                    extra = [res.pop()]
                res = [(res[i], res[i+1]) for i in range(0, len(res), 2)]
                res = pool.map(merge_interface, res)
                res += extra
        A = res[0]
    return A


if __name__ == "__main__":
    import random
    n = 500
    arr = [random.randint(0, n*10) for x in range(n)]
    arr = mergesort_notinplace_mt(arr)
    print(arr)
